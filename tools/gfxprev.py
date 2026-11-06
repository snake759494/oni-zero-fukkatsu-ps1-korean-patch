import sys,os;sys.path.insert(0,'tools');sys.path.insert(0,'text')
import gfx_spec
from PIL import Image
d=bytearray(open('orig/DATA00.DAT','rb').read())
names=sys.argv[1:]
ims=[]
for f in gfx_spec.SPEC:
    if names and f.__name__ not in names: continue
    r=f(d); r=r if isinstance(r,list) else [r]
    for s in r: ims.append(s.preview(3))
W=max(i.width for i in ims); H=sum(i.height+6 for i in ims)
o=Image.new('RGB',(W,H),(255,0,255)); y=0
for i in ims: o.paste(i,(0,y)); y+=i.height+6
o.save('gfx/prev.png')
