#!/bin/sh
# Start the lab listserver (14900 for the gserver, 14921/14922/14923 for clients)
# and GServer-v2 on 127.0.0.1:14802. Logs go to ./logs. Stop with: ./run-lab.sh stop
# ./run-lab.sh stock uses unpatched gs2lib (2.05 is then treated as pre-2.1).
# If accounts.txt exists ("account password" per line), only those accounts may log in.
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$D/logs"
if [ "$1" = stop ]; then
  [ -f "$D/logs/gs.pid" ] && kill "$(cat "$D/logs/gs.pid")" 2>/dev/null
  [ -f "$D/logs/ls.pid" ] && kill "$(cat "$D/logs/ls.pid")" 2>/dev/null
  rm -f "$D/logs/"*.pid; exit 0
fi
ACC=""
[ -f "$D/accounts.txt" ] && ACC="--accounts $D/accounts.txt"
python3 -I "$D/listserver.py" "$D/logs/listserver.log" $ACC > "$D/logs/listserver.out" 2>&1 &
echo $! > "$D/logs/ls.pid"
sleep 1
LIB="$D/lib"
[ "$1" = stock ] && LIB="$D/lib-stock:$D/lib"
cd "$D/bin" && LD_LIBRARY_PATH="$LIB" ./gs2emu > "$D/logs/gserver.out" 2>&1 &
echo $! > "$D/logs/gs.pid"
sleep 3
echo "listserver pid $(cat "$D/logs/ls.pid"), gserver pid $(cat "$D/logs/gs.pid")"
tail -3 "$D/logs/listserver.log"
