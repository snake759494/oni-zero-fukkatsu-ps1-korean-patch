# 사용: python tools/zv.py out.png lo hi [scale]  (범위 내 고유 TIM을 확대 시트로)
import sys,pickle,hashlib;sys.path.insert(0,'tools')
from tim import *
from PIL import ImageDraw
d=open('orig/DATA00.DAT','rb').read()
ts=pickle.load(open('gfx/tims.pkl','rb'))
lo,hi=int(sys.argv[2],16),int(sys.argv[3],16); sc=int(sys.argv[4]) if len(sys.argv)>4 else 2
seen=set();ims=[]
for t in ts:
    if not lo<=t["o"]<hi: continue
    if len(sys.argv)>5 and t["h"]>int(sys.argv[5]): continue
    h=hashlib.md5(d[t['pix']:t['end']]).hexdigest()
    if h in seen: continue
    seen.add(h); im=render(d,t); im=im.resize((im.width*sc,im.height*sc),0); ims.append((t,im))
W=1600; x=y=0; rh=0; pos=[]
for t,im in ims:
    if x+im.width>W: x=0; y+=rh+14; rh=0
    pos.append((x,y)); x+=im.width+6; rh=max(rh,im.height)
sh=Image.new('RGB',(W,y+rh+14),(70,70,70)); dr=ImageDraw.Draw(sh)
for (t,im),(x,y) in zip(ims,pos):
    sh.paste(im,(x,y+12),im); dr.text((x,y),'%x %dx%d'%(t['o'],im.width//sc,im.height//sc),fill=(255,255,0))
sh.save(sys.argv[1]); print(len(ims),sh.size)
