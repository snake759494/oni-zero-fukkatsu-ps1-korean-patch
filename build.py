# 오니제로 부활 한글패치 빌드
#   python build.py            → ../...[KR].bin 생성
import sys,os,struct,json,re,glob,bisect,pickle,collections,shutil
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'))
import font,kglyph,strings
from disc import Writer
from iso import Disc,SEC
from cdsec import form1
W=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(W)
SRC=os.path.join(ROOT,'Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin')
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan) [KR].bin')
os.chdir(W)
log=open('build.log','w',encoding='utf-8')
def warn(*a): print(*a,file=log)

# ---------- 번역 로드 ----------
def load_tsv(pat,cols):
    m={}
    for fn in sorted(glob.glob(pat)):
        for l in open(fn,encoding='utf-8'):
            l=l.rstrip('\n').rstrip('\r')
            if not l: continue
            p=l.split('\t')
            if len(p)>=2: m[p[0]]=p[-1]
    return m
def load_pairs(kind):
    src={};ko=load_tsv(f'text/ko/{kind}*.tsv',2)
    for fn in sorted(glob.glob(f'text/src/{kind}*.tsv')):
        for l in open(fn,encoding='utf-8'):
            p=l.rstrip('\n').split('\t'); src[p[0]]=p[-1]
    out={}
    for k,ja in src.items():
        if k in ko and ko[k]!=ja: out[ja]=ko[k]
        elif k not in ko: warn('번역없음',k,ja)
    return out
MAIN=load_pairs('d'); MISC=load_pairs('m'); MISC_FIX=set()
HJ=json.load(open('text/hash_ja.json',encoding='utf-8'))   # prepare.py가 원본에서 만든 해시→원문표
for l in open('text/ko/fix.tsv',encoding='utf-8'):   # 수동 교정(원문 SHA-1 앞 16자리<TAB>한국어)
    p=l.rstrip('\n').split('\t')
    if len(p)!=2: continue
    if p[0] not in HJ: warn('교정 원문 없음',p[0]); continue
    ja=HJ[p[0]]; MAIN[ja]=p[1]; MISC[ja]=p[1]; MISC_FIX.add(ja)

# ---------- 문자 정규화 / 문자셋 ----------
CTRL=re.compile(r'(\^[A-Za-z](?:[0-9A-Fa-f]{6}|[0-9]{2})?)')
HALF2FULL={'!':'！','?':'？',',':'，','.':'．','、':'，','。':'．','~':'～','(':'（',')':'）',':':'：','-':'－','+':'＋','%':'％','/':'／','"':'”',"'":'’','<':'〈','>':'〉','&':'＆','*':'＊','=':'＝','·':'・','…':'…','“':'「','”':'」','‘':'『','’':'』','—':'―','–':'－','「':'「','」':'」'}
for i in range(10): HALF2FULL[str(i)]=chr(0xFF10+i)
for i in range(26): HALF2FULL[chr(65+i)]=chr(0xFF21+i); HALF2FULL[chr(97+i)]=chr(0xFF41+i)
SPACE=' '   # 좁은 공백(전용 코드)
def norm(t):
    out=[]
    for part in CTRL.split(t):
        if CTRL.fullmatch(part): out.append(part); continue
        s=''
        for ch in part:
            if ch==' ' or ch=='　': s+=SPACE
            else: s+=HALF2FULL.get(ch,ch)
        out.append(s)
    return ''.join(out)
def is_hangul(ch): return 0xAC00<=ord(ch)<=0xD7A3
# 피해야 할 코드: 런타임 이름 글리프(司 狼 丸)와 특수코드
AVOID={0x8e69,0x9854,0x8adb,0x8140}
def code_iter():
    for lead in list(range(0x88,0xa0))+list(range(0xe0,0xeb)):
        for tr in list(range(0x40,0x7f))+list(range(0x80,0xfd)):
            c=(lead<<8)|tr
            if c<0x889f or c in AVOID: continue
            yield c
