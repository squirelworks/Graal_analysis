#!/bin/sh
# keysweep.sh CLIENT SWEEP : press every key of keysweep.keys on one real client in the probe lab and
# record what each does (keysweep.py). CLIENT is 603 (native Linux 6.03r7, run603.sh) or
# 205 / 217 / 222 / 231 / 420 / 524 (Windows clients under Wine, runwine.sh). SWEEP names the output
# folder $PROBE_ROOT/out/keysweep-SWEEP (rows.tsv, sweep.log, shots/; raw material, keep it off the repo).
# Environment:
#   PROBE_ROOT  lab folder (default $HOME/probelab; holds lab.env, tools/, out/, run/)
#   KEYLOG=1    a key logger that copies the key event params and the keydown(0..10) bits into the player's
#               chat, so they show up as C>S chat props; 0 = clean run. 2.x: keylog-gs1.npc, a GS1 level NPC
#               (keypressed). 4.x-6.x get bytecode, and the lab gserver's GS1 lowering has no keypressed:
#               keylog-stub.npc goes in the level and keysweep.py replaces its script through the proxy with
#               keylog-gs2.bc.hex (keylog.gs2, onKeyPressed, compiled by Seihai's own GS2 compiler)
#   TARGETS     mouse targets relative to the game window: 'player=X,Y ground=X,Y npc=X,Y hud=X,Y'
#   LOADMAX     wait before each client start while the 1-minute load is above this (default 3)
#   KEYS        key list (default $T/keysweep.keys)   DISP  X display (default 61)   START  first index
# The client is started again (a full login) whenever it dies, loses its session or keeps a window
# open; the sweep goes on from the next key. A key that fails three runs in a row is skipped.
# For the Wine clients, WINELAB (lab.env) must be a private copy of the Wine lab tree marked with a
# file .keysweep-ok: the start levels are rewritten there before every run.
set -u
PROBE_ROOT=${PROBE_ROOT:-$HOME/probelab}; export PROBE_ROOT
R=$PROBE_ROOT; T=$R/tools; [ -f $R/lab.env ] && . $R/lab.env
CL=$1; SW=$2; KEYLOG=${KEYLOG:-1}; KEYS=$(readlink -f ${KEYS:-$T/keysweep.keys}); DISP=${DISP:-61}; export DISP
OUT=$R/out/keysweep-$SW; mkdir -p $OUT
N=$(grep -vc '^#' $KEYS)
next=${START:-0}; [ -f $OUT/next.txt ] && next=$(cat $OUT/next.txt)
echo "$(date -u +%FT%TZ) sweep $SW client $CL keylog $KEYLOG keys $N from $next" >> $OUT/runs.txt
if [ $CL != 603 ]; then
  G=${WINELAB:?}; [ -f $G/.keysweep-ok ] || { echo "WINELAB $G is not marked as a private copy (.keysweep-ok)"; exit 1; }
fi
fails=0; last=-1; run=0
while [ $next -lt $N ] && [ $run -lt ${MAXRUNS:-30} ]; do
  run=$((run+1)); RUN=ks-$SW-$run
  # shared VM: wait (up to an hour) while the 1-minute load is above LOADMAX (default 3)
  w=0; while [ $w -lt 720 ] && awk -v m=${LOADMAX:-3} '{exit !($1 > m)}' /proc/loadavg; do sleep 5; w=$((w+1)); done
  if [ $CL = 603 ]; then SOCK=$R/run/world.sock; else SOCK=$R/run/wine.sock
    for lv in w/servers/gs1world/world/gs1lab.nw w/servers/gs1classic/world/gs1ctl.nw; do
      [ -f $G/$lv.orig ] || cp $G/$lv $G/$lv.orig; cp $G/$lv.orig $G/$lv
      KL=$T/keylog-gs1.npc; case $lv in *gs1world*) KL=$T/keylog-stub.npc;; esac   # bytecode clients get the stub
      [ $KEYLOG = 1 ] && cat $KL >> $G/$lv
    done
  fi
  P=$OUT/plan-$run.txt; BC=""
  case $CL in 603|420|512|524) [ $KEYLOG = 1 ] && BC="--bytecode $T/keylog-gs2.bc.hex";; esac
  printf 'waitsession 240\nsleep %s\nsh python3 %s/keysweep.py --disp %s --sock %s --proxylog %s --out %s --keys %s --start %s --targets "%s" --label %s %s\n' \
    "${SETTLE:-15}" $T $DISP $SOCK $R/out/$RUN/proxy.log $OUT $KEYS $next "${TARGETS:-}" $RUN "$BC" > $P
  echo "$(date -u +%TZ) run $RUN from $next" >> $OUT/runs.txt
  if [ $CL = 603 ]; then
    X=""; [ $KEYLOG = 1 ] && X=$T/keylog-stub.npc
    NOBLACK=0 GS2EMU=${GS2EMU_GS1:-} EXTRANPC=$X sh $T/run603.sh $P $RUN > $OUT/$RUN.out 2>&1
  else
    sh $T/runwine.sh $CL $P $RUN > $OUT/$RUN.out 2>&1
  fi
  n2=$next; [ -f $OUT/next.txt ] && n2=$(cat $OUT/next.txt)
  if [ $n2 -le $next ]; then
    [ $next = $last ] && fails=$((fails+1)) || fails=1; last=$next
    echo "$(date -u +%TZ) run $RUN made no progress at $next (try $fails)" >> $OUT/runs.txt
    if [ $fails -ge 3 ]; then
      echo "$(date -u +%TZ) skipping key $next" >> $OUT/runs.txt; printf '{"i": %d, "skipped": true}\n' $next >> $OUT/rows.tsv
      next=$((next+1)); echo $next > $OUT/next.txt; fails=0
    fi
  else next=$n2; fails=0; fi
done
echo "$(date -u +%FT%TZ) end at $next of $N after $run runs" >> $OUT/runs.txt
