#!/bin/sh
# loadguard.sh [CMD ARGS...] : wait while the 1-minute load average is above LOADMAX (default 4),
# polling every LOADPOLL seconds (default 30) and logging each hold to LOADLOG (default stderr),
# then run CMD (if given). For shared lab VMs: start a client run only when the box has room.
# LOADWAITMAX (seconds, default 0 = no limit) gives up with exit 3 after that long.
MAX=${LOADMAX:-4}; POLL=${LOADPOLL:-30}; WMAX=${LOADWAITMAX:-0}; LOG=${LOADLOG:-/dev/stderr}
t0=$(date +%s); held=0
while :; do
  l=$(cut -d' ' -f1 /proc/loadavg)
  # compare as decimals with awk (no bc on the lab VM)
  if awk -v l="$l" -v m="$MAX" 'BEGIN{exit !(l > m)}'; then
    now=$(date +%s); w=$((now - t0)); held=1
    echo "$(date -u +%FT%TZ) loadguard hold: load1=$l > $MAX (waited ${w}s)" >> "$LOG"
    if [ "$WMAX" -gt 0 ] && [ $w -ge "$WMAX" ]; then echo "$(date -u +%FT%TZ) loadguard gave up after ${w}s" >> "$LOG"; exit 3; fi
    sleep "$POLL"
  else
    [ $held = 1 ] && echo "$(date -u +%FT%TZ) loadguard release: load1=$l after $(( $(date +%s) - t0 ))s" >> "$LOG"
    break
  fi
done
[ $# -gt 0 ] && exec "$@"
exit 0
