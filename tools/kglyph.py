# 오니제로 폰트용 한글 글리프: 15x15, 2bpp (0 투명, 1 채움, 2 중간, 3 외곽선)
from PIL import Image,ImageDraw,ImageFont
import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS={'neo':os.path.join(ROOT,'NanumSquareNeo-cBd.ttf'),'neoeb':os.path.join(ROOT,'NanumSquareNeo-dEb.ttf'),
       'neohv':os.path.join(ROOT,'NanumSquareNeo-eHv.ttf'),'hg':os.path.join(ROOT,'SeoulHangangB.ttf'),
       'g11':os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'fonts','Galmuri11.ttf')}
_ft={}
def ft(name,size):
    k=(name,size)
    if k not in _ft: _ft[k]=ImageFont.truetype(FONTS[name],size)
    return _ft[k]
def mask(ch,name='neo',size=13,box=13,thr=100,mid=60):
    """box x box 영역에 글자 채움 마스크(0/1/2) 반환"""
    f=ft(name,size)
    im=Image.new('L',(box*3,box*3),0); d=ImageDraw.Draw(im)
    d.text((box,box),ch,font=f,fill=255)
    bb=im.point(lambda v:255 if v>=thr else 0).getbbox()
    out=[[0]*box for _ in range(box)]
    if not bb: return out
    # 한글은 em 기준 위치 유지: 가로는 잉크 중앙, 세로는 잉크 중앙
    gw=bb[2]-bb[0]; gh=bb[3]-bb[1]
    ox=bb[0]-(box-gw)//2; oy=bb[1]-(box-gh)//2
    for y in range(box):
        for x in range(box):
            sx,sy=x+ox,y+oy
            if 0<=sx<im.width and 0<=sy<im.height:
                v=im.getpixel((sx,sy))
                out[y][x]=1 if v>=thr else (2 if v>=mid else 0)
    return out
def outline(m,W=15,H=15,off=1):
    """마스크를 (off,off)에 놓고 8방향 1px 외곽선(3)"""
    g=[[0]*W for _ in range(H)]
    for y,row in enumerate(m):
        for x,v in enumerate(row):
            if v: g[y+off][x+off]=v
    o=[r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x]==0:
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        yy,xx=y+dy,x+dx
                        if 0<=yy<H and 0<=xx<W and g[yy][xx]==1: o[y][x]=3
            elif g[y][x]==2:
                # 중간톤 화소는 외곽선과 채움 사이
                pass
    # 바깥쪽에 노출된 중간톤은 외곽선으로
    for y in range(H):
        for x in range(W):
            if o[y][x]==2:
                edge=any(0<=y+dy<H and 0<=x+dx<W and o[y+dy][x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
                if edge: o[y][x]=3
    return o
def encode(px,w=15,rows=15,b1=0):
    bpr=(w+4)>>2 if w&3 else w>>2
    out=bytearray([(w<<4)|rows,b1])
    for r in range(rows):
        for c in range(bpr):
            v=0
            for k in range(4):
                x=c*4+k; p=px[r][x] if x<len(px[r]) else 0
                v|=(p&3)<<(6-2*k)
            out.append(v)
    return bytes(out)
