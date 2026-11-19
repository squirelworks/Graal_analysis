#!/bin/sh
# runnc.sh CLIENT PLAN RUN [VAR=VALUE ...] : one probe run of an NPC-Control client under Wine.
#
# CLIENT is 713 (nc7132001, the standalone NPCControl of 2001-07-13) or 2002 (a second standalone
# NPCControl dir, e.g. the 2001-05-21 build that the Jan-2002 leak carries under a Jan-2002 file
# date). NB: there is no standalone NPCControl built in Jan 2002 -- the only true Jan-2002 NC is the
# socket inside RC 2002/01/11, which this script can't drive (it needs the RC game-server login plus
# the 94/79 "(Server)" discovery flow, not a direct NC connect). Use gen5probe + an RC harness for that.
# Both standalone builds open the NC socket: login type 3 + token NCL15031 + account + password (the
# RC-2002 embedded socket uses NCL11012 instead), then a cipher-free zlib frame stream
# (protocol/npc-control.md). This script puts ncprobe.py between the client and our own lab npcserver,
# on $LO1:$NCPORT, and drives the plan through it.
#
# Lab only. Everything runs inside the tree's bwrap namespace (loopback only), never a public server.
#
# It reuses the same lab tree as runwine.sh ($HOME/probelab, with lab.env, the Wine prefix, the
# helper scripts E / k.sh / cl.sh and tools/ns.sh). lab.env must also define the NC-specific hooks
# below; they name lab copies that are NOT in this repo (the clients and the npcserver stay on the
# lab host / Drive):
#
#   NCLAB      tree root that holds the NC client dirs and the npcserver (defaults to $WINELAB)
#   NCPORT     loopback port ncprobe listens on for the client            (e.g. 14950)
#   NCSRVPORT  the lab npcserver's own NC socket port                     (e.g. 14951)
#   NCSERVER   command that starts the lab npcserver bound to $LO2:$NCSRVPORT, run from $NCLAB/w
#              (seihai-npcserver or the gserver-v2 fork; must expose the NC socket, no cipher)
#   NC713_DIR / NC713_EXE   client dir under $NCLAB/clients and its exe, for CLIENT=713
#   NC2002_DIR / NC2002_EXE  same, for CLIENT=2002 (a second standalone NPCControl dir)
#   NC_LOGIN(CL,D,ACC)       shell function (defined in lab.env) that fills the client's login
#              form on display :D with host=$LO1 port=$NCPORT account=$ACC password=labpass and
#              clicks connect. It is build-specific (window title and field offsets), so it lives
#              in lab.env next to the binary, like the 2.22/4.20 form steps in runwine.sh. If the
#              build auto-connects from a seeded config/registry instead, make NC_LOGIN a no-op.
set -u
LO1=$(printf '%d.%d.%d.%d' 127 0 0 1); LO2=$(printf '%d.%d.%d.%d' 127 0 0 2)
CL=$1; PLAN=$(readlink -f "$2"); RUN=$3; shift 3
[ -f $HOME/probelab/lab.env ] && . $HOME/probelab/lab.env
G=${NCLAB:-${WINELAB:?}}; R=$HOME/probelab; O=$R/out/$RUN; T=$R/tools
NCPORT=${NCPORT:-14950}; NCSRVPORT=${NCSRVPORT:-14951}
mkdir -p $O $R/run; cd $G
case $CL in
  713)  D=89; DIR=${NC713_DIR:?};  EXE=${NC713_EXE:?};  FT="@2001-07-13 12:00:00";;
  2002) D=88; DIR=${NC2002_DIR:?}; EXE=${NC2002_EXE:?}; FT="@2002-02-01 12:00:00";;
  *) echo "client 713 or 2002"; exit 1;; esac

[ -e ns.pid ] && [ -d /proc/$(cat ns.pid) ] || sh tools/ns.sh > /dev/null
./k.sh "ncprobe|${EXE}|wine|\.exe|npcserver|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null
# NCSERVER is operator-defined, so its process name need not match the kill list above; free the NC
# ports directly so a lingering server/stub from a previous run can't fail the next one with EADDRINUSE.
./E sh -c "fuser -k ${NCPORT}/tcp ${NCSRVPORT}/tcp 2>/dev/null"; sleep 1
cp $PLAN $O/plan.txt

# lab npcserver, bound to $LO2:$NCSRVPORT (the NC socket the proxy forwards to)
./E sh -c "cd $G/w && setsid nohup ${NCSERVER:?} > $O/npcserver.txt 2>&1 &"; sleep 2

# ncprobe between the client ($LO1:$NCPORT) and the npcserver ($LO2:$NCSRVPORT)
./E sh -c "setsid nohup python3 $T/ncprobe.py $LO1 $NCPORT $LO2 $NCSRVPORT $O/proxy.log nc $R/run/nc.sock > $O/proxy.out 2>&1 &"
sleep 2

# launch the NC client under Wine (clock pinned so any date gate passes)
C=clients/$DIR; : > $C/nc_console.log 2>/dev/null
rm -f /tmp/.X11-unix/X$D /tmp/.X$D-lock
./cl.sh xvfb $D
./cl.sh start $D $DIR $EXE wpD "$FT"

# fill the login form (build-specific; defined in lab.env) -> connect through the proxy
ACC=nc$(date +%H%M%S)
if command -v NC_LOGIN >/dev/null 2>&1 || type NC_LOGIN >/dev/null 2>&1; then
  NC_LOGIN $CL $D $ACC
fi

# the crash oracle: after each inject the plan calls `shot`, which records window alive / gone
export PROBE_SHOT="DISPLAY=:$D scrot -o $O/{name}.png 2>/dev/null; W=\$(DISPLAY=:$D xdotool search --onlyvisible --name . 2>/dev/null | head -1); [ -n \"\$W\" ] && echo '{name} alive' >> $O/marks.txt || echo '{name} CLIENT-GONE' >> $O/marks.txt"
python3 $T/probectl.py $R/run/nc.sock plan $PLAN "$@" > $O/plan.log 2>&1

cp $C/nc_console.log $O/ 2>/dev/null
./k.sh "ncprobe|${EXE}|wine|wineserver|winedevice|services.exe|plugplay|explorer.exe|rpcss|npcserver|gs2emu|seihai-listserver|Xvfb :$D" > /dev/null
./E sh -c "fuser -k ${NCPORT}/tcp ${NCSRVPORT}/tcp 2>/dev/null"   # drop the npcserver/stub by port, whatever it's named
echo done $O
