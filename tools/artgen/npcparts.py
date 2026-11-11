"""Layered NPC portrait parts ("trait" layers), composed in game: every port's banker, barkeep, etc. is a
unique combination of face, skin tone, hair, beard, clothes, hat and accessory, chosen once per save.

All parts share one 320x400 frame (2x the 160x200 portrait), so any combination lines up. Parts that are
tinted at runtime (skin, hair, clothes) are drawn in neutral light tones; GameMaker multiplies them by the
chosen colour. Writes vector/npc_<layer>_<variant>.png. comfy_gen.py repaints the large parts (art_spec.json
entries with "ref":"npc_..."); small features stay crisp vector.

To add a variant: draw it in a function below, add it to PARTS, rerun this script, add the art_spec entry if
it should be painted, and list it in datafiles/data/npc_parts.json.
usage: python3 -I tools/artgen/npcparts.py [--install]   (--install copies the vector parts into the game)
"""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import Canvas, bezier, vgrad, shade

HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.join(HERE, 'vector')
SPRITES = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'game', 'ExchangeTides', 'datafiles', 'sprites')
INK = (38, 30, 36)
K = 2                      # parts are drawn on the 160x200 portrait grid, scaled x2
NEUTRAL = (226, 222, 216)  # tinted parts (hair, clothes) are drawn in this light grey
SKIN = (246, 222, 200)     # faces are drawn in a light skin tone and multiplied by the chosen tone


class S:
    """Canvas proxy that scales the 160x200 design grid to the 320x400 part frame."""
    def __init__(self):
        self.c = Canvas(160 * K, 200 * K)

    @staticmethod
    def _col(col):
        return (lambda x, y: col(x / K, y / K)) if callable(col) else col

    def shape(self, pts, col, outline=None, width=2.0, alpha=1.0):
        self.c.shape([(x * K, y * K) for x, y in pts], self._col(col), outline, width * K, alpha)

    def fill(self, pts, col, alpha=1.0):
        self.c.fill([(x * K, y * K) for x, y in pts], self._col(col), alpha)

    def ellipse(self, cx, cy, rx, ry, col, outline=None, width=2.0, alpha=1.0):
        self.c.ellipse(cx * K, cy * K, rx * K, ry * K, self._col(col), outline, width * K, alpha)

    def rect(self, x0, y0, x1, y1, col, outline=None, width=2.0, r=0):
        self.c.rect(x0 * K, y0 * K, x1 * K, y1 * K, self._col(col), outline, width * K, r=r * K)

    def line(self, x0, y0, x1, y1, w, col, alpha=1.0):
        self.c.line(x0 * K, y0 * K, x1 * K, y1 * K, w * K, col, alpha)

    def polyline(self, pts, w, col, alpha=1.0):
        self.c.polyline([(x * K, y * K) for x, y in pts], w * K, col, alpha)


N = NEUTRAL


def g(c0, k0=1.15, k1=0.8, y0=36, y1=82):
    return vgrad(y0, y1, shade(c0, k0), shade(c0, k1))


# ---- layers (back to front) ---------------------------------------------------------------
def plate(_v=None):
    c = S()
    c.rect(0, 0, 160, 200, vgrad(0, 200, (236, 234, 230), (176, 174, 170)), r=14)
    return c


def hairback(kind):
    c = S()
    if kind == 'long':
        c.shape(bezier((40, 70), (24, 150), (44, 176), None, 12) + bezier((116, 176), (136, 150), (120, 70), None, 12), shade(N, 0.85), outline=INK, width=2.5)
    elif kind == 'tail':
        c.shape(bezier((96, 60), (130, 90), (120, 150), None, 10) + [(108, 150), (112, 96), (90, 70)], shade(N, 0.85), outline=INK, width=2.5)
    return c


