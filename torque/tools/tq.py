# minimal Torque (TGE 1.x) server for the 5.12 handshake: logs every datagram, answers 0x1A with 0x1E, and with "accept" answers 0x20 with a 0x24 (class table + protocol 24)
import socket,sys,time,struct,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import tbits
CLASSES=[]  # (type, server id, class name) sent in the accept
out=sys.argv[1]; port=int(sys.argv[2]); accept='accept' in sys.argv # usage: tq.py <logdir> <udp port> [accept]
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',port))
def log(m): open(out+'/udp.txt','a').write('%.3f %s\n'%(time.time(),m))
n=0
while True:
    d,a=s.recvfrom(65536); n+=1
    open('%s/udp_%03d.bin'%(out,n),'wb').write(d)
    log('C->S %d bytes type=0x%02x %s'%(len(d),d[0],d.hex()))
    if d[0]==0x1a:
        seq=d[1:5]; r=b'\x1e'+seq+bytes(range(16)); s.sendto(r,a); log('S->C challenge response '+r.hex())
    elif d[0]==0x20 and accept:
        log('  '+repr(tbits.connect_request(d)))
        w=tbits.W(); w.u8(0x24); w.u32(struct.unpack('<I',d[1:5])[0])
        for t,i,nm in CLASSES: w.flag(1); w.int(t,12); w.int(i,12); w.str(nm)
        w.flag(0); w.u32(24); r=w.bytes(); s.sendto(r,a); log('S->C connect accept '+r.hex())
    elif d[0]&1:
        log('  data packet')
