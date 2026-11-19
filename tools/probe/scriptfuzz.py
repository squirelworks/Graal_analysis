#!/usr/bin/env python3
"""scriptfuzz: turn GS1/GS2 fuzz cases into a probe plan, and score a run's proxy log.

The cases come from seihai-core's generators (examples `gs2_fuzzcases` and
`gs1_fuzzcases`). Each case is one NPC script that sets `player.chat` to
`FZ<id>a`, waits briefly, computes one value and sets `player.chat` to
`FZ<id>:<value>`. The client sends both chat values to the server as player
props (PLI 2, prop 12), which gen5probe logs. The case file carries what
Seihai's own VM or GS1 engine predicts, per client generation.

  scriptfuzz.py plan CASES.tsv [--gap 1.2] [--x 30] [--y 30] [--from ID] [--to ID]
                               [--family F] [--max-bytes N] [--canary [--canary-gap 1.0]]  > fuzz.plan
  scriptfuzz.py score CASES.tsv PROXY.LOG --column 6.03r7  > scored.tsv

`plan` writes one block per case: create a fresh NPC (PLO_NPCPROPS, 3),
give it the script, wait, delete it (PLO_NPCDEL, 29). A GS2 case (a `hex`
column) goes as PLO_RAWDATA (100) + PLO_NPCBYTECODE (131) in one inject, the
way GServer-v2 sends a level NPC's bytecode; the proxy's own trailing newline
is the compiler's final newline. A GS1 case (a `script` column) goes as NPC
prop 1 (GSHORT length + text) in the NPCPROPS itself. Every 50 cases the plan
takes a screenshot, so a dead client shows in the shots. With `--canary`, every case is
followed by a copy of the control case (30000 or 40000) under a fresh id: some cases leave the
client connected but its script engine dead, and two silent canaries in a row show that.

`score` reads every C>S PLI 2 line of the log (run the proxy with
PROBE_FULLHEX=2 so whole bodies are logged), pulls each `FZ<id>` chat value
out of the prop stream, and compares the values seen with the prediction in
the chosen column. Verdicts:

  match       the client sent exactly the predicted values
  differs     both values came, but the second is not the predicted one
  stopped     only `FZ<id>a` came: the script started and did not finish
  predicted-stop  Seihai predicts a stop and the client did stop
  ran-past    Seihai predicts a stop (or a refused file) and the client finished
  silent      nothing came: the client did not load or start the script
  predicted-silent  Seihai refuses the file and the client sent nothing

Lab only: the plan is for gen5probe between a lab client and a lab gserver on
loopback (README.md). Nothing here talks to any other server.
"""
import argparse, csv, re, sys

csv.field_size_limit(1 << 30)



def gint3_hex(n):
    return bytes((((n >> s) & 0x7f) + 32) for s in (14, 7, 0)).hex()


def read_cases(path):
    with open(path, newline='', encoding='latin1') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def plan(args):
    cases = read_cases(args.cases)
    # canary source: GS2 control 30000 (bytecode) or GS1 control 40000 (script text)
    canary = next((c for c in cases if c['id'] in ('30000', '40000')), None) if args.canary else None
    if args.canary and canary is None:
        sys.exit('--canary needs control case 30000 (GS2) or 40000 (GS1) in the case file')
    out = ['# scriptfuzz plan from %s (%d cases)' % (args.cases, len(cases)),
           'waitsession 240', 'wait s2c 9 90', 'sleep 10', 'shot fz-start']
    n = 0
    for c in cases:
        cid = int(c['id'])
        if args.from_id is not None and cid < args.from_id or args.to_id is not None and cid > args.to_id:
            continue
        if args.family and c['family'] != args.family:
            continue
        xy = 'c:2 c:%d c:3 c:%d' % (2 * args.x, 2 * args.y)
        out.append('mark CASE %d %s' % (cid, c['family']))
        if 'hex' in c:
            code = bytes.fromhex(c['hex'])
            if len(code) > args.max_bytes:
                out.append('mark SKIP %d %d bytes' % (cid, len(code)))
                continue
            out.append('s2c 3 i3:%d %s' % (cid, xy))
            # 131 + GINT3 id + bytecode + the proxy's newline (the compiler's last byte)
            msg_len = 1 + 3 + len(code) + 1
            out.append('s2c 100 i3:%d hex:0a%s%s%s' % (msg_len, '%02x' % (131 + 32), gint3_hex(cid), code.hex()))
        else:
            text = c['script'].encode('latin1')
            out.append('s2c 3 i3:%d %s c:1 s:%d hex:%s' % (cid, xy, len(text), text.hex()))
        out.append('sleep %s' % args.gap)
        out.append('s2c 29 i3:%d' % cid)
        if args.canary:
            # a copy of the control under a fresh NPC id and FZ9nnnn strings: shows the client's
            # script engine still runs after this case
            k = 90000 + n % 10000
            out.append('mark CANARY %d after %d' % (k, cid))
            if 'hex' in canary:
                code = bytes.fromhex(canary['hex']).replace(b'FZ30000', b'FZ%d' % k)
                out.append('s2c 3 i3:%d %s' % (k, xy))
                out.append('s2c 100 i3:%d hex:0a%s%s%s' % (len(code) + 5, '%02x' % (131 + 32), gint3_hex(k), code.hex()))
            else:
                text = canary['script'].encode('latin1').replace(b'FZ40000', b'FZ%d' % k)
                out.append('s2c 3 i3:%d %s c:1 s:%d hex:%s' % (k, xy, len(text), text.hex()))
            out.append('sleep %s' % args.canary_gap)
            out.append('s2c 29 i3:%d' % k)
        n += 1
        if n % 50 == 0:
            out.append('shot fz-%d' % cid)
    out += ['sleep 3', 'shot fz-end']
    print('\n'.join(out))


