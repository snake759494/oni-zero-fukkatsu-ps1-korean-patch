import sys;sys.path.insert(0,'tools')
from gfx import *
MAPS=[0x83cd010+i*0x13800 for i in range(36)]
def L(s,v): r,g,b=s.rgb(v); return (r*3+g*6+b)/10
def xbtn(s):
    # 파란 × 버튼(밝은 파랑) 찾기
    pts=[(x,y) for y in range(60,240) for x in range(320) if (lambda c:c[2]>150 and c[0]<120 and c[2]-c[0]>70)(s.rgb(s.px[y][x]))]
    if not pts: return None
    xs=sorted(p[0] for p in pts); ys=sorted(p[1] for p in pts)
    return xs[len(xs)//2]-6, ys[len(ys)//2]-6
def title(s):
    best=None
    for y in range(15,90):
        run=m=0
        for x in range(10,310):
            if L(s,s.px[y][x])<70: run+=1; m=max(m,run)
            else: run=0
        if m>50 and (best is None or m>best[1]): best=(y,m)
    if not best: return None
    uy=best[0]
    # 밑줄 위쪽 글자
    pts=[(x,y) for y in range(max(5,uy-26),uy-3) for x in range(10,310) if L(s,s.px[y][x])<70]
    if not pts: return None
    return min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts)+1,max(p[1] for p in pts)+1,uy
if __name__=='__main__':
    from PIL import Image,ImageDraw
    d=bytearray(open('orig/DATA00.DAT','rb').read())
    out=Image.new('RGB',(1600,40*20),(0,0,0)); dr=ImageDraw.Draw(out)
    for i,o in enumerate(MAPS):
        s=Img(d,o); xb=xbtn(s); tb=title(s); print(hex(o),xb,tb)
        if tb:
            im=s.preview(1).crop((tb[0]-4,tb[1]-4,tb[2]+4,tb[3]+4)); im=im.resize((im.width*2,im.height*2),0)
            out.paste(im,((i%2)*800+60,(i//2)*40)); dr.text(((i%2)*800,(i//2)*40),'%d'%i,fill=(255,255,0))
    out.save('gfx/titles.png')