def coat(kind):
    c = S()
    body = bezier((8, 200), (14, 150), (52, 136), None, 10) + bezier((108, 136), (146, 150), (152, 200), None, 10)
    if kind == 'robe':
        body = bezier((14, 200), (24, 150), (56, 136), None, 10) + bezier((104, 136), (136, 150), (146, 200), None, 10)
    c.shape(body, vgrad(136, 200, shade(N, 1.05), shade(N, 0.72)), outline=INK, width=3)
    if kind in ('coat', 'naval'):
        for side in (-1, 1):  # lapels
            c.shape([(80 + side * 16, 140), (80 + side * 34, 150), (80 + side * 20, 196), (80 + side * 8, 172)], shade(N, 0.88), outline=INK, width=2)
    if kind == 'naval':
        for side in (-1, 1):
            c.shape([(80 + side * 44, 146), (80 + side * 64, 150), (80 + side * 60, 158), (80 + side * 42, 155)], (226, 186, 90), outline=INK, width=1.5)
    if kind == 'vest':
        for y in (160, 176, 192):
            c.ellipse(80, y, 2.5, 2.5, (200, 170, 90), outline=INK, width=1)
    if kind == 'apron':
        c.shape([(58, 150), (102, 150), (106, 200), (54, 200)], (236, 228, 210), outline=INK, width=2)
    return c


def collar(kind):
    c = S()
    if kind == 'v':
        c.shape([(64, 140), (80, 176), (96, 140)], (240, 232, 214), outline=INK, width=2)
    elif kind == 'cravat':
        c.shape([(64, 140), (80, 170), (96, 140)], (244, 238, 224), outline=INK, width=2)
        c.shape([(72, 146), (88, 146), (84, 168), (76, 168)], (250, 246, 236), outline=INK, width=1.5)
    elif kind == 'ruff':
        for i in range(7):
            c.ellipse(58 + i * 7.3, 142 + (i % 2) * 2, 6, 5, (248, 244, 236), outline=INK, width=1.2)
    elif kind == 'scarf':
        c.shape([(58, 138), (80, 152), (102, 138), (96, 160), (80, 166), (64, 160)], (176, 64, 60), outline=INK, width=2)
    return c


def face(kind):
    c = S()
    sk = SKIN
    c.rect(68, 112, 92, 146, shade(sk, 0.88), outline=INK, width=2.5, r=6)
    for ex in (46, 114):
        c.ellipse(ex, 92, 8, 11, shade(sk, 0.93), outline=INK, width=2.5)
    w = {'oval': 0, 'round': 4, 'long': -3, 'square': 3}[kind]
    chin = {'oval': 136, 'round': 132, 'long': 142, 'square': 136}[kind]
    if kind == 'square':
        f = bezier((48 - w, 70), (46 - w, 124), (60, chin), (80, chin), 14) + bezier((80, chin), (100, chin), (114 + w, 124), (112 + w, 70), 14)
    else:
        f = bezier((48 - w, 70), (44 - w, 118), (66, chin), (80, chin), 14) + bezier((80, chin), (94, chin), (116 + w, 118), (112 + w, 70), 14)
    f += bezier((112 + w, 70), (110 + w, 40), (50 - w, 40), (48 - w, 70), 14)[1:-1]
    c.shape(f, vgrad(50, chin, shade(sk, 1.04), shade(sk, 0.9)), outline=INK, width=3)
    c.ellipse(60, 104, 7, 4, (230, 120, 110), alpha=0.22)
    c.ellipse(100, 104, 7, 4, (230, 120, 110), alpha=0.22)
    return c


HEAD_SKINS = {'fair': (246, 222, 200), 'olive': (226, 186, 148), 'tan': (196, 146, 104), 'brown': (150, 100, 66), 'dark': (104, 68, 46)}
HEADS = {'a': ('oval', 'calm'), 'b': ('round', 'smile'), 'c': ('long', 'stern'), 'd': ('square', 'old'), 'e': ('oval', 'smile'), 'f': ('square', 'stern')}


def head(v):
    """Face + features in one painted layer, one per skin tone (variant 'a_fair' etc.)."""
    hv, sk = v.split('_')
    shape, expr = HEADS[hv]
    global SKIN
    keep = SKIN
    SKIN = HEAD_SKINS[sk]
    c = face(shape)
    f = features(expr)
    SKIN = keep
    # Merge the feature layer on top.
    for y in range(len(c.c.px)):
        row, frow = c.c.px[y], f.c.px[y]
        for x in range(len(row)):
            a = frow[x][3] / 255.0
            if a <= 0:
                continue
            p = row[x]
            for k in range(3):
                p[k] = p[k] * (1 - a) + frow[x][k] * a
            p[3] = max(p[3], frow[x][3])
    return c