NAMES='게도마루 사키 유즈루 스즈카 오로치 이즈키 세이메이 세이메이 오즈누 오즈누 도쿄 기카쿠 기겐 아카메 기구치 오니스케 오니이치 오니지 오니토라 오니히코 간나 덴치마루 야스노리 야스노리 고바 스바 하다바 젠도키 묘도키 다테하'.split()
HERO='시로마루'
used=collections.Counter()
for t in NAMES+[HERO]:
    for ch in t: used[ch]+=1
for t in list(MAIN.values())+list(MISC.values()):
    for part in CTRL.split(norm(t)):
        if CTRL.fullmatch(part): continue
        for ch in part:
            if is_hangul(ch) or ch==SPACE: used[ch]+=1
CHARS=[SPACE]+sorted(c for c in used if c!=SPACE)
CODE={}
it=code_iter()
for ch in CHARS: CODE[ch]=next(it)
print('한글 글자 수',len(CHARS))
def enc(t,ctx=''):
    b=bytearray()
    for part in CTRL.split(norm(t)):
        if CTRL.fullmatch(part): b+=part.encode('ascii'); continue
        for ch in part:
            if ch in CODE: b+=CODE[ch].to_bytes(2,'big')
            else:
                try:
                    e=ch.encode('cp932')
                    if len(e)!=2: raise ValueError
                    b+=e
                except Exception:
                    warn('인코딩불가',repr(ch),ctx); b+=b'\x81\x48'
    return bytes(b)

# ---------- 폰트 ----------
def build_font(d,F=0x325d000,blob_end=0x2785a-0x75ec):
    font.F=F; f=font.load(d)
    n=39*191
    offs=[struct.unpack_from('<I',f,8+i*4)[0] for i in range(n)]
    # 0~3행(기호·가나·영숫자) 글리프는 유지, 나머지는 새로 배치
    keep={}
    for i in range(4*191):
        if offs[i]!=0xffffffff: keep[i]=offs[i]
    old=bytes(f[font.GB:font.GB+blob_end])
    def gsize(o):
        h=old[o]; w=h>>4; r=h&15; bpr=(w+4)>>2 if w&3 else w>>2; return 2+bpr*r
    new=bytearray(); remap={}
    for i,o in sorted(keep.items(),key=lambda x:x[1]):
        if o not in remap: remap[o]=len(new); new+=old[o:o+gsize(o)]
    newoffs=[0xffffffff]*n
    for i,o in keep.items(): newoffs[i]=remap[o]
    q=remap[offs[font.idx(0x8148)]]   # '？' 대체
    # 런타임 이름 글리프 자리(司 狼 丸)는 원래 글리프 유지
    for c in (0x8e69,0x9854,0x8adb):
        o=offs[font.idx(c)]; newoffs[font.idx(c)]=len(new); new+=old[o:o+gsize(o)]
    for ch in CHARS:
        if ch==SPACE: g=encode_space()
        else: g=kglyph.encode(kglyph.outline(kglyph.mask(ch,'neo',14,13)))
        newoffs[font.idx(CODE[ch])]=len(new); new+=g
    for i in range(4*191,n):
        if newoffs[i]==0xffffffff and offs[i]!=0xffffffff: newoffs[i]=q
    if len(new)>blob_end: raise SystemExit(f'폰트 공간 부족 {len(new)}>{blob_end}')
    new+=b'\0'*(blob_end-len(new))
    for i in range(n): struct.pack_into('<I',f,8+i*4,newoffs[i])
    f[font.GB:font.GB+blob_end]=new
    print('폰트 사용',len(new),'/',blob_end)
    return bytes(f)
def encode_space(w=5):
    return kglyph.encode([[0]*8 for _ in range(15)],w=w)

