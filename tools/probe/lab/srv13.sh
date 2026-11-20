#!/bin/sh
# srv13.sh start|shot NAME|click X Y|stop : the original GServer13 under Wine in the fz12c namespace (Xvfb :114)
F=$HOME/fz12c; S=$F/gs13; D=114; cd $F
# inside the namespace already (srvfuzz --relaunch runs there): no nsenter
e() { if [ "$(readlink /proc/self/ns/net)" = "$(readlink /proc/$(cat $F/ns.pid)/ns/net)" ]; then "$@"; else $F/E "$@"; fi; }
case $1 in
start) rm -rf $S; mkdir -p $S; cp -a $HOME/fz12/cl/graal13b/GServer13.exe $S/; cp -a $HOME/fz12/cl/graal13b/levels $S/ 2>/dev/null
  [ -f $HOME/fz12/cl/15thgraal/levels/onlinestartlocal.graal ] && cp $HOME/fz12/cl/15thgraal/levels/onlinestartlocal.graal $S/levels/ 2>/dev/null
  cp $F/gs13acc.txt $S/accounts.txt
  rm -f /tmp/.X11-unix/X$D /tmp/.X$D-lock; e sh -c "Xvfb :$D -screen 0 1024x768x24 -nolisten tcp -ac > $S/xvfb.log 2>&1 &"; sleep 2
  e sh -c "cd $S && DISPLAY=:$D WINEPREFIX=$F/wps WINEARCH=win32 WINEDEBUG=-all setsid nohup /usr/lib/wine/wine GServer13.exe > $S/wine.log 2>&1 &"; sleep 15;;
shot) DISPLAY=:$D scrot -o $S/$2.png; echo $S/$2.png;;
click) DISPLAY=:$D xdotool mousemove $2 $3 click 1;;
key) shift; DISPLAY=:$D xdotool key --delay 80 "$@";;
type) DISPLAY=:$D xdotool type --delay 60 "$2";;
stop) sh $F/k.sh "GServer13|Xvfb :$D" > /dev/null;;
esac
# srv13.sh up : (re)start and press OK in the start dialog, then wait for the listener (srvfuzz --relaunch)
[ "$1" = up ] && { sh $0 stop; sh $0 start; sh $0 click 472 353; for i in 1 2 3 4 5 6 7 8 9 10; do sleep 2; e ss -ltn | grep -q 14804 && break; done; }
