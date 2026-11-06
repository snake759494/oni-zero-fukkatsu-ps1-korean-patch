# 타이틀 화면이 나올 때까지 START 입력
import subprocess,sys
from PIL import Image
def c(cmd): return subprocess.run([sys.executable,'tools/c.py',cmd],capture_output=True,text=True).stdout
for i in range(40):
    c('p start w2;shot shots/t.png')
    im=Image.open('shots/t.png').convert('RGB')
    w,h=im.size; px=[im.getpixel((int(w*x),int(h*y))) for x,y in((0.05,0.3),(0.9,0.15),(0.6,0.95))]
    if all(p[2]>60 and p[2]>p[0]+20 for p in px): print('title',i); break
