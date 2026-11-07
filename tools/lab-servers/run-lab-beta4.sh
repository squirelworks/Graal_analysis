#!/bin/sh
# Start the lab listserver (14900 for the gserver, 14921/14922/14923 for clients)
# and GServer-v2 beta4 (with gserver-beta4-lab.patch): servers/default (2.x) on
# the loopback address:14802 and servers/classic (1.33 to 1.41r1, generation classic) on 14803.
# Logs go to ./logs. Stop with: ./run-lab.sh stop
# If accounts.txt exists ("account password" per line), only those accounts may log in.
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$D/logs"
if [ "$1" = stop ]; then
  [ -f "$D/logs/gs.pid" ] && kill "$(cat "$D/logs/gs.pid")" 2>/dev/null
  [ -f "$D/logs/gsc.pid" ] && kill "$(cat "$D/logs/gsc.pid")" 2>/dev/null
  [ -f "$D/logs/ls.pid" ] && kill "$(cat "$D/logs/ls.pid")" 2>/dev/null
  rm -f "$D/logs/"*.pid; exit 0
fi
ACC=""
[ -f "$D/accounts.txt" ] && ACC="--accounts $D/accounts.txt"
python3 -I "$D/listserver.py" "$D/logs/listserver.log" $ACC > "$D/logs/listserver.out" 2>&1 &
echo $! > "$D/logs/ls.pid"
sleep 1
cd "$D/bin" && ./gs2emu > "$D/logs/gserver.out" 2>&1 &
echo $! > "$D/logs/gs.pid"
cd "$D/bin" && ./gs2emu --server classic > "$D/logs/gserver-classic.out" 2>&1 &
echo $! > "$D/logs/gsc.pid"
sleep 3
echo "listserver pid $(cat "$D/logs/ls.pid"), gserver pids $(cat "$D/logs/gs.pid") (2.x) and $(cat "$D/logs/gsc.pid") (classic)"
tail -3 "$D/logs/gserver.out"