# ---------- DATA00 ----------
OP_OK=(b'\x30\x17',b'\x30\x1d')
def patch_script(f,stat):
    """f: bytes(파일 전체, 크기헤더 포함). 반환 bytearray"""
    L=strings.scan(f)
    if not L: return None
    f=bytearray(f); free=[]; pending=[]
    changed=False
    for x in L:
        ja=x['text'].decode('cp932'); ko=MAIN.get(ja)
        if ko is None: continue
        b=enc(ko,ja)+b'\0'
        slot=x['en']-x['st']
        refs=[r for r in x['refs'] if bytes(f[r-8:r-6]) in OP_OK]
        changed=True
        if len(b)<=slot:
            f[x['st']:x['en']]=b+b'\0'*(slot-len(b)); stat['inplace']+=1
            if slot-len(b)>=4: free.append([x['st']+len(b)+((-(x['st']+len(b)))%4), x['en']])
        elif refs:
            f[x['st']:x['en']]=b'\0'*slot; free.append([x['st'],x['en']])
            pending.append((b,refs,x['base']))
        else:
            # 참조를 못 찾음 → 잘라서 제자리
            e=enc(ko.replace(' ',''),ja)
            cut=e[:slot-1]
            if len(cut)%2: cut=cut[:-1]
            f[x['st']:x['en']]=cut+b'\0'*(slot-len(cut)); stat['cut']+=1; warn('잘림',ja,'→',ko)
    for b,refs,base in sorted(pending,key=lambda p:-len(p[0])):
        pos=None
        for fr in sorted(free,key=lambda r:r[1]-r[0]):
            a=fr[0]+((-fr[0])%2)
            if a>=base and fr[1]-a>=len(b): pos=a; fr[0]=a+len(b); break
        if pos is None:
            while len(f)%4: f+=b'\0'
            pos=len(f); f+=b; stat['append']+=1
        else: stat['reuse']+=1
        f[pos:pos+len(b)]=b
        for r in refs: struct.pack_into('<I',f,r,pos-base)
    while len(f)%4: f+=b'\0'
    struct.pack_into('<I',f,0,len(f))
    return f if changed else None

GRID_SYL='가간강거건경고공구국군권규근기길김나남노누니다단달대도동두라란래로루류리린마만명모무문미민바박반배백범보봉부비빈사산상서석선설성세소손송수순승시신실아안애야양여연영예오옥온완요용우운원월유윤은을의이인일임자장재전정제조종주준중지진찬창채천철청초최춘치카케코쿠키타태토하한해허혁현호홍화환효후훈휘희'
GRID_PAGES=[('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ',0),
            ('アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンヴァィゥェォッャュョヵガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヶ',1)]
def patch_namegrid(bufs):
    syl=[c for c in GRID_SYL if c in CODE]
    n=0
    for kana,pg in GRID_PAGES:
        mp={}
        for i,k in enumerate(kana):
            j=pg*90+i
            mp[k.encode('cp932')]=CODE[syl[j]].to_bytes(2,'big') if j<len(syl) else CODE[SPACE].to_bytes(2,'big')
        # 그리드 표/표시 문자열: 가나 2바이트를 치환(대응 표에 있는 글자만)
        for key in ({0:['あいうえおまみむめもがぎぐげご','^PC000^PL000あいうえお','^PC000^PL000まみむめも','^PC000^PL000がぎぐげご'],
                     1:['アイウエオマミムメモガギグゲゴ','^PC000^PL000アイウエオ','^PC000^PL000マミムメモ','^PC000^PL000ガギグゲゴ']}[pg]):
            kb=key.encode('cp932')
            for buf in bufs:
                i=0
                while (i:=buf.find(kb,i))>=0:
                    e=buf.find(bytes(1),i); j=i
                    while j<e:
                        c=bytes(buf[j:j+1])
                        if c==b'^': j+=1+1+ (3 if buf[j+1:j+2] in (b'P',) and buf[j+2:j+3] in (b'C',b'L') and False else 0); continue
                        if buf[j]>=0x80:
                            two=bytes(buf[j:j+2])
                            if two in mp: buf[j:j+2]=mp[two]; n+=1
                            j+=2
                        else: j+=1
                    i=e
    print('이름 그리드',n)

