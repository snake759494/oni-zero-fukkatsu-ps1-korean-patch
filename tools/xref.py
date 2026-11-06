import sys,struct,capstone
b=open('orig/SLPS_031.06','rb').read();base=struct.unpack_from('<I',b,0x18)[0]
md=capstone.Cs(capstone.CS_ARCH_MIPS,capstone.CS_MODE_MIPS32+capstone.CS_MODE_LITTLE_ENDIAN);md.skipdata=True
ins=list(md.disasm(b[0x800:],base))
tg=[int(x,16) for x in sys.argv[1:]]
for i,x in enumerate(ins):
    if x.mnemonic=='lui':
        hi=int(x.op_str.split(',')[1],0);r=x.op_str.split(',')[0]
        for y in ins[i+1:i+8]:
            if r in y.op_str and y.mnemonic in('addiu','lw','sw','lh','lhu','sh','lbu','sb','lb','ori'):
                imm=y.op_str.split(',')[-1].strip().split('(')[0]
                try: v=((hi<<16)+(int(imm,0) if y.mnemonic=='ori' else struct.unpack('<h',struct.pack('<H',int(imm,0)&0xffff))[0]))&0xffffffff
                except: continue
                if any(t<=v<t+0x40 for t in tg): print(hex(v),hex(y.address),y.mnemonic,y.op_str)
                break
