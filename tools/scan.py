import struct,re,collections
d=open('orig/DATA00.DAT','rb').read()
L=[0]+[o for o in range(0x800,len(d),0x800) if d[o-4:o]==b'\xff'*4 and d[o:o+4]!=b'\xff'*4]
pat=re.compile(rb'(?:[\x81-\x9f\xe0-\xef][\x40-\xfc]){2,}')
for F in L:
  sz=struct.unpack_from('<I',d,F)[0]
  if sz>0x100000 or sz<8: continue
  f=d[F:F+sz]
  ms=list(pat.finditer(f))
  if len(ms)<3: continue
  c=collections.Counter()
  for m in ms:
    s=m.start()
    for k in range(4,0x40,4):
      v=struct.unpack_from('<I',f,s-k)[0]
      if v<sz: c[s-v]+=1
  b,n=c.most_common(1)[0]
  print(hex(F),hex(sz),len(ms),hex(b),n,f[4:16].hex(' ',4),f[b-8:b+4].hex(' ',4))
