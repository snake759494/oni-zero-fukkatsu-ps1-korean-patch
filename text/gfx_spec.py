# 그래픽 한글화 명세: 각 함수는 (d)를 받아 Img를 편집하고 commit
from gfx import Img,commit
W=(255,255,255)
SPEC=[]
def sp(f): SPEC.append(f); return f

@sp
def title_menu(d):
    s=Img(d,0x1d3bc74); s.fill(0,0,s.W,s.H,0)
    for i,t in enumerate(['처음부터','이어하기','덤']):
        s.text(t,0,i*16,72,16,font='serifB',size=14,fg=(240,240,240),ol=(8,8,8),aa=(24,24,24),sp=1)
    return s

def lum(s,i): r,g,b=s.rgb(i); return (r*3+g*6+b)/10
def tbbox(s,y0,y1,x0=0,x1=None,th=170):
    x1=x1 or s.W; xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if s.pal[s.px[y][x]]!=0 and lum(s,s.px[y][x])>th: xs.append(x);ys.append(y)
    return (min(xs),min(ys),max(xs)+1,max(ys)+1) if xs else None
def banner_erase(s,bb,y0=2,y1=22,inner=(0,None)):
    ix0,ix1=inner[0],inner[1] or s.W
    x0=max(ix0,bb[0]-2); x1=min(ix1,bb[2]+2)
    # 원본 패턴 띠: 글자 왼쪽 또는 오른쪽 빈 영역
    if x0-ix0>=6: sx0,sx1=ix0,x0
    elif ix1-x1>=6: sx0,sx1=x1,ix1
    else: sx0,sx1=None,None
    if sx0 is None:
        # 빈 띠가 없으면 글자 아닌 픽셀로 열 단위 대체
        for y in range(y0,y1):
            row=[v for v in s.px[y] if s.pal[v]!=0 and lum(s,v)<150] or [s.px[y][0]]
            for x in range(x0,x1): s.px[y][x]=row[(x*7)%len(row)]
    else:
        s.copy(sx0,y0,sx1,y1,x0,y0,x1,y1)
    return x0,x1
