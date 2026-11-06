# 빌드 준비: 원본 디스크에서 파일·원문 목록·참조표를 뽑아 냄(모두 배포하지 않는 원본 유래 파일)
#   python tools/prepare.py "../Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin"
import sys,os,subprocess,json,re,struct,pickle,hashlib
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(W)
T=os.path.join(W,'tools'); sys.path.insert(0,T)
def run(*a): subprocess.check_call([sys.executable,*a])
src=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(W),'Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin')
os.makedirs('text/src',exist_ok=True); os.makedirs('gfx',exist_ok=True)
print('1/6 디스크 추출'); run('tools/extract.py',src)
print('2/6 파일 참조표'); run('tools/refs.py')
print('3/6 대사 원문 목록')
from strings import files,scan
d,hits=files(); order=[];seen=set()
for so in sorted(hits):
    F=so*2048; sz=struct.unpack_from('<I',d,F)[0]; f=d[F:F+sz]
    if b'\x04\x00\x00\x00' not in f: continue
    for x in scan(f):
        t=x['text'].decode('cp932')
        if t not in seen: seen.add(t); order.append(t)
json.dump(order,open('text/ja_all.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('4/6 기타 문자열'); run('tools/misc_scan.py')
mr=json.load(open('text/misc_raw.json',encoding='utf-8'))
dbg=re.compile(r'ラベル|Ｌａ|もどる\^m|\^C00ff00|セリフ|テスト|デバッ|イベント|ＶＲＭ|コンバート')
misc=[t for t,p in sorted(mr.items(),key=lambda x:x[1][0]) if not dbg.search(t)]
for i in range(0,len(order),650):
    with open(f'text/src/d{i//650+1:02d}.tsv','w',encoding='utf-8') as f:
        for j in range(i,min(i+650,len(order))): f.write(f'd{j:05d}\t{order[j]}\n')
for i in range(0,len(misc),650):
    with open(f'text/src/m{i//650+1:02d}.tsv','w',encoding='utf-8') as f:
        for j in range(i,min(i+650,len(misc))):
            t=misc[j]; n=len(re.sub(r'\^[A-Za-z][0-9A-Fa-f]*','',t))
            f.write(f'm{j:04d}\t{n}\t{t}\n')
print('5/6 수동 교정용 문자열 해시표')
pat=re.compile(rb'(?<=[\x00\x01\x03])(?:[\x81-\x9f\xe0-\xef][\x40-\x7e\x80-\xfc]|[\x20-\x7e])+(?=\x00)')
H={}
for m in pat.finditer(d):
    try: t=m.group().decode('cp932')
    except: continue
    H.setdefault(hashlib.sha1(t.encode('utf-8')).hexdigest()[:16],t)
for t in order+list(mr): H.setdefault(hashlib.sha1(t.encode('utf-8')).hexdigest()[:16],t)
json.dump(H,open('text/hash_ja.json','w',encoding='utf-8'),ensure_ascii=False)
print('6/6 CLUT 없는 그림 목록')
res=[];i=0;seen=set()
while (i:=d.find(b'\x10\0\0\0',i))>=0:
    if i%4==0 and struct.unpack_from('<I',d,i+4)[0] in (0,1):
        L,x,y,w,h=struct.unpack_from('<IHHHH',d,i+8); fl=d[i+4]
        if L==12+w*h*2 and 0<w<=256 and 0<h<=256:
            hh=hashlib.md5(d[i+20:i+20+w*h*2]).hexdigest()
            if hh not in seen and w*(4 if fl==0 else 2)>=24 and h>=8: seen.add(hh); res.append((i,fl,x,y,w,h))
    i+=4
pickle.dump(res,open('gfx/nc.pkl','wb'))
print('완료')
