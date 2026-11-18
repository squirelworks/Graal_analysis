#!/bin/sh
# runwine.sh CLIENT PLAN RUN [VAR=VALUE ...] : one probe run of a Windows client under Wine.
# CLIENT is 420 (4.20r8, faketime 2007-07-01, login form filled), 524 (5.24r4), or 222 / 231
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
[ -f $HOME/probelab/lab.env ] && . $HOME/probelab/lab.env; G=${WINELAB:?}; R=$HOME/probelab; O=$R/out/$RUN; T=$R/tools; mkdir -p $O $R/run; cd $G
case $CL in 420) D=94; DIR=c420; EXE=Graal4.exe; FT="@2007-07-01 12:00:00"; LOG=graal4console.log;;
            524) D=91; DIR=c524; EXE=Graal.exe; FT=""; LOG=game_console.log;;
            222|231) D=93; DIR=c22x; EXE=Graal_$CL.exe; FT=""; LOG=graalconsole.log;; *) echo "client 420, 524, 222 or 231"; exit 1;; esac
[ -e ns.pid ] && [ -d /proc/$(cat ns.pid) ] || sh tools/ns.sh > /dev/null
./k.sh "Graal4?\.exe|wine|\.exe|gen5swap|gen5probe|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null; sleep 1
cp $PLAN $O/plan.txt
./E sh -c "cd $G/w && setsid nohup ./seihai-listserver --config ls.toml > $O/listserver.txt 2>&1 &"; sleep 1
if [ $D = 93 ]; then
  P=$G/w/servers/probeclassic; rm -rf $P; cp -a $G/w/servers/gs1classic $P
  sed -i "s/^serverinterface = .*/serverinterface = $LO2/" $P/config/serveroptions.txt
  ./E sh -c "cd $G/w && setsid nohup ./gs2emu-73 --server probeclassic > $O/gs-world.txt 2>&1 &"
  ./E sh -c "setsid nohup python3 $T/gen5probe.py $LO1 14808 $LO2 14808 $O/proxy.log world $R/run/wine.sock > $O/proxy.out 2>&1 &"
else
  LB=gs2emu-hud1111; [ $CL = 524 ] && LB=gs2emu-73   # hud1111 refuses the 5.24r4 token (G3D15010)
  ./E sh -c "cd $G/w && setsid nohup ./$LB --server gs1login > $O/gs-login.txt 2>&1 &"
  ./E sh -c "cd $G/w && setsid nohup ./gs2emu-73 --server gs1world > $O/gs-world.txt 2>&1 &"
  ./E sh -c "setsid nohup python3 $T/gen5probe.py $LO1 14807 $LO2 14807 $O/proxy.log world $R/run/wine.sock > $O/proxy.out 2>&1 &"
fi
sleep 4
C=clients/$DIR; : > $C/$LOG; rm -f $C/FILENAMECACHE.txt
mkdir -p $C/levels/images/downloads; cp w/servers/gs1world/world/pics1.png $C/levels/images/downloads/pics1.png
rm -f /tmp/.X11-unix/X$D /tmp/.X$D-lock
./cl.sh xvfb $D; ./cl.sh start $D $DIR $EXE wpD "$FT"
win() { DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | while read w; do eval $(DISPLAY=:$D xdotool getwindowgeometry --shell $w); [ $WIDTH -ge 600 ] && echo $w; done | head -1; }
if [ $CL = 420 ]; then
  for i in $(seq 1 90); do W=$(win); [ -n "$W" ] && break; sleep 2; done; sleep 8   # the login form; slow under VM load
  ACC=p$(date +%H%M%S); W=$(win); eval $(DISPLAY=:$D xdotool getwindowgeometry --shell $W); dx=$((X-380)); dy=$((Y-290))
  B="End $(printf 'BackSpace %.0s' $(seq 12))"; c(){ DISPLAY=:$D xdotool mousemove $(($1+dx)) $(($2+dy)) click 1; sleep 1; }
  c 752 472; DISPLAY=:$D xdotool key --delay 80 $B; DISPLAY=:$D xdotool type --delay 100 $ACC
  c 805 532; DISPLAY=:$D xdotool key --delay 80 $B; DISPLAY=:$D xdotool type --delay 150 $ACC
  c 818 557; DISPLAY=:$D xdotool key --delay 80 $B; DISPLAY=:$D xdotool type --delay 100 labpass; sleep 1; c 696 643
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
