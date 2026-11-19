#!/bin/sh
# runwine.sh CLIENT PLAN RUN [VAR=VALUE ...] : one probe run of a Windows client under Wine.
# CLIENT is 420 (4.20r8, faketime 2007-07-01, login form filled), 512 (5.12, faketime 2007-11-19),
# 524 (5.24r4), or 222 / 231
# (2.22 / 2.31: login form, then the server list; they play on a copy of the "A GS1 Control"
# world, moved to $LO2 behind gen5probe on $LO1:14808).
# Reuses a Wine lab tree ($WINELAB, set in $HOME/probelab/lab.env: Wine clients, prefix, worlds,
# helper scripts E, k.sh, cl.sh and tools/ns.sh, and its own bwrap namespace with
# loopback only): GS1 Login (serverwarp) -> GS1 Lab world behind gen5probe on $LO1:14807.
# Output in ~/probelab/out/RUN. Every process it kills is inside that namespace (the tree's k.sh).
set -u
# the loopback address and a second loopback address (no dotted literals in this repo)
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2)
CL=$1; PLAN=$(readlink -f "$2"); RUN=$3; shift 3
# PROBE_ROOT: the lab folder (default $HOME/probelab); DISP: override the client's display number
PROBE_ROOT=${PROBE_ROOT:-$HOME/probelab}; DISP0=${DISP:-}
[ -f $PROBE_ROOT/lab.env ] && . $PROBE_ROOT/lab.env; G=${WINELAB:?}; R=$PROBE_ROOT; O=$R/out/$RUN; T=$R/tools; mkdir -p $O $R/run; cd $G
case $CL in 420) D=94; DIR=c420; EXE=Graal4.exe; FT="@2007-07-01 12:00:00"; LOG=graal4console.log;;
            524) D=91; DIR=c524; EXE=Graal.exe; FT=""; LOG=game_console.log;;
            512) D=97; DIR=c512; EXE=Graal.exe; FT="@2007-11-19 12:00:00"; LOG=game_console.log;;
            222|231) D=93; DIR=c22x; EXE=Graal_$CL.exe; FT=""; LOG=graalconsole.log;;
            217) D=96; DIR=c22x; EXE=Graal_2171.exe; FT=""; LOG=graalconsole.log;;
            205) D=95; DIR=c205; EXE=Graal.exe; FT=""; LOG=graalconsole.log;; # needs WINELAB205 (client + GDI-renderer prefix)
            *) echo "client 205, 217, 222, 231, 420, 512 or 524"; exit 1;; esac
[ -n "$DISP0" ] && D=$DISP0
CLASSIC=0; case $CL in 205|217|222|231) CLASSIC=1;; esac
[ -e ns.pid ] && [ -d /proc/$(cat ns.pid) ] || sh tools/ns.sh > /dev/null
./k.sh "Graal4?\.exe|wine|\.exe|gen5swap|gen5probe|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null; sleep 1
cp $PLAN $O/plan.txt
./E sh -c "cd $G/w && setsid nohup ./seihai-listserver --config ls.toml > $O/listserver.txt 2>&1 &"; sleep 1
if [ $CLASSIC = 1 ]; then
  P=$G/w/servers/probeclassic; rm -rf $P; cp -a $G/w/servers/gs1classic $P
  sed -i "s/^serverinterface = .*/serverinterface = $LO2/" $P/config/serveroptions.txt
  # let 2.05 (GNW03081) and 2.17.1 (GNW22122) in as well
  sed -i 's/^newmain = GNW07080,/newmain = GNW03081, GNW22122, GNW07080,/' $P/config/allowedversions.txt
  ./E sh -c "cd $G/w && setsid nohup ./gs2emu-73 --server probeclassic > $O/gs-world.txt 2>&1 &"
  ./E sh -c "setsid nohup python3 $T/gen5probe.py $LO1 14808 $LO2 14808 $O/proxy.log world $R/run/wine.sock > $O/proxy.out 2>&1 &"
else
  LB=gs2emu-hud1111; [ $CL = 524 ] && LB=gs2emu-73   # hud1111 refuses the 5.24r4 token (G3D15010)
  ./E sh -c "cd $G/w && setsid nohup ./$LB --server gs1login > $O/gs-login.txt 2>&1 &"
  ./E sh -c "cd $G/w && setsid nohup ./gs2emu-73 --server gs1world > $O/gs-world.txt 2>&1 &"
  ./E sh -c "setsid nohup python3 $T/gen5probe.py $LO1 14807 $LO2 14807 $O/proxy.log world $R/run/wine.sock > $O/proxy.out 2>&1 &"
