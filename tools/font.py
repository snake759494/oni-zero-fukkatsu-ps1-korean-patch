# 폰트 파일(DATA00 0x325d000) 읽기/글리프 디코드
import struct
F=0x325d000; GB=0x75ec
LEAD={}
for i,l in enumerate(list(range(0x81,0x85))+list(range(0x88,0xa0))+list(range(0xe0,0xeb))): LEAD[l]=i
def idx(code): return LEAD[code>>8]*191+(code&0xff)-0x40
def load(d):
    sz=struct.unpack_from('<I',d,F)[0]; return bytearray(d[F:F+sz])
def glyph(f,code):
    o=struct.unpack_from('<I',f,8+idx(code)*4)[0]
    if o==0xffffffff: return None
    p=GB+o; h=f[p]; b1=f[p+1]; w=h>>4; rows=h&15
    bpr=(w+4)>>2 if w&3 else w>>2
    px=[[0]*(bpr*4) for _ in range(rows)]
    for r in range(rows):
        for c in range(bpr):
            v=f[p+2+r*bpr+c]
            for k in range(4): px[r][c*4+k]=(v>>(6-2*k))&3
    return w,rows,b1,px
