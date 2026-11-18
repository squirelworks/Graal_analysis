#!/bin/sh
# run603.sh PLAN RUN [VAR=VALUE ...] : one probe run of the native Linux 6.03r7 client.
# Login gserver (serverwarp) -> world gserver behind gen5probe, all inside a private
# network namespace (bwrap --unshare-net), own Xvfb, no window manager. Output: $R/out/RUN.
# Lab-only: the namespace has loopback only, so nothing can reach a public server.
set -u
# Lab inputs come from $HOME/probelab/lab.env (kept on the lab VM, not in this repo):
#   CLIENT_TREE   a prepared Linux 6.03r7 client folder (run-client.sh, runtime-home)
#   CLIENT_BIN    the 6.03r7 Graal binary          GSERVER_DIR  folder with gs2emu and seihai-listserver
#   WORLD_TEMPLATE  a gs2emu server folder copied for the login and world servers
#   GS2EMU        optional other gserver binary for the world only (CHATBACK needs one that sends level NPC bytecode)
#   PICS1         the lab tile sheet               LAB_DNS      the lab's loopback DNS responder script
[ -f $HOME/probelab/lab.env ] && . $HOME/probelab/lab.env
: ${CLIENT_TREE:?} ${CLIENT_BIN:?} ${GSERVER_DIR:?} ${WORLD_TEMPLATE:?} ${LAB_DNS:?}
# the loopback address and a second loopback address (no dotted literals in this repo)
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2)
PLAN=$(readlink -f "$1"); RUN=$2; shift 2
[ -z "${PROBE_TRY:-}" ] && rm -f $HOME/probelab/out/$RUN.tries
R=$HOME/probelab; O=$R/out/$RUN; T=$R/tools; DISP=${DISP:-87}
rm -rf $O $R/client; mkdir -p $O $R/run
cp -a $CLIENT_TREE $R/client
cp $CLIENT_BIN $R/client/Graal
W=$R/world; rm -rf $W; mkdir -p $W/servers; cp -f $GSERVER_DIR/gs2emu $GSERVER_DIR/seihai-listserver $W/; cp -f ${GS2EMU:-$GSERVER_DIR/gs2emu} $W/gs2emu-world
printf 'bind = "%s"
gserver_port = 14950
client_ports = [14971]
list_name = "Probe netns"
silent_list_after_ms = 500
gserver_ip = "peer"
' "$LO1" > $W/ls.toml
for s in probe probelogin; do cp -a $WORLD_TEMPLATE $W/servers/$s; rm -rf $W/servers/$s/logs; mkdir $W/servers/$s/logs
  find $W/servers/$s/accounts -name "*.txt" ! -name "(defaultaccount).txt" ! -name "(npcserver).txt" -delete; done
