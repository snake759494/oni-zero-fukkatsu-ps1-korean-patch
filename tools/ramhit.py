import sys,pickle
sys.path.insert(0,'tools')
d=open('orig/DATA00.DAT','rb').read(); r=open(sys.argv[1],'rb').read()
ts=pickle.load(open('gfx/tims.pkl','rb'))
seen=set()
for t in ts:
    b=d[t['pix']:t['end']]
    if len(b)<512 or b in seen: continue
    k=b[len(b)//2:len(b)//2+64]
    if len(set(k))<4: continue
    if k in r: seen.add(b); print(hex(t['o']),t['bpp'],t['w'],t['h'])
