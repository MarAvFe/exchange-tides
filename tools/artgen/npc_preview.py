"""Preview random NPC compositions from part PNGs (same rules as the game's npc_draw).
usage: python3 -I npc_preview.py OUT.png [DIR]   DIR = folder with npc_*.png (default: vector/)"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import read_png, write_png

HERE = os.path.dirname(os.path.abspath(__file__))
SKINS = [(255, 236, 222), (240, 204, 170), (214, 168, 128), (176, 124, 88), (130, 88, 60), (98, 66, 46)]
HAIRS = [(60, 44, 36), (30, 26, 26), (120, 80, 50), (180, 130, 70), (150, 60, 40), (200, 200, 200), (120, 116, 112)]
CLOTH = [(70, 90, 140), (140, 50, 50), (60, 110, 80), (120, 90, 60), (90, 70, 110), (200, 180, 130), (60, 60, 64)]
BGS = [(110, 140, 170), (160, 120, 90), (110, 140, 110), (150, 110, 130), (170, 150, 110)]
TINT = {'plate': 'bg', 'hairback': 'hair', 'coat': 'cloth', 'beard': 'hair', 'hair': 'hair'}


def compose(d, rnd):
    t = {'skin': rnd.choice(SKINS), 'hair': rnd.choice(HAIRS), 'cloth': rnd.choice(CLOTH), 'bg': rnd.choice(BGS)}
    hatk = rnd.choice(['', '', 'tricorn', 'bicorne', 'bandana', 'wig', 'cap', 'widebrim'])
    layers = [('plate', '0'), ('hairback', rnd.choice(['', '', 'long', 'tail'])), ('coat', rnd.choice(['coat', 'naval', 'vest', 'apron', 'robe'])),
              ('collar', rnd.choice(['v', 'cravat', 'ruff', 'scarf'])),
              ('head', rnd.choice('abcdef') + '_' + rnd.choice(['fair', 'olive', 'tan', 'brown', 'dark'])), ('beard', rnd.choice(['', '', 'full', 'moustache', 'goatee', 'stubble'])),
              ('hair', '' if hatk in ('tricorn', 'bicorne', 'wig') else rnd.choice(['short', 'swept', 'bun', 'curly', 'receding'])),
              ('hat', hatk), ('acc', rnd.choice(['', '', '', 'earring', 'eyepatch', 'spectacles', 'pipe', 'scar']))]
    W, H = 320, 400
    out = [0.0] * (W * H * 3)
    for layer, v in layers:
        if not v:
            continue
        p = os.path.join(d, 'npc_%s_%s.png' % (layer, v))
        if not os.path.exists(p):
            continue
        w, h, bpp, px = read_png(p)
        tint = t.get(TINT.get(layer, ''), (255, 255, 255))
        if layer == 'hat' and v in ('bandana', 'cap', 'widebrim'):
            tint = t['cloth']
        for i in range(w * h):
            a = px[i * bpp + 3] / 255 if bpp == 4 else 1
            if a <= 0:
                continue
            for k in range(3):
                out[i * 3 + k] = out[i * 3 + k] * (1 - a) + px[i * bpp + k] * tint[k] / 255 * a
    return W, H, [int(x) for x in out]


if __name__ == '__main__':
    d = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'vector')
    rnd = random.Random(5)
    tiles = [compose(d, rnd)[2] for _ in range(8)]
    W, H = 320 * 4, 400 * 2
    img = [0] * (W * H * 3)
    for n, t in enumerate(tiles):
        ox, oy = (n % 4) * 320, (n // 4) * 400
        for y in range(400):
            row = t[y * 960:(y + 1) * 960]
            s = ((oy + y) * W + ox) * 3
            img[s:s + 960] = row
    write_png(sys.argv[1], W, H, img)
