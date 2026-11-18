#!/usr/bin/env python3
"""chatcanary: read the CHATBACK canary from a probe run's proxy log.

  chatcanary.py PROXYLOG

With CHATBACK=1 the client copies its own counts into its chat ("b<bombs> r<gralats>")
and reports the chat to the server in PLI_PLAYERPROPS (prop 12). For each `shot NAME`
step in the plan, this prints the last chat the client had reported before the next
step began: NAME, the chat text, and `landed` when the bomb count is 99, else `lost`.
"""
import re, sys


def chat_of(hexbody):
    b = bytes.fromhex(hexbody); i = 0; out = None
    while i < len(b):
        pid = b[i] - 32; i += 1
        if pid == 12 and i < len(b):
            n = b[i] - 32; out = b[i + 1:i + 1 + n].decode('latin1'); i += 1 + n
        else:
            break  # only the leading chat prop is needed
    return out


def main():
    chat = None; pending = None
    for line in open(sys.argv[1], encoding='latin1'):
        m = re.search(r'C>S id=2 .*\| hex=([0-9a-f]*)', line)
        if m:
            c = chat_of(m.group(1))
            if c is not None:
                chat = c
            continue
        m = re.search(r'MARK plan: (.*)', line)
        if m:
            step = m.group(1)
            if pending:
                b = re.match(r'b(\d+)', chat or '')
                print('%s\t%s\t%s' % (pending, chat, 'landed' if b and b.group(1) == '99' else 'lost'))
                pending = None
            if step.startswith('shot '):
                pending = step[5:]
    if pending:
        print('%s\t%s\t-' % (pending, chat))


if __name__ == '__main__':
    main()
