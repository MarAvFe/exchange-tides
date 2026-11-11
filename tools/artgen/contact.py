#!/usr/bin/env python3
"""Make a labelled-free contact sheet of PNGs (standard library only).

Usage: python3 -I contact.py OUT.png [--cell W H] [--cols N] IMG...
Each image is scaled (nearest neighbour) to fit its cell. Transparent pixels show a checker background,
so alpha edges are easy to judge. Images are laid out left to right, top to bottom.
"""
import struct, sys, zlib


def read_png(path):
    data = open(path, 'rb').read()
    i, idat = 8, b''
    while i < len(data):
        n, = struct.unpack('>I', data[i:i + 4]); t = data[i + 4:i + 8]; c = data[i + 8:i + 8 + n]
        if t == b'IHDR':
            w, h, depth, ctype = struct.unpack('>IIBB', c[:10])
        elif t == b'IDAT':
            idat += c
        i += 12 + n
    if depth != 8 or ctype not in (2, 6):
        raise ValueError(f'{path}: unsupported PNG type {depth}/{ctype}')
    bpp = 4 if ctype == 6 else 3
    raw = zlib.decompress(idat)
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]; line = bytearray(raw[p + 1:p + 1 + stride]); p += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, bpp, out


def write_png(path, w, h, rgb):
    raw = b''.join(b'\x00' + bytes(rgb[y * w * 3:(y + 1) * w * 3]) for y in range(h))
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) +
                          chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))


def main():
    args = sys.argv[1:]
    out = args.pop(0)
    cw, ch, cols = 200, 200, 6
    while args and args[0].startswith('--'):
        if args[0] == '--cell': cw, ch = int(args[1]), int(args[2]); args = args[3:]
        elif args[0] == '--cols': cols = int(args[1]); args = args[2:]
    rows = (len(args) + cols - 1) // cols
    W, H = cols * cw, rows * ch
    sheet = bytearray(W * H * 3)
    for y in range(H):
        for x in range(W):
            v = 70 if ((x // 8) + (y // 8)) % 2 else 95
            o = (y * W + x) * 3; sheet[o:o + 3] = bytes((v, v, v))
    for k, path in enumerate(args):
        w, h, bpp, px = read_png(path)
        s = min((cw - 6) / w, (ch - 6) / h)
        dw, dh = int(w * s), int(h * s)
        ox = (k % cols) * cw + (cw - dw) // 2
        oy = (k // cols) * ch + (ch - dh) // 2
        for y in range(dh):
            sy = int(y / s)
            for x in range(dw):
                si = (sy * w + int(x / s)) * bpp
                a = px[si + 3] if bpp == 4 else 255
                o = ((oy + y) * W + ox + x) * 3
                for c in range(3):
                    sheet[o + c] = (px[si + c] * a + sheet[o + c] * (255 - a)) // 255
    write_png(out, W, H, sheet)


if __name__ == '__main__':
    main()
