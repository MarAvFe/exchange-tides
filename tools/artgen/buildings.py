"""Vector base shapes for the port buildings (repainted by comfy_gen.py img2img).

Every building is 320x280 with a transparent background and its door centred at (160, 262).
The game uses that convention to place the glowing door (see scr_port.gml).
usage: python3 -I buildings.py OUT_DIR
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import Canvas, vgrad, shade

INK = (38, 30, 36)
W, H = 320, 280
DOOR_X, DOOR_Y = 160, 262


def door(c, w=34, h=56, col=(92, 58, 36), arch=True):
    x0, y1 = DOOR_X - w // 2, DOOR_Y + 12
    c.rect(x0, y1 - h, x0 + w, y1, col, outline=INK, width=3, r=w // 2 if arch else 2)
    c.ellipse(x0 + w - 8, y1 - h // 2, 3, 3, (220, 180, 80))


def windows(c, xs, y, w=24, h=30, lit=(250, 214, 140)):
    for x in xs:
        c.rect(x, y, x + w, y + h, lit, outline=INK, width=2, r=3)
        c.line(x + w / 2, y, x + w / 2, y + h, 2, INK)


def walls(c, x0, y0, x1, y1, col):
    c.rect(x0, y0, x1, y1, vgrad(y0, y1, col, shade(col, 0.75)), outline=INK, width=3)


def roof(c, x0, x1, y_base, y_top, col, overhang=14):
    c.shape([(x0 - overhang, y_base), ((x0 + x1) / 2, y_top), (x1 + overhang, y_base)], vgrad(y_top, y_base, col, shade(col, 0.7)), outline=INK, width=3)


def tavern():
    c = Canvas(W, H)
    walls(c, 50, 120, 270, 274, (214, 180, 130))
    roof(c, 50, 270, 124, 40, (170, 70, 50))
    windows(c, [72, 224], 150); windows(c, [72, 224], 206)
    c.line(196, 150, 238, 150, 4, (90, 60, 40)); c.ellipse(232, 172, 16, 20, (150, 100, 50), outline=INK, width=2)
    door(c, 44, 66)
    return c


def bank():
    c = Canvas(W, H)
    walls(c, 46, 110, 274, 274, (226, 218, 196))
    c.shape([(36, 112), (160, 50), (284, 112)], (236, 228, 206), outline=INK, width=3)
    for x in (70, 112, 196, 238):
        c.rect(x, 116, x + 16, 256, (244, 238, 222), outline=INK, width=2)
    c.rect(36, 256, 284, 274, (200, 190, 170), outline=INK, width=2)
    door(c, 40, 70, (70, 60, 50), arch=False)
    return c


def governor():
    c = Canvas(W, H)
    walls(c, 30, 110, 290, 274, (90, 130, 190))
    roof(c, 30, 290, 112, 60, (200, 190, 170), overhang=8)
    c.rect(150, 10, 154, 62, (90, 70, 50)); c.shape([(154, 12), (190, 20), (154, 30)], (200, 60, 60), outline=INK, width=2)
    windows(c, [54, 100, 196, 242], 130); windows(c, [54, 100, 196, 242], 196)
    c.rect(116, 176, 204, 186, (240, 236, 220), outline=INK, width=2)
    door(c, 40, 74)
    return c


def market():
    c = Canvas(W, H)
    cols = [(200, 70, 60), (60, 120, 170), (220, 170, 60)]
    for i, x in enumerate((20, 115, 210)):
        c.rect(x + 8, 150, x + 82, 274, (170, 130, 90), outline=INK, width=2)
        col = cols[i]
        c.shape([(x, 150), (x + 90, 150), (x + 80, 116), (x + 10, 116)], col, outline=INK, width=3)
        for k in range(4):
            c.rect(x + 12 + k * 18, 118, x + 20 + k * 18, 148, shade(col, 1.3))
        c.rect(x + 16, 236, x + 74, 270, (140, 100, 60), outline=INK, width=2)
    c.rect(DOOR_X - 22, 200, DOOR_X + 22, 274, (60, 44, 34), outline=INK, width=2)
    return c


def shipyard():
    c = Canvas(W, H)
    walls(c, 40, 120, 280, 274, (150, 110, 74))
    roof(c, 40, 280, 124, 30, (110, 80, 56))
    c.line(30, 30, 290, 30, 6, (90, 66, 44)); c.line(270, 30, 270, 120, 5, (90, 66, 44))
    c.line(270, 34, 220, 110, 2, (60, 50, 40))
    c.rect(DOOR_X - 60, 160, DOOR_X + 60, 274, (60, 44, 34), outline=INK, width=3, r=56)
    c.shape([(DOOR_X - 50, 250), (DOOR_X + 50, 250), (DOOR_X + 30, 270), (DOOR_X - 30, 270)], (160, 110, 70), outline=INK, width=2)
    return c


def lender():
    c = Canvas(W, H)
    walls(c, 100, 60, 220, 274, (120, 80, 130))
    roof(c, 100, 220, 64, 8, (70, 50, 80), overhang=10)
    windows(c, [118, 178], 84); windows(c, [118, 178], 140)
    c.ellipse(240, 150, 18, 18, (220, 180, 70), outline=INK, width=3)
    c.line(220, 130, 240, 130, 3, (80, 60, 50))
    door(c, 30, 58, (60, 40, 60))
    return c


def curio():
    c = Canvas(W, H)
    c.ellipse(160, 200, 96, 76, vgrad(130, 276, (190, 150, 110), (130, 96, 70)), outline=INK, width=3)
    c.rect(64, 200, 256, 274, vgrad(200, 274, (190, 150, 110), (130, 96, 70)), outline=INK, width=3)
    c.shape([(50, 150), (160, 30), (270, 150)], vgrad(30, 150, (60, 140, 120), (30, 80, 70)), outline=INK, width=3)
    for x in (90, 230):
        c.line(x, 150, x, 172, 2, INK); c.ellipse(x, 182, 9, 12, (250, 200, 90), outline=INK, width=2)
    c.shape([(160, 70), (168, 90), (190, 92), (172, 104), (178, 126), (160, 112), (142, 126), (148, 104), (130, 92), (152, 90)], (250, 220, 120), outline=INK, width=2)
    door(c, 36, 60, (70, 50, 70))
    return c


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'vector'
    os.makedirs(out, exist_ok=True)
    for name, fn in (('tavern', tavern), ('bank', bank), ('governor', governor), ('market', market),
                     ('shipyard', shipyard), ('lender', lender), ('curio', curio)):
        fn().save(os.path.join(out, 'bld_' + name + '.png'))
        print('wrote bld_' + name)


if __name__ == '__main__':
    main()
