# minimal Torque (TGE 1.x) handshake responder: logs every datagram and answers the connect challenge (0x1A) with a 0x1E response
import socket,sys,time,struct,os
out=sys.argv[1]; port=int(sys.argv[2])  # usage: tq.py <logdir> <udp port>
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',port))
def log(m): open(out+'/udp.txt','a').write('%.3f %s\n'%(time.time(),m))
n=0
while True:
    d,a=s.recvfrom(65536); n+=1
    open('%s/udp_%03d.bin'%(out,n),'wb').write(d)
    log('C->S %d bytes type=0x%02x %s'%(len(d),d[0],d.hex()))
    if d[0]==0x1a:
        seq=d[1:5]; r=b'\x1e'+seq+bytes(range(16)); s.sendto(r,a); log('S->C challenge response '+r.hex())