# tile art, so the screen repaints between shots (without it, HUD digits draw over each other)
PICS1=${PICS1:-}
for s in probe probelogin; do [ -f "$PICS1" ] && cp "$PICS1" $W/servers/$s/world/pics1.png; done
# also seed the client's cache, so the tiles do not depend on the download beating the login warp
K=$R/client/runtime-home/.graal/graal4/levels/images/downloads; mkdir -p $K; [ -f "$PICS1" ] && cp "$PICS1" $K/pics1.png
o() { f=$W/servers/$1/config/serveroptions.txt; if grep -q "^$2 = " $f; then sed -i "s|^$2 = .*|$2 = $3|" $f; else echo "$2 = $3" >> $f; fi; }
for s in probe probelogin; do o $s localhostlist true; o $s listport 14950; o $s listip $LO1; o $s serverinterface $LO2; o $s serverip $LO1; o $s localip $LO1; done
o probe name "Probe Lab 603"; o probe serverport 14901; o probe heartlimit 20; o probe gmaps ""
o probelogin name "Probe Login 603"; o probelogin serverport 14900
o probelogin serverside true; o probelogin serversidescriptlevels "probe_login*"; o probelogin startlevel probe_login.nw; o probelogin gmaps ""
L=$W/servers/probelogin/world/probe_login.nw; grep -E "^(GLEVNW01|BOARD)" $W/servers/probelogin/world/issho_a.nw > $L
# The warp is immediate. It can beat pics1.png and leave the screen black (HUD digits then draw over
# each other; compare newly drawn pixels between shots). A serverside timeout before the warp never fired.
printf 'NPC - 30 30\nif (playerenters) {\n  serverwarp Probe Lab 603;\n}\nNPCEND\n' >> $L
# READBACK=1: a level NPC (GS1, run by the client) that shows the client's own player values above it
rm -f $R/run/npc-readback.txt $R/run/npc-chatback.txt
[ "${READBACK:-0}" = 1 ] && printf 'NPC - 30 26\nif (created||timeout) {\n  message r=#v(playerrupees) b=#v(playerbombs) a=#v(playerdarts);\n  timeout = 0.5;\n}\nNPCEND\n' > $R/run/npc-readback.txt
# CHATBACK=1: a level NPC (GS1, run by the client) that copies the client's own bomb and gralat counts
# into the player's chat, so the client reports them to the server (read by chatcanary.py; no screen needed)
[ "${CHATBACK:-0}" = 1 ] && printf 'NPC - 30 27\nif (created||timeout) {\n  setplayerprop #c,b#v(playerbombs) r#v(playerrupees) x#v(x);\n  timeout = 0.3;\n}\nNPCEND\n' > $R/run/npc-chatback.txt
# put those NPCs right after the board (the level's last block is a SIGN with no SIGNEND, which would swallow them)
SL=$W/servers/probe/world/issho_a.nw; rm -f $R/run/npc-add.txt
for f in readback chatback; do [ -f $R/run/npc-$f.txt ] && cat $R/run/npc-$f.txt >> $R/run/npc-add.txt && rm $R/run/npc-$f.txt; done
[ -f $R/run/npc-add.txt ] && awk -v F=$R/run/npc-add.txt '{print} /^BOARD 0 63 /{while ((getline l < F) > 0) print l}' $SL > $SL.new && mv $SL.new $SL
A="$W/servers/probe/accounts/(defaultaccount).txt"
a() { sed -i "s|^$1 .*|$1 $2|" "$A"; }
a MAXHP 3.00; a HP 3.00; a RUPEES ${RUPEES:-7}; a BOMBS ${BOMBS:-5}; a ARROWS ${ARROWS:-10}
cp "$A" $O/world-defaultaccount.txt; cp $PLAN $O/plan.txt
echo "nameserver $LO1" > $O/resolv.conf
export DISPLAY=:$DISP
[ -e /tmp/.X11-unix/X$DISP ] && { echo "display :$DISP is in use; pick another DISP"; exit 1; }
Xvfb :$DISP -screen 0 1280x1024x24 -nolisten tcp > $O/xvfb.log 2>&1 & XV=$!; sleep 2
cat > $R/run/inner.sh <<IN
ip addr add $LO2/8 dev lo 2>/dev/null; ip link set lo up 2>/dev/null
python3 $LAB_DNS --private-log $O/dns.jsonl --seconds 400 > $O/dns.log 2>&1 &
(cd $W && ./seihai-listserver --config ./ls.toml > $O/listserver.txt 2>&1 &)
sleep 1
(cd $W && ./gs2emu-world --server probe > $O/gs-world.txt 2>&1 &)
(cd $W && ./gs2emu --server probelogin -p 14900 > $O/gs-login.txt 2>&1 &)
python3 $T/gen5probe.py $LO1 14900 $LO2 14900 $O/proxy.log login $R/run/login.sock &
python3 $T/gen5probe.py $LO1 14901 $LO2 14901 $O/proxy.log world $R/run/world.sock &
sleep 5
cd $R/client; HOME=$R/client/runtime-home LIBGL_ALWAYS_SOFTWARE=1 SDL_AUDIODRIVER=dummy exec ./run-client.sh > $O/client.log 2>&1
IN
# The tile layer sometimes never draws (a black screen, see README). With NOBLACK=1 (the default),
# check a shot of the game area once the session is up; if it is black, end this run and start the
# whole script again from scratch (PROBE_TRY counts, at most 4 tries).
bwrap --unshare-user --uid 0 --gid 0 --cap-add CAP_NET_BIND_SERVICE --unshare-net --unshare-pid --die-with-parent   --ro-bind / / --ro-bind $O/resolv.conf /etc/resolv.conf --bind $R $R --tmpfs /tmp --bind /tmp/.X11-unix /tmp/.X11-unix --tmpfs /run --dev /dev --proc /proc   --chdir $R sh $R/run/inner.sh &
BW=$!
WIN=""; for i in $(seq 1 240); do WIN=$(xdotool search --onlyvisible --name . 2>/dev/null | head -1); [ -n "$WIN" ] && break; sleep 0.5; done
TRY=${PROBE_TRY:-1}; echo "try $TRY window=$WIN" >> $R/out/$RUN.tries
if [ "${NOBLACK:-1}" = 1 ]; then
  python3 $T/probectl.py $R/run/world.sock plan $T/settle.plan > $O/settle.log 2>&1
  [ -n "$WIN" ] && xwd -silent -id $WIN > $O/settle.xwd && python3 $T/xwd2png.py $O/settle.xwd $O/settle.png > /dev/null; rm -f $O/settle.xwd
  if ! python3 -c "import sys;from PIL import Image;h=Image.open(sys.argv[1]).convert('L').crop((100,150,900,700)).histogram();sys.exit(0 if sum(h[12:])>0.5*sum(h) else 1)" $O/settle.png 2>/dev/null && [ $TRY -lt 4 ]; then
    echo "try $TRY black, starting again" >> $R/out/$RUN.tries
    kill $BW 2>/dev/null; sleep 2; kill $XV 2>/dev/null; sleep 2
    PROBE_TRY=$((TRY+1)) exec sh $0 "$PLAN" "$RUN" "$@"
  fi
fi
echo "window=$WIN" >> $O/marks.txt; cp $R/out/$RUN.tries $O/tries.txt 2>/dev/null
export PROBE_SHOT="W=\$(xdotool search --onlyvisible --name . 2>/dev/null | head -1); [ -n \"\$W\" ] && xwd -silent -id \$W > $O/{name}.xwd && python3 $T/xwd2png.py $O/{name}.xwd $O/{name}.png > /dev/null && rm $O/{name}.xwd; xdotool search --onlyvisible --name . > /dev/null 2>&1 && echo '{name} alive' >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"
python3 $T/probectl.py $R/run/world.sock plan $PLAN "$@" > $O/plan.log 2>&1
cp $R/client/runtime-home/.graal/graal4/game_console.log $O/ 2>/dev/null
# --unshare-pid + --die-with-parent: ending bwrap ends every process of this run, and only those
kill $BW 2>/dev/null; sleep 1; kill $XV 2>/dev/null; true
echo done $O
