#!/bin/sh
# run3x.sh CLIENTDIR PLAN RUN [VAR=VALUE ...] : one probe run of a native Linux 3.x client (3.04).
#
# The 3.x client uses the same Torque engine and gen-5 login as 4.x, but a LISTSERVER flow instead
# of the 4.x login-server+serverwarp: client -> listserver (its license/license.graal names
# listserver host:14922) -> picks a server from the list -> connects to that game server. So this
# runs one gserver that registers with seihai-listserver and is advertised to the client; hostshim
# maps the official hostname to LO1 and GRAAL_PORTMAP maps the client's 14922 to the listserver's
# client port 14971. The game-server connection (LO1:14901) goes through gen5probe.
#
# The 3.04 build is the static `graalexe` with SDL/fmod bundled in its own lib/; same i386 runtime,
# arial X font and 32-bit hostshim as run4x.sh (see that script's header). Its login screen is
# 800x600 at the origin with labelled fields, and it has an extra step: after Start, a server list
# appears and the server must be selected and "connect" clicked.
#
# Canary: 3.04 ships its own HUD assets, so unlike run4x.sh the on-screen bomb-count canary works;
# shots are classified by tools/probe/canary.py with the 3.04 bomb-count box (324 46 354 66). The
# chatback canary is NOT used (3.04's clientside GS1 does not reflect setplayerprop #c the way 6.x
# does).
set -u
CLIENTDIR=$1; PLAN=$(readlink -f "$2"); RUN=$3; shift 3
STAGE=${STAGE:-$HOME/m446/stage}; S=$STAGE; R=${PROBE3X_ROOT:-$HOME/probe3x}; O=$R/out/$RUN; T=$S/tools; DISP=${DISP:-98}
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2)
ACC=${ACC:-labplayer}; PW=${PW:-labpass}
rm -rf $O $R/client $R/world $R/run; mkdir -p $O $R/run
# --- world: one game server + listserver (real list flow) ---
W=$R/world; mkdir -p $W/servers; cp $S/bin/gs2emu $S/bin/seihai-listserver $W/
printf 'bind = "%s"\ngserver_port = 14950\nclient_ports = [14971]\nlist_name = "probe3x"\nsilent_list_after_ms = 500\ngserver_ip = "peer"\n' $LO1 > $W/ls.toml
cp -a $S/world-template $W/servers/probe; mkdir -p $W/servers/probe/logs
o() { f=$W/servers/probe/config/serveroptions.txt; if grep -q "^$1 = " $f; then sed -i "s|^$1 = .*|$1 = $2|" $f; else echo "$1 = $2" >> $f; fi; }
o localhostlist true; o listport 14950; o listip $LO1; o serverinterface $LO2; o serverip $LO1; o localip $LO1; o gmaps '""'
o name "Probe Lab 3x"; o serverport 14901; o startlevel issho_a.nw
for a in $W/servers/probe/accounts/*.txt; do sed -i "s|^LEVEL .*|LEVEL issho_a.nw|" "$a"; done
AV=$W/servers/probe/config/allowedversions.txt
[ -f "$AV" ] && sed -i 's|^modern = .*|modern = G3D03014:G3D0511C|' "$AV"
A="$W/servers/probe/accounts/(defaultaccount).txt"
[ -f "$A" ] && { sed -i "s|^MAXHP .*|MAXHP 3.00|;s|^HP .*|HP 3.00|;s|^RUPEES .*|RUPEES ${RUPEES:-7}|;s|^BOMBS .*|BOMBS ${BOMBS:-5}|;s|^ARROWS .*|ARROWS ${ARROWS:-10}|" "$A"; cp "$A" $O/world-defaultaccount.txt; }
cp $W/servers/probe/world/issho_a.nw $O/world-level.nw; cp "$PLAN" $O/plan.txt
# --- client tree: 3.04 release/ + static graalexe (SDL/fmod in ./lib) ---
mkdir -p $R/client/runtime-home; cp -a $S/$CLIENTDIR/data/. $R/client/
printf '#!/bin/sh\nset -eu\ncd -- "$(dirname -- "$0")"\nexport LD_LIBRARY_PATH="$PWD/lib:$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\nexec ./graalexe "$@"\n' > $R/client/run-client.sh
chmod +x $R/client/run-client.sh $R/client/graalexe
# --- display with the arial/helvetica font path ---
export DISPLAY=:$DISP
[ -e /tmp/.X11-unix/X$DISP ] && { echo "display :$DISP in use"; exit 1; }
FP=/usr/share/fonts/X11/misc,/usr/share/fonts/X11/75dpi,/usr/share/fonts/X11/100dpi,/usr/share/fonts/X11/Type1,$HOME/labfonts
Xvfb :$DISP -screen 0 1280x1024x24 -nolisten tcp -fp "$FP" > $O/xvfb.log 2>&1 & XV=$!; sleep 2
cat > $R/run/inner.sh <<IN
ip addr add $LO2/8 dev lo 2>/dev/null; ip link set lo up 2>/dev/null
(cd $W && ./seihai-listserver --config ./ls.toml > $O/listserver.txt 2>&1 &)
sleep 1
(cd $W && ./gs2emu --server probe > $O/gs-world.txt 2>&1 &)
python3 $T/gen5probe.py $LO1 14901 $LO2 14901 $O/proxy.log world $R/run/world.sock &
sleep 4
cd $R/client
HOME=$R/client/runtime-home LIBGL_ALWAYS_SOFTWARE=1 SDL_AUDIODRIVER=dummy \
  GRAAL_LAB_IP=$LO1 GRAAL_PORTMAP="14922=14971" LD_PRELOAD=$T/hostshim32.so exec ./run-client.sh > $O/client.log 2>&1
IN
bwrap --unshare-user --uid 0 --gid 0 --cap-add CAP_NET_BIND_SERVICE --unshare-net --unshare-pid --die-with-parent \
  --ro-bind / / --bind $R $R --tmpfs /tmp --bind /tmp/.X11-unix /tmp/.X11-unix --tmpfs /run --dev /dev --proc /proc \
  --chdir $R sh $R/run/inner.sh &
BW=$!; echo $BW > $O/bw.pid
# --- wait for the 800x600 login window, then drive the form + server list ---
for i in $(seq 1 90); do xdotool search --name "^Graal$" >/dev/null 2>&1 && break; sleep 1; done
sleep 3
cl() { xdotool mousemove $1 $2 click 1; sleep 0.4; xdotool key End; i=0; while [ $i -lt 24 ]; do xdotool key BackSpace; i=$((i+1)); done; xdotool type --delay 60 "$3"; sleep 0.3; }
cl 395 424 "$ACC"   # Account
cl 395 457 "$PW"    # Password
cl 395 341 "$ACC"   # Nickname
sleep 0.3; xdotool mousemove 592 440 click 1   # Start -> server list
for i in $(seq 1 60); do grep -aq "on 14971" $O/listserver.txt 2>/dev/null && break; sleep 1; done
sleep 4
xdotool mousemove 250 293 click 1; sleep 0.5; xdotool mousemove 250 293 click 1; sleep 0.5   # select "Probe Lab 3x"
xdotool mousemove 580 473 click 1   # connect
# --- wait for the game-server session through the proxy ---
for i in $(seq 1 120); do grep -aq "world C>S LOGIN" $O/proxy.log 2>/dev/null && break; sleep 1; done
sleep 6
export PROBE_SHOT="W=\$(xdotool search --name '^Graal\$' 2>/dev/null | head -1); [ -n \"\$W\" ] && xwd -silent -id \$W > $O/{name}.xwd 2>/dev/null && ffmpeg -y -loglevel error -i $O/{name}.xwd $O/{name}.png 2>/dev/null && rm -f $O/{name}.xwd; xdotool search --name '^Graal\$' >/dev/null 2>&1 && echo '{name} alive' >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"
python3 $T/probectl.py $R/run/world.sock plan "$PLAN" "$@" > $O/plan.log 2>&1
cp $R/client/runtime-home/.graal/graal4/console.log $O/ 2>/dev/null
kill $BW 2>/dev/null; sleep 1; kill $XV 2>/dev/null; true
echo "done $O"
