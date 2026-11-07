"""pos.py PID PLAYER_GLOBAL_HEX: print the player's x, y from a running client.

PLAYER_GLOBAL_HEX is the static global that points at the player object; find it
on a live client with live-runs/2gta-222-2026-10-30/tools/findptr.py. Addresses are
not kept in the repo.
"""
import sys,struct
pid=int(sys.argv[1]); glob=int(sys.argv[2],16); m=open(f'/proc/{pid}/mem','rb')
m.seek(glob); p=struct.unpack('<I',m.read(4))[0]; m.seek(p+4); x,y=struct.unpack('<dd',m.read(16))
print('pos',x,y)