def features(kind):
    """Eyes, brows, nose and mouth; drawn untinted (dark lines work on every skin tone)."""
    c = S()
    eye_col = {'calm': (60, 44, 30), 'smile': (50, 60, 80), 'stern': (40, 30, 30), 'old': (70, 80, 70)}[kind]
    for ex in (65, 95):
        c.ellipse(ex, 88, 7, 5, (250, 248, 240), outline=INK, width=2)
        c.ellipse(ex + 1, 88.5, 3.4, 3.8, eye_col)
        c.ellipse(ex + 2, 87, 1.2, 1.2, (255, 255, 255))
    by = {'calm': 0, 'smile': -1, 'stern': 3, 'old': 1}[kind]
    c.line(57, 76 + (by if kind != 'stern' else 0), 72, 74 + by, 3.5, (60, 46, 40))
    c.line(88, 74 + by, 103, 76 + (by if kind != 'stern' else 0), 3.5, (60, 46, 40))
    c.polyline([(81, 88), (77, 104), (83, 106)], 2.2, (60, 40, 30), alpha=0.55)
    if kind == 'smile':
        c.polyline(bezier((68, 115), (80, 126), (92, 115), None, 8), 2.6, (120, 50, 50))
    elif kind == 'stern':
        c.line(70, 119, 90, 118, 2.6, (110, 50, 50))
    else:
        c.polyline(bezier((70, 117), (80, 122), (90, 117), None, 8), 2.4, (120, 50, 50))
    if kind == 'old':
        for x0, x1 in ((56, 60), (104, 100)):
            c.line(x0, 98, x1, 100, 1.5, (60, 40, 30), alpha=0.4)
        c.line(64, 64, 96, 64, 1.2, (60, 40, 30), alpha=0.3)
    return c


def beard(kind):
    c = S()
    if kind == 'full':
        c.shape(bezier((50, 96), (52, 140), (80, 150), None, 12) + bezier((80, 150), (108, 140), (110, 96), None, 12) + [(102, 110), (80, 126), (58, 110)], shade(N, 0.9), outline=INK, width=2.5)
    elif kind == 'moustache':
        c.shape(bezier((64, 114), (80, 104), (96, 114), None, 10) + [(90, 112), (80, 110), (70, 112)], shade(N, 0.9), outline=INK, width=2)
    elif kind == 'goatee':
        c.shape(bezier((66, 112), (80, 106), (94, 112), None, 8) + [(88, 114), (86, 136), (80, 142), (74, 136), (72, 114)], shade(N, 0.9), outline=INK, width=2)
    elif kind == 'stubble':
        c.shape(bezier((52, 100), (58, 136), (80, 137), None, 10) + bezier((80, 137), (102, 136), (108, 100), None, 10) + [(80, 128)], shade(N, 0.7), alpha=0.35)
    return c


def hair(kind):
    c = S()
    if kind == 'short':
        c.shape(bezier((46, 82), (40, 34), (120, 34), (114, 82), 18) + [(106, 62), (80, 54), (56, 64)], g(N), outline=INK, width=2.5)
    elif kind == 'swept':
        c.shape(bezier((46, 84), (36, 30), (124, 28), (116, 80), 18) + [(110, 58), (70, 64), (52, 60)], g(N), outline=INK, width=2.5)
    elif kind == 'bun':
        c.ellipse(80, 34, 16, 13, g(N, y0=20, y1=48), outline=INK, width=2.5)
        c.shape(bezier((46, 80), (42, 36), (118, 36), (114, 80), 18) + [(100, 58), (80, 52), (60, 58)], g(N), outline=INK, width=2.5)
    elif kind == 'curly':
        for i in range(9):
            x = 48 + i * 8
            c.ellipse(x, 52 + abs(4 - i) * 3, 11, 10, g(N, y0=36, y1=70), outline=INK, width=2)
    elif kind == 'receding':
        for side in (-1, 1):
            c.shape(bezier((80 + side * 34, 82), (80 + side * 38, 54), (80 + side * 24, 52), None, 10) + [(80 + side * 28, 72)], g(N), outline=INK, width=2)
    return c


