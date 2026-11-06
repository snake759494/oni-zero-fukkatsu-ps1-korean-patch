# CLUT 없는 TIM 확대 시트: python tools/zvn.py out lo hi scale
import sys,pickle,struct
from PIL import Image,ImageDraw
d=open('orig/DATA00.DAT','rb').read()
lo,hi,sc=int(sys.argv[2],16),int(sys.argv[3],16),int(sys.argv[4])
ims=[]
for o,fl,x,y,w,h in pickle.load(open('gfx/nc.pkl','rb')):
    if not lo<=o<hi: continue
    W=w*(4 if fl==0 else 2); im=Image.new('L',(W,h)); p=o+20
    if fl==0: im.putdata([((d[p+(yy*w*2)+xx//2]>>((xx&1)*4))&15)*17 for yy in range(h) for xx in range(W)])
    else: im.putdata([d[p+yy*w*2+xx] for yy in range(h) for xx in range(W)])
    ims.append((o,x,y,im.resize((W*sc,h*sc),0)))
s=Image.new('L',(1600,3000),60); X=Y=rh=0; g=ImageDraw.Draw(s)
for o,x,y,i in ims:
    if X+i.width>1600: X=0;Y+=rh+14;rh=0
    s.paste(i,(X,Y+12)); g.text((X,Y),'%x %d,%d'%(o,x,y),fill=255); X+=i.width+8; rh=max(rh,i.height)
s.crop((0,0,1600,Y+rh+14)).save(sys.argv[1]); print(len(ims))
