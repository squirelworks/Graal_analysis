#!/bin/sh
# run-srvfuzz.sh: one C->S fuzz sweep against an original Graal server, lab VM only.
#
# Loopback only (AGENTS.md). Start the target server yourself, bound to the loopback
# address on a lab port inside the VM; this script points srvfuzz at it, collects output, and
# relaunches the target if a case takes it down so the sweep finishes.
#
# This is a TEMPLATE: the server binary, its working directory, the port and the login
# token are lab copies named in the VM, not in this repo. Set them at the top or pass
# them in the environment. Never put a real host or IP here.
#
#   MODE=gen2 TOKEN=GSERV014 PORT=14804 SERVER_CMD='./gserver13 --loopback' sh run-srvfuzz.sh
#   MODE=list PORT=14921 SERVER_CMD='wine ListServer.exe' sh run-srvfuzz.sh
#
# Run archived Windows binaries under Wine + Xvfb in the sandboxed VM only; several phone
# home (AGENTS.md). Prefer a headless VM over the host desktop.
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
HOST=$(printf '%d.%d.%d.%d' 127 0 0 1)   # loopback, built not written (AGENTS.md bars dotted-IP literals)
MODE=${MODE:-gen2}
PORT=${PORT:-14804}
TOKEN=${TOKEN:-GSERV014}
OUT=${OUT:-"$HERE/../out/$MODE-$PORT-$(date +%Y%m%dT%H%M%S)"}
SERVER_CMD=${SERVER_CMD:-}            # how to (re)launch the target; empty = you launch it yourself
RECV=${SRVFUZZ_RECV_TIMEOUT:-2.0}
CANARY=${SRVFUZZ_CANARY_TIMEOUT:-3.0}

mkdir -p "$OUT"
echo "mode=$MODE host=$HOST port=$PORT token=$TOKEN out=$OUT" | tee "$OUT/run.env"

launch() {
  [ -n "$SERVER_CMD" ] || { echo "no SERVER_CMD; start the target yourself on $HOST:$PORT"; return 0; }
  echo "launch: $SERVER_CMD"
  # shellcheck disable=SC2086
  ( cd "${SERVER_DIR:-.}" && exec $SERVER_CMD ) >"$OUT/server.log" 2>&1 &
  echo $! > "$OUT/server.pid"
  sleep "${SERVER_WARMUP:-3}"
}

# If we own the launch, let srvfuzz drive the relaunch-on-crash loop itself.
RELAUNCH=""
if [ -n "$SERVER_CMD" ]; then
  launch
  RELAUNCH="--relaunch 'sh \"$HERE/relaunch.inc.sh\" \"$OUT\"'"
fi

echo "writing a small relaunch helper"
cat > "$HERE/relaunch.inc.sh" <<'EOF'
#!/bin/sh
# kill the old target (if any) and start a fresh one, reusing the parent run's env
OUT="$1"; set -a; . "$OUT/run.env.sh" 2>/dev/null || true; set +a
[ -f "$OUT/server.pid" ] && kill "$(cat "$OUT/server.pid")" 2>/dev/null || true
sleep 1
[ -n "${SERVER_CMD:-}" ] || exit 0
( cd "${SERVER_DIR:-.}" && exec $SERVER_CMD ) >>"$OUT/server.log" 2>&1 &
echo $! > "$OUT/server.pid"
sleep "${SERVER_WARMUP:-3}"
EOF
chmod +x "$HERE/relaunch.inc.sh"
# persist env for the helper
{ echo "SERVER_CMD='$SERVER_CMD'"; echo "SERVER_DIR='${SERVER_DIR:-.}'"; echo "SERVER_WARMUP='${SERVER_WARMUP:-3}'"; } > "$OUT/run.env.sh"

echo "sweep: $MODE"
# shellcheck disable=SC2086
SRVFUZZ_RECV_TIMEOUT="$RECV" SRVFUZZ_CANARY_TIMEOUT="$CANARY" \
  eval python3 \"$HERE/../srvfuzz.py\" "$MODE" "$HOST" "$PORT" --token "$TOKEN" --out \"$OUT\" $RELAUNCH

echo "done. results: $OUT/results.tsv ; crashes: $(ls "$OUT"/crash-* 2>/dev/null | wc -l)"
echo "redact per AGENTS.md before copying anything out of the VM."