def hat(kind):
    c = S()
    if kind in ('tricorn', 'bicorne'):
        hc = (44, 40, 48) if kind == 'tricorn' else (34, 42, 72)
        c.shape(bezier((30, 70), (80, 50), (130, 70), None, 12) + bezier((130, 70), (120, 30), (40, 30), (30, 70), 14)[1:], vgrad(30, 70, shade(hc, 1.4), hc), outline=INK, width=3)
        c.shape(bezier((24, 72), (80, 54), (136, 72), None, 14) + bezier((136, 72), (80, 66), (24, 72), None, 14)[1:-1], shade(hc, 1.2), outline=INK, width=2.5)
        c.line(38, 66, 122, 66, 3, (212, 170, 80))
        if kind == 'bicorne':
            c.ellipse(80, 50, 8, 8, (230, 190, 90), outline=INK, width=2)
    elif kind == 'bandana':   # tinted
        c.shape(bezier((44, 76), (40, 36), (120, 36), (116, 76), 16) + [(80, 66)], shade(N, 0.95), outline=INK, width=2.5)
        c.shape([(112, 66), (132, 84), (124, 92), (108, 74)], shade(N, 0.9), outline=INK, width=2)
    elif kind == 'wig':
        for side in (-1, 1):
            for k in range(3):
                c.ellipse(80 + side * 34, 76 + k * 16, 12, 9, (236, 232, 224), outline=INK, width=2)
        c.shape(bezier((44, 78), (40, 30), (120, 30), (116, 78), 18) + [(80, 62)], (240, 236, 228), outline=INK, width=2.5)
    elif kind == 'cap':       # tinted
        c.shape(bezier((44, 72), (46, 30), (114, 30), (116, 72), 16), shade(N, 0.95), outline=INK, width=2.5)
        c.shape([(40, 70), (120, 70), (124, 78), (36, 78)], shade(N, 0.8), outline=INK, width=2)
    elif kind == 'widebrim':  # tinted
        c.shape(bezier((16, 74), (80, 60), (144, 74), None, 12) + bezier((144, 74), (80, 84), (16, 74), None, 12)[1:-1], shade(N, 0.85), outline=INK, width=2.5)
        c.shape(bezier((50, 70), (54, 30), (106, 30), (110, 70), 14), shade(N, 0.95), outline=INK, width=2.5)
    return c


def acc(kind):
    c = S()
    if kind == 'earring':
        c.ellipse(44, 106, 4, 4, (236, 196, 80), outline=INK, width=1.5)
    elif kind == 'eyepatch':
        c.line(46, 72, 114, 96, 2.2, INK)
        c.ellipse(95, 88, 9, 8, (30, 26, 28), outline=INK, width=1.5)
    elif kind == 'spectacles':
        for ex in (65, 95):
            c.ellipse(ex, 88, 9, 8, (220, 236, 240), outline=(120, 100, 60), width=2, alpha=0.5)
        c.line(74, 88, 86, 88, 2, (120, 100, 60))
    elif kind == 'pipe':
        c.line(92, 120, 112, 132, 3, (90, 60, 40))
        c.rect(110, 124, 120, 138, (110, 74, 48), outline=INK, width=1.5, r=2)
    elif kind == 'scar':
        c.line(58, 94, 66, 112, 2, (150, 70, 70), alpha=0.8)
    return c


PARTS = {
    'plate': (plate, ['0']),
    'hairback': (hairback, ['long', 'tail']),
    'coat': (coat, ['coat', 'naval', 'vest', 'apron', 'robe']),
    'collar': (collar, ['v', 'cravat', 'ruff', 'scarf']),
    'head': (head, [h + '_' + k for h in 'abcdef' for k in ['fair', 'olive', 'tan', 'brown', 'dark']]),
    'beard': (beard, ['full', 'moustache', 'goatee', 'stubble']),
    'hair': (hair, ['short', 'swept', 'bun', 'curly', 'receding']),
    'hat': (hat, ['tricorn', 'bicorne', 'bandana', 'wig', 'cap', 'widebrim']),
    'acc': (acc, ['earring', 'eyepatch', 'spectacles', 'pipe', 'scar']),
}


def main():
    os.makedirs(VEC, exist_ok=True)
    names = []
    for layer, (fn, variants) in PARTS.items():
        for v in variants:
            name = 'npc_%s_%s' % (layer, v)
            fn(v).c.save(os.path.join(VEC, name + '.png'))
            names.append(name)
            if '--install' in sys.argv:
                shutil.copyfile(os.path.join(VEC, name + '.png'), os.path.join(SPRITES, name + '.png'))
    print('parts:', len(names))


if __name__ == '__main__':
    main()
