#!/bin/sh
# fzq.sh: queue of fz runs; each starts only when load1<4 and no other thread's probe run is live. Stops starting after DEADLINE (epoch).
cd $HOME/fzlab; export PROBE_ROOT=$HOME/fzlab
LOG=$HOME/fzlab/fz/queue.log
busy() {
  awk '{exit !($1 >= 4)}' /proc/loadavg && { echo load; return 0; }
  for p in $(ps -eo pid=,args= | awk '/[r]unwine\.sh|[r]un603\.sh/ {print $1}'); do
    a=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null); c=$(readlink /proc/$p/cwd 2>/dev/null)
    case "$a $c" in *"/home/<user>/fzlab/"*|*"/home/<user>/fzlab "*) ;; *) echo "other:$p"; return 0;; esac
  done
  return 1
}
while read -r CL PLAN RUN EXTRA; do
  case "$CL" in ''|\#*) continue;; esac
  [ -d out/$RUN ] && [ -f fz/$RUN.out ] && grep -q '^done' fz/$RUN.out && { echo "$(date +%T) skip done $RUN" >> $LOG; continue; }
  while r=$(busy); do
    [ $(date +%s) -ge $DEADLINE ] && { echo "$(date +%T) deadline before $RUN ($r)" >> $LOG; exit 0; }
    sleep 10
  done
  [ $(date +%s) -ge $DEADLINE ] && { echo "$(date +%T) deadline before $RUN" >> $LOG; exit 0; }
  echo "$(date +%T) start $RUN load $(cut -d' ' -f1 /proc/loadavg)" >> $LOG
  if [ $CL = 603 ]; then
    env DISP=187 NOBLACK=0 timeout 1500 sh tools/run603.sh fz/$PLAN $RUN $EXTRA > fz/$RUN.out 2>&1
  else
    env DISP=183 timeout 1500 sh tools/runwine.sh $CL fz/$PLAN $RUN $EXTRA > fz/$RUN.out 2>&1
  fi
  echo "$(date +%T) end $RUN rc=$?" >> $LOG
done < fz/queue.txt
echo "$(date +%T) queue empty" >> $LOG
