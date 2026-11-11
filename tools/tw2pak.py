"""Tradewinds 2 .data archive tool.

Format (little-endian): u32 magic 0x0000DCAC, u32 count, then per entry:
NUL-terminated path, u32 offset, u32 size. XML (*.txt) entries are obfuscated
with an additive repeating key: plain[i] = (cipher[i] - KEY[i % 20]) & 0xFF.
Key from TWApp ctor (0x4438c0) / assets/xml/assetfile.txt. Reader: 0x45d110.

usage: tw2pak.py list ARCHIVE
       tw2pak.py extract ARCHIVE OUTDIR
"""
import os, struct, sys
KEY = b"klxd8794lkds87934poi"

def read_index(path):
    b = open(path, 'rb').read()
    if b[:4] != b'\xac\xdc\x00\x00': raise ValueError('bad magic')
    n, = struct.unpack_from('<I', b, 4); p = 8; out = []
    for _ in range(n):
        e = b.index(b'\0', p); name = b[p:e].decode('latin1'); p = e + 1
        off, size = struct.unpack_from('<II', b, p); p += 8
        out.append((name, off, size))
    return b, out

def decode(data, key=KEY):
    return bytes((c - key[i % len(key)]) & 0xFF for i, c in enumerate(data))

def extract(path, outdir):
    b, idx = read_index(path); root = os.path.realpath(outdir)
    for name, off, size in idx:
        dst = os.path.realpath(os.path.join(root, name))
        if not dst.startswith(root + os.sep): raise ValueError(f'unsafe path {name!r}')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        data = b[off:off + size]
        if name.lower().endswith('.txt'): data = decode(data)
        open(dst, 'wb').write(data)
    return len(idx)

if __name__ == '__main__':
    cmd, arc = sys.argv[1], sys.argv[2]
    if cmd == 'list':
        for name, off, size in read_index(arc)[1]: print(f'{off:#010x} {size:9d} {name}')
    elif cmd == 'extract':
        print(extract(arc, sys.argv[3]), 'entries ->', sys.argv[3])
    else: sys.exit(__doc__)
