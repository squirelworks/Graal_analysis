#!/bin/sh
# case.sh up|down ROOT WORLD GSBIN PORT LOBBYPORT WARP BIND : (server VM, lab only)
# up: fresh ROOT/run from ROOT/base + the case overlay WORLD, then the lobby,
# the artefact receiver and the gserver; down: stop all three.
set -u
op=$1 R=$2
case $R in /*) ;; *) R=$HOME/$R;; esac
stop() { for f in gserver lobby putsrv; do [ -f $R/$f.pid ] && kill $(cat $R/$f.pid) 2>/dev/null; rm -f $R/$f.pid; done; }
if [ "$op" = down ]; then stop; exit 0; fi
W=$3 BIN=$4 PORT=$5 LP=$6 WARP=$7 BIND=$8
case $W in /*) ;; *) W=$HOME/$W;; esac
case $BIN in /*) ;; *) BIN=$HOME/$BIN;; esac
stop; sleep 1
rm -rf $R/run $R/out && mkdir -p $R/out && cp -a $R/base $R/run && cp -a $W/. $R/run/
cat $R/run/config/server.add >> $R/run/config/server.txt
printf 'port = %s\nbind = %s\n' "$PORT" "$BIND" >> $R/run/config/server.txt
nohup python3 -I -u $R/guest/lobby.py $LP "$WARP" > $R/out/lobby.log 2>&1 & echo $! > $R/lobby.pid
nohup python3 -I -u $R/guest/putsrv.py 18080 $R/out > $R/out/put.log 2>&1 & echo $! > $R/putsrv.pid
cd $R/run && nohup $BIN --world $R/run --verbose > $R/out/gserver.log 2>&1 & echo $! > $R/gserver.pid
sleep 2; kill -0 $(cat $R/gserver.pid) && echo up