CHAT = 12
FZ = re.compile(rb'FZ(\d+)(a|:)')


def chats_in(body):
    """Every FZ chat value in a PLI_PLAYERPROPS body: prop 12 is GCHAR length + text."""
    found = []
    for m in FZ.finditer(body):
        i = m.start()
        if i >= 2 and body[i - 2] - 32 == CHAT:
            ln = body[i - 1] - 32
            found.append(body[i:i + ln].decode('latin1'))
        else:  # not at a prop boundary we can see: take to the end of the printable run
            j = i
            while j < len(body) and 32 <= body[j] < 127:
                j += 1
            found.append(body[i:j].decode('latin1'))
    return found


def score(args):
    cases = read_cases(args.cases)
    seen = {}
    for line in open(args.log, encoding='latin1'):
        if 'C>S id=2 ' not in line or 'hex=' not in line:
            continue
        body = bytes.fromhex(line.rsplit('hex=', 1)[1].strip())
        for v in chats_in(body):
            m = re.match(r'FZ(\d+)', v)
            lst = seen.setdefault(int(m.group(1)), [])
            if not lst or lst[-1] != v:
                lst.append(v)
    w = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    w.writerow(['id', 'family', 'what', 'verdict', 'seen', 'predicted'])
    tally = {}
    for c in cases:
        cid = int(c['id'])
        pred = c[args.column]
        pvals, _, pend = pred.rpartition('; ')
        pvals = [v for v in pvals.split(' | ') if v]
        obs = seen.get(cid, [])
        refused = pend.startswith('parse')
        pstop = pend.startswith('stopped') or len(pvals) == 1
        if not obs:
            verdict = 'predicted-silent' if refused or not pvals else 'silent'
        elif len(obs) == 1 and obs[0].endswith('a') and obs[0] == 'FZ%da' % cid:
            verdict = 'predicted-stop' if pstop else 'stopped'
        elif obs == pvals:
            verdict = 'match'
        elif refused or pstop:
            verdict = 'ran-past'
        else:
            verdict = 'differs'
        tally[verdict] = tally.get(verdict, 0) + 1
        w.writerow([cid, c['family'], c['what'], verdict, ' | '.join(obs), pred])
    print('# ' + ', '.join('%s %d' % kv for kv in sorted(tally.items())), file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('plan'); p.add_argument('cases')
    p.add_argument('--gap', default='1.2'); p.add_argument('--x', type=int, default=30); p.add_argument('--y', type=int, default=30)
    p.add_argument('--from', dest='from_id', type=int); p.add_argument('--to', dest='to_id', type=int)
    p.add_argument('--family'); p.add_argument('--max-bytes', type=int, default=100000)
    p.add_argument('--canary', action='store_true', help='after every case, a copy of the control script under a fresh id, which must report')
    p.add_argument('--canary-gap', default='1.0')
    s = sub.add_parser('score'); s.add_argument('cases'); s.add_argument('log'); s.add_argument('--column', required=True)
    a = ap.parse_args()
    (plan if a.cmd == 'plan' else score)(a)


if __name__ == '__main__':
    main()
