import struct,re,pickle,collections
d=open('orig/DATA00.DAT','rb').read()
hits=pickle.load(open('refs.pkl','rb'))
pat=re.compile(rb'\x04\x00\x00\x00(....)((?:[\x81-\x9f\xe0-\xef][\x40-\xfc]|[\x20-\x7e])+)\x00',re.S)
tot=0;nf=0;nref=0;nob=0;files=0
ex=[];U=collections.Counter()
for so in sorted(hits):
  F=so*2048; sz=struct.unpack_from('<I',d,F)[0]; f=d[F:F+sz]
  if b'\x82' not in f: continue
  cnt=0
  W=collections.defaultdict(list)
  for i in range(0,len(f)-3,4): W[f[i:i+4]].append(i)
  for m in pat.finditer(f):
    s=m.group(2)
    if not re.search(rb'[\x81-\x9f\xe0-\xef]',s): continue
    try: s.decode('cp932')
    except: continue
    endoff=struct.unpack('<I',m.group(1))[0]
    st=m.start(2); en=m.end()   # after NUL
    pad=(-en)%4; en2=en+pad
    base=en2-endoff
    if base<0 or base>st: nob+=1; continue
    rel=struct.pack('<I',st-base)
    r=[i for i in W.get(rel,[]) if i!=m.start(1)]
    cnt+=1; tot+=1; nref+=bool(r)
    U[s]+=1
    if len(ex)<0: ex.append((hex(F),hex(base),len(r),s.decode('cp932')))
  if cnt: files+=1
print('files',files,'strings',tot,'withref',nref,'nobase',nob)
for e in ex: print(e)

print('unique',len(U),'chars',sum(len(k.decode('cp932')) for k in U))
import json;json.dump([k.decode('cp932') for k in U],open('uniq.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(set(''.join(k.decode('cp932') for k in U))))
