#!/bin/sh
# case.sh up|v2up|down ROOT WORLD GSBIN PORT LOBBYPORT WARP BIND : (server VM, lab only)
# up: fresh ROOT/run from ROOT/base + the case overlay WORLD, then the lobby,
# the artefact receiver and the gserver; down: stop all three.
# v2up: the same with seihai-gserver-v2: ROOT/run from ROOT/base_v2, the
# overlay's options merged into config/serveroptions.txt (a key the overlay
# sets replaces the folder's), its files in world/3d/, and gs2emu started in
# ROOT/run, which it takes as its server folder.
set -u
op=$1 R=$2
case $R in /*) ;; *) R=$HOME/$R;; esac
stop() { for f in gserver lobby putsrv; do [ -f $R/$f.pid ] && kill $(cat $R/$f.pid) 2>/dev/null; rm -f $R/$f.pid; done; }
if [ "$op" = down ]; then stop; exit 0; fi
W=$3 BIN=$4 PORT=$5 LP=$6 WARP=$7 BIND=$8
case $W in /*) ;; *) W=$HOME/$W;; esac
case $BIN in /*) ;; *) BIN=$HOME/$BIN;; esac
stop; sleep 1
rm -rf $R/run $R/out && mkdir -p $R/out
if [ "$op" = v2up ]; then
  cp -a $R/base_v2 $R/run && mkdir -p $R/run/world/3d $R/run/config
  cp -a $W/config/graal3dworld.txt $R/run/config/
  [ -f $W/config/serverflags.txt ] && cp $W/config/serverflags.txt $R/run/serverflags.txt
  [ -d $W/files ] && cp -a $W/files/. $R/run/world/3d/
  O=$R/run/config/serveroptions.txt
  printf 'serverport = %s\nserverip = %s\nlocalip = %s\nserverinterface = %s\n' "$PORT" "$BIND" "$BIND" "$BIND" \
    | cat $W/config/server.add - > $R/out/options.add
  while IFS= read -r line; do
    k=$(printf '%s' "$line" | sed 's/[[:space:]]*=.*//')
    [ -n "$k" ] && sed -i "/^[[:space:]]*$k[[:space:]]*=/d" $O
  done < $R/out/options.add
  cat $R/out/options.add >> $O
else
  cp -a $R/base $R/run && cp -a $W/. $R/run/
  cat $R/run/config/server.add >> $R/run/config/server.txt
  printf 'port = %s\nbind = %s\n' "$PORT" "$BIND" >> $R/run/config/server.txt
fi
nohup python3 -I -u $R/guest/lobby.py $LP "$WARP" > $R/out/lobby.log 2>&1 & echo $! > $R/lobby.pid
nohup python3 -I -u $R/guest/putsrv.py 18080 $R/out > $R/out/put.log 2>&1 & echo $! > $R/putsrv.pid
if [ "$op" = v2up ]; then
  cd $R/run && nohup $BIN > $R/out/gserver.log 2>&1 & echo $! > $R/gserver.pid
else
  cd $R/run && nohup $BIN --world $R/run --verbose > $R/out/gserver.log 2>&1 & echo $! > $R/gserver.pid
fi
sleep 2; kill -0 $(cat $R/gserver.pid) && echo up
