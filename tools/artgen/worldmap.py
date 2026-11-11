"""World map of the Reach: mainland coasts + islands, port placement and sea routes.

Writes:
  tools/artgen/vector/worldmap.png      the vector map (reference for the painted img2img pass, see art_spec.json)
  datafiles/sprites/worldmap.png        installed as-is unless --no-install (repaint later with comfy_gen.py)
  datafiles/data/routes.json            {"a|b": [[x,y],...]} water-only route for every port pair (a < b)
  datafiles/data/ports.json             x/y of every port updated to its coastal spot
Routes are A* paths on a 4 px land mask that keep clear of coasts, then string-pulled and smoothed.
To add a port: add it to ports.json and PORT_SPOTS below (rough spot near a coast), then rerun:
  python3 -I tools/artgen/worldmap.py
"""
import heapq, json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import Canvas, bezier, vgrad, offset_poly

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, 'game', 'ExchangeTides', 'datafiles', 'data')
SPRITES = os.path.join(ROOT, 'game', 'ExchangeTides', 'datafiles', 'sprites')
W, H, CELL = 1280, 720, 4
GW, GH = W // CELL, H // CELL
INK = (52, 40, 36)

# Coarse outlines (clockwise-ish); they are roughened by coast().
MAINLAND_NW = [(-40, -40), (930, -40), (900, 40), (820, 92), (740, 74), (660, 118), (575, 100), (500, 132), (430, 112),
               (360, 160), (285, 150), (240, 210), (180, 236), (160, 300), (115, 350), (128, 430), (80, 500), (-40, 530)]
MAINLAND_NE = [(1010, -40), (1320, -40), (1320, 480), (1236, 452), (1180, 400), (1150, 330), (1100, 280), (1060, 214),
               (1004, 168), (978, 108), (1002, 52)]
SOUTH_COAST = [(-40, 760), (-40, 640), (60, 622), (170, 652), (250, 616), (340, 636), (420, 680), (520, 676), (590, 760)]
ISLANDS = [  # (cx, cy, rx, ry, seed)
    (705, 262, 62, 44, 'brasa'), (430, 372, 86, 52, 'velo'), (648, 468, 44, 30, 'mangrove'),
    (905, 398, 66, 44, 'iron'), (1090, 590, 70, 46, 'tide'), (790, 640, 40, 26, 'cay'),
    (300, 288, 22, 15, 'r1'), (560, 296, 18, 13, 'r2'), (1000, 486, 20, 14, 'r3'), (860, 236, 22, 16, 'r4'),
    (560, 590, 24, 15, 'r5'), (230, 520, 20, 13, 'r6'), (1220, 680, 26, 18, 'r7'), (960, 650, 16, 11, 'r8'),
]
# Rough port spots; each is snapped to the nearest coastal land cell.
PORT_SPOTS = {
    'saltmere': (262, 196), 'coralhaven': (540, 120), 'kestrel_bay': (1010, 160), 'lanterna': (1170, 380),
    'driftmoor': (128, 420), 'puerto_ambar': (330, 640), 'isla_brasa': (705, 296), 'san_velo': (450, 414),
    'mangrove_key': (648, 490), 'ironreef': (880, 432), 'tidewell': (1060, 624), 'blackwater_cay': (790, 658),
}
VOLCANIC = {'brasa'}


def coast(pts, seed, rough=0.22, depth=5):
    """Fractal midpoint displacement + Chaikin smoothing of a closed outline."""
    rnd = random.Random(seed)
    p = list(pts)
    for d in range(depth):
        q = []
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            nx, ny = -(b[1] - a[1]) / (L or 1), (b[0] - a[0]) / (L or 1)
            off = rnd.uniform(-1, 1) * L * rough
            q += [a, ((a[0] + b[0]) / 2 + nx * off, (a[1] + b[1]) / 2 + ny * off)]
        p = q
    for _ in range(2):
        q = []
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            q += [(a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25), (a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75)]
        p = q
    return p


