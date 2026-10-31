#!/usr/bin/env python3
"""Print the newline-terminated lines of each TCP stream in a pcap (lo, IPv4)."""
import struct, sys
def main(path, port):
    d = open(path, 'rb').read()
    link = struct.unpack('<I', d[20:24])[0]
    off = 24; streams = {}; t0 = None
    while off + 16 <= len(d):
        ts, tu, cl, _ = struct.unpack('<IIII', d[off:off+16]); pkt = d[off+16:off+16+cl]; off += 16 + cl
        t = ts + tu / 1e6; t0 = t0 or t
        ip = pkt[4:] if link == 0 else pkt[14:]  # DLT_NULL or ethernet
        if link == 1 and pkt[12:14] != b'\x08\x00': continue
        if ip[0] >> 4 != 4 or ip[9] != 6: continue
        ihl = (ip[0] & 15) * 4; tcp = ip[ihl:]
        sp, dp, seq = struct.unpack('>HHI', tcp[:8]); doff = (tcp[12] >> 4) * 4
        pay = tcp[doff:struct.unpack('>H', ip[2:4])[0] - ihl]
        if not pay: continue
        key = (sp, dp); s = streams.setdefault(key, {'seen': set(), 'buf': b''})
        if seq in s['seen']: continue
        s['seen'].add(seq); s['buf'] += pay
        while b'\n' in s['buf']:
            line, s['buf'] = s['buf'].split(b'\n', 1)
            d_ = 'C>S' if dp == port else 'S>C'
            c = sp if dp == port else dp
            print(f'{t - t0:8.2f} {c} {d_} {line!r}')
main(sys.argv[1], int(sys.argv[2]))
