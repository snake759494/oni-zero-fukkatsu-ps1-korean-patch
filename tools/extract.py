import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from iso import Disc
d=Disc(sys.argv[1]); os.makedirs('orig',exist_ok=True)
for p,l,sz,_,_ in d.walk():
    if p.endswith('.STR'): continue
    open('orig/'+p[1:],'wb').write(d.read(l,sz))