def blob(cx, cy, rx, ry, seed, n=14):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 + 0.16 * math.sin(2 * t + ph[0]) + 0.1 * math.sin(3 * t + ph[1])
        pts.append((cx + math.cos(t) * rx * k, cy + math.sin(t) * ry * k))
    return coast(pts, seed, 0.18, 3)


def scan_mask(polys):
    """Land mask on the CELL grid (even-odd fill of every polygon)."""
    m = [[False] * GW for _ in range(GH)]
    for poly in polys:
        edges = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        for gy in range(GH):
            sy = (gy + 0.5) * CELL
            xs = sorted(ax + (sy - ay) * (bx - ax) / (by - ay) for (ax, ay), (bx, by) in edges if (ay <= sy < by) or (by <= sy < ay))
            for i in range(0, len(xs) - 1, 2):
                for gx in range(max(0, int(xs[i] / CELL)), min(GW, int(xs[i + 1] / CELL) + 1)):
                    if xs[i] <= (gx + 0.5) * CELL < xs[i + 1]:
                        m[gy][gx] = True
    return m


def distance_to_land(m):
    INF = 10 ** 9
    d = [[0 if m[y][x] else INF for x in range(GW)] for y in range(GH)]
    q = [(x, y) for y in range(GH) for x in range(GW) if m[y][x]]
    head = 0
    while head < len(q):
        x, y = q[head]; head += 1
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < GW and 0 <= ny < GH and d[ny][nx] > d[y][x] + 1:
                d[ny][nx] = d[y][x] + 1
                q.append((nx, ny))
    return d


def astar(m, dist, a, b, open_land):
    """8-way A*; cells near land cost more so routes keep to open water."""
    def cost(x, y):
        if m[y][x] and (x, y) not in open_land:
            return None
        return 1 + max(0, 5 - dist[y][x]) * 0.9
    g = {a: 0}
    prev = {}
    pq = [(0, a)]
    while pq:
        _, cur = heapq.heappop(pq)
        if cur == b:
            break
        x, y = cur
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < GW and 0 <= ny < GH):
                    continue
                c = cost(nx, ny)
                if c is None:
                    continue
                if dx and dy and (cost(x + dx, y) is None or cost(x, y + dy) is None):
                    continue
                ng = g[cur] + c * (1.4142 if dx and dy else 1)
                if ng < g.get((nx, ny), 1e18):
                    g[(nx, ny)] = ng
                    prev[(nx, ny)] = cur
                    heapq.heappush(pq, (ng + math.hypot(b[0] - nx, b[1] - ny), (nx, ny)))
    path = [b]
    while path[-1] != a:
        path.append(prev[path[-1]])
    return path[::-1]


def clear_line(m, dist, p, q, open_land, margin):
    n = int(math.hypot(q[0] - p[0], q[1] - p[1]) * 2) + 1
    for i in range(n + 1):
        x = round(p[0] + (q[0] - p[0]) * i / n); y = round(p[1] + (q[1] - p[1]) * i / n)
        if (x, y) in open_land:
            continue
        if m[y][x] or dist[y][x] < margin:
            return False
    return True


