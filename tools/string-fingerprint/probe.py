#!/usr/bin/env python3
"""Print which marker strings each client binary contains.

Usage: python3 -I probe.py FILE [FILE ...]

Y = present as ASCII, w = present as UTF-16LE only, - = absent.
Also prints any comma-separated property registry (a run of 40+ names
starting with "account" or containing "ismuted") with its length and
the position of "ismuted". Standard library only; reads files, runs nothing.
Used for protocol/client-string-fingerprints-3x-6x.md.
"""
import os
import re
import sys

PROBES = [
    "Illegal characters in the outgoing data",
    "Received illegal data (1)", "Received illegal data (2)",
    "Received invalid data (1)", "Received invalid data (2)",
    "Received invalid data (3)",
    "Cannot send data, socket is not initialized yet.",
    "DOQLHRbY", "Arc4Process", "Arc4SetKey",
    "StartScript_Connector", "StartScript_Fail", "scriptsslcipher", "scriptip",
    "StartScript_Profiles", "StartScript_QuitDialog",
    "onSendWantWeaponScript", "onSendPingAnswer", "tclient_",
    "onReceiveUDPData", "onReceiveDataPackage", "onBind",
    "GRESCR01", "quattro_lib", "SimObject", "Con::",
    "Torque Game Engine Demo", "TGraalConnection",
    "graal://", "graal3://", "setGraalProtocolString", "getGraalLoginInfo",
    "14899", "14900", "loginserver", "guest_", "-guestaccount",
    "hvdiPacketEncode", "hcryptEncryptPacket", "descipher",
    "GSERVL01", "GRMAP001", "GWEBL001", "GRPKG001", "GR-V1.04", "Z3-V1.04",
    ".gupd", "fixedudpport", "noudp", "switchToOpenGL",
    "Mass message:", "onRemotePlayerChats", "onPlayerLogin",
    "setplayerprop", "playerhp", "sendServerText",
    "Client-version: ", "User-Agent: Graal/",
    "Linux Cyberjoueur", "Eurocenter Games",
]


def main(paths):
    data = {p: open(p, "rb").read() for p in paths}
    names = [os.path.basename(p) for p in paths]
    print("probe\t" + "\t".join(names))
    for probe in PROBES:
        row = []
        for p in paths:
            d = data[p]
            if probe.encode() in d:
                row.append("Y")
            elif probe.encode("utf-16-le") in d:
                row.append("w")
            else:
                row.append("-")
        print(probe + "\t" + "\t".join(row))
    send_name = re.compile(rb"onSend[A-Z][A-Za-z0-9]+(?=\x00)")
    for p, n in zip(paths, names):
        print("onSend-names\t%s\t%d" % (n, len(set(send_name.findall(data[p])))))
        for m in re.finditer(rb"[a-z0-9]+(?:,[a-z0-9]+){40,}", data[p]):
            items = m.group().decode().split(",")
            if "account" in items[:3] or "ismuted" in items:
                pos = items.index("ismuted") if "ismuted" in items else None
                print("registry\t%s\t%d names\tismuted at %s" % (n, len(items), pos))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
