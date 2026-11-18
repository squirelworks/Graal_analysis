#!/bin/sh
# run603.sh PLAN RUN [VAR=VALUE ...] : one probe run of the native Linux 6.03r7 client.
# Login gserver (serverwarp) -> world gserver behind gen5probe, all inside a private
# network namespace (bwrap --unshare-net), own Xvfb, no window manager. Output: $R/out/RUN.
# Lab-only: the namespace has loopback only, so nothing can reach a public server.
set -u
# Loopback addresses are built, not written, as in tools/lab-servers (the repo bars dotted IP literals).
LO=$(printf "%d.%d.%d.%d" 127 0 0 1); LO2=$(printf "%d.%d.%d.%d" 127 0 0 2)
PLAN=$1; RUN=$2; shift 2
R=$HOME/probelab; O=$R/out/$RUN; T=$R/tools; DISP=${DISP:-87}
rm -rf $O $R/client; mkdir -p $O $R/run
cp -a /opt/graal-lab/work/network-client-runs/6.03r7-x64-gserver-final-auto-first $R/client
cp /opt/graal-lab/work/graal6-linux64/Graal $R/client/Graal
W=$R/world; rm -rf $W; mkdir -p $W/servers; cp -f $HOME/seihai-lab/world/gs2emu $HOME/seihai-lab/world/seihai-listserver $W/
printf 'bind = "%s"\ngserver_port = 14950\nclient_ports = [14971]\nlist_name = "Probe netns"\nsilent_list_after_ms = 500\ngserver_ip = "peer"\n' "$LO" > $W/ls.toml
for s in probe probelogin; do cp -a $HOME/issho-lab/world/servers/issho6 $W/servers/$s; rm -rf $W/servers/$s/logs; mkdir $W/servers/$s/logs
  find $W/servers/$s/accounts -name "*.txt" ! -name "(defaultaccount).txt" ! -name "(npcserver).txt" -delete; done
# tile art, so the screen repaints between shots (without it, HUD digits draw over each other)
PICS1=${PICS1:-$HOME/gs1lab/w/servers/gs1world/world/pics1.png}
for s in probe probelogin; do [ -f "$PICS1" ] && cp "$PICS1" $W/servers/$s/world/pics1.png; done
o() { f=$W/servers/$1/config/serveroptions.txt; if grep -q "^$2 = " $f; then sed -i "s|^$2 = .*|$2 = $3|" $f; else echo "$2 = $3" >> $f; fi; }
for s in probe probelogin; do o $s listport 14950; o $s listip $LO; o $s serverinterface $LO2; o $s serverip $LO; o $s localip $LO; done
o probe name "Probe Lab 603"; o probe serverport 14901; o probe heartlimit 20; o probe gmaps ""
o probelogin name "Probe Login 603"; o probelogin serverport 14900
o probelogin serverside true; o probelogin serversidescriptlevels "probe_login*"; o probelogin startlevel probe_login.nw; o probelogin gmaps ""
L=$W/servers/probelogin/world/probe_login.nw; grep -E "^(GLEVNW01|BOARD)" $W/servers/probelogin/world/issho_a.nw > $L
# The warp is immediate. It can beat pics1.png and leave the screen black (HUD digits then draw over
# each other; compare newly drawn pixels between shots). A serverside timeout before the warp never fired.
printf 'NPC - 30 30\nif (playerenters) {\n  serverwarp Probe Lab 603;\n}\nNPCEND\n' >> $L
# start level: one grass tile everywhere (tile 2047 = "f/" in the lab tile sheet), so HUD shots have a background
LV=$W/servers/probe/world/probe_start.nw; echo GLEVNW01 > $LV
ROW=$(printf 'f/%.0s' $(seq 64)); for y in $(seq 0 63); do echo "BOARD 0 $y 64 0 $ROW" >> $LV; done
A="$W/servers/probe/accounts/(defaultaccount).txt"
a() { sed -i "s|^$1 .*|$1 $2|" "$A"; }
a LEVEL probe_start.nw; a MAXHP 3.00; a HP 3.00; a RUPEES ${RUPEES:-7}; a BOMBS ${BOMBS:-5}; a ARROWS ${ARROWS:-10}
cp "$A" $O/world-defaultaccount.txt; cp $PLAN $O/plan.txt
echo "nameserver $LO" > $O/resolv.conf
export DISPLAY=:$DISP
[ -e /tmp/.X11-unix/X$DISP ] && { echo "display :$DISP is in use; pick another DISP"; exit 1; }
Xvfb :$DISP -screen 0 1280x1024x24 -nolisten tcp > $O/xvfb.log 2>&1 & XV=$!; sleep 2
cat > $R/run/inner.sh <<IN
ip addr add $LO2/8 dev lo 2>/dev/null; ip link set lo up 2>/dev/null
python3 \$HOME/issho-lab/real603/linux-lab-dns.py --private-log $O/dns.jsonl --seconds 400 > $O/dns.log 2>&1 &
(cd $W && ./seihai-listserver --config ./ls.toml > $O/listserver.txt 2>&1 &)
sleep 1
(cd $W && ./gs2emu --server probe > $O/gs-world.txt 2>&1 &)
(cd $W && ./gs2emu --server probelogin -p 14900 > $O/gs-login.txt 2>&1 &)
python3 $T/gen5probe.py $LO 14900 $LO2 14900 $O/proxy.log login $R/run/login.sock &
python3 $T/gen5probe.py $LO 14901 $LO2 14901 $O/proxy.log world $R/run/world.sock &
sleep 5
cd $R/client; HOME=$R/client/runtime-home LIBGL_ALWAYS_SOFTWARE=1 SDL_AUDIODRIVER=dummy exec ./run-client.sh > $O/client.log 2>&1
IN
bwrap --unshare-user --uid 0 --gid 0 --cap-add CAP_NET_BIND_SERVICE --unshare-net --unshare-pid --die-with-parent \
  --ro-bind / / --ro-bind $O/resolv.conf /etc/resolv.conf --bind $R $R --tmpfs /tmp --bind /tmp/.X11-unix /tmp/.X11-unix --tmpfs /run --dev /dev --proc /proc \
  --chdir $R sh $R/run/inner.sh &
BW=$!
WIN=""; for i in $(seq 1 240); do WIN=$(xdotool search --onlyvisible --name . 2>/dev/null | head -1); [ -n "$WIN" ] && break; sleep 0.5; done
echo "window=$WIN" > $O/marks.txt
export PROBE_SHOT="W=\$(xdotool search --onlyvisible --name . 2>/dev/null | head -1); [ -n \"\$W\" ] && xwd -silent -id \$W > $O/{name}.xwd && python3 $T/xwd2png.py $O/{name}.xwd $O/{name}.png > /dev/null && rm $O/{name}.xwd; xdotool search --onlyvisible --name . > /dev/null 2>&1 && echo '{name} alive' >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"
python3 $T/probectl.py $R/run/world.sock plan $PLAN "$@" > $O/plan.log 2>&1
cp $R/client/runtime-home/.graal/graal4/game_console.log $O/ 2>/dev/null
# --unshare-pid + --die-with-parent: ending bwrap ends every process of this run, and only those
kill $BW 2>/dev/null; sleep 1; kill $XV 2>/dev/null; true
echo done $O
