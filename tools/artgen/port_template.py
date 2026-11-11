"""Layout template for port backgrounds: sky, distant sea, a ground band where the buildings stand
(door rows at y~390 and y~476), harbour water in front. Repainted per port by comfy_gen.py img2img.
usage: python3 -I port_template.py OUT.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import Canvas, vgrad

c = Canvas(1280, 720, (150, 200, 230))
c.rect(0, 0, 1280, 250, vgrad(0, 250, (120, 175, 225), (225, 230, 225)))
c.shape([(0, 250), (180, 170), (420, 215), (700, 150), (980, 205), (1280, 160), (1280, 300), (0, 300)], (90, 130, 100))
c.rect(0, 255, 1280, 330, vgrad(255, 330, (90, 170, 190), (70, 150, 175)))
c.shape([(0, 340), (300, 322), (700, 318), (1100, 324), (1280, 335), (1280, 520), (0, 520)], vgrad(320, 520, (150, 160, 110), (205, 185, 140)))
c.rect(0, 500, 1280, 560, vgrad(500, 560, (215, 195, 150), (190, 165, 120)))
c.rect(0, 560, 1280, 720, vgrad(560, 720, (60, 160, 175), (30, 100, 130)))
for x in range(340, 1280, 90):
    c.rect(x, 548, x + 10, 640, (110, 80, 55))
c.rect(300, 548, 1280, 562, (150, 110, 70))
c.save(sys.argv[1])
