import glob,re,sys,os
CT=re.compile(r'\^[A-Za-z](?:[0-9A-Fa-f]{6}|[0-9]{2})?')
for fn in sorted(glob.glob('text/src/*.tsv')):
    k=os.path.basename(fn); ko='text/ko/'+k
    if not os.path.exists(ko): continue
    S=[l.rstrip('\n').split('\t') for l in open(fn,encoding='utf-8')]
    K={p[0]:p[-1] for p in (l.rstrip('\n').split('\t') for l in open(ko,encoding='utf-8')) if len(p)>=2}
    miss=bad=lng=kana=0
    for p in S:
        i,ja=p[0],p[-1]
        if i not in K: miss+=1; continue
        t=K[i]
        if CT.findall(ja)!=CT.findall(t): bad+=1; print(' CTRL',i,ja,'|',t) if bad<4 else None
        core=CT.sub('',t).replace(' ','')
        lim=int(p[1]) if len(p)==3 else max(14,len(CT.sub('',ja)))
        if len(core)>lim: lng+=1
        if re.search('[ぁ-んァ-ヶ]',core) and t!=ja: kana+=1
    print(k,'줄',len(S),'누락',miss,'코드불일치',bad,'초과',lng,'가나',kana)