fi
sleep 4
C=clients/$DIR; [ $CL = 205 ] && C=${WINELAB205:?}/c205
: > $C/$LOG; rm -f $C/FILENAMECACHE.txt
mkdir -p $C/levels/images/downloads; cp w/servers/gs1world/world/pics1.png $C/levels/images/downloads/pics1.png
rm -f /tmp/.X11-unix/X$D /tmp/.X$D-lock
./cl.sh xvfb $D
if [ $CL = 205 ]; then
  ./E sh -c "cd $C && DISPLAY=:$D WINEPREFIX=$WINELAB205/wp205 WINEARCH=win32 WINEDEBUG=-all setsid nohup /usr/lib/wine/wine $EXE > $G/run/wine$D.log 2>&1 &"
else ./cl.sh start $D $DIR $EXE wpD "$FT"; fi
win() { DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | while read w; do eval $(DISPLAY=:$D xdotool getwindowgeometry --shell $w); [ $WIDTH -ge 600 ] && echo $w; done | head -1; }
if [ $CL = 420 ]; then
  for i in $(seq 1 90); do W=$(win); [ -n "$W" ] && break; sleep 2; done; sleep 8   # the login form; slow under VM load
  ACC=p$(date +%H%M%S); W=$(win); eval $(DISPLAY=:$D xdotool getwindowgeometry --shell $W); dx=$((X-380)); dy=$((Y-290))
  B="End $(printf 'BackSpace %.0s' $(seq 12))"; c(){ DISPLAY=:$D xdotool mousemove $(($1+dx)) $(($2+dy)) click 1; sleep 1; }
  c 752 472; DISPLAY=:$D xdotool key --delay 80 $B; DISPLAY=:$D xdotool type --delay 100 $ACC
  c 805 532; DISPLAY=:$D xdotool key --delay 80 $B; DISPLAY=:$D xdotool type --delay 150 $ACC
  c 818 557; DISPLAY=:$D xdotool key --delay 80 $B; DISPLAY=:$D xdotool type --delay 100 labpass; sleep 1; c 696 643
fi
ck() { DISPLAY=:$D xdotool mousemove $1 $2 click 1; sleep 1; }; ky() { DISPLAY=:$D xdotool key --delay 80 "$@"; }; ty() { DISPLAY=:$D xdotool type --delay 60 "$1"; }
BK="End BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace"; AC=o$(date +%H%M%S)
if [ $CL = 205 ]; then   # 2.05 rev 2: nickname screen, then server list with account and password
  sleep 25; ck 657 417; ky $BK; ty $AC; ck 660 523; sleep 6
  ck 435 521; ky $BK; ty $AC; ck 703 521; ky $BK; ty labpass; ck 300 319; sleep 1; ck 720 576; sleep 12
elif [ $CL = 217 ]; then   # 2.17.1: account and password, then the server list
  sleep 25; ck 505 367; ky $BK; ty $AC; ck 510 421; ky $BK; ty labpass; ck 508 575; sleep 6
  ck 300 331; sleep 1; ck 510 575; sleep 12; ck 815 300
fi
if [ $D = 93 ]; then   # 2.22 / 2.31 login form, then the server list (window offsets of the 2.22 login form)
  ww() { i=0; while [ $i -lt $2 ]; do w=$(DISPLAY=:$D xdotool search --onlyvisible --name "$1" 2>/dev/null | head -1); [ -n "$w" ] && { echo $w; return 0; }; sleep 1; i=$((i+1)); done; return 1; }
  pos() { w=$(ww "$1" 120) || return 1; eval $(DISPLAY=:$D xdotool getwindowgeometry --shell $w); dx=$((X-223)); dy=$((Y-189)); }
  c() { DISPLAY=:$D xdotool mousemove $(($1+dx)) $(($2+dy)) click 1; sleep 1; }
  k() { DISPLAY=:$D xdotool key --delay 80 "$@"; }; t() { DISPLAY=:$D xdotool type --delay 80 "$1"; }
  B="End BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace BackSpace"; ACC=c$(date +%H%M%S)
  if pos "^(Graal Reborn|GraalOnline)$"; then sleep 4
    c 510 441; k $B; t $ACC; c 505 529; k $B; t $ACC; c 512 561; k $B; t labpass; sleep 1
    c 696 545; pos "Server [Ll]ist$" && { sleep 5; c 300 440; c 712 575; }
  else echo "no login window" >> $O/marks.txt; fi
fi
export PROBE_SHOT="DISPLAY=:$D scrot -o $O/{name}.png; W=\$(DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | head -1); [ -n \"\$W\" ] && echo '{name} alive' >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"
python3 $T/probectl.py $R/run/wine.sock plan $PLAN "$@" > $O/plan.log 2>&1
cp $C/$LOG $O/ 2>/dev/null; cp run/wine$D.log $O/ 2>/dev/null
./k.sh "Graal4?\.exe|wine|\.exe|wineserver|winedevice|services.exe|plugplay|explorer.exe|rpcss|gen5probe|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null
echo done $O
