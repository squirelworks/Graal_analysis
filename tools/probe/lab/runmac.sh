#!/bin/sh
# runmac.sh : serve one playable 6.x world behind gen5probe for the 6.015 macOS client running in
# the Lion research VM. Run this INSIDE the debian lab VM (so the server stack stays in a VM, not on
# the host). See protocol/probe-mac-6015-2026-11-19.md for the whole path.
#
# Wiring (ports only; no dotted literals in this repo):
#   * Lion VM guest resolves the Graal login host (via its /etc/hosts) to its private lab address and
#     guestfwd's the guest login port 14900 to the host loopback port 14806.
#   * On the host, a QMP `hostfwd_add` on the debian VM exposes the debian guest's 14806 at host
#     loopback 14806, so host 14806 -> debian 14806.
#   * Here, gen5probe listens on 0.0.0.0:14806 inside debian and forwards to the world gserver on
#     loopback 14801. The Mac thus plays over one gen5-probed connection.
# The gserver is a NORMAL playable world (not a serverside login that serverwarps), so there is no
# cross-VM warp address to configure. Inject probes via the world .sock; canary is screen-free
# chatback (6.x runs the clientside setplayerprop #c NPC, as 6.03r7 does).
set -u
S=$HOME/m446/stage; R=$HOME/probemac; O=$R/out; T=$S/tools
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1)
sh ~/pkillprobe.sh >/dev/null 2>&1
rm -rf $R; mkdir -p $O $R/run
W=$R/world; mkdir -p $W/servers; cp $S/bin/gs2emu $S/bin/seihai-listserver $W/
printf 'bind = "%s"\ngserver_port = 14950\nclient_ports = [14971]\nlist_name = "maclab"\nsilent_list_after_ms = 500\ngserver_ip = "peer"\n' $LO1 > $W/ls.toml
cp -a $S/world-template $W/servers/probe; mkdir -p $W/servers/probe/logs
o() { f=$W/servers/probe/config/serveroptions.txt; if grep -q "^$1 = " $f; then sed -i "s|^$1 = .*|$1 = $2|" $f; else echo "$1 = $2" >> $f; fi; }
o localhostlist true; o listport 14950; o listip $LO1; o serverinterface $LO1; o serverip $LO1; o localip $LO1; o gmaps '""'
o name "Lion Lab"; o serverport 14801; o startlevel issho_a.nw
avf=$W/servers/probe/config/allowedversions.txt
[ -f "$avf" ] && sed -i 's|^modern = .*|modern = G3D11125:G3D0511C, G3D3107A, G3D14097|' "$avf"
for a in $W/servers/probe/accounts/*.txt; do sed -i "s|^LEVEL .*|LEVEL issho_a.nw|" "$a"; done
A="$W/servers/probe/accounts/(defaultaccount).txt"
[ -f "$A" ] && sed -i "s|^MAXHP .*|MAXHP 3.00|;s|^HP .*|HP 3.00|;s|^RUPEES .*|RUPEES 7|;s|^BOMBS .*|BOMBS 5|;s|^ARROWS .*|ARROWS 10|" "$A"
SL=$W/servers/probe/world/issho_a.nw
printf 'NPC - 30 27\nif (created||timeout) {\n  setplayerprop #c,b#v(playerbombs) r#v(playerrupees) a#v(playerarrows);\n  timeout = 0.3;\n}\nNPCEND\n' > $R/run/npc.txt
awk -v F=$R/run/npc.txt '{print} /^BOARD 0 63 /{while ((getline l < F) > 0) print l}' $SL > $SL.new && mv $SL.new $SL
(cd $W && setsid nohup ./seihai-listserver --config ./ls.toml > $O/listserver.txt 2>&1 &)
sleep 1
(cd $W && setsid nohup ./gs2emu --server probe -p 14801 > $O/gs-world.txt 2>&1 &)
sleep 2
setsid nohup python3 $T/gen5probe.py 0.0.0.0 14806 $LO1 14801 $O/proxy.log world $R/run/world.sock > $O/probe-world.out 2>&1 &
sleep 2
echo "runmac up: world gserver on 14801 behind gen5probe 0.0.0.0:14806 ; inject via $R/run/world.sock"
ss -ltn 2>/dev/null | grep -E ':(14801|14806|14950)\b' || true
