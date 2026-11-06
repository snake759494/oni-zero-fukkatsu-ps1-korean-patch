import struct,numpy as np,collections,pickle
d=open('orig/DATA00.DAT','rb').read()
N=len(d)//2048
heads=np.frombuffer(d,dtype='<u4')[::512]  # size header per sector
hits=collections.defaultdict(list)
for src,buf in [('D',d),('E',open('orig/SLPS_031.06','rb').read())]:
  for al in (0,):
    v=np.frombuffer(buf[:len(buf)//4*4],dtype='<u4')
    idx=np.nonzero(v[:-1]==0)[0]+1
    x=v[idx]; ns=x>>24; so=x&0xffffff
    m=(ns>0)&(so<N)&(so+ns<=N)
    idx,ns,so=idx[m],ns[m],so[m]
    sz=heads[so]
    m=((sz.astype(np.int64)+2047)//2048==ns)&(sz>8)
    for i,s in zip(idx[m],so[m]): hits[int(s)].append((src,int(i)*4))
print(len(hits))
for so in sorted(hits)[:30]: print(hex(so),hex(int(heads[so])),len(hits[so]),hits[so][:3])
pickle.dump(dict(hits),open('refs.pkl','wb'))
