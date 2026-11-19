#!/usr/bin/env python3
"""rccanary: classify each probe shot against a Remote Control client from the proxy log.

  rccanary.py PROXYLOG [MARKSFILE] [--silent-secs N]

A game client shows a bomb-count HUD, so its canary is a screenshot (canary.py). An RC has
no HUD: its always-visible surfaces are the player list and the console, and it answers only
when a user clicks. So the RC canary is what the proxy can see for free -- whether the client
is still there and still talking -- which is exactly the fuzzing signal: did this injected
packet crash it, wedge its receive parser, or drop the connection.

For each `shot NAME` step (a `MARK plan: shot NAME` line in the log) this prints one line:

  NAME   VERDICT   c2s_after=<n>   note

VERDICT, worst first:
  gone        the shot recorded the window as gone (MARKSFILE has `NAME CLIENT-GONE`): a crash.
  disconnect  the RC socket closed at or before this shot (a `conn N closed/error` line): the
              client or the connection dropped after an earlier inject.
  silent      the RC sent no client->server packet between the last inject and this shot, and is
              still connected. An RC only sends when a user acts, so an idle RC is silent too (the
              base shot, before any inject, is the baseline for this): silent means "no crash, no
              disconnect", NOT "parser wedged". To tell a wedge from idleness, read the shot (did
              the injected packet's visible effect appear?) or drive a reply in the plan.
  alive       the RC sent at least one client->server packet after the last inject: the receive
              stream stayed in step past the injected packet.

`c2s_after` counts the RC->server packets seen between the last inject before the shot and the
shot itself. A width canary (does the RC read an injected field at the width we gave it?) is a
screenshot check: inject `55 ADDPLAYER ... <test field> c:0 str:<token>` so a mis-read swallows
the nickname, and diff the player-list box with canary.py and two reference shots.
"""
import re, sys

TS = re.compile(r'^\s*([\d.]+)\s')
MARK = re.compile(r'MARK plan: (.*)')
C2S = re.compile(r' C>S id=(\d+)')
INJECT = re.compile(r' INJECT (S>C|C>S) ')
CLOSE = re.compile(r' conn \d+ (closed|error)')


def ts(line):
    m = TS.match(line)
    return float(m.group(1)) if m else None


def main():
    args = sys.argv[1:]
    silent_secs = None
    if '--silent-secs' in args:
        i = args.index('--silent-secs'); silent_secs = float(args[i + 1]); del args[i:i + 2]
    logpath = args[0]
    marks = {}
    if len(args) > 1:
        for ln in open(args[1], encoding='latin1'):
            p = ln.split()
            if len(p) >= 2:
                marks[p[0]] = p[1]  # NAME -> alive | CLIENT-GONE

    # Walk the log once, building a timeline of events with timestamps.
    events = []  # (t, kind, detail)
    for ln in open(logpath, encoding='latin1'):
        t = ts(ln)
        if t is None:
            continue
        m = MARK.search(ln)
        if m:
            events.append((t, 'mark', m.group(1))); continue
        if INJECT.search(ln):
            events.append((t, 'inject', None)); continue
        m = C2S.search(ln)
        if m:
            events.append((t, 'c2s', int(m.group(1)))); continue
        if CLOSE.search(ln):
            events.append((t, 'close', None)); continue

    last_inject = None
    closed_at = None
    c2s_since_inject = 0
    for t, kind, detail in events:
        if kind == 'close' and closed_at is None:
            closed_at = t
        elif kind == 'inject':
            last_inject = t; c2s_since_inject = 0
        elif kind == 'c2s':
            if last_inject is not None and t >= last_inject:
                c2s_since_inject += 1
        elif kind == 'mark' and detail.startswith('shot '):
            name = detail[5:].strip()
            if marks.get(name) == 'CLIENT-GONE':
                verdict, note = 'gone', 'window gone'
            elif closed_at is not None and closed_at <= t:
                verdict, note = 'disconnect', 'socket closed at %.3f' % closed_at
            elif last_inject is not None and c2s_since_inject == 0:
                verdict, note = 'silent', 'no c2s since inject at %.3f' % last_inject
                if silent_secs is not None and t - last_inject < silent_secs:
                    note += ' (<%.0fs; may be too soon)' % silent_secs
            else:
                verdict, note = 'alive', ''
            print('%s\t%s\tc2s_after=%d\t%s' % (name, verdict, c2s_since_inject, note))


if __name__ == '__main__':
    main()
