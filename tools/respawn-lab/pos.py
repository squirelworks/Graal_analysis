import sys,struct
pid=int(sys.argv[1]); m=open(f'/proc/{pid}/mem','rb')
m.seek(0x54B7E4); p=struct.unpack('<I',m.read(4))[0]; m.seek(p+4); x,y=struct.unpack('<dd',m.read(16))
print('pos',x,y)
