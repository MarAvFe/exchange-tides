"""Tiny dependency-free anti-aliased vector rasterizer + PNG writer.

Shapes are polygons filled with analytic horizontal coverage over 4 sub-scanlines.
Colors are (r, g, b[, a]) 0..255, or a callable (x, y) -> (r, g, b, a) for gradients.
"""
import math, struct, zlib

SUB = 4


def _rgba(c):
    return (c[0], c[1], c[2], c[3] if len(c) > 3 else 255)


class Canvas:
    def __init__(self, w, h, bg=(0, 0, 0, 0)):
        self.w, self.h = w, h
        bg = _rgba(bg)
        self.px = [[list(bg) for _ in range(w)] for _ in range(h)]

    # ---- core fill -------------------------------------------------------------------------
    def fill(self, pts, color, alpha=1.0):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        y0, y1 = max(0, int(math.floor(min(ys)))), min(self.h - 1, int(math.ceil(max(ys))))
        edges = [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
        func = callable(color)
        if not func:
            cr, cg, cb, ca = _rgba(color)
        for y in range(y0, y1 + 1):
            acc = {}
            for k in range(SUB):
                sy = y + (k + 0.5) / SUB
                xs = []
                for (ax, ay), (bx, by) in edges:
                    if (ay <= sy < by) or (by <= sy < ay):
                        xs.append(ax + (sy - ay) * (bx - ax) / (by - ay))
                xs.sort()
                for i in range(0, len(xs) - 1, 2):
                    xa, xb = max(0.0, xs[i]), min(float(self.w), xs[i + 1])
                    if xb <= xa:
                        continue
                    ia, ib = int(xa), int(xb)
                    if ia == ib:
                        acc[ia] = acc.get(ia, 0.0) + (xb - xa) / SUB
                        continue
                    acc[ia] = acc.get(ia, 0.0) + (ia + 1 - xa) / SUB
                    for x in range(ia + 1, ib):
                        acc[x] = acc.get(x, 0.0) + 1.0 / SUB
                    if ib < self.w:
                        acc[ib] = acc.get(ib, 0.0) + (xb - ib) / SUB
            row = self.px[y]
            for x, cov in acc.items():
                if cov <= 0:
                    continue
                if func:
                    cr, cg, cb, ca = _rgba(color(x + 0.5, y + 0.5))
                a = min(1.0, cov) * alpha * ca / 255.0
                if a <= 0:
                    continue
                p = row[x]
                da = p[3] / 255.0
                oa = a + da * (1 - a)
                if oa <= 0:
                    continue
                p[0] = (cr * a + p[0] * da * (1 - a)) / oa
                p[1] = (cg * a + p[1] * da * (1 - a)) / oa
                p[2] = (cb * a + p[2] * da * (1 - a)) / oa
                p[3] = oa * 255.0

    # ---- helpers ---------------------------------------------------------------------------
    def shape(self, pts, color, outline=None, width=2.0, alpha=1.0):
        if outline is not None:
            self.fill(offset_poly(pts, width / 2), outline, alpha)
            self.fill(offset_poly(pts, -width / 2), color, alpha)
        else:
            self.fill(pts, color, alpha)

    def ellipse(self, cx, cy, rx, ry, color, outline=None, width=2.0, alpha=1.0, rot=0.0):
        self.shape(ellipse_pts(cx, cy, rx, ry, rot=rot), color, outline, width, alpha)

    def rect(self, x0, y0, x1, y1, color, outline=None, width=2.0, alpha=1.0, r=0):
        self.shape(rrect_pts(x0, y0, x1, y1, r), color, outline, width, alpha)

    def line(self, x0, y0, x1, y1, width, color, alpha=1.0):
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * width / 2, dx / L * width / 2
        self.fill([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], color, alpha)

    def polyline(self, pts, width, color, alpha=1.0):
        for a, b in zip(pts, pts[1:]):
            self.line(a[0], a[1], b[0], b[1], width, color, alpha)
            self.ellipse(b[0], b[1], width / 2, width / 2, color, alpha=alpha)

    def save(self, path):
        raw = bytearray()
        for row in self.px:
            raw.append(0)
            for p in row:
                raw += bytes(max(0, min(255, int(round(v)))) for v in p)
        def chunk(t, d):
            c = struct.pack('>I', len(d)) + t + d
            return c + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
        png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 6, 0, 0, 0))
        png += chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
        open(path, 'wb').write(png)


# ---- geometry ------------------------------------------------------------------------------
def ellipse_pts(cx, cy, rx, ry, n=48, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def rrect_pts(x0, y0, x1, y1, r=0):
    if r <= 0:
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    out = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(7):
            a = math.radians(a0 + 15 * i)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def bezier(p0, p1, p2, p3=None, n=16):
    out = []
    for i in range(n + 1):
        t = i / n
        if p3 is None:
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        else:
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1]
        out.append((x, y))
    return out


def offset_poly(pts, d):
    """Offset a simple polygon by d (positive = outward for clockwise-in-screen polygons; auto-detects)."""
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sgn = 1 if area > 0 else -1
    out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nrm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            return (dy / L * sgn, -dx / L * sgn)
        n1, n2 = nrm(p0, p1), nrm(p1, p2)
        mx, my = n1[0] + n2[0], n1[1] + n2[1]
        L = math.hypot(mx, my)
        if L < 1e-6:
            mx, my, L = n1[0], n1[1], 1
        mx, my = mx / L, my / L
        dot = mx * n1[0] + my * n1[1]
        k = d / max(dot, 0.35)
        out.append((p1[0] + mx * k, p1[1] + my * k))
    return out


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))


def vgrad(y0, y1, c0, c1):
    c0, c1 = _rgba(c0), _rgba(c1)
    return lambda x, y: lerp(c0, c1, max(0.0, min(1.0, (y - y0) / ((y1 - y0) or 1))))


def shade(c, k):
    """k<1 darker, k>1 lighter."""
    c = _rgba(c)
    if k < 1:
        return (c[0] * k, c[1] * k, c[2] * k, c[3])
    t = k - 1
    return (c[0] + (255 - c[0]) * t, c[1] + (255 - c[1]) * t, c[2] + (255 - c[2]) * t, c[3])
