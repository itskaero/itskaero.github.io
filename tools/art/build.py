#!/usr/bin/env python3
"""
The Systems Atlas: illustration generator for itskaero.github.io
-------------------------------------------------------------------
Every illustration on the site comes out of this one file, so the plates
share a palette, a line weight and a hand. Standard library only.

    python3 tools/art/build.py

Writes:
  assets/illustrations/*.svg   decorative and chapter artwork
  assets/projects/*-art.svg    one plate per project
and injects two inline SVGs into index.html between marker comments:
  <!-- art:hero -->     ...  <!-- /art:hero -->
  <!-- art:process -->  ...  <!-- /art:process -->
(inline so the page CSS can draw them on and the webfonts apply).

Everything is seeded: running it twice produces identical files.
"""

import math
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ILL = os.path.join(ROOT, 'assets', 'illustrations')
PRJ = os.path.join(ROOT, 'assets', 'projects')

# ── palette (mirrors the :root tokens in style.css) ──────────────────────
PAPER = '#F1ECDF'
PAPER2 = '#E7E0CF'
INK = '#1C1F1C'
INK2 = '#4A4F48'
INK3 = '#8A8D82'
FOREST = '#10241B'
FOREST2 = '#183528'
FOREST3 = '#2C5A43'
MOSS = '#6E8B6A'
LIME = '#C8F05A'
STAIN = '#B4502F'

MONO = "'JetBrains Mono', ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace"


PREC = [1]   # decimals; the hero drops to whole units to stay small inline


def f(v):
    """Short number formatting keeps the files small."""
    if PREC[0] == 0:
        return str(int(round(v)))
    s = ('%.1f' % v).rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def poly(points, close=False):
    d = 'M' + ' L'.join('%s %s' % (f(x), f(y)) for x, y in points)
    return d + (' Z' if close else '')


def smooth(points, close=False):
    """Catmull-Rom through the points, emitted as cubic Béziers."""
    pts = list(points)
    if close:
        pts = pts[-1:] + pts + pts[:2]
    else:
        pts = pts[:1] + pts + pts[-1:]
    d = 'M%s %s' % (f(pts[1][0]), f(pts[1][1]))
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%s %s %s %s %s %s' % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d + (' Z' if close else '')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print('  %-48s %6.1f KB' % (os.path.relpath(path, ROOT), len(text.encode()) / 1024))


