# 타이틀에서 はじめから 선택 → 변환 취소 → 무비 빨리감기 → 이름 입력 화면
import subprocess,sys,time
from PIL import Image
def c(cmd): return subprocess.run([sys.executable,'tools/c.py',cmd],capture_output=True,text=True).stdout
def state():
    im=Image.open('shots/t.png').convert('RGB'); w,h=im.size
    f=lambda y:sum(1 for x in range(620,810,4) if (lambda p:p[0]>180 and p[1]>160 and p[2]<120)(im.getpixel((int(w*x/960),int(h*y/766)))))
    v=[f(185),f(235),f(285)]
    return v.index(max(v)) if max(v)>2 else -1
subprocess.run([sys.executable,'tools/totitle.py'])
c('shot shots/t.png')
for i in range(10):
    st=state(); print('state',st)
    if st==0: break
    if st==-1:
        subprocess.run([sys.executable,'tools/totitle.py']); c('shot shots/t.png'); continue
    c('k up 0.2;w 0.25;shot shots/t.png')
c('k o 0.15;w 6;shot shots/t2.png')
c('k o 0.1;w 2;k x 0.1;w 2;k up 0.1;w 0.5;k o 0.1;w 3;ff 40;w 1;k o 0.1;w 1;shot shots/d.png')
print('done')
