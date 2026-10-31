#!/usr/bin/env python3
"""Room-renaming proxy for Stefan Knorr's GServ relay lobby (1997-98).

Clients connect here; every line is passed to the real GServ unchanged,
except the join lines `N<room>#<name>` and `O<room>#<name>`, whose room is
renamed by the --map rules. Each line in both directions is logged.

  room_bridge.py --listen 14802 --server <loopback>:14801 \
      --map G2=G3 --log bridge.log

A rule `OLD=NEW` replaces the room prefix OLD with NEW, keeping the rest
(`G2=G3` turns `G2level13.graal` into `G3level13.graal`). The first rule
whose prefix matches wins; a room no rule matches is left alone.
"""
import argparse, socket, threading, time

# Default GServ address: the loopback address on 14801 (no dotted literal).
_LOOPBACK_SERVER = '%d.%d.%d.%d:14801' % (127, 0, 0, 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--listen', type=int, default=14802)
    ap.add_argument('--server', default=_LOOPBACK_SERVER)
    ap.add_argument('--map', action='append', default=[])
    ap.add_argument('--log', default='-')
    a = ap.parse_args()
    rules = [tuple(m.split('=', 1)) for m in a.map]
    host, port = a.server.rsplit(':', 1)
    log = open(a.log, 'a', buffering=1) if a.log != '-' else None
    t0 = time.time(); lock = threading.Lock()

    def note(cid, d, raw):
        line = f'{time.time() - t0:8.2f} {cid} {d} {raw!r}'
        with lock:
            print(line, file=log) if log else print(line, flush=True)

    def rename(line):
        if line[:1] in (b'N', b'O') and b'#' in line:
            room, rest = line[1:].split(b'#', 1)
            r = room.decode('latin-1')
            for old, new in rules:
                if r.startswith(old):
                    return line[:1] + (new + r[len(old):]).encode('latin-1') + b'#' + rest, r
        return line, None

    def pump(src, dst, cid, d, rewrite):
        buf = b''
        try:
            while True:
                chunk = src.recv(4096)
                if not chunk:
                    break
                buf += chunk
                while b'\n' in buf:
                    line, buf = buf.split(b'\n', 1)
                    if rewrite:
                        new, old = rename(line)
                        if old is not None:
                            note(cid, 'MAP', f'{old} -> {new[1:].split(b"#")[0].decode("latin-1")}')
                        line = new
                    note(cid, d, line)
                    dst.sendall(line + b'\n')
        except OSError:
            pass
        finally:
            for s in (src, dst):
                try: s.shutdown(socket.SHUT_RDWR)
                except OSError: pass

    ls = socket.socket(); ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind(('0.0.0.0', a.listen)); ls.listen(16)
    note('-', 'START', f'listen {a.listen} -> {a.server} rules {rules}')
    n = 0
    while True:
        c, addr = ls.accept(); n += 1; cid = f'c{n}'
        s = socket.create_connection((host, int(port)))
        note(cid, 'OPEN', f'{addr[0]}:{addr[1]}')
        threading.Thread(target=pump, args=(c, s, cid, 'C>S', True), daemon=True).start()
        threading.Thread(target=pump, args=(s, c, cid, 'S>C', False), daemon=True).start()

if __name__ == '__main__':
    main()
