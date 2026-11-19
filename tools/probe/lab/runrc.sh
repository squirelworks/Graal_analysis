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
# rights (this script sets ADMINRIGHTS/IPRANGE on the world's super account — see below).
#
# Reuses the same lab tree as runwine.sh ($WINELAB in $HOME/probelab/lab.env: Wine prefix, the E /
# k.sh / cl.sh / tools/ns.sh helpers, the gserver build and world, and its loopback-only namespace).
# Put the RC binaries under $WINELAB/clients/<DIR> (rc2004/rc205/rc3/rc2002/rcpre); RC_EXE overrides
# the exe name. Output in ~/probelab/out/RUN.
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
set -u
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2)
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
./k.sh "RemoteControl|remotecontrol|wine|\.exe|gen5probe|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null; sleep 1
cp $PLAN $O/plan.txt

# A gserver world behind the proxy, and the listserver advertising the proxy address.
# The world is bound to $LO2:$PORT so the proxy on $LO1:$PORT is the only thing the RC reaches
# (gs1world ships on 14807, so serverport must be rewritten too or nothing listens behind the proxy).
P=$G/w/servers/probrc; rm -rf $P; cp -a $G/w/servers/gs1world $P
SO=$P/config/serveroptions.txt
sed -i "s/^serverinterface = .*/serverinterface = $LO2/" $SO 2>/dev/null || true
sed -i "s/^serverport = .*/serverport = $PORT/" $SO 2>/dev/null || true
# The RC login account needs RC rights, not just a place on the staff list, or GServer-v2 answers
# "You do not have RC rights." Ensure the super account has full admin rights and an open IP range.
ACC=$P/accounts/super.txt
if [ -f "$ACC" ]; then
  grep -q '^ADMINRIGHTS ' "$ACC" && sed -i 's/^ADMINRIGHTS .*/ADMINRIGHTS 1048575/' "$ACC" || echo 'ADMINRIGHTS 1048575' >> "$ACC"
  grep -q '^IPRANGE ' "$ACC" && sed -i 's/^IPRANGE .*/IPRANGE */' "$ACC" || echo 'IPRANGE *' >> "$ACC"
fi
./E sh -c "cd $G/w && setsid nohup ./seihai-listserver --config ls.toml > $O/listserver.txt 2>&1 &"; sleep 1
./E sh -c "cd $G/w && setsid nohup ./gs2emu-73 --server probrc > $O/gs-world.txt 2>&1 &"; sleep 1
./E sh -c "setsid nohup python3 $T/gen5probe.py $LO1 $PORT $LO2 $PORT $O/proxy.log rc $R/run/rc.sock > $O/proxy.out 2>&1 &"
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

# The shot hook records the window state and a CPU sample (a wedged RC often pegs a core and
# stops sending; rccanary reads window-gone from marks and silence from the proxy log).
export PROBE_SHOT="DISPLAY=:$D scrot -o $O/{name}.png 2>/dev/null; \
W=\$(DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | head -1); \
PC=\$(ps -o %cpu= -C $EXE 2>/dev/null | awk '{s+=\$1} END{printf \"%.0f\", s}'); \
[ -n \"\$W\" ] && echo '{name} alive cpu='\$PC >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"

python3 $T/probectl.py $R/run/rc.sock plan $PLAN "$@" > $O/plan.log 2>&1
cp $C/$LOG $O/ 2>/dev/null; cp run/rc$D.log $O/ 2>/dev/null
./k.sh "RemoteControl|remotecontrol|wine|\.exe|gen5probe|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null
echo "done: $O"
