# 대사(04000000 접두) 외의 NUL 종료 일본어 문자열 수집 → text/misc_raw.json
import re,json,collections
d=open('orig/DATA00.DAT','rb').read()
S=set(json.load(open('text/ja_all.json',encoding='utf-8')))
pat=re.compile(rb'(?:[\x81-\x9f\xe0-\xef][\x40-\x7e\x80-\xfc]|\^[A-Za-z]|[0-9A-Fa-f\x20])+\x00')
JP=re.compile(rb'[\x81-\x9f\xe0-\xef]')
res={}
for m in pat.finditer(d):
    b=m.group()[:-1]; st=m.start()
    if not JP.search(b): continue
    # 앞쪽 ASCII 잡음 제거
    k=re.match(rb'[0-9A-Fa-f\x20]*',b).end(); b=b[k:]; st+=k
    try: t=b.decode('cp932')
    except: continue
    if t in S: continue
    core=re.sub(r'\^[A-Za-z][0-9A-Fa-f]*','',t)
    ok=len(re.findall('[ぁ-ん]',core))>=2 or (len(core)>=3 and len(re.findall('[ァ-ヶー]',core))>=3 and 'ャャ' not in core) or (re.search('の|を|に|ン|ー',core) and len(core)>=3)
    if ok: res.setdefault(t,[]).append(st)
json.dump(res,open('text/misc_raw.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(res),sum(len(v) for v in res.values()))
