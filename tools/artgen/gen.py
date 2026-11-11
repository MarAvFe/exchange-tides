"""Generate original illustrated sprites for Exchange Tides.
usage: python3 -I gen.py OUT_DIR   (writes PNGs + map_ports.json)
"""
import json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import Canvas, ellipse_pts, rrect_pts, bezier, vgrad, shade, lerp

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
os.makedirs(OUT, exist_ok=True)
INK = (38, 30, 36)


def save(c, name):
    c.save(os.path.join(OUT, name + '.png'))
    print('wrote', name)


# ---------------------------------------------------------------------------------------- ships
SHIP_TYPES = {  # name: (hull length, masts, hull height)
    'sloop': (130, 1, 30), 'schooner': (150, 2, 32), 'brigantine': (165, 2, 36), 'barque': (180, 3, 38),
    'galleon': (195, 3, 46), 'frigate': (205, 3, 42), 'manowar': (215, 3, 50), 'raider': (140, 2, 30),
}


def ship(kind, hull=(120, 72, 44), trim=(212, 168, 82), sail=(244, 236, 214), flag=(40, 110, 170), tattered=False):
    L, masts, H = SHIP_TYPES[kind]
    W, Hc = 260, 220
    c = Canvas(W, Hc)
    cx, wl = W / 2, 168  # waterline
    x0, x1 = cx - L / 2, cx + L / 2
    # hull (bow to the right)
    top = wl - H
    pts = bezier((x0 - 6, top + 4), (x0 + 10, wl + 10), (x0 + 40, wl + 6), (x0 + 50, wl + 6), 14)
    pts += bezier((x1 - 40, wl + 6), (x1 - 8, wl + 4), (x1 + 18, top + 10), (x1 + 26, top - 4), 14)
    pts += [(x1 - 10, top + 2), (x0 + 22, top + 4), (x0 + 4, top - 10)]
    c.shape(pts, vgrad(top, wl + 8, shade(hull, 1.15), shade(hull, 0.6)), outline=INK, width=3)
    # trim stripe + gun ports
    c.line(x0 + 8, top + 12, x1 + 6, top + 9, 4, trim)
    n_ports = max(2, int(L / 30))
    for i in range(n_ports):
        px = x0 + 34 + i * (L - 50) / n_ports
        c.rect(px, top + 18, px + 9, top + 25, INK, r=1)
    # stern castle for big ships
    if H >= 38:
        c.shape([(x0 - 6, top - 14), (x0 + 36, top - 12), (x0 + 36, top + 4), (x0 - 2, top + 4)],
                shade(hull, 0.9), outline=INK, width=2.5)
        for i in range(3):
            c.rect(x0 + 2 + i * 11, top - 9, x0 + 9 + i * 11, top - 2, (250, 214, 120), r=1)
    # bowsprit
    c.line(x1 + 10, top + 2, x1 + 52, top - 22, 4, INK)
    # masts + sails
    mx = [cx + 10] if masts == 1 else ([cx - 28, cx + 34] if masts == 2 else [cx - 50, cx + 4, cx + 54])
    mast_h = 118 if masts > 1 else 112
    rnd = random.Random(kind + str(sail))
    for i, m in enumerate(mx):
        h = mast_h - (12 if i != len(mx) // 2 and masts == 3 else 0)
        c.line(m, top + 4, m, top - h, 5, (92, 62, 40))
        for tier in range(2 if masts > 1 else 1):
            sy0 = top - h + 10 + tier * 48
            sy1 = sy0 + (42 if masts > 1 else 82)
            w = 30 - tier * -6 if masts > 1 else 36
            sp = bezier((m - w, sy0), (m - w + 4, (sy0 + sy1) / 2), (m - w + 2, sy1), None, 8)
            sp += bezier((m + w + 2, sy1), (m + w + 14, (sy0 + sy1) / 2), (m + w, sy0), None, 8)
            if tattered:
                sp = [(x + rnd.uniform(-2, 2), y + rnd.uniform(-2, 2)) for x, y in sp]
            c.shape(sp, vgrad(sy0, sy1, shade(sail, 1.05), shade(sail, 0.78)), outline=INK, width=2.5)
            c.line(m - w - 2, sy0, m + w + 2, sy0, 3, (92, 62, 40))
        if masts == 1:  # jib
            c.shape([(m + 4, top - h + 6), (x1 + 46, top - 18), (m + 6, top - 6)],
                    vgrad(top - h, top, sail, shade(sail, 0.8)), outline=INK, width=2.5)
    # flag
    fm = mx[-1] if masts > 1 else mx[0]
    fh = top - mast_h - 2
    c.shape([(fm, fh), (fm + 26, fh + 5), (fm + 20, fh + 9), (fm + 26, fh + 14), (fm, fh + 16)], flag, outline=INK, width=2)
    # water wash
    c.fill(bezier((x0 - 10, wl + 4), (cx, wl + 18), (x1 + 20, wl), None, 20) + [(x1 + 20, wl + 12), (x0 - 10, wl + 12)],
           (255, 255, 255, 140))
    return c


def fort():
    c = Canvas(260, 220)
    c.shape([(30, 200), (40, 120), (220, 120), (232, 200)], vgrad(120, 200, (196, 180, 150), (120, 104, 86)), outline=INK, width=3)
    for i in range(8):
        c.rect(40 + i * 23, 108, 54 + i * 23, 122, (180, 164, 136), outline=INK, width=2)
    c.shape([(96, 120), (104, 50), (160, 50), (168, 120)], vgrad(50, 120, (210, 194, 160), (140, 122, 100)), outline=INK, width=3)
    for i in range(4):
        c.rect(100 + i * 17, 40, 112 + i * 17, 54, (190, 174, 144), outline=INK, width=2)
    for i in range(4):
        c.rect(52 + i * 44, 150, 72 + i * 44, 164, INK, r=3)
    c.line(132, 40, 132, 6, 4, (92, 62, 40))
    c.shape([(132, 6), (160, 12), (132, 20)], (190, 50, 50), outline=INK, width=2)
    return c


# ---------------------------------------------------------------------------------------- people
SKIN = [(244, 205, 170), (214, 160, 120), (164, 110, 76), (112, 72, 48), (236, 190, 150)]


def portrait(skin, hair, coat, hat=None, beard=None, bg=(70, 96, 120), earring=False, scarf=None, eyes=(40, 30, 30),
             long_hair=False, female=False, age=0):
    c = Canvas(160, 200)
    c.rect(0, 0, 160, 200, vgrad(0, 200, shade(bg, 1.25), shade(bg, 0.7)), r=14)
    # back hair
    if long_hair:
        c.shape(bezier((40, 70), (24, 150), (44, 176), None, 12) + bezier((116, 176), (136, 150), (120, 70), None, 12),
                shade(hair, 0.85), outline=INK, width=2.5)
    # shoulders / coat
    c.shape(bezier((8, 200), (14, 150), (52, 136), None, 10) + bezier((108, 136), (146, 150), (152, 200), None, 10),
            vgrad(136, 200, shade(coat, 1.1), shade(coat, 0.7)), outline=INK, width=3)
    c.shape([(64, 140), (80, 176), (96, 140)], (240, 232, 214), outline=INK, width=2)  # shirt V
    if scarf:
        c.shape([(58, 138), (80, 152), (102, 138), (96, 160), (80, 166), (64, 160)], scarf, outline=INK, width=2)
    # neck + face
    c.rect(68, 112, 92, 146, shade(skin, 0.86), outline=INK, width=2.5, r=6)
    c.ellipse(46, 92, 8, 11, shade(skin, 0.92), outline=INK, width=2.5)
    c.ellipse(114, 92, 8, 11, shade(skin, 0.92), outline=INK, width=2.5)
    face = bezier((48, 70), (44, 118), (66, 136), (80, 136), 14) + bezier((80, 136), (94, 136), (116, 118), (112, 70), 14)
    face += bezier((112, 70), (110, 40), (50, 40), (48, 70), 14)[1:-1]
    c.shape(face, vgrad(50, 136, shade(skin, 1.06), shade(skin, 0.9)), outline=INK, width=3)
    if earring:
        c.ellipse(44, 106, 4, 4, (236, 196, 80), outline=INK, width=1.5)
    # cheeks
    c.ellipse(60, 104, 7, 4, (230, 120, 110), alpha=0.25)
    c.ellipse(100, 104, 7, 4, (230, 120, 110), alpha=0.25)
    # eyes + brows
    for ex in (65, 95):
        c.ellipse(ex, 88, 7, 5 if not female else 5.5, (250, 248, 240), outline=INK, width=2)
        c.ellipse(ex + 1, 88.5, 3.4, 3.8, eyes)
        c.ellipse(ex + 2, 87, 1.2, 1.2, (255, 255, 255))
        if female:
            c.line(ex - 7, 84, ex - 10, 82, 1.8, INK)
    c.line(57, 76 - age, 72, 74, 3.5, shade(hair, 0.7))
    c.line(88, 74, 103, 76 - age, 3.5, shade(hair, 0.7))
    # nose + mouth
    c.polyline([(81, 88), (77, 104), (83, 106)], 2.2, shade(skin, 0.6))
    c.polyline(bezier((70, 117), (80, 123), (90, 117), None, 8), 2.4, (120, 50, 50))
    if age > 3:
        c.line(56, 98, 60, 100, 1.5, shade(skin, 0.7))
        c.line(104, 98, 100, 100, 1.5, shade(skin, 0.7))
    # beard
    if beard == 'full':
        c.shape(bezier((50, 96), (52, 140), (80, 150), None, 12) + bezier((80, 150), (108, 140), (110, 96), None, 12)
                + [(102, 110), (80, 126), (58, 110)], shade(hair, 0.9), outline=INK, width=2.5)
        c.polyline(bezier((70, 115), (80, 120), (90, 115), None, 8), 2.4, (120, 50, 50))
    elif beard == 'moustache':
        c.shape(bezier((64, 114), (80, 104), (96, 114), None, 10) + [(90, 112), (80, 110), (70, 112)], shade(hair, 0.9), outline=INK, width=2)
    elif beard == 'stubble':
        c.shape(bezier((52, 100), (58, 136), (80, 137), None, 10) + bezier((80, 137), (102, 136), (108, 100), None, 10)
                + [(80, 128)], shade(hair, 0.8), alpha=0.25)
    # hair top
    if hat != 'tricorn' and hat != 'captain':
        c.shape(bezier((46, 82), (40, 34), (120, 34), (114, 82), 18) + [(106, 62), (80, 54), (56, 64)],
                vgrad(36, 82, shade(hair, 1.2), shade(hair, 0.85)), outline=INK, width=2.5)
    # hats
    if hat == 'tricorn' or hat == 'captain':
        hc = (40, 36, 44) if hat == 'tricorn' else (30, 40, 70)
        c.shape(bezier((30, 70), (80, 50), (130, 70), None, 12) + bezier((130, 70), (120, 30), (40, 30), (30, 70), 14)[1:],
                vgrad(30, 70, shade(hc, 1.4), hc), outline=INK, width=3)
        c.shape(bezier((24, 72), (80, 54), (136, 72), None, 14) + bezier((136, 72), (80, 66), (24, 72), None, 14)[1:-1],
                shade(hc, 1.2), outline=INK, width=2.5)
        c.line(38, 66, 122, 66, 3, (212, 170, 80))
        if hat == 'captain':
            c.ellipse(80, 50, 8, 8, (230, 190, 90), outline=INK, width=2)
    elif hat == 'bandana':
        c.shape(bezier((44, 76), (40, 36), (120, 36), (116, 76), 16) + [(80, 66)], (186, 52, 52), outline=INK, width=2.5)
        c.shape([(112, 66), (132, 84), (124, 92), (108, 74)], (186, 52, 52), outline=INK, width=2)
        for i in range(5):
            c.ellipse(56 + i * 12, 54 + (i % 2) * 6, 2.5, 2.5, (250, 240, 220))
    elif hat == 'wig':
        for side in (-1, 1):
            for k in range(3):
                c.ellipse(80 + side * 34, 76 + k * 16, 12, 9, (236, 232, 224), outline=INK, width=2)
        c.shape(bezier((44, 78), (40, 30), (120, 30), (116, 78), 18) + [(80, 62)], (240, 236, 228), outline=INK, width=2.5)
    elif hat == 'kerchief':
        c.shape(bezier((44, 74), (46, 40), (114, 40), (116, 74), 16) + [(80, 64)], (90, 130, 110), outline=INK, width=2.5)
    return c


# ---------------------------------------------------------------------------------------- goods icons
def icon(kind):
    c = Canvas(64, 64)
    c.ellipse(32, 34, 28, 26, (250, 240, 214), outline=INK, width=2.5)
    if kind == 'fish':
        c.shape(ellipse_pts(30, 34, 16, 8), vgrad(26, 42, (130, 180, 210), (60, 110, 150)), outline=INK, width=2)
        c.shape([(44, 34), (56, 25), (54, 43)], (70, 120, 160), outline=INK, width=2)
        c.ellipse(21, 32, 2, 2, INK)
    elif kind == 'cotton':
        for x, y in ((24, 30), (36, 26), (40, 38), (28, 40), (32, 33)):
            c.ellipse(x, y, 9, 8, (252, 252, 250), outline=INK, width=1.8)
        c.line(32, 46, 32, 56, 3, (110, 80, 50))
    elif kind == 'timber':
        for i, y in enumerate((44, 34, 24)):
            c.rect(14 + i * 3, y - 5, 50 - i * 3, y + 5, (170, 112, 64), outline=INK, width=2, r=4)
            c.ellipse(50 - i * 3, y, 4, 5, (226, 190, 140), outline=INK, width=1.5)
    elif kind == 'cocoa':
        c.ellipse(32, 34, 12, 18, vgrad(16, 52, (190, 110, 60), (110, 56, 30)), outline=INK, width=2, rot=0.4)
        c.line(26, 22, 38, 46, 1.6, shade((110, 56, 30), 0.7))
    elif kind == 'sugar':
        c.shape(bezier((18, 54), (12, 30), (24, 18), None, 8) + bezier((40, 18), (52, 30), (46, 54), None, 8),
                (238, 228, 200), outline=INK, width=2)
        c.line(22, 22, 42, 22, 3, (150, 110, 70))
        c.ellipse(32, 40, 7, 5, (255, 255, 255), outline=INK, width=1.5)
    elif kind == 'arms':
        c.line(16, 48, 48, 18, 5, (110, 80, 50))
        c.line(16, 18, 48, 48, 5, (110, 80, 50))
        c.line(36, 30, 50, 16, 3, (90, 90, 100))
        c.line(28, 30, 14, 16, 3, (90, 90, 100))
    elif kind == 'textiles':
        c.rect(16, 20, 48, 48, (170, 70, 110), outline=INK, width=2, r=6)
        for i in range(4):
            c.line(16, 26 + i * 6, 48, 26 + i * 6, 1.5, (230, 180, 200))
    elif kind == 'tobacco':
        c.ellipse(32, 34, 10, 20, vgrad(14, 54, (140, 150, 70), (90, 90, 40)), outline=INK, width=2, rot=-0.5)
        c.line(22, 48, 42, 20, 1.5, (60, 60, 30))
    elif kind == 'wine':
        c.rect(26, 26, 38, 54, vgrad(26, 54, (120, 30, 60), (60, 10, 30)), outline=INK, width=2, r=4)
        c.rect(29, 12, 35, 28, (60, 10, 30), outline=INK, width=2, r=2)
        c.rect(27, 34, 37, 44, (240, 230, 200))
    elif kind == 'gem':
        c.shape([(20, 28), (28, 18), (36, 18), (44, 28), (32, 50)], vgrad(18, 50, (120, 230, 200), (20, 130, 120)), outline=INK, width=2)
        c.line(20, 28, 44, 28, 1.5, INK)
    elif kind == 'spice':
        c.ellipse(32, 40, 16, 10, (200, 120, 50), outline=INK, width=2)
        for x in (24, 32, 40):
            c.ellipse(x, 34, 3, 3, (150, 60, 30))
    return c


# ---------------------------------------------------------------------------------------- world map
PORTS = [
    ('saltmere', 'Port Saltmere', 250, 210), ('coralhaven', 'Coralhaven', 470, 140),
    ('isla_brasa', 'Isla Brasa', 700, 190), ('kestrel_bay', 'Kestrel Bay', 960, 150),
    ('lanterna', 'Lanterna', 1130, 300), ('driftmoor', 'Driftmoor', 160, 430),
    ('san_velo', 'San Velo', 420, 370), ('mangrove_key', 'Mangrove Key', 650, 430),
    ('ironreef', 'Ironreef', 880, 380), ('tidewell', 'Tidewell', 1060, 520),
    ('puerto_ambar', 'Puerto Ambar', 330, 600), ('blackwater_cay', 'Blackwater Cay', 760, 610),
]


def island(c, x, y, r, seed):
    rnd = random.Random(seed)
    n = 40
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    def blob(rr):
        pts = []
        for i in range(n):
            t = 2 * math.pi * i / n
            k = 1 + 0.18 * math.sin(3 * t + ph[0]) + 0.12 * math.sin(5 * t + ph[1]) + 0.07 * math.sin(9 * t + ph[2])
            pts.append((x + math.cos(t) * rr * k * 1.25, y + math.sin(t) * rr * k * 0.85))
        return pts
    c.fill(blob(r * 1.45), (120, 200, 210, 120))            # shallows
    c.shape(blob(r * 1.08), (236, 214, 160), outline=(150, 120, 80), width=2.5)  # sand
    c.fill(blob(r * 0.9), vgrad(y - r, y + r, (120, 170, 90), (70, 120, 60)))     # grass
    for k in range(rnd.randint(1, 3)):                        # hills
        hx, hy = x + rnd.uniform(-r * .5, r * .5), y + rnd.uniform(-r * .3, r * .2)
        hr = r * rnd.uniform(.25, .4)
        c.shape([(hx - hr, hy + hr * .5), (hx, hy - hr * .8), (hx + hr, hy + hr * .5)],
                vgrad(hy - hr, hy + hr, (150, 140, 110), (90, 100, 70)), outline=(60, 70, 50), width=1.5)
    for k in range(rnd.randint(3, 6)):                        # palms
        px, py = x + rnd.uniform(-r * .7, r * .7), y + rnd.uniform(-r * .4, r * .4)
        c.line(px, py, px + 2, py - 10, 2, (110, 80, 50))
        for a in range(5):
            ang = -math.pi / 2 + (a - 2) * 0.6
            c.line(px + 2, py - 10, px + 2 + math.cos(ang) * 8, py - 10 + math.sin(ang) * 6 + 3, 2.2, (50, 120, 60))


def world_map():
    W, H = 1280, 720
    c = Canvas(W, H)
    c.rect(0, 0, W, H, vgrad(0, H, (64, 150, 180), (28, 86, 130)))
    rnd = random.Random(7)
    for i in range(260):  # wave marks
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        c.polyline(bezier((x, y), (x + 6, y - 4), (x + 12, y), None, 6), 1.4, (210, 236, 240, 110))
    for i, (pid, name, x, y) in enumerate(PORTS):
        island(c, x + rnd.uniform(-14, 14), y + 18, rnd.uniform(34, 52), pid)
    for k in range(6):  # small uninhabited islets
        island(c, rnd.uniform(80, 1200), rnd.uniform(80, 680), rnd.uniform(10, 18), 'islet%d' % k)
    # compass rose
    cx, cy = 1180, 640
    c.ellipse(cx, cy, 44, 44, (244, 232, 200, 220), outline=INK, width=2)
    for a in range(8):
        t = a * math.pi / 4
        L = 40 if a % 2 == 0 else 24
        c.fill([(cx + math.cos(t) * L, cy + math.sin(t) * L), (cx + math.cos(t + .25) * 8, cy + math.sin(t + .25) * 8),
                (cx, cy), (cx + math.cos(t - .25) * 8, cy + math.sin(t - .25) * 8)], (170, 60, 50) if a == 6 else INK)
    # parchment vignette border
    for i in range(14):
        col = (70, 50, 30, max(0, 90 - i * 6))
        c.rect(i, i, W - i, i + 1, col)
        c.rect(i, H - i - 1, W - i, H - i, col)
        c.rect(i, i, i + 1, H - i, col)
        c.rect(W - i - 1, i, W - i, H - i, col)
    return c


def title_bg():
    W, H = 1280, 720
    c = Canvas(W, H)
    c.rect(0, 0, W, 430, vgrad(0, 430, (40, 50, 110), (246, 160, 110)))
    c.ellipse(860, 410, 110, 110, (255, 214, 140))
    c.ellipse(860, 410, 150, 150, (255, 214, 140), alpha=0.25)
    for i in range(5):
        y = 120 + i * 50
        c.ellipse(200 + i * 210, y, 120, 18, (250, 200, 190), alpha=0.35)
    c.rect(0, 420, W, H, vgrad(420, H, (60, 90, 130), (16, 30, 60)))
    rnd = random.Random(3)
    for i in range(180):
        x, y = rnd.uniform(0, W), rnd.uniform(430, H)
        w = rnd.uniform(10, 40) * (y - 400) / 300
        c.line(x, y, x + w, y, 1.5, (255, 200, 150, 90 if abs(x - 860) < 200 else 40))
    s = ship('galleon', hull=(40, 30, 40), trim=(120, 90, 60), sail=(60, 50, 60), flag=(150, 40, 40))
    # paste silhouette scaled 1x
    for yy in range(s.h):
        for xx in range(s.w):
            p = s.px[yy][xx]
            if p[3] > 0:
                X, Y = 330 + xx, 250 + yy
                if 0 <= X < W and 0 <= Y < H:
                    q = c.px[Y][X]
                    a = p[3] / 255
                    for k in range(3):
                        q[k] = q[k] * (1 - a) + p[k] * a
    return c


def main():
    hulls = {'merchant': ((150, 92, 52), (212, 168, 82), (244, 236, 214), (40, 110, 170)),
             'navy': ((70, 80, 110), (220, 200, 120), (250, 248, 240), (40, 60, 160)),
             'pirate': ((54, 40, 44), (150, 40, 40), (90, 80, 82), (20, 20, 20)),
             'raider': ((90, 50, 40), (200, 120, 60), (200, 170, 140), (170, 40, 40))}
    for kind in ('sloop', 'schooner', 'brigantine', 'barque', 'galleon', 'frigate', 'manowar'):
        save(ship(kind, *hulls['merchant']), 'ship_' + kind)
    for kind in ('sloop', 'schooner', 'brigantine', 'barque', 'galleon', 'frigate', 'manowar'):
        save(ship(kind, *hulls['pirate'], tattered=True), 'ship_' + kind + '_pirate')
    save(ship('frigate', *hulls['navy']), 'ship_frigate_navy')
    save(ship('raider', *hulls['raider']), 'ship_raider')
    save(fort(), 'fort')

    people = {
        'vega': dict(skin=SKIN[1], hair=(60, 34, 30), coat=(40, 110, 120), hat='tricorn', earring=True, long_hair=True, female=True, bg=(120, 90, 70)),
        'wren': dict(skin=SKIN[0], hair=(200, 150, 80), coat=(40, 60, 120), hat='captain', beard='stubble', bg=(70, 96, 120)),
        'calder': dict(skin=SKIN[4], hair=(30, 28, 30), coat=(90, 50, 40), hat='bandana', earring=True, long_hair=True, female=True, scarf=(60, 60, 60), bg=(80, 70, 90)),
        'bale': dict(skin=SKIN[3], hair=(30, 24, 22), coat=(140, 110, 50), hat='kerchief', beard='full', bg=(60, 110, 100)),
        'grimmer': dict(skin=SKIN[0], hair=(70, 70, 76), coat=(30, 26, 34), hat='tricorn', beard='moustache', eyes=(120, 30, 30), bg=(90, 40, 40), age=4),
        'governor': dict(skin=SKIN[0], hair=(220, 220, 220), coat=(120, 30, 50), hat='wig', bg=(130, 110, 80), age=4),
        'banker': dict(skin=SKIN[2], hair=(40, 30, 30), coat=(50, 60, 60), beard='moustache', bg=(90, 110, 90)),
        'barkeep': dict(skin=SKIN[4], hair=(160, 70, 40), coat=(120, 90, 60), long_hair=True, female=True, scarf=(200, 160, 60), bg=(140, 90, 60)),
        'shipwright': dict(skin=SKIN[2], hair=(90, 60, 40), coat=(100, 80, 60), hat='kerchief', beard='full', bg=(70, 100, 130)),
        'lender': dict(skin=SKIN[0], hair=(50, 50, 50), coat=(60, 40, 70), hat='tricorn', beard='stubble', bg=(70, 50, 80), age=5),
        'merchant': dict(skin=SKIN[1], hair=(40, 30, 30), coat=(160, 120, 60), beard='moustache', bg=(110, 120, 80)),
        'sailor': dict(skin=SKIN[3], hair=(20, 20, 20), coat=(70, 90, 120), hat='bandana', earring=True, bg=(60, 90, 120)),
        'smuggler': dict(skin=SKIN[1], hair=(20, 20, 20), coat=(40, 40, 40), hat='bandana', beard='stubble', scarf=(120, 30, 30), bg=(50, 50, 60)),
    }
    for k, v in people.items():
        save(portrait(**v), 'portrait_' + k)
    for g in ('fish', 'cotton', 'timber', 'cocoa', 'sugar', 'arms', 'textiles', 'tobacco', 'wine', 'gem', 'spice'):
        save(icon(g), 'good_' + g)
    save(world_map(), 'worldmap')
    save(title_bg(), 'title')
    json.dump([{'id': p, 'name': n, 'x': x, 'y': y} for p, n, x, y in PORTS],
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_ports.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
