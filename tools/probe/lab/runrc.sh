#!/bin/sh
# runrc.sh RC PLAN RUN [VAR=VALUE ...] : one probe run of a Remote Control client behind gen5probe.
#
# RC selects the build and its login codec:
#   rc2004  2004 Delphi RC   (GSERV024, login type 6 -> gen 5)   Wine
#   rc205   RC2 2.05 GTK     (GSERV025, login type 6 -> gen 5)   native Linux (set RC_NATIVE=1) or Wine
#   rc3     RC3 beta         (GSERV025, login type 6 -> gen 5)   Wine
#   rcpre   pre-2002 Delphi  (GSERV0xx, login id 1  -> gen 2)    Wine
# Gen 5 builds reuse the same cipher as 2.22/2.31, so gen5probe fits them unchanged. The gen-2
# builds are plain zlib with no cipher; gen5probe picks that from the GSERV/G2NRC/NCL token.
#
# Topology (loopback only, inside the lab namespace): RC -> gen5probe on $LO1:14804 -> gserver on
# $LO2:14804. The lab listserver advertises $LO1:14804, and the RC builds reach the world through the
# server list (the 2004/RC2/RC3/2002 builds all pick it from the list, not a typed address). The RC
# logs in as super/super (the build default); the gserver must accept that account AND grant it RC
# rights (this script sets LOCALRIGHTS/IPRANGE on the world's super account — see below).
#
# Reuses the same lab tree as runwine.sh ($WINELAB in $HOME/probelab/lab.env: Wine prefix, the E /
# k.sh / cl.sh / tools/ns.sh helpers, the gserver build and world, and its loopback-only namespace).
# Put the RC binaries under $WINELAB/clients/<DIR> (rc2004/rc205/rc3/rc2002/rcpre); RC_EXE overrides
# the exe name. Output in ~/probelab/out/RUN.
#
# RC_WORLD picks the gserver world (default gs1world). To fuzz the NC socket that RC 2002/01/11 opens,
# run `RC_WORLD=npcdemo RC_NC=1 sh runrc.sh rc2002 ...`: the NPC server then answers the RC login with
# PLO 79 and the RC dials its NC socket back through this same proxy as a second (gen-2, NCL) session.
#
# Connecting the RC is GUI-driven. rc2004 has a calibrated default (dismiss Options, click the server
# list's Connect, at 1024x768). For another build or window size, set RC_CONNECT to the xdotool
# command that dismisses any dialog and clicks Connect (run once by hand, read the geometry, pin it).
# $D is the Xvfb display.
#
# Read a run with:  python3 tools/rccanary.py out/RUN/proxy.log out/RUN/marks.txt
# An RC only sends when a user acts, so every post-base shot reads `silent`: that is liveness
# (no crash / no disconnect), not proof the parser stayed in step. In-step is read from the shots
# (player count rising, dialogs opening with the injected values) and from rc-widths.plan's canary.
# Known rendering gaps under Wine (2026-11-19 run): RC3's main window stays BLACK (no paint), so its
# width canary can't be read from shots — set a Wine virtual desktop in the prefix registry first
# (HKCU\Software\Wine\Explorer\Desktops). RC2 2.05 (GTK) fails Pango font fallback ("All font
# fallbacks failed") and draws text as boxes; it also sets no X window title, so match it with
# `xdotool search --class .`, not `--name .`. Both are prefix/Wine issues, not proxy issues.
set -u
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2); LO3=$(printf '%d.%d.%d.%d' 127 0 0 3)
RC=$1; PLAN=$(readlink -f "$2"); RUN=$3; shift 3
[ -f $HOME/probelab/lab.env ] && . $HOME/probelab/lab.env; G=${WINELAB:?}; R=$HOME/probelab
O=$R/out/$RUN; T=$R/tools; mkdir -p $O $R/run; cd $G
# EXE can be overridden with RC_EXE (the archived builds use different exe names).
case $RC in
  rc2004) D=81; DIR=rc2004; EXE=RemoteControl.exe;  GEN=5; LIST=1;;
  rc205)  D=82; DIR=rc205;  EXE=RemoteControl.exe;  GEN=5; LIST=1;;
  rc3)    D=83; DIR=rc3;    EXE=RemoteControl3.exe; GEN=5; LIST=1;;
  rc2002) D=85; DIR=rc2002; EXE=RemoteControl.exe;  GEN=2; LIST=1;;  # RC 2002/01/11 (GSERV023, gen 2); has the NC socket
  rcpre)  D=84; DIR=rcpre;  EXE=remotecontrol.exe;  GEN=2; LIST=0;;
  *) echo "RC = rc2004 | rc205 | rc3 | rc2002 | rcpre"; exit 1;; esac
