"""Read typed constants from tw2_vista.exe by virtual address. usage: peconst.py EXE VA:type ... (type: d=double f=float i=int)"""
import struct, sys
b = open(sys.argv[1], 'rb').read()
pe = struct.unpack_from('<I', b, 0x3c)[0]; nsec = struct.unpack_from('<H', b, pe + 6)[0]
opt = struct.unpack_from('<H', b, pe + 20)[0]; base = struct.unpack_from('<I', b, pe + 24 + 28)[0]
secs = [struct.unpack_from('<8sIIII', b, pe + 24 + opt + 40 * i) for i in range(nsec)]
def off(va):
    rva = va - base
    for name, vsz, vaddr, rsz, raddr in secs:
        if vaddr <= rva < vaddr + max(vsz, rsz):
            return raddr + rva - vaddr if rva - vaddr < rsz else None
for a in sys.argv[2:]:
    va, t = a.split(':'); va = int(va, 16); o = off(va)
    fmt = {'d': '<d', 'f': '<f', 'i': '<i'}[t]
    print(f'{va:#x} {t}', 'uninitialized (set at runtime)' if o is None else struct.unpack_from(fmt, b, o)[0])