def svg_file(w, h, body, title, extra_style=''):
    """A standalone SVG with its own colours (it is loaded through <img>)."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img">\n'
        '<title>%s</title>\n<style>\n'
        '.l{fill:none;stroke:%s;stroke-width:1.1;stroke-linecap:round;stroke-linejoin:round}\n'
        '.h{fill:none;stroke:%s;stroke-width:.6}\n'
        '.f{fill:%s}.p{fill:%s}.lime{fill:%s}.st{fill:%s}\n'
        '.t{font:500 11px %s;letter-spacing:.12em;fill:%s;text-transform:uppercase}\n'
        '.tl{font:400 10px %s;letter-spacing:.08em;fill:%s}\n%s'
        '</style>\n%s\n</svg>\n'
    ) % (w, h, title, FOREST, INK3, FOREST, PAPER, LIME, STAIN, MONO, INK2, MONO, INK3,
         extra_style, body)


def label(x, y, text, cls='t', anchor='start'):
    a = '' if anchor == 'start' else ' text-anchor="%s"' % anchor
    return '<text class="%s" x="%s" y="%s"%s>%s</text>' % (cls, f(x), f(y), a, text)


# ═════════════════════════════════════════════════════════════════════════
#  00 · HERO: the panoramic atlas (inline)
# ═════════════════════════════════════════════════════════════════════════

def ridge(rng, y0, amp, n=56, w=1600, slope=0):
    phases = [rng.uniform(0, math.tau) for _ in range(4)]
    freqs = [rng.uniform(.8, 1.4), rng.uniform(2, 3.2), rng.uniform(4.5, 6.5), rng.uniform(9, 13)]
    amps = [1, .45, .2, .08]
    pts = []
    for i in range(n + 1):
        x = -20 + (w + 40) * i / n
        t = x / w
        y = y0 - amp * sum(a * (0.5 + 0.5 * math.sin(fr * math.tau * t + ph))
                           for a, fr, ph in zip(amps, freqs, phases))
        # the land falls away to the left, leaving the headline column clear
        if slope and x < 860:
            y += slope * ((860 - x) / 860) ** 1.4
        pts.append((x, y))
    return pts


def skyline(rng, x0, x1, base):
    """
    An original, generic skyline in the idiom of Bahawalpur's Nawabi
    architecture (onion domes, chhatris, slender minarets, round fort
    bastions with crenellations). Line drawing only, no single building
    is reproduced.
    """
    out = []
    x = x0

    def dome(cx, w, h, y):
        # onion dome with a finial
        s = w / 2
        d = 'M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s' % (
            f(cx - s), f(y),
            f(cx - s * 1.25), f(y - h * .55), f(cx - s * .2), f(y - h * .75), f(cx), f(y - h),
            f(cx + s * .2), f(y - h * .75), f(cx + s * 1.25), f(y - h * .55), f(cx + s), f(y))
        out.append(d)
        out.append(poly([(cx, y - h), (cx, y - h - w * .32)]))
        out.append('M%s %s a%s %s 0 1 0 .1 0' % (f(cx - .05), f(y - h - w * .36), f(w * .05), f(w * .05)))

    def arches(xa, xb, y, h):
        n = max(1, int((xb - xa) / 16))
        step = (xb - xa) / n
        for i in range(n):
            a = xa + i * step + 3
            b = a + step - 6
            m = (a + b) / 2
            out.append('M%s %s L%s %s Q%s %s %s %s L%s %s' % (
                f(a), f(y), f(a), f(y - h * .55), f(m), f(y - h), f(b), f(y - h * .55), f(b), f(y)))

    while x < x1:
        kind = rng.choice(['block', 'block', 'domed', 'minaret', 'bastion', 'chhatri', 'gap'])
        if kind == 'gap':
            x += rng.uniform(10, 24)
            continue
        if kind == 'block':
            w = rng.uniform(40, 90)
            h = rng.uniform(26, 58)
            out.append(poly([(x, base), (x, base - h), (x + w, base - h), (x + w, base)]))
            arches(x + 4, x + w - 4, base, min(22, h * .5))
            # parapet
            out.append(poly([(x - 2, base - h), (x + w + 2, base - h)]))
            x += w + rng.uniform(2, 8)
        elif kind == 'domed':
            w = rng.uniform(70, 120)
            h = rng.uniform(40, 62)
            out.append(poly([(x, base), (x, base - h), (x + w, base - h), (x + w, base)]))
            arches(x + 6, x + w - 6, base, h * .55)
            dome(x + w / 2, w * .46, w * .5, base - h)
            for cx in (x + 8, x + w - 8):
                out.append(poly([(cx - 5, base - h), (cx - 5, base - h - 14), (cx + 5, base - h - 14), (cx + 5, base - h)]))
                dome(cx, 12, 11, base - h - 14)
            x += w + rng.uniform(4, 12)
        elif kind == 'minaret':
            h = rng.uniform(120, 170)
            w = 10
            out.append(poly([(x, base), (x + 1.5, base - h), (x + w - 1.5, base - h), (x + w, base)]))
            for k in (0.38, 0.7):
                yb = base - h * k
                out.append(poly([(x - 4, yb), (x + w + 4, yb)]))
            out.append(poly([(x - 3, base - h), (x - 3, base - h - 10), (x + w + 3, base - h - 10), (x + w + 3, base - h)]))
            dome(x + w / 2, w + 4, 14, base - h - 10)
            x += w + rng.uniform(14, 30)
        elif kind == 'bastion':
            w = rng.uniform(46, 62)
            h = rng.uniform(64, 92)
            # tapering round bastion with crenellations
            out.append(poly([(x, base), (x + 5, base - h), (x + w - 5, base - h), (x + w, base)]))
            n = int(w / 9)
            cr = []
            for i in range(n + 1):
                cx = x + 5 + (w - 10) * i / n
                cr += [(cx, base - h), (cx, base - h - 7)] if i % 2 == 0 else [(cx, base - h - 7), (cx, base - h)]
            out.append(poly(cr))
            for k in (.3, .62):
                out.append('M%s %s Q%s %s %s %s' % (f(x + 3), f(base - h * k), f(x + w / 2), f(base - h * k + 6),
                                                    f(x + w - 3), f(base - h * k)))
            x += w + rng.uniform(2, 10)
        else:  # chhatri
            w = rng.uniform(22, 32)
            h = rng.uniform(30, 44)
            out.append(poly([(x, base), (x, base - h * .6), (x + w, base - h * .6), (x + w, base)]))
            out.append(poly([(x + 3, base - h * .6), (x + 3, base - h), (x + w - 3, base - h), (x + w - 3, base - h * .6)]))
            out.append('M%s %s Q%s %s %s %s' % (f(x - 3), f(base - h), f(x + w / 2), f(base - h - w * .7), f(x + w + 3), f(base - h)))
            x += w + rng.uniform(6, 16)
    return out


def tree(rng):
    """A bronchial / dendritic tree that resolves into a network at its tips."""
    segs = []      # (depth, path)
    tips = []

    def branch(x, y, ang, ln, depth, maxd):
        ex = x + ln * math.cos(ang)
        ey = y - ln * math.sin(ang)
        bend = rng.uniform(-.18, .18) * ln
        mx = (x + ex) / 2 + bend * math.sin(ang)
        my = (y + ey) / 2 + bend * math.cos(ang)
        segs.append((depth, 'M%s %s Q%s %s %s %s' % (f(x), f(y), f(mx), f(my), f(ex), f(ey))))
        if depth >= maxd:
            tips.append((ex, ey))
            return
        kids = 3 if (depth in (1, 3) and rng.random() < .35) else 2
        spread = rng.uniform(.34, .56)
        for k in range(kids):
            off = (k - (kids - 1) / 2) * spread * (1.25 if kids == 2 else .9)
            branch(ex, ey, ang + off + rng.uniform(-.08, .08), ln * rng.uniform(.7, .8), depth + 1, maxd)

    branch(1190, 612, math.pi / 2 + .04, 112, 0, 6)
    return segs, tips


def hero():
    PREC[0] = 0
    rng = random.Random(26)
    W, H = 1600, 1000
    horizon = 640
    p = []
    p.append('<svg class="atlas" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">' % (W, H))
    p.append('<defs>'
             '<pattern id="atlas-grid" width="40" height="40" patternUnits="userSpaceOnUse">'
             '<path d="M40 0H0V40" class="a-grid"/></pattern>'
             '<pattern id="atlas-grid-major" width="200" height="200" patternUnits="userSpaceOnUse">'
             '<path d="M200 0H0V200" class="a-grid-major"/></pattern>'
             '<clipPath id="atlas-lens"><circle cx="1395" cy="812" r="118"/></clipPath>'
             '</defs>')

    # grid sheet
    p.append('<g class="a-sheet"><rect width="%d" height="%d" fill="url(#atlas-grid)"/>'
             '<rect width="%d" height="%d" fill="url(#atlas-grid-major)"/></g>' % (W, H, W, H))

    # edge rulers: coordinate ticks like a map sheet
    t = ['<g class="a-ruler">']
    for i in range(0, W + 1, 40):
        hgt = 10 if i % 200 == 0 else 5
        t.append('<path d="M%d %d v%d"/>' % (i, H - 1, -hgt))
    for i, c in enumerate('ABCDEFGH'):
        t.append('<text class="a-lbl a-faint" x="%d" y="%d">%s</text>' % (i * 200 + 8, H - 14, c))
    t.append('</g>')
    p.append(''.join(t))

    # faint plan-view contour rings (behind everything)
    rings = ['<g class="a-contour">']
    crng = random.Random(7)
    ph = [crng.uniform(0, math.tau) for _ in range(3)]
    for k in range(9):
        r0 = 40 + k * 26
        pts = []
        for i in range(30):
            a = math.tau * i / 30
            r = r0 * (1 + .13 * math.sin(2 * a + ph[0]) + .07 * math.sin(3 * a + ph[1] + k * .2) + .04 * math.sin(5 * a + ph[2]))
            pts.append((1380 + r * math.cos(a) * 1.25, 250 + r * math.sin(a) * .8))
        rings.append('<path pathLength="1" class="draw" style="--d:%dms" d="%s"/>' % (300 + k * 60, smooth(pts, True)))
    rings.append('</g>')
    p.append(''.join(rings))

    # skyline on the horizon (drawn before the strata so they occlude its base)
    city = skyline(random.Random(71), 840, 1540, horizon + 6)
    p.append('<g class="a-city">' + ''.join(
        '<path pathLength="1" class="draw" style="--d:%dms" d="%s"/>' % (900 + i * 9, d) for i, d in enumerate(city)) + '</g>')

    # the tree rises out of the city
    segs, tips = tree(random.Random(12))
    tg = ['<g class="a-tree">']
    for depth in range(7):
        tg.append('<g class="t%d" style="--d:%dms">' % (depth, 1400 + depth * 230))
        tg += ['<path pathLength="1" class="draw" d="%s"/>' % d for dd, d in segs if dd == depth]
        tg.append('</g>')
    tg.append('</g>')
    p.append(''.join(tg))

    # network across the tips: each tip links to its nearest neighbours
    trng = random.Random(3)
    edges = set()
    for i, a in enumerate(tips):
        near = sorted(range(len(tips)), key=lambda j: (tips[j][0] - a[0]) ** 2 + (tips[j][1] - a[1]) ** 2)[1:3]
        for j in near:
            edges.add(tuple(sorted((i, j))))
    ng = ['<g class="a-net">']
    for i, j in sorted(edges):
        if trng.random() < .55:
            ng.append('<path class="a-edge" d="%s"/>' % poly([tips[i], tips[j]]))
    signal = sorted(range(len(tips)), key=lambda k: trng.random())[:4]
    for k, (x, y) in enumerate(tips):
        cls = 'a-node a-sig' if k in signal else 'a-node'
        ng.append('<circle class="%s" style="--d:%dms" cx="%s" cy="%s" r="%s"/>' % (
            cls, 2900 + (k % 9) * 70, f(x), f(y), '4.2' if k in signal else '2.4'))
    ng.append('</g>')
    p.append(''.join(ng))

    # layered terrain: back to front, each strip filled with paper to occlude
    srng = random.Random(41)
    st = ['<g class="a-strata">']
    n = 15
    for i in range(n):
        y0 = horizon + 4 + i * 24 + i * i * .9
        amp = 18 + i * 5.5
        pts = ridge(srng, y0, amp, n=34, slope=190 - i * 6)
        d = smooth(pts) + ' L%d %d L-20 %d Z' % (W + 20, H + 40, H + 40)
        st.append('<path pathLength="1" class="draw s%d" style="--d:%dms" d="%s"/>' % (i % 3, 200 + i * 70, d))
    st.append('</g>')
    p.append(''.join(st))

    # microscopy lens inset, set into the terrain
    mrng = random.Random(400)
    cx, cy, R = 1395, 812, 118
    m = ['<g class="a-lens">', '<circle class="a-lens-bg" cx="%d" cy="%d" r="%d"/>' % (cx, cy, R)]
    m.append('<g clip-path="url(#atlas-lens)">')
    for k in range(-14, 15):
        m.append('<path class="a-hatch" d="M%d %d l240 -240"/>' % (cx - 120 + k * 16, cy + 120))
    cells = []
    tries = 0
    while len(cells) < 26 and tries < 900:
        tries += 1
        r = mrng.uniform(11, 21)
        x = cx + mrng.uniform(-R, R)
        y = cy + mrng.uniform(-R, R)
        if any((x - a) ** 2 + (y - b) ** 2 < (r + c + 3) ** 2 for a, b, c in cells):
            continue
        cells.append((x, y, r))
    for i, (x, y, r) in enumerate(cells):
        pts = []
        ph = mrng.uniform(0, math.tau)
        for s in range(10):
            a = math.tau * s / 10
            rr = r * (1 + .1 * math.sin(3 * a + ph) + .05 * math.sin(5 * a))
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        m.append('<path class="a-cell" d="%s"/>' % smooth(pts, True))
        nuc = 'a-nuc a-nuc-sig' if i in (4, 17) else 'a-nuc'
        m.append('<circle class="%s" cx="%s" cy="%s" r="%s"/>' % (nuc, f(x + r * .15), f(y - r * .1), f(r * .32)))
    m.append('</g>')
    m.append('<circle class="a-lens-ring" cx="%d" cy="%d" r="%d"/>' % (cx, cy, R))
    m.append('<circle class="a-lens-ring a-thin" cx="%d" cy="%d" r="%d"/>' % (cx, cy, R + 8))
    for a in range(0, 360, 10):
        rad = math.radians(a)
        l = 7 if a % 90 == 0 else 3.5
        m.append('<path class="a-tick" d="%s"/>' % poly([(cx + (R + 8) * math.cos(rad), cy + (R + 8) * math.sin(rad)),
                                                        (cx + (R + 8 + l) * math.cos(rad), cy + (R + 8 + l) * math.sin(rad))]))
    m.append('<path class="a-tick" d="M%d %d h28 M%d %d v-4 M%d %d v-4"/>' % (cx - 14, cy + R - 18, cx - 14, cy + R - 18, cx + 14, cy + R - 18))
    m.append('</g>')
    p.append(''.join(m))

    # annotations: leader lines + mono labels
    tip = max(tips, key=lambda q: q[0] - abs(q[1] - 230))
    ann = [
        # (from, elbow, figure, title, sub)
        ((tip[0], tip[1]), (1360, 130), 'fig. 0.1', 'NETWORK', 'branching → nodes'),
        ((cx - R * .7, cy - R * .7), (1180, 700), 'fig. 0.2', 'FIELD ×400', 'tissue, observed'),
        ((1490, horizon - 30), (1400, 480), 'fig. 0.3', 'STRUCTURE', 'after Bahawalpur'),
        ((980, 790), (1000, 910), 'fig. 0.4', 'STRATA', 'layered terrain'),
    ]
    a = ['<g class="a-ann">']
    for i, ((x0, y0), (x1, y1), fig, title, sub) in enumerate(ann):
        a.append('<g class="a-note" style="--d:%dms">' % (3200 + i * 160))
        a.append('<circle class="a-dot" cx="%s" cy="%s" r="3"/>' % (f(x0), f(y0)))
        a.append('<path class="a-leader" d="%s"/>' % poly([(x0, y0), (x1, y1), (x1 + 26, y1)]))
        a.append('<text class="a-lbl a-faint" x="%s" y="%s">%s</text>' % (f(x1 + 32), f(y1 - 9), fig))
        a.append('<text class="a-lbl" x="%s" y="%s">%s</text>' % (f(x1 + 32), f(y1 + 4), title))
        a.append('<text class="a-lbl a-faint" x="%s" y="%s">%s</text>' % (f(x1 + 32), f(y1 + 17), sub))
        a.append('</g>')
    # scale bar + north arrow, lower left
    a.append('<g class="a-note" style="--d:3900ms">'
             '<path class="a-leader" d="M1190 968 h120 M1190 962 v12 M1250 965 v6 M1310 962 v12"/>'
             '<text class="a-lbl a-faint" x="1186" y="954">0</text>'
             '<text class="a-lbl a-faint" x="1290" y="954">10 KM</text>'
             '<path class="a-leader" d="M1348 974 l10 -30 l10 30 l-10 -9 z"/>'
             '<text class="a-lbl a-faint" x="1354" y="990">N</text></g>')
    a.append('</g>')
    p.append(''.join(a))
    p.append('</svg>')
    PREC[0] = 1
    return '\n'.join(p)


# ═════════════════════════════════════════════════════════════════════════
#  01 · MANIFESTO: observe → disassemble → patterns → build → test → refine
# ═════════════════════════════════════════════════════════════════════════

def process_strip():
    rng = random.Random(5)
    W, H = 1200, 300
    cy = 130
    out = ['<svg class="process" viewBox="0 0 %d %d" aria-hidden="true" focusable="false">' % (W, H)]
    out.append('<path class="pr-axis" pathLength="1" d="M20 %d H1180"/>' % (H - 70))
    names = ['Observe', 'Disassemble', 'Find patterns', 'Build', 'Test', 'Refine']
    for i, nm in enumerate(names):
        x = 20 + i * 200
        out.append('<g class="pr-step" data-step="%d">' % i)
        out.append('<path class="pr-tick" d="M%d %d v10"/>' % (x + 100, H - 75))
        out.append('<text class="pr-num" x="%d" y="%d">0%d</text>' % (x + 100, H - 40, i + 1))
        out.append('<text class="pr-name" x="%d" y="%d">%s</text>' % (x + 100, H - 20, nm))
        out.append('</g>')

    def P(d, cls='pr-line'):
        out.append('<path class="%s" pathLength="1" d="%s"/>' % (cls, d))

    # 1 observe: a tangle inside a lens
    cx = 120
    pts = []
    x, y = cx, cy
    for k in range(34):
        x += rng.uniform(-26, 26)
        y += rng.uniform(-24, 24)
        x = min(max(x, cx - 58), cx + 58)
        y = min(max(y, cy - 58), cy + 58)
        pts.append((x, y))
    P(smooth(pts))
    P('M%d %d m-74 0 a74 74 0 1 0 148 0 a74 74 0 1 0 -148 0' % (cx, cy), 'pr-line pr-faint')
    # 2 disassemble: separate strands, still wavy
    cx = 320
    for k in range(5):
        y0 = cy - 60 + k * 30
        pts = [(cx - 70 + j * 14, y0 + rng.uniform(-9, 9) + (k - 2) * j * .6) for j in range(11)]
        P(smooth(pts))
    # 3 patterns: aligned lines with a repeating mark
    cx = 520
    for k in range(5):
        y0 = cy - 56 + k * 28
        P('M%d %d H%d' % (cx - 72, y0, cx + 72))
        for j in range(5):
            xx = cx - 60 + j * 30
            cls = 'pr-dot pr-sig' if (j + k) % 3 == 0 else 'pr-dot'
            out.append('<circle class="%s" cx="%d" cy="%d" r="%s"/>' % (cls, xx, y0, '3.6' if 'sig' in cls else '2.4'))
    # 4 build: a frame of connected modules
    cx = 720
    boxes = [(-66, -60, 52, 36), (-6, -60, 72, 36), (-66, -14, 132, 40), (-66, 36, 60, 30), (2, 36, 64, 30)]
    for bx, by, bw, bh in boxes:
        P(poly([(cx + bx, cy + by), (cx + bx + bw, cy + by), (cx + bx + bw, cy + by + bh), (cx + bx, cy + by + bh)], True))
    P('M%d %d V%d M%d %d V%d' % (cx - 40, cy - 24, cy - 14, cx + 30, cy - 24, cy - 14), 'pr-line pr-faint')
    # 5 test: the build under a probe, ticks and one mark
    cx = 920
    for bx, by, bw, bh in boxes:
        P(poly([(cx + bx, cy + by), (cx + bx + bw, cy + by), (cx + bx + bw, cy + by + bh), (cx + bx, cy + by + bh)], True), 'pr-line pr-faint')
    P('M%d %d L%d %d' % (cx - 84, cy + 84, cx + 84, cy - 84), 'pr-line pr-probe')
    for (dx, dy) in [(-40, -42), (30, -42), (0, 6), (-36, 51)]:
        P('M%d %d l5 5 l10 -11' % (cx + dx - 7, cy + dy), 'pr-line pr-ok')
    out.append('<circle class="pr-dot pr-warn" cx="%d" cy="%d" r="4.5"/>' % (cx + 34, cy + 51))
    # 6 refine: one clean branching structure
    cx = 1120

    def br(x, y, a, l, d):
        ex, ey = x + l * math.cos(a), y - l * math.sin(a)
        P('M%s %s L%s %s' % (f(x), f(y), f(ex), f(ey)))
        if d == 3:
            out.append('<circle class="pr-dot pr-sig" cx="%s" cy="%s" r="3.2"/>' % (f(ex), f(ey)))
            return
        for s in (-.5, .5):
            br(ex, ey, a + s, l * .72, d + 1)
    br(cx, cy + 74, math.pi / 2, 52, 0)
    out.append('</svg>')
    return '\n'.join(out)


# ═════════════════════════════════════════════════════════════════════════
#  02 · PROJECT PLATES (external, loaded lazily through <img>)
# ═════════════════════════════════════════════════════════════════════════

def meritnama():
    """Candidates ranked by merit → preference flows → a seat grid."""
    rng = random.Random(19)
    W, H = 800, 600
    b = []
    # candidate rows: abstract bars, descending merit
    n = 16
    vals = sorted([rng.uniform(.45, 1) for _ in range(n)], reverse=True)
    ys = []
    for i, v in enumerate(vals):
        y = 92 + i * 27
        ys.append(y)
        b.append('<rect class="p" x="60" y="%d" width="150" height="14" stroke="%s" stroke-width=".6"/>' % (y - 7, INK3))
        b.append('<rect class="%s" x="60" y="%d" width="%s" height="14"/>' % ('f', y - 7, f(150 * v)))
        b.append(label(52, y + 4, '%02d' % (i + 1), 'tl', 'end'))
    b.append(label(60, 64, 'Candidates · by merit', 't'))
    # seat grid: specialties (rows) x hospitals (cols)
    gx, gy, cw, ch = 520, 92, 26, 26
    rows, cols = 9, 8
    seats = {}
    for r in range(rows):
        for c in range(cols):
            if rng.random() < .78:
                seats[(r, c)] = 0
    b.append(label(gx, 64, 'Seats · specialty × hospital', 't'))
    # each candidate flows to a preferred seat; the first free one wins
    order = list(seats.keys())
    for i, y in enumerate(ys):
        prefs = rng.sample(order, 3)
        got = None
        for k, s in enumerate(prefs):
            r, c = s
            tx, ty = gx + c * cw + cw / 2, gy + r * ch + ch / 2
            if got is None and seats[s] == 0:
                got = s
                seats[s] = 2 if i < 3 else 1
                cls = 'l'
                sw = 1.3
            else:
                cls = 'h'
                sw = .6
            b.append('<path class="%s" stroke-width="%s" d="M218 %s C360 %s 400 %s %s %s"%s/>' % (
                cls, sw, f(y), f(y), f(ty), f(tx - cw / 2 - 2), f(ty),
                '' if cls == 'l' else ' stroke-dasharray="2 4"'))
    for (r, c), state in seats.items():
        x, y = gx + c * cw, gy + r * ch
        if state == 2:
            b.append('<rect class="lime" x="%d" y="%d" width="%d" height="%d" stroke="%s" stroke-width="1"/>' % (x + 3, y + 3, cw - 6, ch - 6, FOREST))
        elif state == 1:
            b.append('<rect class="f" x="%d" y="%d" width="%d" height="%d"/>' % (x + 3, y + 3, cw - 6, ch - 6))
        else:
            b.append('<rect class="p" x="%d" y="%d" width="%d" height="%d" stroke="%s" stroke-width=".8"/>' % (x + 3, y + 3, cw - 6, ch - 6, INK3))
    # round ruler along the bottom
    b.append('<path class="l" d="M60 %d H730"/>' % (H - 70))
    for k in range(8):
        x = 60 + k * (670 / 7)
        b.append('<path class="l" d="M%s %d v8"/>' % (f(x), H - 74))
        b.append(label(x, H - 48, 'R%d' % (k + 1), 'tl', 'middle'))
    b.append(label(730, H - 22, 'Schematic · allocation by merit and preference', 'tl', 'end'))
    return svg_file(W, H, '\n'.join(b), 'MeritNama: candidates ranked by merit, flowing through their preferences into a grid of seats')


def nabz():
    """One record, two readers: an English sheet and its Urdu column, under a pulse."""
    rng = random.Random(8)
    W, H = 800, 600
    b = []
    # pulse trace across the top (nabz = pulse)
    pts = []
    x = 40
    while x < 760:
        pts += [(x, 70), (x + 40, 70), (x + 48, 62), (x + 56, 70), (x + 66, 70), (x + 72, 80), (x + 80, 28), (x + 88, 92), (x + 96, 70), (x + 130, 70)]
        x += 130
    b.append('<path class="l" stroke-width="1.4" d="%s"/>' % poly([q for q in pts if q[0] <= 760]))
    # the sheet
    sx, sy, sw, sh = 110, 120, 580, 430
    b.append('<rect class="p" x="%d" y="%d" width="%d" height="%d" stroke="%s" stroke-width="1.1"/>' % (sx, sy, sw, sh, FOREST))
    b.append('<path class="l" stroke-width="2.2" d="M%d %d H%d"/>' % (sx + 30, sy + 56, sx + sw - 30))
    b.append('<rect class="lime" x="%d" y="%d" width="70" height="8"/>' % (sx + 30, sy + 28))
    b.append('<rect class="f" x="%d" y="%d" width="140" height="6" opacity=".5"/>' % (sx + 110, sy + 29))
    secs = ['Complaints', 'Examination', 'Diagnosis', 'Medications']
    y = sy + 92
    mid = sx + sw * .54
    for si, s in enumerate(secs):
        b.append(label(sx + 30, y, s, 't'))
        b.append('<path class="h" d="M%d %d H%d"/>' % (sx + 30, y + 8, sx + sw - 30))
        y += 26
        lines = 1 if si < 3 else 3
        for k in range(lines):
            ln = rng.uniform(.5, .9)
            if si < 3:
                b.append('<rect class="f" x="%d" y="%d" width="%s" height="5" opacity=".75"/>' % (sx + 30, y - 4, f((sw - 60) * ln * .7)))
                y += 22
            else:
                # medication row: english left, urdu right (right-aligned, slanted baseline strokes)
                b.append('<rect class="f" x="%d" y="%d" width="%s" height="6"/>' % (sx + 30, y - 6, f(150 * ln)))
                b.append('<rect class="f" x="%d" y="%d" width="%s" height="4" opacity=".55"/>' % (sx + 30, y + 8, f(200 * ln)))
                b.append('<path class="h" d="M%s %d V%d"/>' % (f(mid), y - 12, y + 26))
                xr = sx + sw - 30
                for w in range(rng.randint(3, 5)):
                    wl = rng.uniform(22, 54)
                    b.append('<path class="l" stroke-width="1.6" d="M%s %s q%s %s %s %s q%s %s %s %s"/>' % (
                        f(xr), f(y + 4), f(-wl * .3), f(-7), f(-wl * .6), f(-2), f(-wl * .2), f(8), f(-wl * .4), f(4)))
                    if rng.random() < .6:
                        b.append('<circle class="f" cx="%s" cy="%s" r="1.6"/>' % (f(xr - wl * .5), f(y + 12)))
                    xr -= wl + 8
                    if xr < mid + 30:
                        break
                # the link between the two columns: one stored object, two readers
                b.append('<circle class="lime" cx="%s" cy="%d" r="5" stroke="%s"/>' % (f(mid), y + 2, FOREST))
                y += 44
        y += 8
    b.append(label(sx + 30, sy + sh + 32, 'EN · clinical record', 'tl'))
    b.append(label(sx + sw - 30, sy + sh + 32, 'UR · patient instructions', 'tl', 'end'))
    return svg_file(W, H, '\n'.join(b), 'Nabz: a prescription sheet with English clinical sections and an Urdu column for each medicine, under a pulse trace')


def antibiome():
    """Culture plate with disc-diffusion zones beside a resistance matrix."""
    rng = random.Random(33)
    W, H = 800, 600
    b = []
    cx, cy, R = 250, 300, 190
    b.append('<circle class="p" cx="%d" cy="%d" r="%d" stroke="%s" stroke-width="1.2"/>' % (cx, cy, R + 10, FOREST))
    b.append('<circle class="l" cx="%d" cy="%d" r="%d"/>' % (cx, cy, R))
    # lawn of colonies
    discs = [(cx + 90 * math.cos(a), cy + 90 * math.sin(a), z) for a, z in
             zip([math.radians(d) for d in (-90, -18, 54, 126, 198)], (58, 22, 44, 14, 66))]
    discs.append((cx, cy, 30))
    for _ in range(700):
        a = rng.uniform(0, math.tau)
        r = R * math.sqrt(rng.random()) * .97
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        if any((x - dx) ** 2 + (y - dy) ** 2 < zr ** 2 for dx, dy, zr in discs):
            continue
        b.append('<circle class="f" cx="%s" cy="%s" r="%s" opacity="%s"/>' % (f(x), f(y), f(rng.uniform(.8, 2.3)), f(rng.uniform(.35, .85))))
    for i, (x, y, zr) in enumerate(discs):
        b.append('<circle class="h" cx="%s" cy="%s" r="%s" stroke-dasharray="3 3"/>' % (f(x), f(y), zr))
        b.append('<circle class="%s" cx="%s" cy="%s" r="9" stroke="%s" stroke-width="1"/>' % (
            'st' if zr < 25 else ('lime' if zr > 55 else 'p'), f(x), f(y), FOREST))
    b.append(label(cx - R, 60, 'Plate · disc diffusion', 't'))
    b.append(label(cx, H - 42, 'zone of inhibition → susceptibility', 'tl', 'middle'))
    # matrix
    mx, my, c = 500, 100, 28
    rows, cols = 10, 9
    b.append(label(mx, 60, 'Antibiogram · %S', 't'))
    for r in range(rows):
        for k in range(cols):
            if rng.random() < .22:
                b.append('<circle class="f" cx="%d" cy="%d" r="1.4" opacity=".5"/>' % (mx + k * c + c / 2, my + r * c + c / 2))
                continue
            s = rng.random()
            x, y = mx + k * c + 2, my + r * c + 2
            if s > .8:
                b.append('<rect class="lime" x="%d" y="%d" width="%d" height="%d"/>' % (x, y, c - 4, c - 4))
            elif s > .45:
                b.append('<rect class="f" x="%d" y="%d" width="%d" height="%d" opacity="%s"/>' % (x, y, c - 4, c - 4, f(.35 + s * .6)))
            elif s > .2:
                b.append('<rect class="p" x="%d" y="%d" width="%d" height="%d" stroke="%s"/>' % (x, y, c - 4, c - 4, FOREST))
            else:
                b.append('<rect class="st" x="%d" y="%d" width="%d" height="%d" opacity=".85"/>' % (x, y, c - 4, c - 4))
    # row trend marks beside the matrix
    for r in range(rows):
        y = my + r * c + c / 2
        v = rng.uniform(.2, 1)
        b.append('<path class="h" d="M%d %s H%d"/>' % (mx + cols * c + 10, f(y), mx + cols * c + 60))
        b.append('<circle class="f" cx="%s" cy="%s" r="3"/>' % (f(mx + cols * c + 10 + 50 * v), f(y)))
    b.append(label(mx, my + rows * c + 40, 'first isolate per patient', 'tl'))
    return svg_file(W, H, '\n'.join(b), 'Antibiome: a culture plate with antibiotic discs and inhibition zones beside a resistance matrix')


def antibiotogram():
    """Organisms × drugs: coverage as sized marks, drug classes joined across rows."""
    rng = random.Random(44)
    W, H = 800, 600
    b = []
    rows, cols = 9, 12
    ox, oy, cw, rh = 150, 110, 50, 46
    classes = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4]
    b.append(label(ox, 64, 'Coverage · organism × agent', 't'))
    for k in range(cols):
        x = ox + k * cw
        b.append('<path class="h" d="M%d %d V%d"/>' % (x, oy - 18, oy + (rows - 1) * rh + 18))
        b.append(label(x, oy - 28, 'D%02d' % (k + 1), 'tl', 'middle'))
    # row labels as short bars (no invented organism names)
    grid = {}
    for r in range(rows):
        y = oy + r * rh
        b.append('<rect class="f" x="40" y="%d" width="%d" height="5" opacity=".7"/>' % (y - 3, rng.randint(40, 80)))
        for k in range(cols):
            v = rng.random()
            grid[(r, k)] = v
    # connect same-class agents with coverage > .55 down the column groups
    for k in range(cols):
        prev = None
        for r in range(rows):
            if grid[(r, k)] > .55:
                p = (ox + k * cw, oy + r * rh)
                if prev and r - prev[2] <= 2:
                    b.append('<path class="l" d="M%s %s L%s %s"/>' % (f(prev[0]), f(prev[1]), f(p[0]), f(p[1])))
                prev = (p[0], p[1], r)
    # class bands along the top
    for c in range(5):
        ks = [k for k in range(cols) if classes[k] == c]
        x0, x1 = ox + ks[0] * cw - 14, ox + ks[-1] * cw + 14
        b.append('<path class="l" d="M%d %d H%d"/>' % (x0, oy - 46, x1))
        b.append('<path class="l" d="M%d %d v6 M%d %d v6"/>' % (x0, oy - 46, x1, oy - 46))
    for (r, k), v in grid.items():
        x, y = ox + k * cw, oy + r * rh
        if v > .82:
            b.append('<circle class="lime" cx="%d" cy="%d" r="11" stroke="%s"/>' % (x, y, FOREST))
        elif v > .55:
            b.append('<circle class="f" cx="%d" cy="%d" r="%s"/>' % (x, y, f(4 + v * 6)))
        elif v > .3:
            b.append('<circle class="p" cx="%d" cy="%d" r="5" stroke="%s"/>' % (x, y, FOREST))
        else:
            b.append('<path class="h" d="M%d %d h8"/>' % (x - 4, y))
    b.append(label(ox, H - 40, '● preferred   ● active   ○ partial   – none', 'tl'))
    return svg_file(W, H, '\n'.join(b), 'Antibiotogram: a susceptibility matrix with coverage marks, linked down each antibiotic class')


def nisbat():
    """A day arc over a household: prayer ticks, the sun's path, a smog band."""
    W, H = 800, 600
    b = []
    cx, cy, R = 400, 430, 300
    b.append('<path class="h" d="M60 %d H740"/>' % cy)
    for k in range(0, 13):
        a = math.pi - math.pi * k / 12
        x0, y0 = cx + R * math.cos(a), cy - R * math.sin(a)
        x1, y1 = cx + (R - (16 if k % 3 == 0 else 8)) * math.cos(a), cy - (R - (16 if k % 3 == 0 else 8)) * math.sin(a)
        b.append('<path class="l" d="M%s %s L%s %s"/>' % (f(x0), f(y0), f(x1), f(y1)))
    b.append('<path class="l" d="M%d %d A%d %d 0 0 1 %d %d"/>' % (cx - R, cy, R, R, cx + R, cy))
    b.append('<path class="h" stroke-dasharray="2 5" d="M%d %d A%d %d 0 0 1 %d %d"/>' % (cx - R + 40, cy, R - 40, R - 40, cx + R - 40, cy))
    # five prayer marks along the inner arc
    for k, frac in enumerate((.04, .48, .66, .97, 1.0)):
        a = math.pi - math.pi * min(frac, .995)
        x, y = cx + (R - 40) * math.cos(a), cy - (R - 40) * math.sin(a)
        b.append('<circle class="%s" cx="%s" cy="%s" r="%s" stroke="%s"/>' % ('lime' if k == 2 else 'p', f(x), f(y), 7 if k == 2 else 5, FOREST))
    # the sun at mid-afternoon
    a = math.pi - math.pi * .6
    sx, sy = cx + R * math.cos(a), cy - R * math.sin(a)
    b.append('<circle class="f" cx="%s" cy="%s" r="14"/>' % (f(sx), f(sy)))
    for k in range(12):
        t = math.tau * k / 12
        b.append('<path class="l" d="M%s %s L%s %s"/>' % (f(sx + 20 * math.cos(t)), f(sy + 20 * math.sin(t)), f(sx + 27 * math.cos(t)), f(sy + 27 * math.sin(t))))
    # house: roofline with a chhatri, a window glow (the TV)
    hx, hw, hh = 300, 200, 110
    b.append('<path class="p" stroke="%s" stroke-width="1.2" d="M%d %d V%d H%d V%d"/>' % (FOREST, hx, cy, cy - hh, hx + hw, cy))
    b.append('<path class="l" d="M%d %d H%d"/>' % (hx - 10, cy - hh, hx + hw + 10))
    for k in range(11):
        x = hx - 6 + k * 21
        b.append('<path class="l" d="M%d %d v-8 h10 v8"/>' % (x, cy - hh))
    b.append('<path class="l" d="M%d %d v-26 h28 v26 M%d %d q14 -26 32 0"/>' % (hx + 150, cy - hh - 8, hx + 148, cy - hh - 34))
    b.append('<rect class="f" x="%d" y="%d" width="74" height="44"/>' % (hx + 28, cy - 80))
    b.append('<rect class="lime" x="%d" y="%d" width="60" height="30"/>' % (hx + 35, cy - 73))
    b.append('<path class="l" d="M%d %d v18" />' % (hx + 65, cy - 36))
    b.append('<path class="l" d="M%d %d V%d Q%d %d %d %d V%d"/>' % (hx + 130, cy, cy - 54, hx + 146, cy - 76, hx + 162, cy - 54, cy))
    # smog band: hatched haze over the horizon
    for k in range(40):
        x = 60 + k * 17
        b.append('<path class="h" d="M%d %d l24 -24"/>' % (x, cy + 60))
    b.append('<path class="h" d="M60 %d H740 M60 %d H740"/>' % (cy + 36, cy + 60))
    b.append(label(60, cy + 92, 'AQI band', 'tl'))
    b.append(label(740, cy + 92, 'Fajr → Isha', 'tl', 'end'))
    b.append(label(60, 70, 'One household · one day', 't'))
    return svg_file(W, H, '\n'.join(b), 'Nisbat: a day arc with prayer times over a household roofline, with a haze band for air quality')


