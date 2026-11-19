#!/usr/bin/env python3
"""relay98: lab-only stand-in for the 1998 relay lobby (Knorr's GServ, the 1.1.9 Gserver.exe).

Enough of the lobby for one or more gen-1 clients to reach a session behind gen5probe:
  N<game>#<name> / O<game>#<name>  join a room   -> NR [NL] I<id8>, then C/+ lines as the 1.1.9 server sends
  P<id8>                         pair            -> P<id8> to both sides
  C                              leave the party -> C<id> to the partners
  -                              leave the room  -> -<id> to the rest of the room
  D<data>                        relay to every partner
Everything else is logged and ignored. Ids are `0000` plus a 4-digit counter across all connections,
as captured (protocol/relay-1998.md, client-internals/live-trace-early.md).

  relay98.py HOST PORT [--nl] [--fakepeer=ID]
    --nl          send `NL` after `NR` (the 1.1.9 server's local-levels mode)
    --fakepeer=N   announce a peer with id N (sent as 8 digits) (`+IDdef`) in every room a client joins, and confirm the client's
                  `P ID`. A client only answers `+` with `P` just after it joins a room, so this is how a
                  probe gets a partner whose `D` lines (injected by gen5probe) the client will take.
"""
import select, socket, sys, time

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
NL = '--nl' in sys.argv
FAKE = next(('%08d' % int(a.split('=', 1)[1]) for a in sys.argv if a.startswith('--fakepeer=')), None)  # id as 8 digits
HOST, PORT = ARGS[0], int(ARGS[1])
T0 = time.monotonic()


def log(*a):
    print('%9.3f %s' % (time.monotonic() - T0, ' '.join(str(x) for x in a)), flush=True)


class Conn:
    n = 0

    def __init__(self, s):
        Conn.n += 1
        self.s = s; self.id = '0000%04d' % Conn.n; self.room = None; self.partners = set(); self.buf = b''

    def send(self, line):
        try:
            self.s.sendall(line.encode('latin1') + b'\n')
        except OSError:
            pass
        log(self.id, '<-', repr(line)[:120])


conns = {}


def room_of(c):
    return [o for o in conns.values() if o is not c and o.room == c.room and c.room is not None]


def leave(c, quiet=False):
    for o in list(c.partners):
        o.partners.discard(c); o.send('C' + c.id)
    c.partners.clear()
    if c.room is not None:
        for o in room_of(c):
            o.send('-' + c.id)
    c.room = None


def line_in(c, line):
    log(c.id, '->', repr(line)[:120])
    if not line:
        return
    k, rest = line[0], line[1:]
    if k in 'NO':
        leave(c)
        c.room = rest.split('#', 1)[0]
        c.send('NR')
        if NL:
            c.send('NL')
        c.send('I' + c.id)
        for o in room_of(c):
            c.send('C' + o.id)
        for o in room_of(c):
            c.send('+' + o.id + 'def'); o.send('+' + c.id + 'def')
        if FAKE:
            c.send('+' + FAKE + 'def')
    elif k == 'P' and FAKE and rest[:8] == FAKE:
        c.send('P' + FAKE)
    elif k == 'P':
        o = next((x for x in conns.values() if x.id == rest[:8]), None)
        if o and o is not c:
            c.partners.add(o); o.partners.add(c); c.send('P' + o.id); o.send('P' + c.id)
    elif k == 'C':
        for o in list(c.partners):
            o.partners.discard(c); o.send('C' + c.id)
        c.partners.clear()
    elif k == '-':
        leave(c)
    elif k == 'D':
        for o in c.partners:
            o.send(line)


def main():
    L = socket.socket(); L.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); L.bind((HOST, PORT)); L.listen(16)
    log('relay98 listening', HOST, PORT, 'NL' if NL else '')
    while True:
        r, _, _ = select.select([L] + [c.s for c in conns.values()], [], [], 1)
        for s in r:
            if s is L:
                cs, _ = L.accept(); c = Conn(cs); conns[cs] = c; log(c.id, 'open'); continue
            c = conns[s]
            try:
                data = s.recv(4096)
            except OSError:
                data = b''
            if not data:
                log(c.id, 'closed'); leave(c); del conns[s]; s.close(); continue
            c.buf += data
            while b'\n' in c.buf:
                ln, c.buf = c.buf.split(b'\n', 1)
                line_in(c, ln.rstrip(b'\r').decode('latin1'))


if __name__ == '__main__':
    main()
