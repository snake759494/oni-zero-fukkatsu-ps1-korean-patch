# 스크립트 파일별 대사 문자열 위치 수집
import struct,re,pickle,collections
pat=re.compile(rb'\x04\x00\x00\x00(....)((?:[\x81-\x9f\xe0-\xef][\x40-\xfc]|[\x20-\x7e])+)\x00',re.S)
JP=re.compile(rb'[\x81-\x9f\xe0-\xef]')
def files():
    d=open('orig/DATA00.DAT','rb').read()
    hits=pickle.load(open('refs.pkl','rb'))
    return d,hits
def scan(f):
    """yield (start,end_after_nul,padded_end,base,text_bytes,refs)"""
    W=collections.defaultdict(list)
    for i in range(0,len(f)-3,4): W[f[i:i+4]].append(i)
    out=[]
    for m in pat.finditer(f):
        s=m.group(2)
        if not JP.search(s): continue
        try: s.decode('cp932')
        except: continue
        endoff=struct.unpack('<I',m.group(1))[0]
        st=m.start(2); en=m.end(); en2=en+((-en)%4)
        base=en2-endoff
        if base<0 or base>st: continue
        rel=struct.pack('<I',st-base)
        r=[i for i in W.get(rel,[]) if i!=m.start(1)]
        out.append(dict(st=st,en=en,en2=en2,base=base,lenpos=m.start(1),text=s,refs=r))
    return out