def shaheen():
    """An original falcon (shaheen) in a stoop, built from feather blades, beside a ranking ladder."""
    rng = random.Random(61)
    W, H = 800, 600
    b = []
    # ranking ladder
    for i in range(12):
        y = 120 + i * 34
        v = 1 - i * .06 - rng.uniform(0, .04)
        b.append(label(80, y + 4, '%02d' % (i + 1), 'tl', 'end'))
        b.append('<path class="h" d="M96 %d H380"/>' % y)
        b.append('<rect class="%s" x="96" y="%d" width="%s" height="10"/>' % ('lime' if i == 0 else 'f', y - 5, f(280 * v)))
        if rng.random() < .5:
            up = rng.random() < .65
            b.append('<path class="%s" d="M392 %d l5 %d l5 %d z"/>' % ('f' if up else 'st', y + (3 if up else -3), -8 if up else 8, 8 if up else -8))
    b.append(label(96, 80, 'Ladder · rating', 't'))

    cx, cy = 590, 270
    b.append('<circle class="h" cx="%d" cy="%d" r="176" stroke-dasharray="2 6"/>' % (cx, cy + 20))

    def blade(x0, y0, ang, length, width, cls='p'):
        """A long feather: a narrow quadrilateral with a rounded-off tip and a rachis line."""
        ca, sa = math.cos(ang), math.sin(ang)
        nx, ny = -sa, ca
        tip = (x0 + ca * length, y0 + sa * length)
        p1 = (x0 + nx * width / 2, y0 + ny * width / 2)
        p2 = (tip[0] + nx * width * .18, tip[1] + ny * width * .18)
        p3 = (tip[0] - nx * width * .18, tip[1] - ny * width * .18)
        p4 = (x0 - nx * width / 2, y0 - ny * width / 2)
        b.append('<path class="%s" stroke="%s" stroke-width="1.1" stroke-linejoin="round" d="%s"/>' % (
            cls, FOREST, poly([p1, p2, tip, p3, p4], True)))
        b.append('<path class="h" d="%s"/>' % poly([(x0, y0), (tip[0] - ca * 8, tip[1] - sa * 8)]))

    # wings: primaries fanned from each shoulder, outermost first so inner ones overlap
    for side in (-1, 1):
        sx, sy = cx + side * 16, cy + 6
        for k in range(7):
            a = math.radians(-152 + k * 13) if side < 0 else math.radians(-28 - k * 13)
            length = 172 - k * 15
            blade(sx, sy, a, length, 26 - k * 1.2, 'lime' if k == 0 else 'p')
        # coverts: short broad feathers over the wing root
        for k in range(4):
            a = math.radians(-170 + k * 16) if side < 0 else math.radians(-10 - k * 16)
            blade(sx, sy + 4, a, 70 - k * 6, 30, 'p')
    # tail fan
    for k in range(5):
        a = math.radians(90 + (k - 2) * 9)
        blade(cx, cy + 40, a, 92 - abs(k - 2) * 8, 22, 'p')
    # body and head
    b.append('<path class="p" stroke="%s" stroke-width="1.3" d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z"/>' % (
        FOREST, cx, cy - 56, cx + 30, cy - 30, cx + 26, cy + 30, cx, cy + 70, cx - 26, cy + 30, cx - 30, cy - 30, cx, cy - 56))
    for k in range(5):
        y = cy - 6 + k * 13
        b.append('<path class="h" d="M%d %d q%d 6 %d 0"/>' % (cx - 14 + k * 2, y, 14 - k * 2, 28 - k * 4))
    b.append('<path class="f" d="M%d %d C%d %d %d %d %d %d L%d %d C%d %d %d %d %d %d Z"/>' % (
        cx, cy - 78, cx + 16, cy - 76, cx + 20, cy - 60, cx + 12, cy - 46, cx, cy - 40, cx - 12, cy - 46, cx - 20, cy - 60, cx, cy - 78))
    # hooked beak and the falcon's moustache mark
    b.append('<path class="lime" stroke="%s" d="M%d %d l-5 13 l5 -4 l5 4 z"/>' % (FOREST, cx, cy - 44))
    b.append('<circle class="p" cx="%d" cy="%d" r="3.2"/><circle class="p" cx="%d" cy="%d" r="3.2"/>' % (cx - 7, cy - 62, cx + 7, cy - 62))
    b.append(label(cx, H - 36, 'Original drawing · not the clan crest', 'tl', 'middle'))
    return svg_file(W, H, '\n'.join(b), 'Shaheen: an original line drawing of a falcon with spread wings beside the rungs of a ranking ladder')


