# 현재 화면 RAM을 덤프해 CLUT 없는/있는 TIM 중 RAM에 있는 것을 출력
import subprocess,sys,pickle,struct
r=bytes.fromhex(subprocess.run([sys.executable,'tools/c.py','rd 80000000 200000'],capture_output=True,text=True).stdout.strip())
d=open('orig/DATA00.DAT','rb').read()
for o,fl,x,y,w,h in pickle.load(open('gfx/nc.pkl','rb')):
    b=d[o+20:o+20+w*h*2]; k=b[len(b)//2:len(b)//2+48]
    if len(set(k))>=4 and k in r: print('nc',hex(o),w*(4-2*fl),h)
