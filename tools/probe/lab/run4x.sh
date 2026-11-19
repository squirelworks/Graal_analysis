#!/bin/sh
# run4x.sh CLIENTDIR PLAN RUN [VAR=VALUE ...] : one probe run of a native Linux 3.x/4.x client.
#
# The 3.x/4.x native Linux clients use the same Torque-based engine, gen-5 login, and GUI login
# form. This script drives one of them through gen5probe the same way run603.sh drives 6.03r7,
# but adds the three things the older clients need (see "Lab setup" below) and automates the GUI
# login form with xdotool (the 6.03r7 lab client auto-logs-in; the 3.x/4.x clients do not).
#
# Login gserver (14900, serverwarp) -> world gserver (14901) behind gen5probe, all inside a
# loopback-only bwrap netns, own Xvfb. Lab-only: the namespace has loopback only.
#
# CLIENTDIR is a prepared client tree under $STAGE (default ~/m446/stage), e.g. "client404",
# holding data/ : the extracted autopackage with the i386 `graal` binary and a license/ subdir.
#
# Lab setup (one-time, inside the lab VM; none of this is in the repo):
#   * i386 runtime: the 3.x/4.x `graal` is a 32-bit ELF. Enable dpkg i386 and install
#       libsdl1.2debian:i386 libgl1:i386 libgl1-mesa-dri:i386 libx11-6:i386 libstdc++6:i386
#     (mesa-dri pulls i386 llvmpipe, used via LIBGL_ALWAYS_SOFTWARE=1 under Xvfb).
#   * license/ subdir: the autopackage extraction flattens it, but the client hard-exits at
#     startup unless data/license/{sig.graal,sig.license,license.graal} exist. license.graal is
#     the server config (loginserver.graalonline.com:14900 for 4.x); hostshim maps that host to
#     $LO1, so no portmap is needed.
#   * arial X font: the client loads "arial" as an X core font (fallback helvetica) via
#     XLoadQueryFont("-*-arial-medium-r-*-*-SIZE-*..."). A bare Xvfb has no fonts, which disables
#     ALL text including HUD digits. Register Liberation Sans under the arial/helvetica families
#     in ~/labfonts (fonts.dir with -misc-arial-* and -misc-helvetica-* entries) and point Xvfb's
#     -fp at it (done below).
#   * 32-bit hostshim: build tools/hostshim.c for i386 (gcc -m32 -shared -fPIC -nostdlib) as
#     $STAGE/tools/hostshim32.so; the shipped hostshim.so is 64-bit (for the 6.03r7 client).
#
# Canary: CHATBACK=1 (default) adds a clientside GS1 NPC in the start level that copies the
# player's own bomb/gralat/arrow counts into chat; the client reports its chat to the server, so
# the canary is read screen-free from the proxy log's "C>S id=2" lines (robust against the missing
# gameplay/HUD assets in the reused world template). This is the pilot's chatback method.
set -u
CLIENTDIR=$1; PLAN=$(readlink -f "$2"); RUN=$3; shift 3
STAGE=${STAGE:-$HOME/m446/stage}; S=$STAGE; R=${PROBE4X_ROOT:-$HOME/probe4x}; O=$R/out/$RUN; T=$S/tools; DISP=${DISP:-96}
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2)
ACC=${ACC:-labplayer}; PW=${PW:-labpass}
rm -rf $O $R/client $R/world $R/run; mkdir -p $O $R/run
# --- world: login + world servers from the lab world template ---
W=$R/world; mkdir -p $W/servers; cp $S/bin/gs2emu $S/bin/seihai-listserver $W/
printf 'bind = "%s"\ngserver_port = 14950\nclient_ports = [14971]\nlist_name = "probe4x"\nsilent_list_after_ms = 500\ngserver_ip = "peer"\n' $LO1 > $W/ls.toml
for s in probe probelogin; do cp -a $S/world-template $W/servers/$s; mkdir -p $W/servers/$s/logs; done
o() { f=$W/servers/$1/config/serveroptions.txt; if grep -q "^$2 = " $f; then sed -i "s|^$2 = .*|$2 = $3|" $f; else echo "$2 = $3" >> $f; fi; }
for s in probe probelogin; do o $s localhostlist true; o $s listport 14950; o $s listip $LO1; o $s serverinterface $LO2; o $s serverip $LO1; o $s localip $LO1; o $s gmaps '""'; done
o probe name "Probe Lab 4x"; o probe serverport 14901; o probe startlevel issho_a.nw
o probelogin name "Probe Login 4x"; o probelogin serverport 14900
o probelogin serverside true; o probelogin serversidescriptlevels "probe_login*"; o probelogin startlevel probe_login.nw
L=$W/servers/probelogin/world/probe_login.nw; grep -E "^(GLEVNW01|BOARD)" $W/servers/probelogin/world/issho_a.nw > $L
printf 'NPC - 30 30\nif (playerenters) {\n  serverwarp Probe Lab 4x;\n}\nNPCEND\n' >> $L
for a in $W/servers/probe/accounts/*.txt; do sed -i "s|^LEVEL .*|LEVEL issho_a.nw|" "$a"; done
for a in $W/servers/probelogin/accounts/*.txt; do sed -i "s|^LEVEL .*|LEVEL probe_login.nw|" "$a"; done
A="$W/servers/probe/accounts/(defaultaccount).txt"
[ -f "$A" ] && { sed -i "s|^MAXHP .*|MAXHP 3.00|;s|^HP .*|HP 3.00|;s|^RUPEES .*|RUPEES ${RUPEES:-7}|;s|^BOMBS .*|BOMBS ${BOMBS:-5}|;s|^ARROWS .*|ARROWS ${ARROWS:-10}|" "$A"; cp "$A" $O/world-defaultaccount.txt; }
SL=$W/servers/probe/world/issho_a.nw
if [ "${CHATBACK:-1}" = 1 ]; then
  printf 'NPC - 30 27\nif (created||timeout) {\n  setplayerprop #c,b#v(playerbombs) r#v(playerrupees) a#v(playerarrows);\n  timeout = 0.3;\n}\nNPCEND\n' > $R/run/npc.txt
  awk -v F=$R/run/npc.txt '{print} /^BOARD 0 63 /{while ((getline l < F) > 0) print l}' $SL > $SL.new && mv $SL.new $SL
fi
cp $SL $O/world-level.nw; cp "$PLAN" $O/plan.txt
# --- client tree ---
mkdir -p $R/client/runtime-home; cp -a $S/$CLIENTDIR/data/. $R/client/
printf '#!/bin/sh\nset -eu\ncd -- "$(dirname -- "$0")"\nexport LD_LIBRARY_PATH="$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\nexec ./graal "$@"\n' > $R/client/run-client.sh
chmod +x $R/client/run-client.sh $R/client/graal
# --- display with the arial/helvetica font path ---
export DISPLAY=:$DISP
[ -e /tmp/.X11-unix/X$DISP ] && { echo "display :$DISP in use"; exit 1; }
FP=/usr/share/fonts/X11/misc,/usr/share/fonts/X11/75dpi,/usr/share/fonts/X11/100dpi,/usr/share/fonts/X11/Type1,$HOME/labfonts
Xvfb :$DISP -screen 0 1280x1024x24 -nolisten tcp -fp "$FP" > $O/xvfb.log 2>&1 & XV=$!; sleep 2
# --- inner: servers + proxies + client (hostshim32 redirects *.graalonline.com -> LO1) ---
cat > $R/run/inner.sh <<IN
ip addr add $LO2/8 dev lo 2>/dev/null; ip link set lo up 2>/dev/null
(cd $W && ./seihai-listserver --config ./ls.toml > $O/listserver.txt 2>&1 &)
sleep 1
(cd $W && ./gs2emu --server probe > $O/gs-world.txt 2>&1 &)
(cd $W && ./gs2emu --server probelogin -p 14900 > $O/gs-login.txt 2>&1 &)
python3 $T/gen5probe.py $LO1 14900 $LO2 14900 $O/proxy.log login $R/run/login.sock &
python3 $T/gen5probe.py $LO1 14901 $LO2 14901 $O/proxy.log world $R/run/world.sock &
sleep 4
cd $R/client
HOME=$R/client/runtime-home LIBGL_ALWAYS_SOFTWARE=1 SDL_AUDIODRIVER=dummy \
  GRAAL_LAB_IP=$LO1 LD_PRELOAD=$T/hostshim32.so exec ./run-client.sh > $O/client.log 2>&1
IN
bwrap --unshare-user --uid 0 --gid 0 --cap-add CAP_NET_BIND_SERVICE --unshare-net --unshare-pid --die-with-parent \
  --ro-bind / / --bind $R $R --tmpfs /tmp --bind /tmp/.X11-unix /tmp/.X11-unix --tmpfs /run --dev /dev --proc /proc \
  --chdir $R sh $R/run/inner.sh &
BW=$!; echo $BW > $O/bw.pid
# --- wait for the login window, then drive the GUI form (coords for the 640x480 window at +320+272) ---
for i in $(seq 1 90); do xdotool search --name "^Graal$" >/dev/null 2>&1 && break; sleep 1; done
sleep 3
cl() { xdotool mousemove $1 $2 click 1; sleep 0.4; xdotool key End; i=0; while [ $i -lt 24 ]; do xdotool key BackSpace; i=$((i+1)); done; xdotool type --delay 60 "$3"; sleep 0.3; }
cl 760 514 "$ACC"   # Account name
cl 760 540 "$PW"    # Password
cl 700 459 "$ACC"   # Nickname
sleep 0.3; xdotool mousemove 636 628 click 1   # Start
# --- wait for the world session (client warped and logged into the world gserver) ---
for i in $(seq 1 120); do grep -aq "world C>S LOGIN" $O/proxy.log 2>/dev/null && break; sleep 1; done
sleep 6
export PROBE_SHOT="W=\$(xdotool search --name '^Graal\$' 2>/dev/null | head -1); [ -n \"\$W\" ] && xwd -silent -id \$W > $O/{name}.xwd 2>/dev/null && ffmpeg -y -loglevel error -i $O/{name}.xwd $O/{name}.png 2>/dev/null && rm -f $O/{name}.xwd; xdotool search --name '^Graal\$' >/dev/null 2>&1 && echo '{name} alive' >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"
python3 $T/probectl.py $R/run/world.sock plan "$PLAN" "$@" > $O/plan.log 2>&1
cp $R/client/runtime-home/.graal/graal4/console.log $O/ 2>/dev/null
kill $BW 2>/dev/null; sleep 1; kill $XV 2>/dev/null; true
echo "done $O"
