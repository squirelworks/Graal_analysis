#!/bin/sh
# camp12.sh BUILD TAG : the whole fuzz12 row set on BUILD (lab tree $FZ, run12.sh). A crash is followed
# by a fresh login that resumes at the next row; a row never shot twice is skipped. A build whose
# login never yields a session twice in a row is abandoned.
B=$1; TAG=$2; F=${FZ:-$HOME/fz12}; T=$(cd "$(dirname "$0")" && pwd); mkdir -p $F/plans
GEN=2; case $B in 1st|2nd|3rd|4th*|5th*|6th|7th|8th|9th*|1?th|11|119) GEN=1;; esac
N=$(python3 $T/../fuzz12.py rows $GEN | wc -l); i=0; k=0; tries=0; nos=0
while [ $i -lt $N ] && [ $k -lt 25 ]; do
  k=$((k+1)); R=$TAG-$k
  python3 $T/../fuzz12.py plan $GEN $i > $F/plans/$R.plan
  sh $T/run12.sh $B $F/plans/$R.plan $R > /dev/null 2>&1
  if ! grep -q "TIMEOUT waitsession" $F/out/$R/plan.log 2>/dev/null && grep -q "plan: mark row" $F/out/$R/proxy.log 2>/dev/null; then nos=0
  else nos=$((nos+1)); echo "$R: no session"; [ $nos -ge 2 ] && { echo "campaign $TAG abandoned: no session twice"; exit 1; }; continue; fi
  nx=$(python3 $T/../fuzz12.py next $GEN $F/out/$R $i)
  if [ "$nx" = "$i" ]; then tries=$((tries+1)); [ $tries -ge 2 ] && { echo "$R: row $i never shot twice, skipping it"; nx=$((i+1)); tries=0; }
  else tries=0; fi
  echo "$(date -u +%H:%M:%S) $R rows $i.. -> next $nx"; i=$nx
done
echo "campaign $TAG done ($k parts)"