def smooth_route(m, dist, cells, open_land):
    out = [cells[0]]
    i = 0
    while i < len(cells) - 1:
        j = len(cells) - 1
        while j > i + 1 and not clear_line(m, dist, cells[i], cells[j], open_land, 2):
            j -= 1
        out.append(cells[j]); i = j
    pts = [((x + .5) * CELL, (y + .5) * CELL) for x, y in out]
    for _ in range(2):  # Chaikin, keeping the end points
        if len(pts) < 3:
            break
        q = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            q += [(a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25), (a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75)]
        q.append(pts[-1])
        pts = q
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def main():
    install = '--no-install' not in sys.argv
    lands = [coast(MAINLAND_NW, 'nw', 0.2), coast(MAINLAND_NE, 'ne', 0.2), coast(SOUTH_COAST, 's', 0.2)]
    isl = [blob(cx, cy, rx, ry, s) for cx, cy, rx, ry, s in ISLANDS]
    polys = lands + isl
    m = scan_mask(polys)
    dist = distance_to_land(m)

    # Snap ports to coastal land cells and pick a dock (adjacent water cell).
    ports = json.load(open(os.path.join(DATA, 'ports.json')))
    spots, docks, open_land = {}, {}, set()
    for p in ports:
        sx, sy = PORT_SPOTS[p['id']]
        best = None
        for y in range(GH):
            for x in range(GW):
                if not m[y][x]:
                    continue
                if not any(0 <= x + dx < GW and 0 <= y + dy < GH and not m[y + dy][x + dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    continue
                d = (x * CELL - sx) ** 2 + (y * CELL - sy) ** 2
                if best is None or d < best[0]:
                    best = (d, x, y)
        _, x, y = best
        spots[p['id']] = (x, y)
        p['x'], p['y'] = int((x + .5) * CELL), int((y + .5) * CELL)
        # The harbour: land cells within 3 of the port are passable for this port only.
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if 0 <= x + dx < GW and 0 <= y + dy < GH:
                    open_land.add((x + dx, y + dy))
    json.dump(ports, open(os.path.join(DATA, 'ports.json'), 'w'), indent=1)

    routes = {}
    ids = sorted(spots)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ol = {c for c in open_land if math.dist(c, spots[a]) <= 4.3 or math.dist(c, spots[b]) <= 4.3}
            cells = astar(m, dist, spots[a], spots[b], ol)
            routes[a + '|' + b] = smooth_route(m, dist, cells, ol)
    json.dump(routes, open(os.path.join(DATA, 'routes.json'), 'w'), separators=(',', ':'))
    print('ports placed:', len(spots), 'routes:', len(routes))

    # ---- drawing ----------------------------------------------------------------------------
    c = Canvas(W, H)
    c.rect(0, 0, W, H, vgrad(0, H, (78, 148, 170), (40, 96, 134)))
    # Shallows: draw each landmass slightly expanded in pale turquoise.
    for poly in polys:
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        grow = [(x + (x - cx) / max(1, math.hypot(x - cx, y - cy)) * 14, y + (y - cy) / max(1, math.hypot(x - cx, y - cy)) * 14) for x, y in poly]
        c.fill(grow, (130, 200, 204, 120))
    rnd = random.Random(7)
    for i in range(320):  # wave marks on open water
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        gx, gy = min(GW - 1, int(x / CELL)), min(GH - 1, int(y / CELL))
        if dist[gy][gx] < 6:
            continue
        c.polyline(bezier((x, y), (x + 6, y - 4), (x + 12, y), None, 6), 1.4, (214, 236, 238, 120))
    for poly in polys:
        c.shape(poly, (232, 212, 162), outline=(120, 92, 62), width=2.5)
    for poly in isl:  # island grass inside the beach
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        c.fill([(cx + (x - cx) * 0.84, cy + (y - cy) * 0.84) for x, y in poly], vgrad(cy - 60, cy + 60, (128, 170, 94), (84, 126, 64)))
    # Mainland grass: the coastline pulled inland (the mainland outlines run off-screen, so an inset works).
    for poly in lands:
        c.fill(offset_poly(poly, -11), vgrad(0, H, (124, 166, 90), (92, 134, 70)))
    # Hills, forests, volcano.
    for poly, seed in zip(polys, ['nw', 'ne', 's'] + [s for *_, s in ISLANDS]):
        r2 = random.Random(seed)
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        for k in range(int(min(40, area / 2600))):
            hx, hy = r2.uniform(min(xs), max(xs)), r2.uniform(min(ys), max(ys))
            gx, gy = int(hx / CELL), int(hy / CELL)
            if not (0 <= gx < GW and 0 <= gy < GH) or not m[gy][gx] or dist_sea(m, gx, gy) < 4:
                continue
            if r2.random() < 0.5:
                hr = r2.uniform(10, 18)
                c.shape([(hx - hr, hy + hr * .45), (hx - hr * .2, hy - hr * .7), (hx + hr, hy + hr * .45)],
                        vgrad(hy - hr, hy + hr, (164, 150, 112), (104, 108, 76)), outline=(70, 66, 50), width=1.4)
            else:
                for t in range(3):
                    tx, ty = hx + r2.uniform(-10, 10), hy + r2.uniform(-6, 6)
                    c.ellipse(tx, ty, 6, 7, (58, 104, 58), outline=(40, 70, 40), width=1)
        if seed in VOLCANIC:
            cx = sum(xs) / len(xs); cy = sum(ys) / len(ys)
            c.shape([(cx - 30, cy + 12), (cx - 8, cy - 26), (cx + 8, cy - 26), (cx + 30, cy + 12)],
                    vgrad(cy - 26, cy + 12, (120, 90, 70), (84, 66, 54)), outline=(50, 40, 36), width=1.6)
            c.ellipse(cx, cy - 30, 9, 6, (150, 150, 150, 160))
            c.ellipse(cx + 6, cy - 40, 12, 8, (170, 170, 170, 120))
    # Port towns: a little cluster of roofs.
    for p in ports:
        x, y = p['x'], p['y']
        r2 = random.Random(p['id'])
        for k in range(4):
            hx, hy = x + r2.uniform(-10, 10), y + r2.uniform(-8, 4)
            c.rect(hx - 4, hy - 3, hx + 4, hy + 4, (236, 226, 204), outline=INK, width=1)
            c.fill([(hx - 5, hy - 3), (hx, hy - 8), (hx + 5, hy - 3)], (176, 70, 52))
    # Compass rose.
    cx, cy = 1210, 120
    c.ellipse(cx, cy, 40, 40, (244, 232, 200, 220), outline=INK, width=2)
    for a in range(8):
        t = a * math.pi / 4
        L = 36 if a % 2 == 0 else 22
        c.fill([(cx + math.cos(t) * L, cy + math.sin(t) * L), (cx + math.cos(t + .25) * 8, cy + math.sin(t + .25) * 8),
                (cx, cy), (cx + math.cos(t - .25) * 8, cy + math.sin(t - .25) * 8)], (170, 60, 50) if a == 6 else INK)
    for i in range(14):  # vignette
        col = (70, 50, 30, max(0, 90 - i * 6))
        c.rect(i, i, W - i, i + 1, col); c.rect(i, H - i - 1, W - i, H - i, col)
        c.rect(i, i, i + 1, H - i, col); c.rect(W - i - 1, i, W - i, H - i, col)
    os.makedirs(os.path.join(HERE, 'vector'), exist_ok=True)
    c.save(os.path.join(HERE, 'vector', 'worldmap.png'))
    if install:
        c.save(os.path.join(SPRITES, 'worldmap.png'))
    # Debug view of the routes (scratch use).
    if '--debug' in sys.argv:
        for r in routes.values():
            c.polyline([tuple(p) for p in r], 1.5, (255, 255, 255, 200))
        for p in ports:
            c.ellipse(p['x'], p['y'], 5, 5, (220, 40, 40))
        c.save(sys.argv[sys.argv.index('--debug') + 1])
    print('map written')


def dist_sea(m, x, y):
    for r in range(1, 8):
        for dx in range(-r, r + 1):
            for dy in (-r, r):
                if 0 <= x + dx < GW and 0 <= y + dy < GH and not m[y + dy][x + dx]:
                    return r
            for dy in range(-r, r + 1):
                for dx2 in (-r, r):
                    if 0 <= x + dx2 < GW and 0 <= y + dy < GH and not m[y + dy][x + dx2]:
                        return r
    return 8


if __name__ == '__main__':
    main()
