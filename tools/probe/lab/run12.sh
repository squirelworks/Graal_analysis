#!/bin/sh
# run12.sh BUILD PLAN RUN : one probe run of an early Windows client under Wine (fuzz12 campaigns).
# Gen 2 (1.21..1.39, GSERV/GNW tokens): seihai-gserver on $LO2:14812 behind gen5probe on $LO1:14812.
# Gen 1 (1st Graal..1.1.9, the relay): relay98 --fakepeer on $LO2:14802 behind gen5probe on $LO1:14802.
# The lab tree $FZ (default ~/fz12) holds its own bwrap namespace (ns.sh, E, k.sh: loopback only, lab
# hosts file), the Wine prefix wp (GDI renderer), the unpacked clients in cl/, the seihai-gserver binary
# in bin/ and world in world2/. VM-only settings come from $FZ/lab.env (REDIR_FROM: the fixed relay
# address the 3rd-5th betas dial, redirected to loopback by shim/redir32.so; CJ_HOST: the dialog host
# of the 6th-13th betas, which sethost.exe replaces in their greyed server box). Output in $FZ/out/RUN.
set -u
# the loopback address and a second loopback address (no dotted literals in this repo)
LO1=$(printf "%d.%d.%d.%d" 127 0 0 1); LO2=$(printf "%d.%d.%d.%d" 127 0 0 2); export LO1
B=$1; PLAN=$(readlink -f "$2"); RUN=$3; shift 3
F=${FZ:-$HOME/fz12}; T=$(cd "$(dirname "$0")" && pwd); D=${DISP:-112}; O=$F/out/$RUN; mkdir -p $O $F/c; cd $F
REDIR_FROM=""; CJ_HOST=""; [ -f $F/lab.env ] && . $F/lab.env; export CJ_HOST
sh $T/waitload.sh >> $O/load.txt 2>&1
[ -e ns.pid ] && [ -d /proc/$(cat ns.pid) ] || sh ns.sh > /dev/null
./k.sh "\.exe|wineserver|seihai-gserver|gen5probe|relay98|xfwm4|Xvfb :$D" > /dev/null; sleep 1
cp $PLAN $O/plan.txt
GEN=2; case $B in 1st|2nd|3rd|4th*|5th*|6th|7th|8th|9th*|1?th|11|119) GEN=1;; esac
if [ $GEN = 2 ]; then
  ./E sh -c "cd $F/world2 && setsid nohup $F/bin/seihai-gserver --world . --verbose > $O/gserver.out 2> $O/gserver.err &"
  ./E sh -c "setsid nohup python3 $T/../gen5probe.py $LO1 14812 $LO2 14812 $O/proxy.log w$B $F/run/ctl.sock > $O/proxy.out 2>&1 &"
else
  NLF=""; case $B in 14th|15th|11|119) NLF=--nl;; esac   # the 1.1.9 server's local-levels mode
  ./E sh -c "setsid nohup python3 $T/../relay98.py $LO2 14802 $NLF --fakepeer=9900 ${RELAYARGS:-} > $O/relay.log 2>&1 &"
  ./E sh -c "setsid nohup python3 $T/../gen5probe.py $LO1 14802 $LO2 14802 $O/proxy.log w$B $F/run/ctl.sock > $O/proxy.out 2>&1 &"
fi
sleep 3
C=$F/c/$B; rm -rf $C; cp -a $F/cl/$(sh $T/clientdir.sh $B) $C
[ -f $T/cfg/$B.txt ] && awk '{ printf "%s\r\n", $0 }' $T/cfg/$B.txt > $C/graalconfig.txt
EXE=$(cd $C && ls Graal*.exe graal*.exe 2>/dev/null | grep -v -i -E "server|remote" | head -1)
rm -f /tmp/.X11-unix/X$D /tmp/.X$D-lock
./E sh -c "Xvfb :$D -screen 0 1024x768x24 -nolisten tcp -ac > $O/xvfb.log 2>&1 &"; sleep 2
[ $GEN = 1 ] && { ./E sh -c "DISPLAY=:$D setsid nohup xfwm4 --compositor=off --sm-client-disable > $O/wm.log 2>&1 &"; sleep 2; }
PRE=""; case $B in 3rd|4th|5th) [ -n "$REDIR_FROM" ] && PRE="REDIR_FROM=$REDIR_FROM LD_PRELOAD='$F/shim/redir32.so $F/shim/redir64.so'";; esac
./E sh -c "cd $C && DISPLAY=:$D WINEPREFIX=$F/wp WINEARCH=win32 WINEDEBUG=${WDBG:--all} $PRE setsid nohup /usr/lib/wine/wine $EXE > $O/wine.log 2>&1 &"
echo "build $B gen $GEN exe $EXE" > $O/marks.txt
export DISP=$D ACC=f$(date +%H%M%S) FZ=$F
sh $T/login1x.sh $B $O >> $O/marks.txt 2>&1
export PROBE_SHOT="DISPLAY=:$D scrot -o $O/{name}.png; sh $T/alive.sh $D {name} >> $O/marks.txt"
python3 $T/../probectl.py $F/run/ctl.sock plan $PLAN "$@" > $O/plan.log 2>&1
./k.sh "\.exe|wineserver|winedevice|services.exe|plugplay|explorer.exe|rpcss|seihai-gserver|gen5probe|relay98|xfwm4|Xvfb :$D" > /dev/null
echo done $O