EXE=${RC_EXE:-$EXE}
NATIVE=${RC_NATIVE:-0}
PORT=14804

[ -e ns.pid ] && [ -d /proc/$(cat ns.pid) ] || sh tools/ns.sh > /dev/null
./k.sh "RemoteControl|remotecontrol|wine|\.exe|gen5probe|ncprobe|ncstub|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null; sleep 1
cp $PLAN $O/plan.txt

# A gserver world behind the proxy, and the listserver advertising the proxy address.
# The world is bound to $LO2:$PORT so the proxy on $LO1:$PORT is the only thing the RC reaches
# (gs1world ships on 14807, so serverport must be rewritten too or nothing listens behind the proxy).
# RC_WORLD selects the source world (default gs1world; use npcdemo for the RC-embedded NC run).
WORLD=${RC_WORLD:-gs1world}
P=$G/w/servers/probrc; rm -rf $P; cp -a $G/w/servers/$WORLD $P
SO=$P/config/serveroptions.txt
sed -i "s/^serverinterface = .*/serverinterface = $LO2/" $SO 2>/dev/null || true
sed -i "s/^serverport = .*/serverport = $PORT/" $SO 2>/dev/null || true
# GServer-v2 reads RC eligibility from the staff list, so super must be on `staff =` (the account
# rights line alone is not enough — the RC login is refused "You do not have RC rights").
if grep -q '^staff = ' "$SO" 2>/dev/null; then
  grep '^staff = ' "$SO" | grep -q 'super' || sed -i '/^staff = /s/$/,super/' "$SO"
else
  echo 'staff = super' >> "$SO"
fi
# RC_NC=1: fuzz the NC socket the RC opens (RC 2002/01/11). The gserver's own NPC server
# (serverside=true) answers RC login with PLO 79, whose connectString points the RC's NC socket.
# The game socket stays on gen5probe ($LO1); the NC socket is fronted by a SEPARATE ncprobe on a
# THIRD loopback ($LO3) so it is the only connection that proxy sees (no session-select race, and
# the ncstub fallback is a one-arg swap). connectString's port is always serverport, so the NC
# proxy needs a distinct IP: ns_ip=$LO3 makes PLO 79 = $LO3,$PORT. The super account carries the
# NPC-Control right (LOCALRIGHTS, set below), so the server answers 94 with 79 on its own and
# npcrights can stay at its default. ns_ip is read from adminconfig.txt, not serveroptions.
if [ "${RC_NC:-0}" = 1 ]; then
  AC=$P/config/adminconfig.txt
  grep -q '^ns_ip ' "$AC" 2>/dev/null && sed -i "s/^ns_ip .*/ns_ip = $LO3/" "$AC" || echo "ns_ip = $LO3" >> "$AC"
fi
# The super account also needs its admin-rights bitmask set so the NPC-Control right
# (PLPERM_NPCCONTROL) is present, or sendNCLoginToPlayer drops PLI_NPCSERVERQUERY (94) and never sends
# PLO 79. The flat-file loader reads this bitmask from the LOCALRIGHTS key (there is no ADMINRIGHTS
# key -- it is ignored). Give it full rights and an open IP range; RC *eligibility* is the staff fix.
ACC=$P/accounts/super.txt
if [ -f "$ACC" ]; then
  grep -q '^LOCALRIGHTS ' "$ACC" && sed -i 's/^LOCALRIGHTS .*/LOCALRIGHTS 1048575/' "$ACC" || echo 'LOCALRIGHTS 1048575' >> "$ACC"
  grep -q '^IPRANGE ' "$ACC" && sed -i 's/^IPRANGE .*/IPRANGE */' "$ACC" || echo 'IPRANGE *' >> "$ACC"