def banner(o,ko,sz=16,pair=None,al=None):
    def f(d):
        s=Img(d,o)
        pink=s.px[0][2]!=0 and lum(s,s.px[0][2])>150 and s.H==24
        inner=(8,s.W-8) if pink else (0,s.W)
        if pair=='L' or al=='f': inner=(8,s.W)
        if pair=='R': inner=(0,s.W-8)
        y0,y1=2,22
        bb=tbbox(s,y0,y1,inner[0],inner[1])
        if not bb: return s
        x0,x1=banner_erase(s,bb,y0,y1,inner)
        if pair: 
            # 좌/우 조각: 128폭 기준으로 그리고 잘라냄
            ox=0 if pair=='L' else -s.W
            s.text(ko,ox+10,4,2*s.W-20,16,font='heavy',size=sz,fg=(240,240,240),shadow=(88,88,104))
        elif al=='f':
            s.text(ko,10,4,s.W-12,16,font='heavy',size=sz,fg=(240,240,240),shadow=(88,88,104))
        elif al=='r':
            s.text(ko,bb[2]-44,4,44,16,font='heavy',size=sz,fg=(240,240,240),shadow=(88,88,104),align='r')
        elif al=='l':
            s.text(ko,bb[0]-1,4,80,16,font='heavy',size=sz,fg=(240,240,240),shadow=(88,88,104),align='l',sx=1)
        else:
            cx=(bb[0]+bb[2])//2; half=max(cx-inner[0],inner[1]-cx) if False else min(cx-inner[0],inner[1]-cx)-1
            half=max(half,(bb[2]-bb[0])//2+2)
            s.text(ko,cx-half,4,2*half,16,font='heavy',size=sz,fg=(240,240,240),shadow=(88,88,104))
        return s
    f.__name__='bn_%x'%o; SPEC.append(f); return f
BN='''9cca0fc 난토 거리
9cca73c 여관
9ccaa7c 신사
9ccac3c 퇴마 중개소
9ccb27c 삼중탑
9ccb73c 헤이조당
9ccbbfc 묘지기의 집
9ccc0bc 민가
9ccc5a4 마을 입구
9ccd964 신사
9cdfa64 사당으로 가는 산길
9ce0224:f 히비키 마을
9ce0564 오로치마루의 집
9ce0d24:r 연못
9ce14f8 덴치마루의 집
9ce1cb8:r 민가
9cf6a60 오쿠미야당
9cf6f20 광장
9cf7260 여관
9cf75b4 오쿠미야 마을
9cf83c8 마을 입구
9d2aa7c 역린당
9d2af3c 다카미 산길
9d2b924 간나의 집
9d2c8cc:f 역린 마을
9d2cf20 마을 입구
9d40a7c 오모모의 집
9d410bc 오로쿠의 집
9d416fc 기스케의 집
9d41d3c 구비오케당
9d4237c 아오타의 집
9d429bc 청년의 집
9d42ffc 아카베에의 집
9d4363c 제쓰넨사
9d43e50 지장보살
9d44190 곤고산 산길
9d447d0 마을 입구
9d44e10 구비오케 마을
9d45810 촌장의 집
9d7c4fc 사카이당
9d7c83c 원로의 집
9d7ccfc 다이조사
9d7d1bc 사카이 거리
9d90a70 행자당
9d91284 젠키당
9d91744 젠키 마을
9d91d84 태동순 동굴 앞
9d92d18 연못
9d94860 다리
9d94ba0 마른 밭
9d94ee0 데이로쿠당
9d953a0 마을 입구
9da96a8 마을 입구 부근
9db36bc 길가
9e10904 가모 야스노리 저택
9e10f44 공터
9e12a6c 헤이안당
9e13280 헤이안쿄
9e26a74 산고 산길
9e27408 미사키 신사
9e29430 미사키 마을
9e40a64 마을 외곽
9e59274 광장
9e595b4 전당포
9e59c48 쇼나의 집
9e5a988 아카치의 집
9e5b79c 다나시 숲
9e5bd1c 마을 입구
9e5d2dc 다나시 신사
9e5f68c 도박장
9e71a80 뒷산
9e71dc0 오치우도 마을
9e727c0 고운사
9e9a810 우마오시 마을'''
for l in BN.split('\n'):
    o,k=l.split(' ',1); o,_,a=o.partition(':'); banner(int(o,16),k,al=a or None)
banner(0x9da8668,'데이로쿠 마을',pair='L'); banner(0x9da89a8,'데이로쿠 마을',pair='R')
banner(0x9e5c29c,'다나시 마을',pair='L'); banner(0x9e5c5dc,'다나시 마을',pair='R')

# ---- 던전 지도: 제목 + 범례 ----
import sys; sys.path.insert(0,'tools')
from mapdet import xbtn
DARK=lambda c:(c[0]*3+c[1]*6+c[2])/10<100
MAPT='''83cd010 160 245 사당 가는 산길
83e0810 210 255 거울 뒤
83f4010 210 250 수해
8407810 200 300 오우다 산길
841b010 40 110 오니타카 산길
842e810 40 170 태동순 동굴
8442010 40 110 숨겨진 통로
8455810 40 110 구라마 산길
8469010 160 245 바위 가는 산길
847c810 190 260 산적 바위
8490010 30 110 조요 산길
84a3810 220 300 가사기 산길
84b7010 160 240 요코야마 산길
84ca810 160 250 창고 지하 1층
84de010 25 130 창고 지하 2층
84f1810 150 245 스기카제 숲
8505010 20 135 칠색수정 계곡
8518810 170 245 고카와 산길
852c010 30 115 기노카와 지류
853f810 160 245 가쓰라기산 정상
8553010 185 275 곤고산 산길
8566810 160 250 다나시 숲
857a010 220 290 미혹의 숲
858d810 190 260 마을 외곽
85a1010 185 275 다카미 산길
85b4810 200 240 뒷산
85c8010 150 275 난요사 가는 산길
85db810 40 130 흑룡의 동굴
85ef010 40 130 산고 산길
860280c 0 0 -'''
def mapf(o,x0,x1,ko):
    def f(d):
        s=Img(d,o)
        if ko!='-':
            X0,X1=max(8,x0-25),min(300,x1+20)
            runs=[]
            for y in range(34,80):
                r=m=0
                for x in range(X0,X1):
                    if DARK(s.rgb(s.px[y][x])): r+=1; m=max(m,r)
                    else: r=0
                runs.append((m,y))
            uy=max(runs)[1]
            while uy>34 and max(m for m,y in runs if y==uy-1)>=20: uy-=1
            dk=[(x,y) for y in range(max(20,uy-30),uy-1) for x in range(X0,X1) if DARK(s.rgb(s.px[y][x]))]
            bx0=min(p[0] for p in dk); bx1=max(p[0] for p in dk); by0=min(p[1] for p in dk)
            s.inpaint(bx0-1,by0-1,bx1+2,uy-1,DARK)
            cx=(bx0+bx1)//2; w=max(bx1-bx0+16,len(ko)*15)
            s.text(ko,cx-w//2,uy-22,w,20,font='brush',size=17,fg=(24,16,16))
        b=xbtn(s)
        if b:
            bx,by=b
            s.inpaint(bx+16,by-42,bx+80,by-8,DARK)
            s.inpaint(bx+12,by-2,bx+66,by+15,DARK)
            s.text('기록',bx+17,by-41,60,15,font='brush',size=13,fg=(24,16,16),align='l')
            s.text('귀심 회복',bx+17,by-25,60,15,font='brush',size=13,fg=(24,16,16),align='l')
            s.text('…종료',bx+14,by,56,15,font='brush',size=13,fg=(24,16,16),align='l')
        return s
    f.__name__='map_%x'%o; SPEC.append(f)
for l in MAPT.split('\n'):
    o,a,b,k=l.split(' ',3); mapf(int(o,16),int(a),int(b),k)

# ---- UI 글자 그림 ----
def ext(s,hi=True,skip=()):
    c=[i for i in range(len(s.pal)) if s.pal[i]!=0 and i not in skip]
    return (max if hi else min)(c,key=lambda i:lum(s,i))
def ui(o,ops,name=None):
    def f(d):
        s=Img(d,o)
        for op in ops: op(s)
        return s
    f.__name__=name or 'ui_%x'%o; SPEC.append(f)
def CLR(x0,y0,x1,y1,c=0): return lambda s:s.fill(x0,y0,x1,y1,ext(s,False) if c=='min' else c)
def T(t,x,y,w,h,font='gothic',size=None,fg='max',ol='min',**k):
    def op(s):
        F=ext(s) if fg=='max' else fg; O=(ext(s,False) if ol=='min' else ol)
        s.text(t,x,y,w,h,font=font,size=size,fg=F,ol=O,**k)
    return op
def INP(x0,y0,x1,y1,pred=DARK,grow=1): return lambda s:s.inpaint(x0,y0,x1,y1,pred,grow)
LIGHT=lambda c:(c[0]*3+c[1]*6+c[2])/10>170
DL=lambda c:DARK(c) or LIGHT(c)

ui(0x4a4a128,[CLR(0,0,72,56)]+[T(t,0,i*18+1,72,18,font='g11',size=12) for i,t in enumerate(['기록한다','교섭한다','아무것도 안 함'])])
ui(0xa406f28,[CLR(0,0,72,56)]+[T(t,0,i*18+1,72,18,font='g11',size=12) for i,t in enumerate(['기록한다','교섭한다','아무것도 안 함'])])
ui(0x4b00834,[CLR(0,0,16,16),CLR(64,0,176,16),CLR(0,16,176,32),CLR(0,32,128,48),
   T('값',0,0,16,16,font='g11',size=12),T('냥이 됩니다만',64,0,112,16,font='g11',size=12,align='l'),
   T('묵으시겠습니까?',8,16,160,16,font='g11',size=12,align='l'),
   T('예',0,32,32,16,font='g11',size=12,align='l'),T('아니오',56,32,60,16,font='g11',size=12,align='l')])
# 정반 도박 글자 타일(16x16)
G=[('홀',0,0),('짝',16,0),('베',32,0),('승',0,16),('리',16,16),('시',32,16),('배',0,32),('당',16,32),('금',32,32),('팅',0,48),('금',16,48),('액',32,48),('예',0,80),(' ',16,80),('아니',32,80)]
ui(0x7796e98,[CLR(x,y,x+16,y+16) for t,x,y in G]+[T(t,x,y,16,16,font='g11',size=12) for t,x,y in G if t.strip()]+
   [CLR(48,0,128,96),T('승리',48,2,80,42,font='brush',size=36,fg=(248,0,0),ol=None),T('패배',48,48,80,42,font='brush',size=36,fg=(0,0,248),ol=None)])
ui(0xa34acf8,[CLR(0,0,200,16),T('이 의뢰로 하시겠습니까?',0,0,200,16,font='g11',size=12,align='l')])
PL='난토 구비오케 마을 데이로쿠 마을 다카미 고개 젠키 마을 헤이안쿄 다나시 마을 구라마산 간나비산 요코야마 오치우도 마을 사카이 미사키 마을 칠색수정 계곡 가쓰라기산'
PLS=['난토','구비오케 마을','데이로쿠 마을','다카미 고개','젠키 마을','헤이안쿄','다나시 마을','구라마산','간나비산','요코야마','오치우도 마을','사카이','미사키 마을','칠색수정 계곡','가쓰라기산']
ui(0xa3fca70,[CLR(0,0,96,240,'min')]+[T(t,0,i*16,96,16,font='heavy',size=13,align='l') for i,t in enumerate(PLS)])
ui(0x9f92f54,[CLR(0,0,32,48)]+[T(t,0,i*16,32,16,font='g11',size=12,ol='min') for i,t in enumerate(['공격','방어','법술'])])
ui(0x482f23c,[CLR(0,0,32,16),T('독',0,0,16,16,font='g11',size=12,fg=(128,64,200)),T('봉',16,0,16,16,font='g11',size=12,fg=(96,96,200))])
ui(0x4831b30,[CLR(0,0,32,32),T('개',0,0,16,16,font='g11',size=12),T('신력',0,16,32,16,font='g11',size=12)])
ui(0x482a230,[CLR(0,0,16,16),T('돈',0,0,16,16,font='g11',size=12)])
ui(0xa51c024,[INP(20,20,190,85,LIGHT),T('올바르지 않은 이름입니다',24,22,170,24,font='g11',size=12,ol=None,align='l'),T('다시 입력해 주십시오',24,46,170,24,font='g11',size=12,ol=None,align='l')])
ui(0xa2ddac8,[INP(0,0,80,40,lambda c:(c[0]*3+c[1]*6+c[2])/10>95),T('슬롯 1',0,1,80,19,font='heavy',size=14,ol=None),T('슬롯 2',0,20,80,19,font='heavy',size=14,ol=None)])
ui(0xa34ddcc,[INP(90,18,228,48),INP(44,62,68,100),T('퇴마 의뢰서',85,19,150,28,font='brush',size=22,fg=(24,16,16),ol=None,sp=2),
   T('제',44,64,22,18,font='brush',size=16,fg=(24,16,16),ol=None)])
NEF=dict(font='serifB',size=13,fg=(24,20,16),ol=(224,216,200))
ui(0xa520ef8,[INP(130,15,256,38,DL),T('한글1',130,17,40,18,**NEF),T('한글2',172,17,40,18,**NEF),T('영숫자',212,17,44,18,**NEF),
   INP(36,169,74,186,DL),INP(100,169,140,186,DL),INP(158,169,198,186,DL),INP(14,185,300,219,DL),
   T('입력',38,170,36,15,**NEF,align='l'),T('삭제',102,170,36,15,**NEF,align='l'),T('변환',160,170,36,15,**NEF,align='l'),
   T('L1/R1 커서 이동   L2/R2 문자 변경',16,186,284,16,**NEF,align='l'),T('START 결정       SELECT 기본값',16,202,284,16,**NEF,align='l')],name='ui_nameentry')
RK={'고':(0,0),'갑':(0,16),'병':(0,32),'정':(0,48),'을':(0,64),'신':(0,80)}

def V(t,x,y,w,cell,**k):
    r=[];yy=y
    for ch in t:
        if ch==' ': yy+=cell//2; continue
        if ch in ',.': r.append(T(ch,x+w//2,yy-cell//3,w//2,cell,**k)); yy+=cell//3; continue
        r.append(T(ch,x,yy,w,cell,**k)); yy+=cell
    return r
VF=dict(font='serifB',size=17,fg='max',ol='min')
ui(0x83788e8,[CLR(0,0,24,168)]+V('주검이 된 은인들의',0,0,24,17,**VF))
ui(0x83920f0,[CLR(0,0,48,216)]+V('…이것이,',26,0,22,18,**VF)+V('은인 일족의 말로였다.',2,8,22,18,**VF))
ui(0x83ac8fc,[CLR(0,0,32,48)]+V('이제,',6,0,22,16,font='serifB',size=15))
ui(0x1dd380c,[CLR(0,0,192,40),T('― 8년 후 ―',0,4,192,32,font='serifB',size=26,fg=1,ol=None)])
ui(0x1d17a9c,[T('부활',122,40,40,15,font='g11',size=12,fg=(248,248,248),ol=(8,8,8))],name='ui_logo')
ui(0x1d3d80c,[T('끝',92,80,34,30,font='brush',size=24,fg=(248,248,248),ol=(0,0,0))],name='ui_end')
WOOD=dict(font='heavy',fg=(56,32,16),ol=None)
ui(0x1dd1448,[INP(8,12,40,30),INP(60,12,82,30),INP(152,12,180,32),INP(196,12,236,32),
   T('입구',8,13,32,16,size=13,**WOOD),T('입구',59,13,24,16,size=10,**WOOD),T('준비중',151,13,30,16,size=10,**WOOD),T('준비중',196,13,40,16,size=13,**WOOD)])
ui(0xa35f7ec,[CLR(0,0,48,48),T('갑',2,2,44,44,font='brush',size=40,fg=(216,24,24),ol=None)])
ui(0xa35fcac,[CLR(0,0,48,48),T('신',2,2,44,44,font='brush',size=40,fg=(24,24,200),ol=None)])
ui(0xa34a838,[CLR(0,0,48,48),T('을',2,2,44,44,font='brush',size=40,fg=(16,16,16),ol=None)])
RKC=[('고',0,'max'),('갑',21,(232,40,40)),('병',37,'max'),('정',53,'max'),('을',69,'max'),('신',86,(80,96,240)),('저',112,'max')]
ui(0xa3610e8,[CLR(0,y,24,y+16) for t,y,c in RKC]+[T(t,2,y,20,16,font='heavy',size=13,fg=c) for t,y,c in RKC])

# ---- 덤: Catch! 코너 메뉴 ----
INK=dict(font='heavy',fg=(32,24,16),ol=None)
DK2=lambda c:(c[0]*3+c[1]*6+c[2])/10<85
for o,t,sz in [(0x8d61038,'일러스트\n갤러리\n코멘트:나카지',13),(0x8d62538,'이런\n코너\n원해요!',15),(0x8d631f8,'무엇이든\n자랑!',15),
               (0x8d63eb8,'판도라\n편집부\n에게\n전언판',13),(0x8d64b78,'응모\n규칙',17),(0x8d65838,'당신 주변의\n별난\n물건',13)]:
    n=t.count('\n')+1
    ui(o,[INP(10,10,70,70,DK2),T(t,10,int(40-n*sz*0.6),60,int(n*sz*1.2),size=sz,**INK)])
ui(0x8d61cf8,[INP(80,4,128,28,DK2),T('모집',80,6,48,20,size=17,align='l',**INK)])
ui(0x8d66f0c,[INP(80,4,160,28,DK2),T('인포메이션',82,6,100,20,size=17,align='l',sx=1,**INK)])
ui(0x8d6794c,[INP(56,4,128,28,DK2),T('독자 사연',50,6,78,20,size=17,**INK)])

# ---- 세이브/로드 화면(CLUT 없는 TIM, 팔레트는 0x9a59078) ----
def uic(o,clut,ops,name=None):
    def f(d):
        s=Img(d,o,clut=clut)
        for op in ops: op(s)
        return s
    f.__name__=name or 'uc_%x'%o; SPEC.append(f)
SV=dict(font='heavy',fg=14,ol=3)
uic(0x9a5c5b0,0x9a59078,[CLR(0,0,88,40),T('데이터',2,1,52,19,size=16,**SV),T('세이브',30,20,56,19,size=16,**SV)])
uic(0x9a5d1b8,0x9a59078,[CLR(0,0,88,40),T('데이터',2,1,52,19,size=16,**SV),T('로드',30,20,56,19,size=16,**SV)])
uic(0x9a5cca4,0x9a59078,[lambda s:s.copy(3,2,17,35,17,2,57,35),T('예',22,3,38,16,font='heavy',size=13,fg=14,ol=3),T('아니오',22,20,38,16,font='heavy',size=12,fg=14,ol=3)])
uic(0x9a5dba8,0x9a59078,[CLR(0,0,48,16),T('슬롯 1',0,2,48,14,font='g11',size=12,fg=14,ol=None)])
uic(0x9a5dd3c,0x9a59078,[CLR(0,0,48,16),T('슬롯 2',0,2,48,14,font='g11',size=12,fg=14,ol=None)])
uic(0x9a5ded0,0x9a59078,[CLR(0,0,24,16),T('시간',0,0,24,16,font='g11',size=12,fg=14,ol=3)])
for o in [0x1d29354,0x1d2abe8,0x1d2c47c,0x1d2dd10]:
    uic(o,0x1d17a9c,[T('부활',122,40,40,15,font='g11',size=12,fg=(248,248,248),ol=(8,8,8))])

# ---- 메뉴/전투/상점 UI (CLUT 없음, 회색조 인덱스: 0=배경, 15=흰색) ----
MF=dict(font='serifB',fg=15,ol=None,aa=(0,0,0))
def g(o,ops): uic(o,'gray',[CLR(0,0,999,999)]+ops,name='ug_%x'%o)
def rows(ts,w,h,size=14,x=0,y=0,**k): return [T(t,x,y+i*h,w,h,size=size,**{**MF,**k}) for i,t in enumerate(ts)]
# 3색(15=글자,4=테두리,1=그림자) 메뉴: 안티앨리어싱 없이
def T3(t,x,y,w,h,size=14,**k):
    a=T(t,x+1,y+1,w,h,size=size,font='serifB',fg=1,ol=1,**k); b=T(t,x,y,w,h,size=size,font='serifB',fg=15,ol=4,**k)
    return lambda s:(a(s),b(s))
def rows3(ts,w,h,size=14): return [T3(t,0,i*h,w-1,h-1,size=size) for i,t in enumerate(ts)]
g(0x482aa8c,rows3(['공격','방어','법술'],32,16))
g(0x482ada0,[T3('신강림',0,0,55,15)])
g(0x482af74,rows3(['변신','도구','도주'],32,16))
g(0x482e958,[T('설정',0,0,32,24,size=18,**MF)])
g(0x482ef54,rows3(['일반','기술'],32,16))
g(0x482f93c,rows(['읽기：','장소：'],48,16))
g(0x482fd14,[T('신체',0,0,32,16,size=14,**MF)])
g(0x48301d4,[T3('개',0,0,15,15),T3('신력',0,16,31,15)])
g(0x4a45a90,[T('상품',0,0,24,16,size=12,**MF),T('금액',25,0,23,16,size=12,**MF),T('수량',49,0,23,16,size=12,**MF)])
g(0x4a47b78,[T('이것으로 괜찮습니까?',0,0,136,16,size=14,align='l',**MF),T('예',12,16,30,16,size=14,align='l',**MF),T('아니오',76,16,60,16,size=14,align='l',**MF)])
g(0x4a4840c,rows(['산다','판다','가게를 나간다'],72,18,size=14))
g(0x4a48c00,[T('몇 개 사시겠습니까?',4,0,124,18,size=13,align='l',sx=1,**MF),T('팔',47,18,14,18,size=13,**MF),
             T('소지수',0,36,48,18,size=14,align='l',**MF),T('합계',92,36,36,18,size=14,align='l',**MF),T('소지금',4,54,48,18,size=14,align='l',**MF)])
g(0x4a49e14,[T('교섭하시겠습니까?',0,0,96,16,size=13,align='l',font='serifB',fg=8,ol=None,aa=(0,0,0))])
g(0x4a4b068,rows(['체력','신력','공격력','방어력','민첩','덕'],48,20,size=15,align='l'))
g(0x4a4bbbc,[T('덕',0,2,24,28,size=22,**MF)])
g(0x4e813ac,[T('효과음량',0,0,64,16,size=14,**MF)])
g(0x4e815c0,[T('문자 속도',0,0,64,16,size=14,**MF)])
g(0x4e81c54,[T('결정',0,0,32,16,size=14,**MF)])
g(0x4e81d68,[T('진동 설정',0,0,64,16,size=14,**MF)])
g(0x4e81f7c,[T('선택지 색 변경',0,0,104,24,size=16,**MF)])

# 배너 남은 조각(CLUT 없음): 글자만 지움
def remnant(o):
    def f(d):
        s=Img(d,o,clut='gray')
        pink=lum(s,s.px[0][s.W//2])>150 if s.pal[s.px[0][s.W//2]] else False
        bb=tbbox(s,2,22,0,s.W,th=150)
        if bb: banner_erase(s,bb,2,22,(0,s.W-8) if pink else (0,s.W))
        return s
    f.__name__='rm_%x'%o; SPEC.append(f)
for o in [0x9ccc27c,0x9ccc410,0x9ce1124,0x9ce20b8,0x9ce248c,0x9cf7420,0x9d2c5b8,0x9d2cc0c,0x9d2d260,0x9d2d3f4,0x9d936ec]: remnant(o)

g(0x482fe28,[T('면',0,0,16,16,size=13,font='serifB',fg=9,ol=None),T('혼',16,0,16,16,size=13,font='serifB',fg=9,ol=None),T('마',32,0,16,16,size=13,font='serifB',fg=9,ol=None)])
# 서두/결말 세로 시
VB=dict(font='brush',fg=15,ol=None,size=19)
import pickle as _pk
_NC={o:h for o,fl,x,y,w,h in _pk.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','gfx','nc.pkl'),'rb'))}
def vp(o,cols,cell=20):
    ops=[]
    for x,y,t in cols:
        n=sum(0.5 if c==' ' else 0.34 if c in ',.' else 1 for c in t)
        c=int(min(cell,(_NC[o]-y)/n))
        ops+=V(t,x,y,24,c,**{**VB,'size':min(19,c-1)})
    g(o,ops)
vp(0x83790d8,[(0,0,'가는 길 비추는 흰 뼈')],cell=17)
vp(0x837986c,[(4,0,'향하는 곳 수라인가 아귀도인가')],cell=14)
vp(0x837a480,[(30,0,'깊은 어둠 끝에서'),(4,24,'그저 사라질 뿐')])
vp(0x8393570,[(24,0,'사람도 되지 못하고,'),(0,20,'요괴도 되지 못하네.')],cell=15)
vp(0x83943c4,[(24,0,'떨어져 가는 끝을,'),(0,20,'아는 이는 없다.')],cell=17)
vp(0x8397d58,[(24,0,'어둠에'),(0,0,'사라져')],cell=18)
vp(0x83982ac,[(12,0,'역사의')],cell=18)
vp(0x8398800,[(12,0,'버린 그들의')],cell=15)
vp(0x83acc3c,[(24,0,'사람 아닌 자가,'),(0,20,'어둠에 울부짖는 일은 없다.')],cell=13)
vp(0x83adf10,[(24,0,'사람이 요마를'),(0,20,'두려워하는 일도 없다.')],cell=15)
vp(0x83b1a24,[(30,0,'신의 힘이 사람에 깃드는 일도,'),(4,0,'이제는 없다.')],cell=12)
vp(0x83c906c,[(0,0,'끝없는 어둠에 잠겨 간다')],cell=13)
vp(0x83c9800,[(4,0,'일족의 운명 이제 다하다')],cell=13)
# 기타 UI
uic(0xa386ee0,'gray',[CLR(0,0,120,40),T('데이터',2,1,60,19,font='heavy',size=16,fg=15,ol=4),T('컨버트',44,20,74,19,font='heavy',size=16,fg=15,ol=4)])
uic(0xa51e5e4,'gray',[INP(20,20,190,80,lambda c:c[0]>120),T('이름을 입력해 주십시오',20,34,170,22,font='g11',size=12,fg=12,ol=None)])
uic(0xa34b378,'gray',[CLR(0,0,144,16),T('의뢰서를 보시겠습니까?',0,0,144,16,font='serifB',size=13,fg=8,ol=None,aa=(0,0,0),align='l')])
uic(0xa36016c,'gray',[CLR(0,0,160,16)]+[T(str(i+1),i*16,0,16,16,font='serifB',size=14,fg=7,ol=None,aa=(0,0,0)) for i in range(10)])
uic(0xa3607c0,'gray',[CLR(0,0,48,48),T('정',2,2,44,44,font='brush',size=40,fg=6,ol=None)])
uic(0xa360c54,'gray',[CLR(0,0,48,48),T('병',2,2,44,44,font='brush',size=40,fg=6,ol=None)])
uic(0xa2e1a94,'gray',[INP(4,2,76,38,lambda c:c[0]>100 or c[0]<30),T('슬롯 1',4,2,72,18,font='heavy',size=14,fg=15,ol=None),T('슬롯 2',4,20,72,18,font='heavy',size=14,fg=15,ol=None)])
uic(0xa388080,'gray',[INP(8,2,136,22,lambda c:c[0]>150 or c[0]<40),T('슬롯 1',10,3,56,18,font='heavy',size=14,fg=15,ol=None),T('슬롯 2',76,3,56,18,font='heavy',size=14,fg=15,ol=None)])
