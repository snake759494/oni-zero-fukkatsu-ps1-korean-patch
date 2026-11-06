# 그래픽 텍스트 한글화 엔진: TIM(4/8bpp)을 인덱스 배열로 열어 지우기/글자 그리기 후 다시 기록
import struct,hashlib,os,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.path.insert(0,os.path.dirname(__file__))
from tim import parse
R=os.path.join(os.path.dirname(__file__),'..','..')
FONT={'brush':os.path.join(R,'SeoulHangangEB.ttf'),'serif':os.path.join(R,'SeoulHangangM.ttf'),'serifB':os.path.join(R,'SeoulHangangB.ttf'),
      'gothic':os.path.join(R,'NanumSquareNeo-cBd.ttf'),'heavy':os.path.join(R,'NanumSquareNeo-eHv.ttf'),'gothicR':os.path.join(R,'NanumSquareNeo-bRg.ttf'),
      'g11':os.path.join(R,os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'fonts','Galmuri11.ttf'),'g9':os.path.join(R,os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'fonts','Galmuri9.ttf'),'g7':os.path.join(R,os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'fonts','Galmuri7.ttf'),'g14':os.path.join(R,os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'fonts','Galmuri14.ttf')}
class Img:
    def __init__(s,d,o,pal=0,clut=None):
        t=parse(d,o); assert t,hex(o); s.t=t; s.d=d
        s.bpp=t['bpp']; s.W=t['w']*(4 if s.bpp==0 else 2); s.H=t['h']
        n=16 if s.bpp==0 else 256
        if clut=='gray':
            s.pal=[0]+[((i*2)|((i*2)<<5)|((i*2)<<10)) for i in range(1,16)]
        else:
            cx,cy,cw,ch,cp=t['clut'] if t['clut'] else parse(d,clut)['clut']
            s.pal=[struct.unpack_from('<H',d,cp+pal*cw*2+i*2)[0] for i in range(min(n,cw))]
        s.px=[[0]*s.W for _ in range(s.H)]
        for y in range(s.H):
            row=t['pix']+y*t['w']*2
            for x in range(s.W):
                s.px[y][x]=(d[row+x//2]>>((x&1)*4))&15 if s.bpp==0 else d[row+x]
        s.orig=bytes(d[t['pix']:t['end']])
    def rgb(s,i):
        v=s.pal[i]; return ((v&31)<<3,((v>>5)&31)<<3,((v>>10)&31)<<3)
    def near(s,c,skip0=True):
        best=None
        for i,v in enumerate(s.pal):
            if skip0 and v==0: continue
            r=s.rgb(i); e=sum((a-b)**2 for a,b in zip(r,c))
            if best is None or e<best[0]: best=(e,i)
        return best[1]
    def idx(s,c): return c if isinstance(c,int) else s.near(c)
    # --- 편집 ---
    def fill(s,x0,y0,x1,y1,c):
        c=s.idx(c)
        for y in range(max(0,y0),min(s.H,y1)):
            for x in range(max(0,x0),min(s.W,x1)): s.px[y][x]=c
    def copy(s,sx0,sy0,sx1,sy1,x0,y0,x1,y1):
        # 소스 영역을 타일링해서 대상 영역 채움(무늬 배경 지우기)
        src=[r[sx0:sx1] for r in s.px[sy0:sy1]]; w=sx1-sx0; h=sy1-sy0
        for y in range(y0,y1):
            for x in range(x0,x1): s.px[y][x]=src[(y-y0)%h][(x-x0)%w]
    def repl(s,x0,y0,x1,y1,frm,to):
        frm={s.idx(f) for f in frm}; to=s.idx(to)
        for y in range(y0,y1):
            for x in range(x0,x1):
                if s.px[y][x] in frm: s.px[y][x]=to
    def text(s,txt,x,y,w,h,font='brush',size=None,fg=(255,255,255),ol=None,ol2=None,align='c',sp=0,thr=110,bold=0,valign='c',shadow=None,sx=None,aa=None):
        # (x,y,w,h) 상자 안에 txt를 그림. ol=외곽선색, shadow=그림자색(오른쪽아래 1px)
        lines=txt.split('\n'); size=size or h//len(lines)
        f=ImageFont.truetype(FONT[font],size)
        S=1 if font[0]=='g' and font[1].isdigit() else 4  # 픽셀폰트는 원래 크기로
        fb=ImageFont.truetype(FONT[font],size*S)
        def lw(l): return sum(fb.getlength(ch) for ch in l)+sp*S*(len(l)-1)
        mw=max(lw(l) for l in lines)/S
        k=min(1.0,(w-(2 if ol else 0))/mw) if mw>0 else 1
        if sx: k=sx
        lh=h/len(lines)
        canvas=Image.new('L',(w*S,h*S),0); dr=ImageDraw.Draw(canvas)
        for li,l in enumerate(lines):
            tw=lw(l)*k
            if align=='c': cx=(w*S-tw)/2
            elif align=='l': cx=(1 if ol else 0)*S
            else: cx=w*S-tw-(1 if ol else 0)*S
            asc,desc=fb.getmetrics()
            bb=fb.getbbox('가나한')
            gh=bb[3]-bb[1]
            cy=li*lh*S+(lh*S-gh)/2-bb[1]
            for ch in l:
                g=Image.new('L',(int(fb.getlength(ch))+4*S,(size+4)*S*2),0)
                ImageDraw.Draw(g).text((0,0),ch,font=fb,fill=255)
                if k<1: g=g.resize((max(1,int(g.width*k)),g.height),Image.LANCZOS)
                canvas.paste(Image.new('L',g.size,255),(int(cx),int(cy)),g)
                cx+=fb.getlength(ch)*k+sp*S*k
        m=canvas.resize((w,h),Image.LANCZOS)
        if bold: m=m.filter(ImageFilter.MaxFilter(3)) if bold>1 else m
        M=[[m.getpixel((i,j))>=thr for i in range(w)] for j in range(h)]
        def put(xx,yy,c):
            X=x+xx;Y=y+yy
            if 0<=X<s.W and 0<=Y<s.H: s.px[Y][X]=c
        if bold==1:
            M=[[M[j][i] or (i>0 and M[j][i-1]) for i in range(w)] for j in range(h)]
        if shadow is not None:
            c=s.idx(shadow)
            for j in range(h):
                for i in range(w):
                    if M[j][i]: put(i+1,j+1,c)
        for ring,col in ((2,ol2),(1,ol)):
            if col is None: continue
            c=s.idx(col)
            for j in range(h):
                for i in range(w):
                    if M[j][i]:
                        for dy in range(-ring,ring+1):
                            for dx in range(-ring,ring+1):
                                if abs(dx)+abs(dy)<=ring+ (1 if ring==2 else 0): put(i+dx,j+dy,c)
        c=s.idx(fg)
        if aa is not None:
            if isinstance(fg,int): fg=s.rgb(fg)
            A=[[m.getpixel((i,j)) for i in range(w)] for j in range(h)]
            for j in range(h):
                for i in range(w):
                    a=A[j][i]/255
                    if a>0.15: put(i,j,s.near(tuple(int(fg[q]*a+aa[q]*(1-a)) for q in range(3))))
            return
        for j in range(h):
            for i in range(w):
                if M[j][i]: put(i,j,c)
    def inpaint(s,x0,y0,x1,y1,pred,grow=1):
        # pred(rgb)가 참인 픽셀(글자)을 주변 색 평균으로 메움
        x0=max(0,x0);y0=max(0,y0);x1=min(s.W,x1);y1=min(s.H,y1)
        M=set((x,y) for y in range(y0,y1) for x in range(x0,x1) if s.pal[s.px[y][x]]!=0 and pred(s.rgb(s.px[y][x])))
        for _ in range(grow):
            M|={(x+dx,y+dy) for x,y in M for dx in (-1,0,1) for dy in (-1,0,1) if x0<=x+dx<x1 and y0<=y+dy<y1}
        col={}
        while M:
            nxt=set(); upd={}
            for x,y in M:
                acc=[0,0,0];n=0
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                    X,Y=x+dx,y+dy
                    if (X,Y) in M or not(0<=X<s.W and 0<=Y<s.H): continue
                    c=col.get((X,Y)) or s.rgb(s.px[Y][X]); acc=[a+b for a,b in zip(acc,c)];n+=1
                if n>=2 or (n and len(M)<50): upd[(x,y)]=tuple(a//n for a in acc)
                else: nxt.add((x,y))
            if not upd: upd={p:(128,128,128) for p in nxt}; nxt=set()
            for p,c in upd.items(): col[p]=c
            M=nxt
        import random
        for (x,y),c in col.items():
            s.px[y][x]=s.near(c)
    def bytes(s):
        out=bytearray()
        for y in range(s.H):
            if s.bpp==0:
                for x in range(0,s.W,2): out.append(s.px[y][x]|(s.px[y][x+1]<<4))
            else: out+=bytes(s.px[y])
        return bytes(out)
    def preview(s,sc=3):
        im=Image.new('RGB',(s.W,s.H))
        for y in range(s.H):
            for x in range(s.W):
                i=s.px[y][x]; im.putpixel((x,y),(60,60,90) if s.pal[i]==0 else s.rgb(i))
        return im.resize((s.W*sc,s.H*sc),0)
def commit(d,img):
    # 같은 픽셀 데이터를 가진 모든 사본에 적용
    nb=img.bytes(); ob=img.orig; n=0; i=0
    while (i:=d.find(ob,i))>=0:
        d[i:i+len(ob)]=nb; n+=1; i+=len(ob)
    return n