fi
./E sh -c "cd $G/w && setsid nohup ./seihai-listserver --config ls.toml > $O/listserver.txt 2>&1 &"; sleep 1
./E sh -c "cd $G/w && setsid nohup ./${RC_GS:-gs2emu-73} --server probrc > $O/gs-world.txt 2>&1 &"; sleep 1
./E sh -c "setsid nohup python3 $T/gen5probe.py $LO1 $PORT $LO2 $PORT $O/proxy.log rc $R/run/rc.sock > $O/proxy.out 2>&1 &"
# RC_NC: front only the NC socket with ncprobe on $LO3:$PORT. Upstream is the gserver's NPC backend
# ($LO2:$PORT); RC_NC_FALLBACK=1 instead runs ncstub on $LO2:14805 and points ncprobe there (used if
# the gserver drops the RC's NCL session). Run nc-core.plan on $R/run/ncrc.sock.
if [ "${RC_NC:-0}" = 1 ]; then
  NCUP_H=$LO2; NCUP_P=$PORT
  if [ "${RC_NC_FALLBACK:-0}" = 1 ]; then
    NCUP_P=14805
    ./E sh -c "setsid nohup python3 $T/ncstub.py $LO2 $NCUP_P $O/ncstub.log ncstub > $O/ncstub.out 2>&1 &"; sleep 1
  fi
  ./E sh -c "setsid nohup python3 $T/ncprobe.py $LO3 $PORT $NCUP_H $NCUP_P $O/ncproxy.log ncrc $R/run/ncrc.sock > $O/ncprobe.out 2>&1 &"
fi
sleep 3

C=clients/$DIR; LOG=controlconsole.log; : > $C/$LOG 2>/dev/null || true
rm -f /tmp/.X11-unix/X$D /tmp/.X$D-lock
./cl.sh xvfb $D
if [ $NATIVE = 1 ]; then
  ./E sh -c "cd $C && DISPLAY=:$D setsid nohup ./$EXE > $G/run/rc$D.log 2>&1 &"
else
  ./cl.sh start $D $DIR $EXE wpD ""
fi

# Wait for a login window, then connect. Calibrate RC_CONNECT per build/window (see header).
win() { DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | head -1; }
for i in $(seq 1 90); do W=$(win); [ -n "$W" ] && break; sleep 2; done; sleep 4
if [ -n "${RC_CONNECT:-}" ]; then
  eval "$RC_CONNECT"
elif [ "$RC" = rc2004 ]; then
  # rc2004 connects through the server list (not a direct address): dismiss the Options dialog,
  # then click Connect in the server list. Coordinates calibrated at 1024x768 (lab run 2026-11-19).
  DISPLAY=:$D xdotool mousemove 181 303 click 1; sleep 6
  DISPLAY=:$D xdotool mousemove 236 359 click 1
else
  DISPLAY=:$D xdotool key --delay 80 Return   # placeholder: calibrate RC_CONNECT for this build
fi

# RC_NC: with the NPC-Control right set (LOCALRIGHTS above), GServer-v2 answers the RC's
# PLI_NPCSERVERQUERY (94) with PLO 79 on its own and the RC opens its NC socket. As a fallback for an
# old binary or an account that still doesn't get the right, RC_NC_INJECT79=1 hand-injects PLO 79 on
# the game socket ($LO3,$PORT = ncprobe). RC_NS_PID is the (Server) player id (seen as 2 in the lab).
if [ "${RC_NC:-0}" = 1 ] && [ "${RC_NC_INJECT79:-0}" = 1 ]; then
  sleep 4
  python3 $T/probectl.py $R/run/rc.sock cmd "s2c 79 s:${RC_NS_PID:-2} t:$LO3,$PORT" >> $O/plan.log 2>&1
fi

# The shot hook records the window state and a CPU sample (a wedged RC often pegs a core and
# stops sending; rccanary reads window-gone from marks and silence from the proxy log).
export PROBE_SHOT="DISPLAY=:$D scrot -o $O/{name}.png 2>/dev/null; \
W=\$(DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | head -1); \
PC=\$(ps -o %cpu= -C $EXE 2>/dev/null | awk '{s+=\$1} END{printf \"%.0f\", s}'); \
[ -n \"\$W\" ] && echo '{name} alive cpu='\$PC >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"

# In RC_NC mode the plan fuzzes the NC socket, so it runs on ncprobe's control socket (ncrc.sock),
# where `waitsession` gates on the RC's 2nd (NC) connection; otherwise it runs on the game proxy.
CTL=$R/run/rc.sock; [ "${RC_NC:-0}" = 1 ] && CTL=$R/run/ncrc.sock
python3 $T/probectl.py $CTL plan $PLAN "$@" > $O/plan.log 2>&1
cp $C/$LOG $O/ 2>/dev/null; cp run/rc$D.log $O/ 2>/dev/null
./k.sh "RemoteControl|remotecontrol|wine|\.exe|gen5probe|ncprobe|ncstub|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null
echo "done: $O"
