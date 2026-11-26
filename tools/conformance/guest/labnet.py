#!/usr/bin/env python3
"""Lab link services for the conformance server VM: DHCP and DNS (lab only).

Runs as root inside the server VM, on the VM-only lab link that joins it to
the client VM (a QEMU dgram link: no host or outside network). The client
images were set up on QEMU user networking, so this answers as that network
did: one DHCP lease (CLIENT), with ROUTER and DNS as the server's own
addresses, and every DNS A query answered with ROUTER, so the client's
listserver host name lands on this VM.

    labnet.py IFACE CLIENT ROUTER DNS PREFIXLEN

Addresses come from the lab's local config (never from the repo).
Python 3 standard library only.
"""
import ipaddress
import socket
import struct
import sys
import threading


def dhcp(iface, client, router, dns, prefix):
    mask = ipaddress.IPv4Network((0, prefix)).netmask.packed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setsockopt(socket.SOL_SOCKET, 25, iface.encode())  # SO_BINDTODEVICE
    s.bind(("", 67))
    while True:
        q, _ = s.recvfrom(1500)
        if len(q) < 240 or q[0] != 1 or q[236:240] != b"\x63\x82\x53\x63":
            continue
        opts, i, kind = {}, 240, 0
        while i < len(q) and q[i] != 255:
            if q[i] == 0:
                i += 1
                continue
            opts[q[i]] = q[i + 2:i + 2 + q[i + 1]]
            i += 2 + q[i + 1]
        kind = opts.get(53, b"\0")[0]
        reply = {1: 2, 3: 5}.get(kind)  # DISCOVER -> OFFER, REQUEST -> ACK
        if not reply:
            continue
        r = bytearray(240)
        r[0:4] = b"\x02\x01\x06\x00"
        r[4:8] = q[4:8]                      # xid
        r[10:12] = q[10:12]                  # flags
        r[16:20] = socket.inet_aton(client)  # yiaddr
        r[20:24] = socket.inet_aton(router)  # siaddr
        r[28:44] = q[28:44]                  # chaddr
        r[236:240] = b"\x63\x82\x53\x63"
        o = bytes([53, 1, reply, 54, 4]) + socket.inet_aton(router)
        o += bytes([51, 4]) + struct.pack(">I", 86400)
        o += bytes([1, 4]) + mask + bytes([3, 4]) + socket.inet_aton(router)
        o += bytes([6, 4]) + socket.inet_aton(dns) + b"\xff"
        s.sendto(bytes(r) + o, ("<broadcast>", 68))
        print("dhcp", {1: "offer", 3: "ack"}[kind], client, flush=True)


def dns(bind, answer):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((bind, 53))
    a = socket.inet_aton(answer)
    while True:
        q, peer = s.recvfrom(512)
        if len(q) < 17:
            continue
        i = 12
        while i < len(q) and q[i]:
            i += q[i] + 1
        qtype = struct.unpack(">H", q[i + 1:i + 3])[0]
        question = q[12:i + 5]
        ans, n = (b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 60, 4) + a, 1) if qtype == 1 else (b"", 0)
        s.sendto(q[:2] + struct.pack(">HHHHH", 0x8180, 1, n, 0, 0) + question + ans, peer)


def main():
    iface, client, router, dns_ip, prefix = sys.argv[1:6]
    threading.Thread(target=dns, args=(dns_ip, router), daemon=True).start()
    dhcp(iface, client, router, dns_ip, int(prefix))


if __name__ == "__main__":
    main()
