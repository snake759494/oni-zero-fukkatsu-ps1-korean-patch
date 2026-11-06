import sys,os,ctypes
sys.path.insert(0,os.path.dirname(__file__))
import emu
class E(emu.Emu):
    def __init__(s,pid):
        class P: pass
        s.p=P(); s.p.pid=pid; s.hwnds=s._find()
E(int(sys.argv[1])).grab(sys.argv[2])
