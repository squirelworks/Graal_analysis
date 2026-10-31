# g2cli.py: minimal gen-2 (GSERV014) client for GServer13. Lines chr(id+32)+data+'\n', frame u16be + zlib.
import socket, zlib, struct, time, sys

# Default host: the loopback address (no dotted literal in source).
_LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)

class Cli:
    def __init__(s, acct, pw, host=None, port=14804):
        if host is None:
            host = _LOOPBACK
        s.sock = socket.create_connection((host, port)); s.buf = b''; s.t0 = time.time()
        s.send(0, b'GSERV014' + bytes([len(acct)+32]) + acct.encode() + bytes([len(pw)+32]) + pw.encode())
    def send(s, mid, data):
        z = zlib.compress(bytes([mid+32]) + data + b'\n')
        s.sock.sendall(struct.pack('>H', len(z)) + z)
    def recv(s, timeout=1.0):
        s.sock.settimeout(timeout); out = []
        try:
            while True:
                d = s.sock.recv(65536)
                if not d: out.append(('EOF', b'')); break
                s.buf += d
                while len(s.buf) >= 2:
                    n = struct.unpack('>H', s.buf[:2])[0]
                    if len(s.buf) < 2+n: break
                    body = zlib.decompress(s.buf[2:2+n]); s.buf = s.buf[2+n:]
                    for line in body.split(b'\n'):
                        if line: out.append((line[0]-32, line[1:]))
                s.sock.settimeout(0.05)
        except socket.timeout: pass
        return out