def bahawalpur_map():
    """
    A stylised plan of the region, drawn as a system: a braided river, a
    canal that branches into distributaries and square fields, a walled
    city, a palace garden, the railway, and the desert with a fort to the
    south. Not to scale and not traced from any map.
    """
    rng = random.Random(1748)
    W, H = 800, 800
    b = []
    # graticule + edge ticks
    for k in range(0, 801, 100):
        b.append('<path class="h" stroke-dasharray="1 5" d="M%d 0 V800 M0 %d H800"/>' % (k, k))
    for k in range(0, 801, 20):
        t = 8 if k % 100 == 0 else 4
        b.append('<path class="l" stroke-width=".7" d="M%d 0 v%d M%d 800 v-%d M0 %d h%d M800 %d h-%d"/>' % (k, t, k, t, k, t, k, t))
    b.append(label(16, 26, '29.40° N', 'tl'))
    b.append(label(784, 26, '71.68° E', 'tl', 'end'))

    # river: two banks, water hatching between, sandbars
    north = [(-20, 120), (110, 150), (230, 128), (350, 180), (470, 168), (590, 222), (700, 214), (820, 262)]
    south = [(x, y + 34 + 8 * math.sin(x / 70)) for x, y in north]
    b.append('<path class="p" d="%s L%s Z"/>' % (smooth(north), ' L'.join('%s %s' % (f(x), f(y)) for x, y in reversed(south))))
    b.append('<path class="l" stroke-width="1.4" d="%s"/>' % smooth(north))
    b.append('<path class="l" stroke-width="1.4" d="%s"/>' % smooth(south))
    for k in range(60):
        x = -10 + k * 14
        t = x / 820
        yn = 120 + 142 * t + 14 * math.sin(x / 90)
        b.append('<path class="h" d="M%s %s l10 6"/>' % (f(x), f(yn + 12 + rng.uniform(-3, 3))))
    for x, y, w in ((180, 150, 46), (420, 186, 60), (650, 232, 40)):
        b.append('<path class="l" stroke-width=".9" d="M%d %d q%d -7 %d 0 q-%d 7 -%d 0"/>' % (x, y, w / 2, w, w / 2, w))
    b.append(label(24, 112, 'river', 'tl'))

    # main canal parallel to the river, with distributaries branching south
    canal = [(-20, 300), (200, 292), (400, 312), (600, 300), (820, 318)]
    b.append('<path class="l" stroke-width="1.6" d="%s"/>' % smooth(canal))
    b.append('<path class="h" d="%s"/>' % smooth([(x, y + 5) for x, y in canal]))
    b.append(label(24, 288, 'canal', 'tl'))

    def dist(x, y, ang, ln, depth):
        ex, ey = x + ln * math.cos(ang), y + ln * math.sin(ang)
        b.append('<path class="l" stroke-width="%s" d="M%s %s L%s %s"/>' % (f(1.2 - depth * .25), f(x), f(y), f(ex), f(ey)))
        if depth < 2:
            for s in (-.42, .42):
                dist(ex, ey, ang + s + rng.uniform(-.08, .08), ln * .62, depth + 1)
    for x in (70, 250, 560, 730):
        dist(x, 302, math.pi / 2 + rng.uniform(-.15, .15), 92, 0)
    # square fields (murabba) along the distributaries
    for _ in range(120):
        x = rng.uniform(20, 780)
        y = rng.uniform(330, 520)
        if 300 < x < 500 and 350 < y < 520:
            continue
        s = rng.choice((12, 14, 16))
        b.append('<rect class="h" x="%s" y="%s" width="%d" height="%d"/>' % (f(x), f(y), s, s))

    # railway: a line with ties, crossing west-east
    rail = [(-20, 552), (260, 538), (520, 556), (820, 540)]
    b.append('<path class="l" stroke-width="1.2" d="%s"/>' % smooth(rail))
    for k in range(0, 840, 14):
        t = k / 840
        y = 552 - 14 * math.sin(t * math.pi * 2.2)
        b.append('<path class="l" stroke-width=".8" d="M%d %s v8"/>' % (k - 10, f(y - 4)))
    b.append(label(24, 580, 'railway', 'tl'))

    # walled city: an octagon with round bastions, gates, radiating streets
    cx, cy, R = 400, 432, 64
    oct_ = [(cx + R * math.cos(math.radians(22.5 + 45 * i)), cy + R * .86 * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    b.append('<path class="p" stroke="%s" stroke-width="2" d="%s"/>' % (FOREST, poly(oct_, True)))
    for x, y in oct_:
        b.append('<circle class="p" stroke="%s" stroke-width="1.4" cx="%s" cy="%s" r="6"/>' % (FOREST, f(x), f(y)))
    for i in range(8):
        a = math.radians(45 * i)
        x1, y1 = cx + R * .92 * math.cos(a), cy + R * .79 * math.sin(a)
        b.append('<path class="l" d="M%d %d L%s %s"/>' % (cx, cy, f(x1), f(y1)))
        b.append('<rect class="f" x="%s" y="%s" width="7" height="7"/>' % (f(x1 - 3.5), f(y1 - 3.5)))
    for _ in range(70):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(10, R * .78)
        x, y = cx + r * math.cos(a), cy + r * .8 * math.sin(a)
        if min(abs(math.atan2(y - cy, x - cx) - math.radians(45 * i)) for i in range(-4, 5)) < .12:
            continue
        b.append('<rect class="f" x="%s" y="%s" width="4" height="4" opacity=".55"/>' % (f(x), f(y)))
    b.append('<circle class="lime" stroke="%s" stroke-width="1.2" cx="%d" cy="%d" r="8"/>' % (FOREST, cx, cy))
    b.append(label(cx + R + 18, cy - 30, 'walled city', 'tl'))
    # palace in a quartered garden, south-east of the walls
    gx, gy, gs = 520, 470, 56
    b.append('<rect class="p" stroke="%s" stroke-width="1.2" x="%d" y="%d" width="%d" height="%d"/>' % (FOREST, gx, gy, gs, gs))
    b.append('<path class="l" d="M%d %d V%d M%d %d H%d"/>' % (gx + gs / 2, gy, gy + gs, gx, gy + gs / 2, gx + gs))
    b.append('<circle class="f" cx="%d" cy="%d" r="7"/>' % (gx + gs / 2, gy + gs / 2))
    for dx in (12, gs - 12):
        for dy in (12, gs - 12):
            b.append('<circle class="h" cx="%d" cy="%d" r="5"/>' % (gx + dx, gy + dy))
    b.append(label(gx + gs + 10, gy + gs + 4, 'palace garden', 'tl'))

    # desert: barchan dunes as crescents, stipple, and a fort in plan
    for _ in range(26):
        x = rng.uniform(30, 770)
        y = rng.uniform(612, 770)
        s = rng.uniform(14, 30)
        b.append('<path class="l" stroke-width="1" d="M%s %s q%s %s %s 0 q%s %s %s 0"/>' % (
            f(x), f(y), f(s), f(-s * .8), f(s * 2), f(-s), f(-s * .35), f(-s * 2)))
    for _ in range(150):
        x = rng.uniform(0, 800)
        y = rng.uniform(600, 800)
        b.append('<circle class="f" cx="%s" cy="%s" r=".9" opacity=".45"/>' % (f(x), f(y)))
    fx, fy, fs = 610, 664, 70
    b.append('<rect class="p" stroke="%s" stroke-width="1.6" x="%d" y="%d" width="%d" height="%d"/>' % (FOREST, fx, fy, fs, fs))
    for k in range(6):
        t = k / 5
        for x, y in ((fx + fs * t, fy), (fx + fs * t, fy + fs), (fx, fy + fs * t), (fx + fs, fy + fs * t)):
            b.append('<circle class="p" stroke="%s" stroke-width="1.1" cx="%s" cy="%s" r="5"/>' % (FOREST, f(x), f(y)))
    b.append(label(fx + fs / 2, fy + fs + 26, 'fort', 'tl', 'middle'))
    b.append(label(24, 640, 'desert · to the south', 'tl'))

    # compass + scale
    b.append('<path class="l" d="M748 92 l-9 26 l9 -7 l9 7 z"/><path class="f" d="M748 92 l-9 26 l9 -7 z"/>')
    b.append(label(748, 136, 'N', 'tl', 'middle'))
    b.append('<path class="l" d="M24 780 h120 M24 774 v12 M84 777 v6 M144 774 v12"/>')
    b.append(label(152, 784, 'not to scale', 'tl'))
    return svg_file(W, H, '\n'.join(b), 'A stylised plan of the Bahawalpur region: a braided river, a canal branching into distributaries and square fields, a walled city, a palace garden, the railway, and desert dunes with a fort to the south')


def contour_divider():
    """A wide separator: three contour lines and a measured rule."""
    rng = random.Random(2)
    W, H = 1600, 60
    b = []
    for k in range(3):
        pts = [(x, 30 + k * 8 + 6 * math.sin(x / 140 + k) + 3 * math.sin(x / 47 + k * 2)) for x in range(-40, 1680, 40)]
        b.append('<path class="h" d="%s"/>' % smooth(pts))
    for x in range(0, 1601, 80):
        b.append('<path class="l" d="M%d 0 v%d"/>' % (x, 8 if x % 400 == 0 else 4))
    return svg_file(W, H, '\n'.join(b), 'Contour separator')


def chapter_marks():
    """Seven small glyphs, one per chapter, as a single sprite."""
    g = {
        'entering': '<circle cx="12" cy="12" r="9"/><path d="M12 3v18M3 12h18"/>',
        'manifesto': '<path d="M4 16c3-8 5-8 8 0s5 8 8 0"/><path d="M4 20h16"/>',
        'work': '<rect x="4" y="4" width="7" height="7"/><rect x="13" y="4" width="7" height="7"/><rect x="4" y="13" width="7" height="7"/><circle cx="16.5" cy="16.5" r="3.5"/>',
        'method': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="4" r="1.6"/><circle cx="19" cy="16" r="1.6"/><circle cx="5" cy="16" r="1.6"/>',
        'notes': '<path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7M9 15h5"/>',
        'next': '<path d="M12 20V8"/><path d="M12 8l-5 -4M12 8l5 -4M12 13l-4 -3M12 13l4 -3"/>',
        'invitation': '<path d="M3 12h15"/><path d="M13 6l6 6-6 6"/>',
    }
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for k, v in g.items():
        out.append('<symbol id="cm-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">%s</symbol>' % (k, v))
    out.append('</svg>')
    return '\n'.join(out)


# ═════════════════════════════════════════════════════════════════════════

def inject(html, name, content):
    pat = re.compile(r'(<!-- art:%s -->)(.*?)(<!-- /art:%s -->)' % (name, name), re.S)
    if not pat.search(html):
        raise SystemExit('marker <!-- art:%s --> not found in index.html' % name)
    return pat.sub(lambda m: m.group(1) + '\n' + content + '\n' + m.group(3), html)


def main():
    print('Systems Atlas: building artwork')
    write(os.path.join(PRJ, 'meritnama-art.svg'), meritnama())
    write(os.path.join(PRJ, 'nabz-art.svg'), nabz())
    write(os.path.join(PRJ, 'antibiome-art.svg'), antibiome())
    write(os.path.join(PRJ, 'antibiotogram-art.svg'), antibiotogram())
    write(os.path.join(PRJ, 'nisbat-art.svg'), nisbat())
    write(os.path.join(PRJ, 'shaheen-art.svg'), shaheen())
    write(os.path.join(ILL, 'bahawalpur-map.svg'), bahawalpur_map())
    write(os.path.join(ILL, 'contour-divider.svg'), contour_divider())

    hero_svg = hero()
    proc_svg = process_strip()
    marks = chapter_marks()
    # standalone copies, for reuse outside the page
    write(os.path.join(ILL, 'hero-atlas.svg'), hero_svg.replace(
        '<svg class="atlas"', '<svg xmlns="http://www.w3.org/2000/svg" class="atlas"').replace(
        '<defs>', '<style>' + STANDALONE_HERO_CSS + '</style><defs>', 1))
    write(os.path.join(ILL, 'chapter-marks.svg'), marks.replace('<svg ', '<svg xmlns:xlink="http://www.w3.org/1999/xlink" ', 1))

    path = os.path.join(ROOT, 'index.html')
    with open(path, encoding='utf-8') as fh:
        html = fh.read()
    html = inject(html, 'hero', hero_svg)
    html = inject(html, 'process', proc_svg)
    html = inject(html, 'marks', marks)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('  index.html: hero, process and chapter marks injected')


STANDALONE_HERO_CSS = (
    'svg{background:%s}path,circle{fill:none;stroke:%s;stroke-width:1.1;stroke-linecap:round;stroke-linejoin:round}'
    '.a-grid{stroke:%s;stroke-width:.4;opacity:.35}.a-grid-major{stroke:%s;stroke-width:.6;opacity:.5}'
    '.a-strata path{fill:%s}.a-contour path{opacity:.35}.a-edge{stroke-dasharray:2 4;opacity:.6}'
    '.a-node{fill:%s;stroke:none}.a-sig{fill:%s;stroke:%s}.a-lens-bg{fill:%s}.a-hatch{opacity:.2}'
    '.a-nuc{fill:%s;stroke:none}.a-nuc-sig{fill:%s}.a-dot{fill:%s;stroke:none}'
    'text{font:500 11px %s;letter-spacing:.14em;fill:%s}.a-faint{fill:%s}'
) % (PAPER, FOREST, INK3, INK3, PAPER, FOREST, LIME, FOREST, PAPER, FOREST, LIME, FOREST, MONO, INK, INK3)


if __name__ == '__main__':
    main()