def patch_misc(d,newf={}):
    raw=json.load(open('text/misc_raw.json',encoding='utf-8'))
    n=0
    for ja,ko in MISC.items():
        if ja not in raw:
            if ja in MISC_FIX:
                ob=ja.encode('cp932'); ps=[]; i=0
                while (i:=d.find(ob+bytes(1),i))>=0:
                    if d[i-1] in (0,1,3): ps.append(i)
                    i+=1
                raw[ja]=ps
            else: continue
        ob=ja.encode('cp932'); nb=enc(ko,ja)
        k2=ko
        while len(nb)>len(ob) and ' ' in k2:
            i=k2.rfind(' '); k2=k2[:i]+k2[i+1:]; nb=enc(k2,ja)
        if len(nb)>len(ob):
            warn('기타 초과',ja,'→',ko,len(nb),len(ob))
            nb=nb[:len(ob)]
        nb+=CODE[SPACE].to_bytes(2,'big')*((len(ob)-len(nb))//2)
        for p in raw[ja]:
            if d[p:p+len(ob)]==ob: d[p:p+len(ob)]=nb; n+=1
        for so,f in newf.items():
            i=0
            while (i:=f.find(ob+bytes(1),i))>=0:
                if True:
                    f[i:i+len(ob)]=nb; n+=1
                i+=len(ob)
    patch_namegrid([d]+list(newf.values()))
    # 이름 입력 화면의 주인공 기본 이름(司狼丸　) → 시로마루
    ob=bytes.fromhex('000303038e6998548adb8140'); nb=bytes.fromhex('00030303')+enc(HERO)
    for buf in [d]+list(newf.values()):
        i=0
        while (i:=buf.find(ob,i))>=0: buf[i:i+len(ob)]=nb; n+=1; i+=len(ob)
    print('기타 문자열',n)

def main():
    disc=Disc(SRC)
    files={p:(l,s) for p,l,s,_,_ in disc.walk()}
    d=bytearray(open('orig/DATA00.DAT','rb').read())
    # 그래픽 글자 한글화
    sys.path.insert(0,os.path.join(W,'tools')); sys.path.insert(0,os.path.join(W,'text'))
    import gfx_spec,gfx
    ng=0
    for f in gfx_spec.SPEC:
        n=gfx.commit(d,f(bytes(d)))
        if n==0: warn('그래픽 미적용',f.__name__)
        ng+=n
    print('그래픽',len(gfx_spec.SPEC),'항목',ng,'곳')
    hits=pickle.load(open('refs.pkl','rb'))
    starts=sorted(hits); N=len(d)//2048
    sizes={so:struct.unpack_from('<I',d,so*2048)[0] for so in starts}
    # 각 파일 처리
    stat=collections.Counter(); newf={}
    for so in starts:
        F=so*2048; f=bytes(d[F:F+sizes[so]])
        if b'\x04\x00\x00\x00' not in f: continue
        r=patch_script(f,stat)
        if r is not None: newf[so]=r
    print('대사',dict(stat),'수정 파일',len(newf))
    # 폰트
    FONTS=[(0x325d000,0x2785a-0x75ec)]
    for s_ in range(len(d)//2048):
        F=s_*2048
        if F!=0x325d000 and d[F:F+8]==bytes.fromhex('65000f0000000000'):
            font.F=F; f_=font.load(d); be=0
            for i in range(39*191):
                o=struct.unpack_from('<I',f_,8+i*4)[0]
                if o==0xffffffff: continue
                p=font.GB+o; h=f_[p]; w=h>>4; r=h&15; be=max(be,o+2+((w+4)>>2 if w&3 else w>>2)*r)
            FONTS.append((F,be))
    for F,be in FONTS:
        fnt=build_font(bytes(d),F,be); d[F:F+len(fnt)]=fnt
    patch_misc(d,newf)
    # 수정 파일을 버퍼에 쓰기(자리 부족시 DATA00 끝으로)
    nxt={}
    allst=sorted(set(starts)|{N})
    for i,so in enumerate(allst[:-1]): nxt[so]=allst[i+1]
    exe=bytearray(open('orig/SLPS_031.06','rb').read())
    for i,nm in enumerate(NAMES):
        b=enc(nm); exe[0x1908+i*8:0x1910+i*8]=b+bytes([0x81,0x40])*((8-len(b))//2); exe[0x19f8+i]=len(b)
    exe[0x1a24:0x1a2c]=enc(HERO)
    # EXE 내장 스크립트의 기본 이름: [　　　　NUL 030303][司狼丸NUL 01] → [　　　NUL 01][시로마루NUL 030303]
    o=0x801937d8-0x80143b00+0x800
    assert exe[o:o+20]==bytes.fromhex('8140814081408140000303038e6998548adb0001')
    assert exe[o+20:o+24]==bytes(4)
    exe[o+12:o+20]=enc(HERO)   # 고정 오프셋(+12)에서 읽음, 종결 NUL은 뒤의 0 워드
    moved=0
    for so,f in newf.items():
        ns=(len(f)+2047)//2048
        if so+ns<=nxt[so]:
            dst=so
        else:
            while len(d)%2048: d+=b'\xff'
            dst=len(d)//2048; d+=b'\xff'*(ns*2048); moved+=1
        blk=bytes(f)+b'\xff'*((-len(f))%2048)
        d[dst*2048:dst*2048+len(blk)]=blk
        if dst!=so or ns!=(sizes[so]+2047)//2048:
            val=struct.pack('<I',(ns<<24)|dst)
            for src,pos in hits[so]:
                tgt=exe if src=='E' else d
                old=struct.pack('<I',(((sizes[so]+2047)//2048)<<24)|so)
                # 위치가 옮겨진 파일 안의 참조는 새 위치에서 고침
                if src=='D':
                    j=bisect.bisect_right(starts,pos//2048)-1; cso=starts[j]
                    if cso in newf and cso!=so and pos<cso*2048+sizes[cso]:
                        pass
                if tgt[pos:pos+4]==old: tgt[pos:pos+4]=val
                else: warn('참조불일치',so,src,hex(pos))
    print('이동 파일',moved,'DATA00',len(d))
    return d,exe

def bcd(x): return ((x//10)<<4)|(x%10)
def move_raw(w,src,dst,n):
    for i in range(n):
        sec=bytearray(w.sector(src+i)); l=dst+i+150
        sec[12:15]=bytes([bcd(l//4500),bcd((l//75)%60),bcd(l%75)])
        if not (sec[18]&0x20): form1(sec)
        w.f.seek((dst+i)*SEC); w.f.write(sec)
    w.end=max(w.end,dst+n)

def write_disc(d,exe):
    print('BIN 복사…'); shutil.copyfile(SRC,OUT)
    w=Writer(OUT)
    p,lba,size,_,_=w.files['/DATA00.DAT']
    need=(len(d)+2047)//2048
    after=sorted((x[1],x[0],x[2]) for x in w.files.values() if x[1]>lba)
    room=after[0][0]-lba
    for flba,fp,fsz in after:
        if room>=need: break
        n=(fsz+2047)//2048; dst=w.end
        move_raw(w,flba,dst,n); w._update_dir(fp,dst,fsz); w.files[fp]=(fp,dst,fsz)+w.files[fp][3:]
        print('이동',fp,flba,'→',dst)
        nxtl=min([x[1] for x in w.files.values() if x[1]>lba])
        room=nxtl-lba
    if room<need: raise SystemExit('공간 부족')
    orig=open('orig/DATA00.DAT','rb').read(); n=0
    for i in range(need):
        blk=bytes(d[i*2048:(i+1)*2048]).ljust(2048,bytes(1))
        if blk!=orig[i*2048:(i+1)*2048]:
            w.wsec(lba+i,blk,last=(i==need-1),keep_sub=(i<len(orig)//2048 and i!=need-1)); n+=1
    w._update_dir('/DATA00.DAT',lba,len(d))
    print('DATA00 섹터 기록',n)
    oe=open('orig/SLPS_031.06','rb').read()
    if bytes(exe)!=oe: w.replace('/SLPS_031.06',bytes(exe),allow_move=False)
    w.f.close(); print('완료',OUT)

if __name__=='__main__':
    d,exe=main()
    write_disc(d,exe)
