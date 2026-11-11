"""Summarize save-writer field sequences from re/decomp.c (primitive call order)."""
import re, sys
src = open('/home/mavila/exchange-tides/re/decomp.c').read()
funcs = {m.group(1): m.group(2) for m in re.finditer(r'// ==== (\S+) @ \S+\n(.*?)(?=\n// ==== |\Z)', src, re.S)}
PRIM = {'FUN_0040f3b0': 'u8', 'FUN_0040f3f0': 'i32', 'FUN_0040f430': 'i64/f64', 'FUN_0040f470': 'str'}
def trace(name, depth=0, seen=()):
    body = funcs.get(name, '')
    pk = re.search(r'FUN_00451d80\([^,]*,"([^"]+)"\);\s*\n[^\n]*FUN_0040f6f0', body)
    out = []
    for m in re.finditer(r'\b(FUN_[0-9a-f]{8})\(|\b(do|while)\b', body):
        f = m.group(1)
        if m.group(2): out.append('loop' if m.group(2) == 'do' else ''); continue
        if f in PRIM: out.append(PRIM[f])
        elif f not in seen and depth < 3 and f in funcs and 'FUN_0040f6f0' in funcs[f]:
            out.append(trace(f, depth + 1, seen + (name,)))
    s = ' '.join(x for x in out if x)
    s = re.sub(r'loop\s*(loop\s*)+', 'loop ', s)
    return f'{pk.group(1) if pk else name}{{ {s} }}'
for n in sys.argv[1:]: print(trace(n)); print()
