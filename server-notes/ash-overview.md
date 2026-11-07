# Ash — Python reference implementation

A rewritten gserver. This is not the Reborn 2.4 binary used by Phoenix.
The code in ashserver.py / protocol.py was written from a comparison of the
source dumps in `graal gservers/`.

## What Ash implements

- servers.txt multi-instance (one world ships: servers/ash/)
- listen socket, 2-byte length framing
- encryption gen 3 / 4 / 5
- login (client + RC + NPC-Server)
- listserver register / ping / VERIACC2 (offline_login=true still works if the list is down)
- GRACC001 accounts, GLEVNW01 levels including BADDY
- props, chat, PM, warp, files
- RC file browser, options, accounts, flags
- gmaps / bigmaps / groupmaps
- baddies (hurt / respawn / optional drops)
- triggeraction hacks
- NPC-Server HASNPCSERVER + address + query relay

Horses, weapon bytecode and UPnP are still out. Phoenix still runs the
Reborn 2.4.0 binary if you need that exact engine.

## Quick start

1. Rename servers/ash/accounts/YOURACCOUNT.txt to your account name.
2. Put that name on staff= in servers/ash/config/serveroptions.txt.
3. python3 ashserver.py or ./start_ash.sh
4. Point a v2 client at your IP, port 14812.

The full Ash sources and world are in the Google Drive archive linked from `../ARCHIVAL.md`.

---
*Summary of the Ash rewrite from the decommissioned local workspace.*
