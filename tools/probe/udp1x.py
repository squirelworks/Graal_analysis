#!/usr/bin/env python3
"""udp1x: lab-only peer-UDP sender for 1.28b2-1.39. Reads the client's own UDP port (its login
prop 31) from a gen5probe log and sends it UDP id-0 movement datagrams (X, Y, SPRITE, STATUS,
CARRYSPRITE, each +32) from a fixed local port, as a peer player would.

  udp1x.py PROXYLOG FROMPORT X2 Y2 [COUNT]     (X2/Y2 in half tiles)
Run inside the lab network namespace.
"""
import re, socket, sys, time

LO = '.'.join(['127', '0', '0', '1'])


def client_port(log):
    for line in open(log, encoding='latin1'):
        m = re.search(r'C>S id=2 len=\d+ \| .* \| hex=([0-9a-f]+)', line)
        if not m:
            continue
        b = bytes.fromhex(m.group(1)); i = 0
        while i < len(b):  # walk the login prop stream: 0 str, 11 str(len-100)/byte, 13 five bytes, 18/33 one byte, 31 GINT3
            p = b[i] - 32; i += 1
            if p in (0, 12):
                i += 1 + (b[i] - 32)
            elif p == 11:
                v = b[i] - 32; i += 1 + (v - 100 if v >= 100 else 0)
            elif p == 13:
                i += 5
            elif p == 31:
                return ((b[i] - 32) << 14) | ((b[i + 1] - 32) << 7) | (b[i + 2] - 32)
            else:
                i += 1
    return None


def main():
    log, fport, x2, y2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    n = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    cp = client_port(log)
    print('client UDP port', cp)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.bind((LO, fport))
    for k in range(n):
        s.sendto(bytes([0 + 32, x2 + 32, y2 + 32, 2 + 32, 16 + 32, -1 + 32]), (LO, cp)); time.sleep(0.1)
    print('sent', n)


if __name__ == '__main__':
    main()
