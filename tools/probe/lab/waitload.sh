#!/bin/sh
# waitload.sh : hold off a new client run while the 1-minute load average is above LOAD_MAX (default 4).
# Polls every LOAD_POLL seconds (default 30) and logs each wait; gives up waiting after LOAD_MAXWAIT
# seconds (default 1800, 0 = wait for ever) and says so, so a busy box slows a campaign but never stops it.
MAX=${LOAD_MAX:-4}; POLL=${LOAD_POLL:-30}; LIM=${LOAD_MAXWAIT:-1800}; t=0
while :; do
  L=$(cut -d' ' -f1 /proc/loadavg)
  if awk -v l="$L" -v m="$MAX" 'BEGIN{exit !(l<=m)}'; then echo "$(date -u +%FT%TZ) load $L <= $MAX, go (waited ${t}s)"; exit 0; fi
  if [ "$LIM" -gt 0 ] && [ $t -ge "$LIM" ]; then echo "$(date -u +%FT%TZ) load $L > $MAX after ${t}s, going anyway (LOAD_MAXWAIT)"; exit 0; fi
  echo "$(date -u +%FT%TZ) load $L > $MAX, waiting ${POLL}s"; sleep $POLL; t=$((t+POLL))
done
