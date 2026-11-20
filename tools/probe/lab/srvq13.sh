#!/bin/sh
# srvq13.sh : srvfuzz gen-2 sweep against the original GServer13 (GSERV014) in the fz12c namespace
LOAD_MAXWAIT=${LOAD_MAXWAIT:-300} sh $(dirname "$0")/waitload.sh
LB=$(printf '%d.%d.%d.%d' 127 0 0 1)
sh $(dirname "$0")/srv13.sh up
$HOME/fz12c/E sh -c "cd $HOME/fz12/srvfuzz-tool/srvfuzz && python3 srvfuzz.py gen2 $LB 14804 --token GSERV014 --out $HOME/fz12c/out/gs13 --relaunch 'sh $(dirname "$0")/srv13.sh up'"
echo SRVQ13 DONE
