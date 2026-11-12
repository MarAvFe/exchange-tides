"""Battle-damage variants of every ship sprite: <ship>_d1 (<=80% hull), _d2 (<=50%), _d3 (<=25%).

Starts from the painted damage pass (comfy_gen.py, art_spec "<ship>_d<k>") when present, else from the
intact sprite, then adds damage that the painting pass cannot (it must keep the ship's outline):
ragged holes torn through the sails/upper works, scorch blotches and soot on the hull.
Damage grows with k and is deterministic per ship. Standard library only.
usage: python3 -I tools/artgen/damage.py
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import read_png
from raster import Canvas

HERE = os.path.dirname(os.path.abspath(__file__))
SPRITES = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'game', 'ExchangeTides', 'datafiles', 'sprites')
OUT = os.path.join(HERE, 'out')
LEVELS = {1: dict(holes=4, rmax=6, scorch=4, soot=0.10), 2: dict(holes=11, rmax=10, scorch=9, soot=0.22),
          3: dict(holes=22, rmax=15, scorch=16, soot=0.38)}


def load_rgba(path):
    w, h, bpp, px = read_png(path)
    out = []
    for i in range(w * h):
        r, g, b = px[i * bpp], px[i * bpp + 1], px[i * bpp + 2]
        a = px[i * bpp + 3] if bpp == 4 else 255
        out.append([r, g, b, a])
    return w, h, out


def damage(name, k):
    base = os.path.join(SPRITES, name + '.png')
    painted = os.path.join(OUT, '%s_d%d_v0.png' % (name, k))
    w, h, px = load_rgba(painted if os.path.exists(painted) else base)
    _, _, orig = load_rgba(base)
    for i in range(w * h):          # keep the intact silhouette (the painted pass may bleed)
        px[i][3] = min(px[i][3], orig[i][3])
    rnd = random.Random(name + str(k))
    L = LEVELS[k]
    rows = [y for y in range(h) if any(px[y * w + x][3] > 128 for x in range(w))]
    top, bot = rows[0], rows[-1]
    hull_y = top + (bot - top) * 0.68     # above: rigging and sails; below: hull
    opaque = [(x, y) for y in range(top, int(hull_y)) for x in range(w) if px[y * w + x][3] > 200]
    # Holes: ragged blobs cut out of the sails, each with a charred rim.
    for _ in range(L['holes']):
        if not opaque:
            break
        cx, cy = rnd.choice(opaque)
        r = rnd.uniform(2.5, L['rmax'])
        for y in range(int(cy - r - 3), int(cy + r + 4)):
            for x in range(int(cx - r - 3), int(cx + r + 4)):
                if not (0 <= x < w and 0 <= y < h):
                    continue
                d = math.hypot(x - cx, (y - cy) * 1.3) / r + rnd.uniform(-0.25, 0.25)
                p = px[y * w + x]
                if d < 0.8:
                    p[3] = 0
                elif d < 1.35 and p[3] > 0:
                    t = 0.55 * (1.35 - d) / 0.55 + 0.25
                    p[0], p[1], p[2] = [int(c * (1 - t) + 30 * t) for c in p[:3]]
    # Scorch blotches over the whole ship, heavier on the hull.
    hull = [(x, y) for y in range(int(hull_y), bot + 1) for x in range(w) if px[y * w + x][3] > 200]
    for _ in range(L['scorch']):
        pool = hull if (hull and rnd.random() < 0.65) else opaque
        if not pool:
            continue
        cx, cy = rnd.choice(pool)
        r = rnd.uniform(5, 9 + 4 * k)
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                if 0 <= x < w and 0 <= y < h and px[y * w + x][3] > 0:
                    d = math.hypot(x - cx, y - cy) / r
                    if d < 1:
                        t = (1 - d) * (0.45 + 0.1 * k)
                        p = px[y * w + x]
                        p[0], p[1], p[2] = int(p[0] * (1 - t) + 26 * t), int(p[1] * (1 - t) + 20 * t), int(p[2] * (1 - t) + 18 * t)
    # Overall soot and desaturation.
    s = L['soot']
    for p in px:
        if p[3] == 0:
            continue
        g = (p[0] + p[1] + p[2]) / 3
        p[0], p[1], p[2] = [int((c * (1 - s) + g * s) * (1 - s * 0.5)) for c in p[:3]]
    c = Canvas(w, h)
    c.px = [[list(px[y * w + x]) for x in range(w)] for y in range(h)]
    c.save(os.path.join(SPRITES, '%s_d%d.png' % (name, k)))


if __name__ == '__main__':
    ships = sorted(f[:-4] for f in os.listdir(SPRITES) if f.startswith('ship_') and f.endswith('.png') and '_d' not in f[-7:])
    for s in ships:
        for k in (1, 2, 3):
            damage(s, k)
        print('damaged', s)
