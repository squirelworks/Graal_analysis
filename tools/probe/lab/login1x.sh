#!/bin/sh
# login1x.sh BUILD OUTDIR : drive an early client's start form on $DISP (account $ACC, password labpass).
B=$1; O=$2; D=$DISP; X="env DISPLAY=:$D xdotool"
ww() { i=0; while [ $i -lt ${2:-120} ]; do w=$($X search --onlyvisible --name "$1" 2>/dev/null | head -1); [ -n "$w" ] && { echo $w; return 0; }; sleep 1; i=$((i+1)); done; return 1; }
ck() { $X mousemove $1 $2 click 1; sleep 0.7; }
clr() { $X key --delay 40 End $(printf "BackSpace %.0s" $(seq 30)) Home $(printf "Delete %.0s" $(seq 30)); }
ty() { $X type --delay 90 "$1"; sleep 0.3; }
shot() { DISPLAY=:$D scrot -o $O/login-$1.png; }
W=$(ww "Graal" 150) || { echo "login: no window"; exit 1; }
echo "login: window $W $($X getwindowname $W)"; sleep ${LOGIN_SETTLE:-20}; shot 0
case $B in
  explore) shot e1; $X key Return; sleep 8; shot e2;;
  121|121x) ck 440 369; ck 370 406; sleep 2; shot mode
     ck 558 407; clr; ty $ACC; ck 455 439; clr; ty $LO1; ck 655 439; clr; ty ${PORT:-14812}
     ck 442 471; clr; ty $ACC; ck 655 471; clr; ty labpass; shot form; ck 668 516; sleep 15; shot after;;
  1st|2nd) ck 347 470; ck 620 497; clr; ty $LO1; ck 620 529; clr; ty 14802; shot form; ck 673 574; sleep 15; shot after;;
  3rd|4th|4thalpha|5th|5thalpha|6th|7th|8th|9th|9thalpha|10th|11th|12th|13th)
     ck 413 387; ck 583 420; clr; ty $ACC; case $B in 4thalpha) ck 507 452; clr; ty $LO1;; esac; ck 650 452; clr; ty 14802; case $B in 6th|7th|8th|9th|9thalpha|10th|11th|12th|13th) $FZ/E env DISPLAY=:$D WINEPREFIX=$FZ/wp WINEARCH=win32 WINEDEBUG=-all /usr/lib/wine/wine ${SETHOST:-$FZ/sethost.exe} "$CJ_HOST" $LO1;; esac; shot form; ck 660 555; sleep 7; shot after0; $X search --onlyvisible --name . getwindowname %@ 2>/dev/null | sort -u | tr '
' '|'; echo; sleep 11; shot after;;
  119|11|14th|15th) ck 514 416; sleep 2; ck 440 369; ck 370 406; sleep 1; shot mode
     ck 580 409; clr; ty $ACC; ck 506 441; clr; ty $LO1; ck 667 441; clr; ty 14802; shot form; ck 667 517; sleep 15; shot after;;
  *) ck 440 344; ck 370 381; sleep 1; shot mode
     ck 555 416; clr; ty $ACC; ck 455 448; clr; ty $LO1; ck 652 448; clr; ty ${PORT:-14812}
     ck 442 480; clr; ty $ACC; ck 652 480; clr; ty labpass; shot form; ck 667 525; sleep 15; shot after;;
esac
