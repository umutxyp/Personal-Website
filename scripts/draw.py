#!/usr/bin/env python3
"""Draws the site's pictures: one small world for every theme, in ink.

Every theme (a fox by the sea, a cat in the ivy, a lion on the savanna, …) gets the same set
of pictures, drawn once in dark ink for the light mode and once in pale ink for the dark one:

    public/scenes/<theme>/<mode>/land.svg      the wide land under the name
    public/scenes/<theme>/<mode>/sky-a.svg     the sky to the left of the name (sky-b: to the right)
    public/scenes/<theme>/<mode>/sleeper.svg   the animal asleep, for the top of a frame
    public/scenes/<theme>/<mode>/plants-N.svg  what grows along the top of a card
    public/scenes/<theme>/<mode>/line-N.svg    the line that runs off a heading
    public/scenes/<theme>/<mode>/ground.svg    the strip above the footer

and the colours of each theme as CSS variables in src/app/themes.css, so the pictures and the
page always agree. Nothing here needs installing:  python3 scripts/draw.py
"""
import json
import math
import os
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREVIEW_T = float(os.environ.get("PREVIEW_T", 0))          # PREVIEW_T=9 writes the pictures as they are 9 s in
OUT = Path(os.environ["PREVIEW_DIR"]) if PREVIEW_T else ROOT / "public" / "scenes"

# ───────────────────────────── THEMES ───────────────────────────────
# id, name, what the animal is, and the colours. `bg` is the page, `ink` the lines and text,
# `leaf` what grows, `accent` links and underlines, `warm` the one colour that stands out,
# `wash`/`deep` the ground, `fur…` the animal.

THEMES = {
    "fox": dict(
        name="Fox by the sea", plant="blade", extra="bubbles",
        light=dict(bg="#fbfdff", card="#ffffff", ink="#14273d", soft="#4d6379", leaf=["#86cfe0", "#4fa9cc", "#b5e2ee"],
                   accent="#2188e0", warm="#ff8559", marker="#bfe2ff", wash="#d6ecfa", deep="#bcdcf2",
                   fur="#4aa8f2", fur2="#2c7fd6", belly="#f6fbff", paper="#ffffff", dark="#14273d", glow="#ffd66e"),
        dark=dict(bg="#0c141d", card="#101b27", ink="#e4eef8", soft="#9db1c6", leaf=["#2f86b3", "#51aad6", "#1f6790"],
                  accent="#47b8f5", warm="#ff9770", marker="#1d5c8f", wash="#10283c", deep="#15344e",
                  fur="#3f9ff0", fur2="#2a78cf", belly="#eaf4ff", paper="#1b3a55", dark="#0b1826", glow="#ffe08f"),
    ),
    "cat": dict(
        name="Cat in the ivy", plant="ivy", extra="berries",
        light=dict(bg="#fcfdf8", card="#ffffff", ink="#1f2a24", soft="#51605a", leaf=["#8fc79c", "#63a97a", "#b7dcab"],
                   accent="#2f8f5b", warm="#d4572f", marker="#ffe38a", wash="#e6f2df", deep="#d3e8c9",
                   fur="#f3b888", fur2="#e39a62", belly="#fff3e6", paper="#ffffff", dark="#1f2a24", glow="#ffdc7a"),
        dark=dict(bg="#0e1512", card="#131c18", ink="#ece8da", soft="#a9ad9f", leaf=["#4f9c69", "#6fbf86", "#3b7a52"],
                  accent="#7fd39b", warm="#ff8f63", marker="#5a4a12", wash="#16241c", deep="#1c2f24",
                  fur="#c97a45", fur2="#a55f30", belly="#f1dcc6", paper="#1c2a23", dark="#14110f"),
    ),
    "lion": dict(
        name="Lion on the savanna", plant="grass", extra="seeds",
        light=dict(bg="#fffbf2", card="#ffffff", ink="#3a2a14", soft="#75624a", leaf=["#e3c46a", "#c9a23f", "#efdc9c"],
                   accent="#c07a16", warm="#e2572b", marker="#ffe08a", wash="#f8ebc8", deep="#f0dba6",
                   fur="#efbf62", fur2="#b9702a", belly="#fff1cf", paper="#ffffff", dark="#3a2a14", glow="#ffd36a"),
        dark=dict(bg="#17130c", card="#1e1910", ink="#f4ead6", soft="#b9aa8e", leaf=["#a8842c", "#cfa646", "#7d6220"],
                  accent="#f0b545", warm="#ff8a5c", marker="#5c4410", wash="#261f10", deep="#322814",
                  fur="#d9a548", fur2="#9a5b22", belly="#f3deb0", paper="#2a2214", dark="#120e08", glow="#f2c14e"),
    ),
    "owl": dict(
        name="Owl at night", plant="round", extra="stars",
        light=dict(bg="#faf9ff", card="#ffffff", ink="#241f47", soft="#5c5780", leaf=["#b4a8ec", "#8d7fd8", "#d6cff7"],
                   accent="#6a55d6", warm="#f2a23a", marker="#e2dcff", wash="#e9e5fb", deep="#d9d3f6",
                   fur="#9a8adf", fur2="#6f5fc0", belly="#f3efff", paper="#ffffff", dark="#241f47"),
        dark=dict(bg="#0f0e1c", card="#151428", ink="#ebe8fb", soft="#a9a5c9", leaf=["#5a4fae", "#7d70d6", "#40377f"],
                  accent="#a99bff", warm="#ffc15e", marker="#3a3180", wash="#19173a", deep="#211e4a",
                  fur="#8777d6", fur2="#5d4fb0", belly="#e9e4ff", paper="#211e45", dark="#0b0a17", glow="#dcd6ff"),
    ),
    "bear": dict(
        name="Bear in the forest", plant="fern", extra="berries",
        light=dict(bg="#fbfcf6", card="#ffffff", ink="#26301f", soft="#5a654f", leaf=["#7fb069", "#4f8a45", "#b6d59c"],
                   accent="#3c7d3a", warm="#c9532c", marker="#d9eebd", wash="#e2eed3", deep="#cfe2ba",
                   fur="#b07a4d", fur2="#845631", belly="#ecd3b2", paper="#ffffff", dark="#26301f", glow="#ffe08a"),
        dark=dict(bg="#0f1410", card="#151c16", ink="#e9edd9", soft="#a7b097", leaf=["#3f7a3c", "#5fa055", "#2c5a2c"],
                  accent="#86c96e", warm="#ff8c5a", marker="#2c4a22", wash="#17251a", deep="#1d3021",
                  fur="#9a6a42", fur2="#6f4827", belly="#dcc09a", paper="#1d2a1f", dark="#0b0f0b", glow="#f6d57a"),
    ),
    "penguin": dict(
        name="Penguin in the snow", plant="twig", extra="snow",
        light=dict(bg="#f8fcff", card="#ffffff", ink="#1b2e3c", soft="#55707f", leaf=["#bfe6f2", "#8fd0e6", "#e2f5fb"],
                   accent="#1697b7", warm="#ff9a3d", marker="#cdeefa", wash="#e6f5fb", deep="#d2ecf6",
                   fur="#2a3f52", fur2="#1b2e3c", belly="#ffffff", paper="#ffffff", dark="#1b2e3c"),
        dark=dict(bg="#0b1418", card="#101c22", ink="#e3f2f8", soft="#9bb6c2", leaf=["#2c6f86", "#4a9db8", "#1d5568"],
                  accent="#5fd0ea", warm="#ffb056", marker="#17505f", wash="#122730", deep="#17333f",
                  fur="#3c5870", fur2="#27405a", belly="#f1f9fc", paper="#17303a", dark="#081014"),
    ),
    "tortoise": dict(
        name="Tortoise in the desert", plant="succulent", extra="flowers",
        light=dict(bg="#fffaf3", card="#ffffff", ink="#3b2a1f", soft="#7a6455", leaf=["#9cc7a0", "#6fa57a", "#c4dfc0"],
                   accent="#c8642f", warm="#e8473a", marker="#ffd9ad", wash="#f9e6c9", deep="#f2d5ac",
                   fur="#8fae6b", fur2="#5f7f47", belly="#d9c28f", paper="#ffffff", dark="#3b2a1f", glow="#ffcf7a"),
        dark=dict(bg="#17120e", card="#1f1812", ink="#f4e7d8", soft="#bba794", leaf=["#4c8a5a", "#6dae76", "#356543"],
                  accent="#f0915a", warm="#ff7466", marker="#5c3a18", wash="#281d13", deep="#352617",
                  fur="#7d9a5c", fur2="#566f3f", belly="#cdb47e", paper="#2a2016", dark="#120d09", glow="#f4b86a"),
    ),
}
DEFAULT_THEME = "fox"

# ───────────────────────────── GEOMETRY ─────────────────────────────


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def smooth(points, closed=False):
    """A smooth path through the points (Catmull-Rom as cubic Béziers)."""
    n = len(points)
    get = (lambda i: points[i % n]) if closed else (lambda i: points[max(0, min(n - 1, i))])
    d = [f"M{f(points[0][0])} {f(points[0][1])}"]
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        d.append(f"C{f(p1[0] + (p2[0] - p0[0]) / 6)} {f(p1[1] + (p2[1] - p0[1]) / 6)} "
                 f"{f(p2[0] - (p3[0] - p1[0]) / 6)} {f(p2[1] - (p3[1] - p1[1]) / 6)} {f(p2[0])} {f(p2[1])}")
    return "".join(d) + ("Z" if closed else "")


def sample(points, step=5.0):
    n, out = len(points), [points[0]]
    for i in range(n - 1):
        p0, p1, p2, p3 = points[max(0, i - 1)], points[i], points[i + 1], points[min(n - 1, i + 2)]
        seg = max(2, int(math.dist(p1, p2) / step))
        for k in range(1, seg + 1):
            t = k / seg
            out.append(tuple(0.5 * (2 * p1[a] + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t ** 3) for a in (0, 1)))
    return out


def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def hand_line(rng, a, b, wobble=1.5, step=44):
    """A straight line as a hand would draw it: nearly straight."""
    dist = math.dist(a, b)
    n = max(2, int(dist / step))
    nx, ny = -(b[1] - a[1]) / dist, (b[0] - a[0]) / dist
    bow = rng.uniform(-1, 1) * wobble * 1.4
    return [(a[0] + (b[0] - a[0]) * i / n + nx * ((rng.uniform(-wobble, wobble) if 0 < i < n else 0) + bow * math.sin(math.pi * i / n)),
             a[1] + (b[1] - a[1]) * i / n + ny * ((rng.uniform(-wobble, wobble) if 0 < i < n else 0) + bow * math.sin(math.pi * i / n)))
            for i in range(n + 1)]


def wave(rng, x0, x1, y, amp=6.0, span=110.0, rough=1.2):
    """A sea line, a dune, a row of hills: gentle crests, never quite the same twice."""
    pts, x, up = [], x0, rng.choice((-1, 1))
    while x < x1:
        pts.append((x, y + up * amp * rng.uniform(.7, 1.15) + rng.uniform(-rough, rough)))
        x += span / 2 * rng.uniform(.82, 1.2)
        up = -up
    pts.append((x1, y + up * amp * .6))
    return pts


def mix(a, b, t):
    """Colour a with a share t of colour b: how something looks through that much air."""
    ca, cb = (int(a[i:i + 2], 16) for i in (1, 3, 5)), (int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def circle_path(cx, cy, r, rng=None, n=10, rough=.06):
    pts = []
    for k in range(n):
        a = k * 2 * math.pi / n
        rr = r * (1 + (rng.uniform(-rough, rough) if rng else 0))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return smooth(pts, closed=True)

# ─────────────────────────────── INK ────────────────────────────────

STYLE = """
.d{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;opacity:0;animation:d 1s linear forwards}
@keyframes d{0%{stroke-dashoffset:1;opacity:1}100%{stroke-dashoffset:0;opacity:1}}
.s{fill:none;stroke-linecap:round;stroke-linejoin:round}
.lf{transform:scale(0);animation:lf .9s cubic-bezier(.34,1.56,.64,1) forwards}
@keyframes lf{to{transform:scale(1)}}
.sw{animation:sw 4s ease-in-out infinite alternate}
@keyframes sw{from{transform:rotate(-6deg)}to{transform:rotate(6deg)}}
.bb{opacity:0;animation:bb 4s ease-in infinite}
@keyframes bb{0%{opacity:0;transform:translateY(8px) scale(.6)}18%{opacity:1}80%{opacity:.9}100%{opacity:0;transform:translateY(-30px) scale(1.05)}}
.fall{opacity:0;animation:fall 7s linear infinite}
@keyframes fall{0%{opacity:0;transform:translate(0,-20px)}12%{opacity:1}88%{opacity:1}100%{opacity:0;transform:translate(26px,150px)}}
.tw{animation:tw 2.6s ease-in-out infinite alternate}
@keyframes tw{from{opacity:.25;transform:scale(.7)}to{opacity:1;transform:scale(1.1)}}
.bob{animation:bob 3.4s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(1.5px) rotate(-3.5deg)}to{transform:translateY(-3.5px) rotate(3deg)}}
.wv{animation:wv 7s ease-in-out infinite alternate}
@keyframes wv{from{transform:translateX(-14px)}to{transform:translateX(14px)}}
.cl{animation:cl 11s ease-in-out infinite alternate}
@keyframes cl{from{transform:translateX(-10px)}to{transform:translateX(16px)}}
.br{animation:br 2.8s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1,1)}to{transform:scale(1.012,1.045)}}
.tl{animation:tl 3.4s ease-in-out infinite alternate}
@keyframes tl{from{transform:rotate(-7deg)}to{transform:rotate(6deg)}}
.zz{opacity:0;animation:zz 3.9s ease-in-out infinite}
@keyframes zz{0%{opacity:0;transform:translate(3px,7px)}35%{opacity:.85}100%{opacity:0;transform:translate(-9px,-17px)}}
.spin{animation:spin 60s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.fly{animation:fly 9s ease-in-out infinite alternate}
@keyframes fly{from{transform:translate(-8px,3px)}to{transform:translate(10px,-5px)}}
.glow{animation:glow 3.2s ease-in-out infinite alternate}
@keyframes glow{from{opacity:.55}to{opacity:1}}
.blink{transform-box:fill-box;transform-origin:center;animation:blink 5.5s infinite}
@keyframes blink{0%,91%,100%{transform:scaleY(1)}95%{transform:scaleY(.08)}}
.swing{animation:swing 3.6s ease-in-out infinite alternate}
@keyframes swing{from{transform:rotate(-9deg)}to{transform:rotate(9deg)}}
.i{opacity:0;animation:i .7s ease forwards}
@keyframes i{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.d{stroke-dashoffset:0;opacity:1}.lf{transform:none}.i{opacity:1}.zz{opacity:.7}.bb{opacity:.85}.fall{opacity:.8}}
"""


class Ink:
    """One picture being drawn, in one theme and mode."""

    def __init__(self, w, h, theme, mode, seed):
        self.w, self.h, self.theme, self.mode = w, h, theme, mode
        self.t, self.p = THEMES[theme], THEMES[theme][mode]
        self.rng = random.Random(seed)
        self.body, self.defs = [], []

    def add(self, s):
        self.body.append(s)

    def gradient(self, stops, x1=0, y1=0, x2=0, y2=1, radial=False):
        """A colour running into another: stops are (offset, colour, opacity). Returns what to fill with."""
        i = f"g{len(self.defs)}"
        inner = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
        self.defs.append(f'<radialGradient id="{i}">{inner}</radialGradient>' if radial else
                         f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{inner}</linearGradient>')
        return f"url(#{i})"

    def line(self, d, at=0.0, dur=0.8, width=2.4, color=None, opacity=None):
        op = f' stroke-opacity="{opacity}"' if opacity else ""
        return (f'<path class="d" pathLength="1" d="{d}" stroke="{color or self.p["ink"]}" stroke-width="{width}"{op} '
                f'style="animation-delay:{at:.2f}s;animation-duration:{dur:.2f}s"/>')

    def stroke(self, d, at=0.0, dur=0.8, width=2.4, color=None, opacity=None):
        self.add(self.line(d, at, dur, width, color, opacity))

    def fill(self, d, color, at=0.0, opacity=None):
        op = f' fill-opacity="{opacity}"' if opacity else ""
        self.add(f'<path class="i" d="{d}" fill="{color}"{op} style="animation-delay:{at:.2f}s"/>')

    def shape(self, d, color, at=0.0, width=2.3, dur=.9, opacity=None):
        """A filled shape with its outline drawn round it."""
        self.fill(d, color, at + .15, opacity)
        self.stroke(d, at, dur, width)

    def pop(self, x, y, inner, at, rot=0.0, sway=None):
        """Something that pops up at (x, y); `sway` is how long one sway takes, if it sways."""
        sw = (f'<g class="sw" style="animation-duration:{sway:.1f}s;animation-delay:-{self.rng.uniform(0, 5):.1f}s">{inner}</g>' if sway else inner)
        self.add(f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)})"><g class="lf" style="animation-delay:{at:.2f}s">{sw}</g></g>')

    # ── what grows ──

    def leaf(self, size, kind=None):
        """A leaf pointing along +x from the origin: (outline, veins)."""
        rng, kind = self.rng, kind or self.t["plant"]
        if kind == "ivy":
            j = lambda v: v + rng.uniform(-.035, .035)
            lean = rng.uniform(.88, 1.1)
            half = [(.10, 0), (j(-.07), j(-.36)), (j(.27), j(-.31)), (j(.47), j(-.58)), (j(.66), j(-.27)), (1.0, 0)]
            pts = [(x * size, y * size) for x, y in half + [(x, -y * lean) for x, y in reversed(half[1:-1])]]
            cx = .42 * size
            d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
            for a, b in zip(pts, pts[1:] + pts[:1]):
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                k = .11 * size / (math.hypot(mx - cx, my) or 1)
                d.append(f"Q{f(mx + (mx - cx) * k)} {f(my + my * k)} {f(b[0])} {f(b[1])}")
            veins = f"M{f(.12 * size)} 0L{f(.84 * size)} 0"
            for i, k, root in ((1, .62, .2), (3, .68, .34), (len(pts) - 1, .62, .2), (len(pts) - 3, .68, .34)):
                veins += f"M{f(root * size)} 0L{f(cx + (pts[i][0] - cx) * k)} {f(pts[i][1] * k)}"
            return "".join(d) + "Z", veins
        if kind == "grass":                          # long and thin, a little bent
            w, bend = rng.uniform(.06, .1) * size, rng.uniform(-.22, .22) * size
            return (f"M0 {f(-w)}Q{f(size * .5)} {f(-w + bend * .5)} {f(size)} {f(bend)}Q{f(size * .5)} {f(w + bend * .5)} 0 {f(w)}Z", "")
        if kind == "round":
            w = rng.uniform(.3, .38) * size
            return (f"M0 0C{f(size * .2)} {f(-w)} {f(size * .8)} {f(-w)} {f(size)} 0C{f(size * .8)} {f(w)} {f(size * .2)} {f(w)} 0 0Z",
                    f"M{f(size * .08)} 0L{f(size * .86)} 0")
        if kind == "fern":                           # a frond: a spine with small leaflets
            d, n = "", 5
            for k in range(n):
                x = size * (.14 + .17 * k)
                l = size * (.3 - .04 * k)
                d += f"M{f(x)} 0Q{f(x + l * .5)} {f(-l * .9)} {f(x + l * .9)} {f(-l * .55)}Q{f(x + l * .5)} {f(-l * .2)} {f(x)} 0Z"
                d += f"M{f(x)} 0Q{f(x + l * .5)} {f(l * .9)} {f(x + l * .9)} {f(l * .55)}Q{f(x + l * .5)} {f(l * .2)} {f(x)} 0Z"
            return d, f"M0 0L{f(size)} 0"
        if kind == "twig":                           # a bare twig with a fork, snow sits on it
            return (f"M0 -1.4L{f(size)} -.6L{f(size)} .6L0 1.4Z", f"M{f(size * .45)} 0L{f(size * .78)} {f(-size * .3)}M{f(size * .6)} 0L{f(size * .9)} {f(size * .26)}")
        if kind == "succulent":                      # fat and rounded
            w = rng.uniform(.26, .34) * size
            return (f"M0 0C{f(size * .1)} {f(-w * 1.2)} {f(size * .9)} {f(-w * 1.1)} {f(size)} 0C{f(size * .9)} {f(w * 1.1)} {f(size * .1)} {f(w * 1.2)} 0 0Z",
                    f"M{f(size * .2)} 0L{f(size * .8)} 0")
        w, bend = rng.uniform(.17, .27) * size, rng.uniform(-.14, .14) * size      # blade: sea grass
        return (f"M0 0C{f(size * .2)} {f(-w * 1.15)} {f(size * .62)} {f(-w * .9 + bend)} {f(size)} {f(bend)}"
                f"C{f(size * .66)} {f(w * .75 + bend)} {f(size * .24)} {f(w * 1.05)} 0 0Z",
                f"M{f(size * .06)} 0Q{f(size * .5)} {f(bend * .45)} {f(size * .86)} {f(bend * .9)}")

    def extra(self, x, y, at, n=2):
        """The small things of a theme: bubbles rise, berries hang, stars twinkle, snow falls, seeds drift."""
        rng, p, kind = self.rng, self.p, self.t["extra"]
        out = []
        for _ in range(n):
            bx, by, r = x + rng.uniform(-10, 10), y + rng.uniform(-7, 7), rng.uniform(2.6, 5)
            delay = at + rng.uniform(0, 3.5)
            if kind == "bubbles":
                out.append(f'<g transform="translate({f(bx)} {f(by)})"><g class="bb" style="animation-duration:{rng.uniform(3.2, 5.6):.1f}s;animation-delay:{delay:.2f}s">'
                           f'<circle r="{f(r)}" fill="{p["belly"]}" fill-opacity=".55" stroke="{p["ink"]}" stroke-width="1.4"/></g></g>')
            elif kind == "snow":
                out.append(f'<g transform="translate({f(bx)} {f(by - 30)})"><g class="fall" style="animation-duration:{rng.uniform(5, 9):.1f}s;animation-delay:{delay:.2f}s">'
                           f'<circle r="{f(r * .6)}" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="1.1"/></g></g>')
            elif kind == "stars":
                s = r * 1.5
                out.append(f'<g transform="translate({f(bx)} {f(by)})"><g class="i" style="animation-delay:{at:.2f}s"><g class="tw" style="animation-duration:{rng.uniform(1.8, 3.4):.1f}s;animation-delay:-{rng.uniform(0, 3):.1f}s">'
                           f'<path d="M0 {f(-s)}Q0 0 {f(s)} 0Q0 0 0 {f(s)}Q0 0 {f(-s)} 0Q0 0 0 {f(-s)}Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1" stroke-linejoin="round"/></g></g></g>')
            elif kind == "berries":
                out.append(f'<g transform="translate({f(bx)} {f(by)})"><g class="lf" style="animation-delay:{at + .2:.2f}s">'
                           f'<circle r="{f(r * .9)}" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.5"/></g></g>')
            elif kind == "flowers":
                petals = "".join(f'<circle cx="{f(math.cos(a) * r * .9)}" cy="{f(math.sin(a) * r * .9)}" r="{f(r * .62)}" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.1"/>'
                                 for a in (k * 1.2566 for k in range(5)))
                out.append(f'<g transform="translate({f(bx)} {f(by)})"><g class="lf" style="animation-delay:{at + .2:.2f}s">{petals}'
                           f'<circle r="{f(r * .45)}" fill="{p["marker"]}" stroke="{p["ink"]}" stroke-width="1"/></g></g>')
            else:                                    # seeds drifting off the grass
                out.append(f'<g transform="translate({f(bx)} {f(by)})"><g class="bb" style="animation-duration:{rng.uniform(4, 7):.1f}s;animation-delay:{delay:.2f}s">'
                           f'<path class="s" d="M0 0l0 -6M-3 -7l3 1l3 -1M-2 -9.5l2 3.5l2 -3.5" stroke="{p["ink"]}" stroke-width="1.1"/></g></g>')
        self.add("".join(out))

    def vine(self, guide, at=0.0, speed=300, leaf=30, gap=(46, 70), sway=6.0, side=1, both=True, curl=1, width=2.6,
             lean=(48, 78), taper=.55, first=26, extra=0.0, kind=None, stalk=0.0):
        """Something that grows along `guide`, a leaf at a time. Returns the stem's path and when it has grown."""
        rng, p = self.rng, self.p
        pts = sample(guide, 5)
        total = length(pts)
        wavel, ph1, ph2 = rng.uniform(150, 200), rng.uniform(0, 6.28), rng.uniform(0, 6.28)
        out, s = [], 0.0
        for i, pt in enumerate(pts):
            a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            n = math.hypot(tx, ty) or 1
            if i:
                s += math.dist(pts[i - 1], pt)
            env = min(1, s / 40) * min(1, (total - s) / 30 + .3)
            off = (math.sin(s / wavel * 6.283 + ph1) * sway + math.sin(s / (wavel * .37) * 6.283 + ph2) * sway * .22) * env
            out.append((pt[0] - ty / n * off, pt[1] + tx / n * off, s, math.atan2(ty, tx)))
        if curl:
            x, y, s, ang = out[-1]
            for k in range(26):
                ang += curl * (0.13 + 0.017 * k)
                st = 5.2 * (1 - k / 34)
                x, y, s = x + math.cos(ang) * st, y + math.sin(ang) * st, s + st
                out.append((x, y, s, ang))
        full = out[-1][2]
        stem = smooth([(q[0], q[1]) for q in out[::3]] + [(out[-1][0], out[-1][1])])
        self.stroke(stem, at, full / speed, width)
        nxt, flip, i = first, side, 0
        while i < len(out):
            x, y, s, ang = out[i]
            if nxt <= s < total - 10:
                k = 1 - (1 - taper) * max(0, (s - total * .55) / (total * .45))
                size = leaf * rng.uniform(.8, 1.2) * k
                turn = ang + flip * math.radians(rng.uniform(*lean))
                outline, veins = self.leaf(size, kind)
                st = size * stalk * rng.uniform(.7, 1.2)
                inner = ((f'<path class="s" d="M0 0L{f(st)} 0" stroke="{p["ink"]}" stroke-width="{f(width * .8)}"/>' if st else "")
                         + f'<g transform="translate({f(st)} 0)"><path d="{outline}" fill="{rng.choice(p["leaf"])}" transform="translate({f(size * .05)} {f(size * .06)})"/>'
                         f'<path class="s" d="{outline}" stroke="{p["ink"]}" stroke-width="{f(width * .8)}"/>'
                         + (f'<path class="s" d="{veins}" stroke="{p["ink"]}" stroke-width="1.1" stroke-opacity=".65"/>' if veins else "") + "</g>")
                self.pop(x, y, inner, at + s / speed + .05, math.degrees(turn), rng.uniform(3.2, 6.4))
                if extra and rng.random() < extra and s > 40:
                    self.extra(x + math.cos(turn) * size * .9, y + math.sin(turn) * size * .9 - 6, at + s / speed + .6, rng.choice((1, 2)))
                nxt = s + rng.uniform(*gap) * (.75 + .25 * k)
                if both:
                    flip = -flip
            i += 1
        return stem, at + full / speed

    def render(self):
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ""
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" fill="none">'
               f'<style>{STYLE.strip()}</style>{defs}{"".join(self.body)}</svg>\n')
        if PREVIEW_T:
            svg = re.sub(r"animation-delay:(-?[\d.]+)s", lambda m: f"animation-delay:{float(m.group(1)) - PREVIEW_T:.2f}s", svg)
            svg = re.sub(r'begin="([\d.]+)s"', lambda m: f'begin="{float(m.group(1)) - PREVIEW_T:.2f}s"', svg)
        return svg


def draw(name, w, h, seed, fn):
    """Draws one picture for every theme and mode with the same hand (the same seed)."""
    for theme in THEMES:
        for mode in ("light", "dark"):
            ink = Ink(w, h, theme, mode, seed + sum(ord(c) for c in theme))
            fn(ink)
            path = OUT / theme / mode / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(ink.render(), encoding="utf-8")
    print(f"  ✓ {name}")

# ───────────────────────────── THE ANIMALS ──────────────────────────
# Each is drawn sitting on a line (y = 0), about a hundred wide, awake or asleep.


def zzz(ink, x, y, at):
    p = ink.p
    return "".join(
        f'<g transform="translate({x - k * 14} {y - k * 13}) scale({1 + k * .22})"><path class="zz s" d="M0 0h8l-8 9h8" stroke="{p["soft"]}" stroke-width="2" '
        f'style="animation-delay:{at + 1.2 + k * 1.3:.2f}s"/></g>' for k in range(3))


def eyes(p, pts, asleep, r=2.4, w=2):
    if asleep:
        return f'<path class="s" d="{"".join(f"M{f(x - 3.6)} {f(y)}q3.6 3.8 7.2 0" for x, y in pts)}" stroke="{p["dark"]}" stroke-width="{w}"/>'
    return "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{p["dark"]}"/>' for x, y in pts)


def fox_head(p, asleep=False, w=2.3):
    """The fox of the mark: a diamond of a face under two tall ears."""
    return (
        f'<path d="M-21 -13L-25 -43L-5 -19ZM21 -13L25 -43L5 -19Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
        f'<path d="M-19 -19L-21.5 -35L-10 -21ZM19 -19L21.5 -35L10 -21Z" fill="{p["fur2"]}"/>'
        f'<path d="M-27 -2L-15 -19L15 -19L27 -2L0 23Z" fill="{p["fur"]}"/>'
        f'<path d="M-25.5 -1.5L-8 5L0 -2L8 5L25.5 -1.5L0 21.5Z" fill="{p["belly"]}"/>'
        f'<path class="s" d="M-27 -2L-15 -19L15 -19L27 -2L0 23Z" stroke="{p["ink"]}" stroke-width="{w}"/>'
        + eyes(p, [(-10.4, -5), (10.4, -5)], asleep, 2.5)
        + f'<path d="M-3.2 17.2L3.2 17.2L0 21.2Z" fill="{p["dark"]}" stroke="{p["dark"]}" stroke-width="1.4" stroke-linejoin="round"/>')


def fox(ink, asleep):
    p, w = ink.p, 2.5
    body = "M-42 1C-50 -26 -30 -43 -2 -43C28 -43 50 -27 48 1Z"
    tail = "M44 -13C62 -9 62 6 40 4C14 2 -8 5 -26 -1C-14 -17 12 -21 30 -18C37 -17 41 -17 44 -13Z"
    tip = "M-26 -1C-18 -11 -8 -15 2 -17.5L5 2.6C-6 2.6 -17 2 -26 -1Z"
    return (f'<g class="br"><path d="{body}" fill="{p["fur"]}"/><path class="s" d="M6 -43q3 7 1 13M20 -41q3 6 1 12" stroke="{p["fur2"]}" stroke-width="4"/>'
            f'<path class="s" d="{body}" stroke="{p["ink"]}" stroke-width="{w}"/></g>'
            f'<g class="tl"><path d="{tail}" fill="{p["fur"]}"/><path d="{tip}" fill="{p["belly"]}"/><path class="s" d="{tail}" stroke="{p["ink"]}" stroke-width="{w}"/></g>'
            f'<g transform="translate(-46 -24) rotate(-9)">{fox_head(p, asleep, w)}</g>', (-92, -52))


def cat(ink, asleep):
    p, w = ink.p, 2.5
    body = "M-47 1C-54 -24 -37 -42 -10 -42L17 -42C41 -42 52 -23 47 1Z"
    head = "M-55 -37C-55 -51 -46 -58 -35 -58C-24 -58 -15 -51 -15 -37C-15 -24 -24 -18 -35 -18C-46 -18 -55 -24 -55 -37Z"
    return (f'<g transform="translate(45 -8)"><g class="tl"><path class="s" d="M0 0C21 -3 26 18 15 31C9 38 2 34 4 27" stroke="{p["ink"]}" stroke-width="13.5"/>'
            f'<path class="s" d="M0 0C21 -3 26 18 15 31C9 38 2 34 4 27" stroke="{p["fur"]}" stroke-width="8.6"/>'
            f'<path class="s" d="M19 9l7 -3M19 19l7 0" stroke="{p["fur2"]}" stroke-width="3"/></g></g>'
            f'<g class="br"><path d="{body}" fill="{p["fur"]}"/><path class="s" d="M-2 -42l2 12M11 -42l1 12M24 -40l-1 11" stroke="{p["fur2"]}" stroke-width="4.5"/>'
            f'<path class="s" d="{body}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<path d="M-52 -46L-54 -68L-39 -56ZM-30 -56L-16 -69L-17 -45Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="{head}" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            + eyes(p, [(-43, -37), (-27, -37)], asleep)
            + f'<path class="s" d="M-37 -30.5l2 2l2 -2M-55 -32l-10 -2M-55 -28l-10 2M-15 -32l10 -2M-15 -28l10 2" stroke="{p["dark"]}" stroke-width="1.4"/></g>', (-70, -40))


def lion(ink, asleep):
    p, w = ink.p, 2.5
    body = "M-40 1C-46 -22 -30 -40 -6 -40L20 -40C44 -40 56 -22 51 1Z"
    mane = smooth([(-36 + math.cos(a) * (31 if k % 2 == 0 else 26), -40 + math.sin(a) * (31 if k % 2 == 0 else 26))
                   for k, a in ((k, k * math.pi / 9) for k in range(18))], closed=True)
    return (f'<g transform="translate(49 -10)"><g class="tl"><path class="s" d="M0 0C16 -4 24 -18 18 -32" stroke="{p["ink"]}" stroke-width="2.4"/>'
            f'<path d="M18 -32C10 -38 12 -50 20 -50C28 -50 30 -38 18 -32Z" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/></g></g>'
            f'<g class="br"><path d="{body}" fill="{p["fur"]}"/><path class="s" d="{body}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<path class="s" d="M-22 1q4 -8 12 -8M8 1q4 -8 12 -8" stroke="{p["ink"]}" stroke-width="1.8" stroke-opacity=".6"/></g>'
            f'<path d="{mane}" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<circle cx="-51" cy="-56" r="6.5" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2"/><circle cx="-21" cy="-56" r="6.5" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2"/>'
            f'<circle cx="-36" cy="-39" r="19.5" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<ellipse cx="-36" cy="-31" rx="9" ry="6.5" fill="{p["belly"]}"/>'
            + eyes(p, [(-43.5, -42), (-28.5, -42)], asleep)
            + f'<path d="M-39.5 -35h7l-3.5 4Z" fill="{p["dark"]}" stroke="{p["dark"]}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path class="s" d="M-36 -31q-3 4 -6.5 1.5M-36 -31q3 4 6.5 1.5" stroke="{p["dark"]}" stroke-width="1.5"/>', (-76, -52))


def owl(ink, asleep):
    p, w = ink.p, 2.5
    body = "M-27 0C-36 -30 -24 -70 0 -70C24 -70 36 -30 27 0Z"
    feathers = "".join(f"M{x - 4} {y}q4 5 8 0" for x, y in ((-8, -24), (8, -24), (0, -15), (-12, -12), (12, -12), (0, -5)))
    lids = (f'<path class="s" d="M-19 -47q8 7 16 0M3 -47q8 7 16 0" stroke="{p["dark"]}" stroke-width="2.2"/>' if asleep else
            f'<circle cx="-11" cy="-47" r="5" fill="{p["dark"]}"/><circle cx="11" cy="-47" r="5" fill="{p["dark"]}"/>'
            f'<circle cx="-9.4" cy="-48.6" r="1.5" fill="{p["belly"]}"/><circle cx="12.6" cy="-48.6" r="1.5" fill="{p["belly"]}"/>')
    return (f'<g class="br"><path d="M-17 -64L-25 -84L-6 -69ZM17 -64L25 -84L6 -69Z" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="{body}" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<path d="M-17 -2C-21 -22 -14 -34 0 -34C14 -34 21 -22 17 -2Z" fill="{p["belly"]}"/>'
            f'<path class="s" d="{feathers}" stroke="{p["fur2"]}" stroke-width="1.8"/>'
            f'<path class="s" d="M-27 -8C-34 -22 -34 -40 -28 -52M27 -8C34 -22 34 -40 28 -52" stroke="{p["ink"]}" stroke-width="2" stroke-opacity=".7"/>'
            f'<circle cx="-11" cy="-47" r="11.5" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="2.1"/><circle cx="11" cy="-47" r="11.5" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="2.1"/>'
            f'{lids}<path d="M-4 -40L4 -40L0 -32Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.8" stroke-linejoin="round"/></g>'
            f'<path class="s" d="M-11 0l-3 5M-8 0l0 6M-5 0l3 5M5 0l-3 5M8 0l0 6M11 0l3 5" stroke="{p["warm"]}" stroke-width="2.4"/>', (-44, -70))


def bear(ink, asleep):
    p, w = ink.p, 2.5
    body = "M-38 1C-46 -30 -30 -54 0 -54C30 -54 46 -30 38 1Z"
    return (f'<g class="br"><path d="{body}" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<ellipse cx="0" cy="-18" rx="19" ry="17" fill="{p["belly"]}"/>'
            f'<path class="s" d="M-30 -8q-8 -14 2 -26M30 -8q8 -14 -2 -26" stroke="{p["ink"]}" stroke-width="2" stroke-opacity=".6"/>'
            f'<ellipse cx="-22" cy="0" rx="11" ry="6" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="2.2"/><ellipse cx="22" cy="0" rx="11" ry="6" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="2.2"/></g>'
            f'<circle cx="-20" cy="-86" r="9" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/><circle cx="20" cy="-86" r="9" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<circle cx="-20" cy="-86" r="4" fill="{p["fur2"]}"/><circle cx="20" cy="-86" r="4" fill="{p["fur2"]}"/>'
            f'<circle cx="0" cy="-66" r="25" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<ellipse cx="0" cy="-58" rx="12" ry="9" fill="{p["belly"]}"/>'
            + eyes(p, [(-10, -70), (10, -70)], asleep)
            + f'<ellipse cx="0" cy="-62" rx="4.6" ry="3.4" fill="{p["dark"]}"/><path class="s" d="M0 -58.6v3.4M0 -55.2q-3 3 -6 1M0 -55.2q3 3 6 1" stroke="{p["dark"]}" stroke-width="1.5"/>', (-42, -84))


def penguin(ink, asleep):
    p, w = ink.p, 2.5
    body = "M-25 0C-34 -28 -24 -74 0 -74C24 -74 34 -28 25 0Z"
    return (f'<path d="M-25 -44C-40 -34 -42 -18 -36 -8C-30 -18 -26 -26 -24 -34Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M25 -44C40 -34 42 -18 36 -8C30 -18 26 -26 24 -34Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<ellipse cx="-11" cy="1" rx="10" ry="4.6" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2"/><ellipse cx="11" cy="1" rx="10" ry="4.6" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2"/>'
            f'<g class="br"><path d="{body}" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<path d="M-17 -3C-23 -24 -19 -40 -9 -52C-4 -58 4 -58 9 -52C19 -40 23 -24 17 -3Z" fill="{p["belly"]}"/>'
            f'<circle cx="-8.5" cy="-56" r="6.5" fill="{p["belly"]}"/><circle cx="8.5" cy="-56" r="6.5" fill="{p["belly"]}"/>'
            + eyes(p, [(-8.5, -56), (8.5, -56)], asleep, 2.5)
            + f'<path d="M-5 -49L5 -49L0 -41Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.8" stroke-linejoin="round"/></g>', (-40, -70))


def tortoise(ink, asleep):
    p, w = ink.p, 2.5
    shell = "M-40 -4C-40 -36 -18 -50 6 -50C32 -50 50 -32 50 -4Z"
    plates = "M-18 -44L-10 -26L8 -26L18 -46M-10 -26L-20 -6M8 -26L20 -6M-34 -22L-10 -26M34 -24L8 -26M-20 -6L20 -6"
    hx, hy = (-56, -9) if asleep else (-58, -18)
    return (f'<rect x="-30" y="-8" width="15" height="14" rx="5" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="2.2"/>'
            f'<rect x="22" y="-8" width="15" height="14" rx="5" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="2.2"/>'
            f'<path d="M48 -8l12 5l-12 3Z" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="2" stroke-linejoin="round"/>'
            f'<g class="tl" style="transform-origin:-40px -10px"><path d="M-40 -12C-46 -14 -50 {hy + 6} {hx + 10} {hy + 3}L{hx + 12} {hy - 8}C-46 {hy - 8} -42 -2 -38 -2Z" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<ellipse cx="{hx}" cy="{hy}" rx="13" ry="10.5" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            + eyes(p, [(hx - 3, hy - 2)], asleep, 2.2)
            + f'<path class="s" d="M{hx - 11} {hy + 3}q4 3 8 1" stroke="{p["dark"]}" stroke-width="1.4"/></g>'
            f'<g class="br"><path d="{shell}" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path class="s" d="{plates}" stroke="{p["fur2"]}" stroke-width="2.6"/>'
            f'<path class="s" d="M-40 -4L50 -4" stroke="{p["ink"]}" stroke-width="{w}"/></g>', (-80, -30))


ANIMALS = dict(fox=fox, cat=cat, lion=lion, owl=owl, bear=bear, penguin=penguin, tortoise=tortoise)


def animal(ink, x, y, at, asleep=False, k=1.0, flip=False):
    """The theme's animal sitting at (x, y). Asleep, it breathes out a few z's."""
    art, z = ANIMALS[ink.theme](ink, asleep)
    sx = -k if flip else k
    ink.add(f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(k)})"><g class="i" style="animation-delay:{at:.2f}s">{art}</g>'
            + (zzz(ink, z[0], z[1], at) if asleep else "") + "</g>")

# ───────────────────────────── THE PROPS ────────────────────────────


def cloud(ink, x, y, k, at):
    p = ink.p
    d = ("M-58 14C-76 14 -78 -8 -58 -10C-58 -30 -30 -36 -20 -20C-10 -42 26 -40 30 -16C48 -24 66 -8 54 8C62 14 56 22 46 20"
         "C30 22 -30 22 -58 14Z")
    ink.add(f'<g transform="translate({x} {y}) scale({k})"><g class="cl" style="animation-delay:-{ink.rng.uniform(0, 8):.1f}s">'
            f'<path class="i" d="{d}" fill="{p["wash"]}" style="animation-delay:{at:.2f}s"/>{ink.line(d, at, 1.1, 2.2 / k)}</g></g>')


def bird(ink, x, y, k, at):
    ink.add(f'<g transform="translate({x} {y}) scale({k})"><g class="cl" style="animation-duration:{ink.rng.uniform(7, 12):.1f}s">'
            f'{ink.line("M-13 1Q-7 -9 0 0Q7 -9 13 1", at, .5, 2.2 / k)}</g></g>')


def sun(ink, x, y, r, at, rays=12):
    p = ink.p
    spokes = "".join(f"M{f(math.cos(a) * r * 1.28)} {f(math.sin(a) * r * 1.28)}L{f(math.cos(a) * r * (1.62 if k % 2 else 1.48))} {f(math.sin(a) * r * (1.62 if k % 2 else 1.48))}"
                     for k, a in ((k, k * 2 * math.pi / rays) for k in range(rays)))
    ink.add(f'<g transform="translate({x} {y})"><g class="spin"><path class="i s" d="{spokes}" stroke="{p["ink"]}" stroke-width="2.3" style="animation-delay:{at + .5:.2f}s"/></g>'
            f'<path class="i" d="{circle_path(0, 0, r, ink.rng)}" fill="{p.get("glow", p["marker"])}" style="animation-delay:{at + .1:.2f}s"/>'
            f'{ink.line(circle_path(0, 0, r, ink.rng), at, 1, 2.5)}</g>')


def moon(ink, x, y, r, at):
    p = ink.p
    d = f"M{f(r * .2)} {f(-r)}A{r} {r} 0 1 0 {f(r)} {f(r * .35)}A{f(r * .78)} {f(r * .78)} 0 0 1 {f(r * .2)} {f(-r)}Z"
    ink.add(f'<g transform="translate({x} {y}) rotate(-18)"><path class="i" d="{d}" fill="{p.get("glow", p["marker"])}" style="animation-delay:{at + .15:.2f}s"/>{ink.line(d, at, 1, 2.5)}</g>')


def star(ink, x, y, s, at):
    p = ink.p
    ink.add(f'<g transform="translate({f(x)} {f(y)})"><g class="i" style="animation-delay:{at:.2f}s"><g class="tw" style="animation-duration:{ink.rng.uniform(1.8, 3.6):.1f}s;animation-delay:-{ink.rng.uniform(0, 3):.1f}s">'
            f'<path d="M0 {f(-s)}Q0 0 {f(s)} 0Q0 0 0 {f(s)}Q0 0 {f(-s)} 0Q0 0 0 {f(-s)}Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.1" stroke-linejoin="round"/></g></g></g>')


def tuft(ink, x, y, at, h=22, n=4, kind="grass"):
    """A tuft of grass on the ground."""
    rng, p = ink.rng, ink.p
    for k in range(n):
        ang = -90 + (k - (n - 1) / 2) * rng.uniform(16, 26) + rng.uniform(-6, 6)
        size = h * rng.uniform(.7, 1.15)
        outline, _ = ink.leaf(size, kind)
        ink.pop(x + (k - (n - 1) / 2) * 3, y, f'<path d="{outline}" fill="{rng.choice(p["leaf"])}" stroke="{p["ink"]}" stroke-width="1.6" stroke-linejoin="round"/>',
                at + k * .06, ang, rng.uniform(3, 5.5))


def pine(ink, x, y, h, at):
    p, rng = ink.p, ink.rng
    w = h * .42
    tiers = "".join(f"M{f(-w * (1 - k * .22))} {f(-h * (.14 + k * .25))}L0 {f(-h * (.5 + k * .25))}L{f(w * (1 - k * .22))} {f(-h * (.14 + k * .25))}Z" for k in range(3))
    trunk = f"M{f(-h * .05)} 0L{f(-h * .05)} {f(-h * .16)}L{f(h * .05)} {f(-h * .16)}L{f(h * .05)} 0Z"
    ink.pop(x, y, f'<path d="{trunk}" fill="{p["fur2"] if ink.theme == "bear" else p["soft"]}" stroke="{p["ink"]}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="{tiers}" fill="{rng.choice(p["leaf"][:2])}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>', at, 0, rng.uniform(5, 8))


def acacia(ink, x, y, h, at):
    p = ink.p
    trunk = f"M-5 0C-3 {f(-h * .3)} -9 {f(-h * .5)} -2 {f(-h * .72)}M5 0C6 {f(-h * .3)} 0 {f(-h * .5)} 4 {f(-h * .72)}M-2 {f(-h * .5)}C-14 {f(-h * .62)} -26 {f(-h * .64)} -34 {f(-h * .72)}M3 {f(-h * .52)}C16 {f(-h * .6)} 26 {f(-h * .66)} 36 {f(-h * .74)}"
    crown = f"M{f(-h * .62)} {f(-h * .7)}C{f(-h * .62)} {f(-h * .92)} {f(-h * .2)} {f(-h * 1.02)} 0 {f(-h * .98)}C{f(h * .3)} {f(-h * 1.04)} {f(h * .66)} {f(-h * .9)} {f(h * .64)} {f(-h * .7)}C{f(h * .3)} {f(-h * .76)} {f(-h * .3)} {f(-h * .76)} {f(-h * .62)} {f(-h * .7)}Z"
    ink.add(f'<g transform="translate({x} {y})">{ink.line(trunk, at, 1, 3)}<path class="i" d="{crown}" fill="{p["leaf"][1]}" style="animation-delay:{at + .7:.2f}s"/>{ink.line(crown, at + .5, 1, 2.5)}</g>')


def cactus(ink, x, y, h, at):
    p = ink.p
    w = h * .16
    d = (f"M{f(-w)} 0L{f(-w)} {f(-h + w)}A{f(w)} {f(w)} 0 0 1 {f(w)} {f(-h + w)}L{f(w)} 0Z")
    arm_l = f"M{f(-w)} {f(-h * .36)}L{f(-w * 2.6)} {f(-h * .36)}A{f(w * .7)} {f(w * .7)} 0 0 1 {f(-w * 3.3)} {f(-h * .44)}L{f(-w * 3.3)} {f(-h * .64)}A{f(w * .7)} {f(w * .7)} 0 0 1 {f(-w * 1.9)} {f(-h * .64)}L{f(-w * 1.9)} {f(-h * .5)}L{f(-w)} {f(-h * .5)}Z"
    arm_r = f"M{f(w)} {f(-h * .5)}L{f(w * 2.4)} {f(-h * .5)}A{f(w * .7)} {f(w * .7)} 0 0 0 {f(w * 3.1)} {f(-h * .58)}L{f(w * 3.1)} {f(-h * .8)}A{f(w * .7)} {f(w * .7)} 0 0 0 {f(w * 1.7)} {f(-h * .8)}L{f(w * 1.7)} {f(-h * .64)}L{f(w)} {f(-h * .64)}Z"
    ribs = f"M0 {f(-h * .9)}L0 {f(-h * .08)}"
    ink.pop(x, y, f'<path d="{arm_l}{arm_r}" fill="{p["leaf"][1]}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{p["leaf"][1]}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
            f'<path class="s" d="{ribs}" stroke="{p["ink"]}" stroke-width="1.3" stroke-opacity=".5"/>'
            f'<circle cx="0" cy="{f(-h - 2)}" r="{f(w * .4)}" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.6"/>', at)


def ground(ink, y, at, amp=5, span=130, layers=1, line=True, bottom=None):
    """The ground: a line, the colour under it, and a deeper layer further down."""
    p, rng, W = ink.p, ink.rng, ink.w
    bottom = bottom or ink.h + 10
    top = wave(rng, -40, W + 40, y, amp, span)
    ink.add(f'<path class="i" d="{smooth(top)}L{W + 40} {bottom}L-40 {bottom}Z" fill="{p["wash"]}" style="animation-delay:{at + .3:.2f}s"/>')
    for k in range(layers):
        low = wave(rng, -40, W + 40, y + 34 + k * 30, amp * .8, span * 1.3)
        ink.add(f'<path class="i" d="{smooth(low)}L{W + 40} {bottom}L-40 {bottom}Z" fill="{p["deep"]}" fill-opacity=".7" style="animation-delay:{at + .5 + k * .2:.2f}s"/>')
    if line:
        ink.stroke(smooth(top), at, 1.5, 2.8)
    return top


def flyer(ink, path, begin, dur, art):
    """Something that follows a path over and over, fading in and out at its ends."""
    ink.add(f'<g opacity="0">{art}<animateMotion path="{path}" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite" rotate="auto"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.04;0.95;1" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite"/></g>')


def fish_shape(p, color):
    return (f'<path d="M-9 0L-19 -7L-16 0L-19 7Z" fill="{color}" stroke="{p["ink"]}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M-11 0C-6 -8 6 -8 12 0C6 8 -6 8 -11 0Z" fill="{color}" stroke="{p["ink"]}" stroke-width="1.5"/>'
            f'<circle cx="6.5" cy="-1.6" r="1.4" fill="{p["dark"]}"/>')


def butterfly(p):
    return (f'<g class="tw" style="animation-duration:.5s"><path d="M0 0C-10 -14 -20 -8 -12 2C-18 8 -8 14 0 4Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M0 0C10 -14 20 -8 12 2C18 8 8 14 0 4Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.4" stroke-linejoin="round"/></g>'
            f'<path class="s" d="M0 -4L0 7" stroke="{p["ink"]}" stroke-width="2"/>')


def flying_bird(p):
    return f'<path class="s" d="M-12 2Q-6 -8 0 0Q6 -8 12 2" stroke="{p["ink"]}" stroke-width="2.2"/>'


def boat(ink, x, y, at, crew=True, k=1.0):
    """A paper boat riding the waves, the fox looking out of it."""
    p = ink.p
    aboard = (f'<path d="M30 -2C38 -26 58 -24 54 -6C53 -1 46 1 40 -2Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>'
              f'<path d="M46.5 -20.5C54 -20 56.5 -13 54 -6C52 -11 49 -15 44.5 -16.5Z" fill="{p["belly"]}"/>'
              f'<g transform="translate(-33 -19) scale(.86)">{fox_head(p, w=2.5)}</g>') if crew else ""
    ink.add(f'<g transform="translate({x} {y}) scale({k})"><g class="i" style="animation-delay:{at:.2f}s"><g class="bob">{aboard}'
            f'<path d="M-17 -2L1 -44L19 -2Z" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
            f'<path class="s" d="M1 -44L1 -58M1 -58L15 -53L1 -48" stroke="{p["ink"]}" stroke-width="2"/><path d="M1 -58L15 -53L1 -48Z" fill="{p["warm"]}"/>'
            f'<path d="M-52 -2L52 -2L35 22L-35 22Z" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
            f'<path class="s" d="M-17 -2L0 22L19 -2" stroke="{p["ink"]}" stroke-width="1.5" stroke-opacity=".55"/></g></g></g>')

# ───────────────────────────── THE LAND ─────────────────────────────
# The wide picture under the name: far things pale, near things strong, the animal in front.
# 2400 × 520 and shown cropped to whatever the screen is, so what matters sits near the middle
# and the animal a little right of it.

LW, LH, MX = 2400, 520, 1590


def band(ink, pts, fill, at, opacity=None, outline=None, width=2.4):
    """A layer of land: everything under a line."""
    d = smooth(pts)
    ink.fill(f"{d}L{f(pts[-1][0])} {ink.h + 20}L{f(pts[0][0])} {ink.h + 20}Z", fill, at, opacity)
    if outline:
        ink.stroke(d, at, 1.5, width, opacity=None if outline is True else outline)


def mountains(ink, x0, x1, y, h, step, color, at, snow=None, line=".45"):
    """A row of peaks, with snow on the tall ones if `snow` is a colour."""
    rng = ink.rng
    pts, x, up = [(x0, y)], x0 + step * .3, True
    while x < x1 - step * .3:
        pts.append((x, y - (h * rng.uniform(.55, 1) if up else h * rng.uniform(.05, .3))))
        x += step * rng.uniform(.55, 1.15)
        up = not up
    pts.append((x1, y))
    d = "M" + "L".join(f"{f(a)} {f(b)}" for a, b in pts)
    ink.fill(f"{d}L{x1} {ink.h + 20}L{x0} {ink.h + 20}Z", color, at)
    ink.stroke(d, at, 1.6, 2, opacity=line)
    for i in range(1, len(pts) - 1):
        (ax, ay), (px, py), (bx, by) = pts[i - 1], pts[i], pts[i + 1]
        if py < ay and py < by:
            # the lit side of the peak a shade darker on the other, and a cap of snow
            ink.fill(f"M{f(px)} {f(py)}L{f(bx)} {f(by)}L{f(px + (bx - px) * .25)} {f(by)}Z", ink.p["ink"], at + .3, ".07")
            if snow and y - py > h * .7:
                k = .26
                l, r = (px + (ax - px) * k, py + (ay - py) * k), (px + (bx - px) * k, py + (by - py) * k)
                m = ((l[0] + r[0]) / 2, (l[1] + r[1]) / 2)
                ink.fill(f"M{f(px)} {f(py)}L{f(l[0])} {f(l[1])}L{f((l[0] + m[0]) / 2)} {f(m[1] - 5)}L{f(m[0])} {f(m[1] + 6)}"
                         f"L{f((r[0] + m[0]) / 2)} {f(m[1] - 4)}L{f(r[0])} {f(r[1])}Z", snow, at + .5)


def shadow(ink, x, y, rx, at, ry=None):
    """What something casts on the ground under it."""
    ink.add(f'<ellipse class="i" cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry or rx * .16)}" fill="{ink.p["ink"]}" fill-opacity=".13" style="animation-delay:{at:.2f}s"/>')


def blob(ink, cx, cy, rx, ry, n=11, rough=.14):
    """A soft uneven round shape: a treetop, a bush, a stone."""
    rng = ink.rng
    return smooth([(cx + math.cos(a) * rx * (1 + rng.uniform(-rough, rough)), cy + math.sin(a) * ry * (1 + rng.uniform(-rough, rough)))
                   for a in (k * 2 * math.pi / n for k in range(n))], closed=True)


def tree(ink, x, y, h, at, color=None, far=0.0):
    """A leafy tree: a trunk, a crown in three masses, light from the left."""
    p, rng = ink.p, ink.rng
    bg, w = p["bg"], h * .11
    leaf = mix(color or p["leaf"][1], bg, far)
    dark = mix(mix(leaf, p["ink"], .22), bg, far)
    trunk = f"M{f(-w * .6)} 0C{f(-w * .4)} {f(-h * .2)} {f(-w * .5)} {f(-h * .36)} {f(-w * .2)} {f(-h * .5)}L{f(w * .3)} {f(-h * .5)}C{f(w * .5)} {f(-h * .34)} {f(w * .4)} {f(-h * .2)} {f(w * .7)} 0Z"
    crowns = [(0, -h * .7, h * .34, h * .28), (-h * .2, -h * .56, h * .22, h * .19), (h * .2, -h * .58, h * .24, h * .2)]
    art = f'<path d="{trunk}" fill="{mix(p["fur2"], bg, far)}" stroke="{p["ink"]}" stroke-width="{f(2.2 * (1 - far * .5))}" stroke-opacity="{1 - far * .6:.2f}" stroke-linejoin="round"/>'
    for cx, cy, rx, ry in crowns[1:] + crowns[:1]:
        d = blob(ink, cx, cy, rx, ry)
        art += (f'<path d="{d}" fill="{leaf}"/><path d="{blob(ink, cx + rx * .3, cy + ry * .28, rx * .62, ry * .58)}" fill="{dark}" fill-opacity=".5"/>'
                f'<path class="s" d="{d}" stroke="{p["ink"]}" stroke-width="{f(2.3 * (1 - far * .5))}" stroke-opacity="{1 - far * .6:.2f}"/>')
    art += f'<path class="s" d="M{f(-h * .14)} {f(-h * .74)}q{f(h * .06)} {f(-h * .05)} {f(h * .12)} 0M{f(h * .02)} {f(-h * .62)}q{f(h * .06)} {f(-h * .05)} {f(h * .12)} 0" stroke="{p["ink"]}" stroke-width="1.5" stroke-opacity="{.5 * (1 - far):.2f}"/>'
    ink.pop(x, y, art, at, 0, rng.uniform(6, 9))


def fir(ink, x, y, h, at, far=0.0, color=None):
    """A fir: four tiers of boughs, the right side in shade."""
    p, rng = ink.p, ink.rng
    leaf = mix(color or rng.choice(p["leaf"][:2]), p["bg"], far)
    w, art = h * .36, ""
    art += f'<path d="M{f(-h * .04)} 0L{f(-h * .04)} {f(-h * .14)}L{f(h * .04)} {f(-h * .14)}L{f(h * .04)} 0Z" fill="{mix(p["fur2"], p["bg"], far)}" stroke="{p["ink"]}" stroke-width="1.8" stroke-opacity="{1 - far * .6:.2f}"/>'
    for k in range(4):
        y0, y1, ww = -h * (.1 + k * .2), -h * (.42 + k * .2), w * (1 - k * .2)
        tier = f"M{f(-ww)} {f(y0)}Q{f(-ww * .5)} {f(y0 + h * .03)} 0 {f(y0)}Q{f(ww * .5)} {f(y0 + h * .03)} {f(ww)} {f(y0)}L0 {f(y1)}Z"
        art += (f'<path d="{tier}" fill="{leaf}"/><path d="M0 {f(y1)}L{f(ww)} {f(y0)}Q{f(ww * .5)} {f(y0 + h * .03)} 0 {f(y0)}Z" fill="{p["ink"]}" fill-opacity="{.16 * (1 - far):.2f}"/>'
                f'<path class="s" d="{tier}" stroke="{p["ink"]}" stroke-width="{f(2.1 * (1 - far * .5))}" stroke-opacity="{1 - far * .6:.2f}"/>')
    ink.pop(x, y, art, at, 0, rng.uniform(6, 10))


def flat_tree(ink, x, y, h, at, far=0.0):
    """An acacia: a forked trunk under a wide flat crown."""
    p = ink.p
    leaf, dark = mix(p["leaf"][1], p["bg"], far), mix(mix(p["leaf"][1], p["ink"], .25), p["bg"], far)
    op = f"{1 - far * .6:.2f}"
    trunk = (f"M-6 0C-4 {f(-h * .3)} -10 {f(-h * .46)} -3 {f(-h * .66)}L4 {f(-h * .66)}C1 {f(-h * .46)} 7 {f(-h * .3)} 7 0Z"
             f"M-3 {f(-h * .5)}C{f(-h * .16)} {f(-h * .6)} {f(-h * .3)} {f(-h * .62)} {f(-h * .42)} {f(-h * .72)}L{f(-h * .36)} {f(-h * .74)}C{f(-h * .26)} {f(-h * .66)} {f(-h * .14)} {f(-h * .64)} 0 {f(-h * .56)}Z"
             f"M3 {f(-h * .5)}C{f(h * .18)} {f(-h * .6)} {f(h * .32)} {f(-h * .64)} {f(h * .44)} {f(-h * .74)}L{f(h * .38)} {f(-h * .76)}C{f(h * .28)} {f(-h * .68)} {f(h * .14)} {f(-h * .64)} 0 {f(-h * .56)}Z")
    crown = (f"M{f(-h * .72)} {f(-h * .7)}C{f(-h * .74)} {f(-h * .88)} {f(-h * .36)} {f(-h * .98)} {f(-h * .1)} {f(-h * .94)}C{f(h * .1)} {f(-h * 1.04)} {f(h * .5)} {f(-h * 1.0)} {f(h * .62)} {f(-h * .88)}"
             f"C{f(h * .8)} {f(-h * .86)} {f(h * .82)} {f(-h * .7)} {f(h * .7)} {f(-h * .68)}C{f(h * .36)} {f(-h * .76)} {f(-h * .3)} {f(-h * .76)} {f(-h * .72)} {f(-h * .7)}Z")
    under = (f"M{f(-h * .72)} {f(-h * .7)}C{f(-h * .3)} {f(-h * .76)} {f(h * .36)} {f(-h * .76)} {f(h * .7)} {f(-h * .68)}C{f(h * .4)} {f(-h * .84)} {f(-h * .36)} {f(-h * .84)} {f(-h * .72)} {f(-h * .7)}Z")
    ink.pop(x, y, f'<path d="{trunk}" fill="{mix(p["fur2"], p["bg"], far)}" stroke="{p["ink"]}" stroke-width="2" stroke-opacity="{op}" stroke-linejoin="round"/>'
            f'<path d="{crown}" fill="{leaf}"/><path d="{under}" fill="{dark}" fill-opacity=".6"/>'
            f'<path class="s" d="{crown}" stroke="{p["ink"]}" stroke-width="2.4" stroke-opacity="{op}"/>', at, 0, 9)


def bush(ink, x, y, s, at, berries=False):
    p, rng = ink.p, ink.rng
    d = blob(ink, 0, -s * .5, s, s * .56, 9, .16)
    art = (f'<path d="{d}" fill="{rng.choice(p["leaf"][:2])}"/><path d="{blob(ink, s * .3, -s * .34, s * .6, s * .34, 8)}" fill="{p["ink"]}" fill-opacity=".1"/>'
           f'<path class="s" d="{d}" stroke="{p["ink"]}" stroke-width="2.2"/>')
    if berries:
        art += "".join(f'<circle cx="{f(rng.uniform(-s * .6, s * .6))}" cy="{f(rng.uniform(-s * .8, -s * .2))}" r="{f(s * .09)}" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.2"/>' for _ in range(5))
    ink.pop(x, y, art, at, 0, rng.uniform(5, 8))


def rock(ink, x, y, s, at, color=None):
    p, rng = ink.p, ink.rng
    pts = [(-s, 0), (-s * .86, -s * .42), (-s * .4, -s * rng.uniform(.62, .8)), (s * .2, -s * rng.uniform(.66, .86)), (s * .78, -s * .44), (s, 0)]
    d = "M" + "L".join(f"{f(a + rng.uniform(-2, 2))} {f(b)}" for a, b in pts) + "Z"
    stone = color or mix(p["soft"], p["bg"], .45)
    ink.pop(x, y, f'<path d="{d}" fill="{stone}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
            f'<path d="M{f(s * .2)} {f(-s * .74)}L{f(s * .78)} {f(-s * .44)}L{f(s)} 0L{f(s * .3)} 0Z" fill="{p["ink"]}" fill-opacity=".14"/>'
            f'<path class="s" d="M{f(-s * .4)} {f(-s * .7)}L{f(-s * .1)} {f(-s * .3)}L{f(s * .2)} {f(-s * .76)}" stroke="{p["ink"]}" stroke-width="1.4" stroke-opacity=".5"/>', at)


def flower(ink, x, y, h, at, color=None):
    p, rng = ink.p, ink.rng
    c, r = color or p["warm"], h * .2
    petals = "".join(f'<ellipse cx="{f(math.cos(a) * r)}" cy="{f(-h + math.sin(a) * r)}" rx="{f(r * .7)}" ry="{f(r * .7)}" fill="{c}" stroke="{p["ink"]}" stroke-width="1.3"/>'
                     for a in (k * 1.2566 + .3 for k in range(5)))
    ink.pop(x, y, f'<path class="s" d="M0 0Q{f(rng.uniform(-5, 5))} {f(-h * .5)} 0 {f(-h)}" stroke="{p["ink"]}" stroke-width="1.8"/>'
            f'<path d="M0 {f(-h * .4)}Q{f(h * .28)} {f(-h * .62)} {f(h * .36)} {f(-h * .38)}Q{f(h * .16)} {f(-h * .34)} 0 {f(-h * .4)}Z" fill="{p["leaf"][1]}" stroke="{p["ink"]}" stroke-width="1.2"/>'
            f'{petals}<circle cx="0" cy="{f(-h)}" r="{f(r * .5)}" fill="{p["marker"]}" stroke="{p["ink"]}" stroke-width="1.1"/>', at, 0, rng.uniform(3, 5))


def grasses(ink, x0, x1, y, at, step=46, h=(18, 34), kind="grass", wave_y=0.0):
    """Grass all along a stretch of ground."""
    rng, x = ink.rng, x0
    while x < x1:
        tuft(ink, x, y + rng.uniform(-3, 4) + wave_y * math.sin(x / 140), at + rng.uniform(0, .8), rng.uniform(*h), rng.choice((3, 4, 5)), kind)
        x += step * rng.uniform(.6, 1.4)

# ── the animals, sitting up ──


def sit_body(p, w=2.6, marks=""):
    body = "M-36 0C-47 -36 -32 -74 0 -74C32 -74 47 -36 36 0Z"
    paw = lambda cx, cy, fill: f'<ellipse cx="{cx}" cy="{cy}" rx="10" ry="5.6" fill="{fill}" stroke="{p["ink"]}" stroke-width="2.1"/>'
    return (f'<g class="br"><path d="{body}" fill="{p["fur"]}"/>'
            f'<path d="M12 -72C36 -62 50 -32 37 0L21 0C34 -30 30 -56 12 -72Z" fill="{p["fur2"]}" fill-opacity=".6"/>{marks}'
            f'<path d="M-17 -3C-25 -30 -13 -58 0 -58C13 -58 25 -30 17 -3Z" fill="{p["belly"]}"/>'
            f'<path class="s" d="{body}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<path class="s" d="M-13 -3L-13 -30M13 -3L13 -30M-4 -44q4 4 8 0M-6 -34q6 5 12 0" stroke="{p["ink"]}" stroke-width="1.7" stroke-opacity=".45"/></g>'
            + paw(-31, -1, p["fur"]) + paw(31, -1, p["fur"]) + paw(-9, 0, p["belly"]) + paw(9, 0, p["belly"]))


def sit_fox(ink, asleep=False):
    p, w = ink.p, 2.6
    tail = "M26 -8C70 -2 90 -44 70 -76C61 -90 44 -82 51 -66C57 -50 47 -34 24 -30Z"
    tip = "M70 -76C61 -90 44 -82 51 -66C54 -58 52 -50 48 -44C60 -48 70 -60 70 -76Z"
    return (f'<g class="tl" style="transform-origin:26px -18px"><path d="{tail}" fill="{p["fur"]}"/><path d="M40 -12C66 -16 80 -42 72 -66C74 -40 62 -24 40 -22Z" fill="{p["fur2"]}" fill-opacity=".6"/>'
            f'<path d="{tip}" fill="{p["belly"]}"/><path class="s" d="{tail}" stroke="{p["ink"]}" stroke-width="{w}"/></g>'
            + sit_body(p, w) + f'<g transform="translate(0 -94) scale(1.34)">{fox_head(p, asleep, 2)}</g>', (-56, -126))


def sit_cat(ink, asleep=False):
    p, w = ink.p, 2.6
    tail = "M30 -8C58 -8 70 -32 60 -56C56 -66 46 -62 49 -53"
    marks = f'<path class="s" d="M-34 -28q8 3 14 0M-36 -42q8 3 13 0M22 -30q7 3 13 0M24 -44q6 3 11 0" stroke="{p["fur2"]}" stroke-width="4.5"/>'
    head = "M-25 -98C-25 -113 -14 -121 0 -121C14 -121 25 -113 25 -98C25 -84 14 -77 0 -77C-14 -77 -25 -84 -25 -98Z"
    look = (f'<path class="s" d="M-13 -99q4 4 8 0M5 -99q4 4 8 0" stroke="{p["dark"]}" stroke-width="2.1"/>' if asleep else
            f'<g class="blink"><ellipse cx="-9" cy="-100" rx="3.4" ry="4.6" fill="{p["dark"]}"/><ellipse cx="9" cy="-100" rx="3.4" ry="4.6" fill="{p["dark"]}"/>'
            f'<circle cx="-7.8" cy="-101.6" r="1.2" fill="{p["belly"]}"/><circle cx="10.2" cy="-101.6" r="1.2" fill="{p["belly"]}"/></g>')
    return (f'<g class="tl" style="transform-origin:30px -8px"><path class="s" d="{tail}" stroke="{p["ink"]}" stroke-width="14"/><path class="s" d="{tail}" stroke="{p["fur"]}" stroke-width="9"/>'
            f'<path class="s" d="M56 -26l8 -3M60 -40l8 -1" stroke="{p["fur2"]}" stroke-width="3.4"/></g>'
            + sit_body(p, w, marks)
            + f'<path d="M-22 -110L-26 -136L-7 -118ZM22 -110L26 -136L7 -118Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="M-20 -114L-22 -128L-12 -118ZM20 -114L22 -128L12 -118Z" fill="{p["fur2"]}"/>'
            f'<path d="{head}" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<path class="s" d="M-6 -120l1 9M0 -121l0 10M6 -120l-1 9" stroke="{p["fur2"]}" stroke-width="3.6"/>'
            f'<ellipse cx="0" cy="-88" rx="11" ry="7.5" fill="{p["belly"]}"/>{look}'
            f'<path d="M-2.8 -92h5.6l-2.8 3.2Z" fill="{p["warm"]}" stroke="{p["dark"]}" stroke-width="1.1" stroke-linejoin="round"/>'
            f'<path class="s" d="M0 -88.6q-3 3.6 -6.4 1.4M0 -88.6q3 3.6 6.4 1.4M-25 -92l-13 -3M-25 -87l-13 2M25 -92l13 -3M25 -87l13 2" stroke="{p["dark"]}" stroke-width="1.4"/>', (-52, -124))


def sit_lion(ink, asleep=False):
    p, w = ink.p, 2.6
    mane = smooth([(math.cos(a) * (41 if k % 2 == 0 else 34), -100 + math.sin(a) * (41 if k % 2 == 0 else 34)) for k, a in ((k, k * math.pi / 10) for k in range(20))], closed=True)
    inner = smooth([(math.cos(a) * (31 if k % 2 == 0 else 27), -100 + math.sin(a) * (31 if k % 2 == 0 else 27)) for k, a in ((k, k * math.pi / 8 + .2) for k in range(16))], closed=True)
    look = (f'<path class="s" d="M-13 -103q4 4 8 0M5 -103q4 4 8 0" stroke="{p["dark"]}" stroke-width="2.1"/>' if asleep else
            f'<g class="blink"><circle cx="-9" cy="-104" r="3" fill="{p["dark"]}"/><circle cx="9" cy="-104" r="3" fill="{p["dark"]}"/>'
            f'<circle cx="-8" cy="-105.2" r="1" fill="{p["belly"]}"/><circle cx="10" cy="-105.2" r="1" fill="{p["belly"]}"/></g>')
    return (f'<g class="tl" style="transform-origin:30px -8px"><path class="s" d="M30 -8C56 -6 70 -26 64 -50" stroke="{p["ink"]}" stroke-width="7.5"/><path class="s" d="M30 -8C56 -6 70 -26 64 -50" stroke="{p["fur"]}" stroke-width="3.6"/>'
            f'<path d="M64 -50C54 -58 56 -74 66 -74C76 -74 78 -58 64 -50Z" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/></g>'
            + sit_body(p, w)
            + f'<path d="{mane}" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="{inner}" fill="{mix(p["fur2"], p["fur"], .45)}"/>'
            f'<circle cx="-19" cy="-121" r="7.5" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2"/><circle cx="19" cy="-121" r="7.5" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2"/>'
            f'<circle cx="0" cy="-100" r="24" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}"/>'
            f'<ellipse cx="0" cy="-90" rx="12" ry="8.5" fill="{p["belly"]}"/>{look}'
            f'<path d="M-4.6 -95h9.2l-4.6 5Z" fill="{p["dark"]}" stroke="{p["dark"]}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path class="s" d="M0 -90q-4 5 -8.4 2M0 -90q4 5 8.4 2" stroke="{p["dark"]}" stroke-width="1.6"/>'
            f'<circle cx="-13" cy="-90" r=".9" fill="{p["dark"]}"/><circle cx="-11" cy="-87" r=".9" fill="{p["dark"]}"/><circle cx="13" cy="-90" r=".9" fill="{p["dark"]}"/><circle cx="11" cy="-87" r=".9" fill="{p["dark"]}"/>', (-60, -128))


SITTERS = dict(fox=sit_fox, cat=sit_cat, lion=sit_lion)


def sitter(ink, x, y, at, k=1.0, flip=False, shade=True):
    """The theme's animal sitting up at (x, y), awake, with its shadow under it."""
    art, _ = (SITTERS.get(ink.theme) or ANIMALS[ink.theme])(ink, False)
    if shade:
        shadow(ink, x + 6 * k, y + 2, 52 * k, at)
    ink.add(f'<g transform="translate({f(x)} {f(y)}) scale({f(-k if flip else k)} {f(k)})"><g class="i" style="animation-delay:{at:.2f}s">{art}</g></g>')

# ── the seven lands ──


def land_fox(ink):
    p, rng = ink.p, ink.rng
    HZ = 214                                         # the horizon
    # far away: islands in the haze, a lighthouse on one
    band(ink, [(380, HZ), (470, HZ - 22), (590, HZ - 40), (700, HZ - 24), (800, HZ - 34), (930, HZ)], mix(p["leaf"][1], p["bg"], .62), .3)
    band(ink, [(1880, HZ), (1960, HZ - 26), (2060, HZ - 44), (2170, HZ - 22), (2260, HZ)], mix(p["leaf"][1], p["bg"], .5), .4)
    tower = "M2050 170L2046 104L2074 104L2070 170Z"
    ink.shape(tower, p["paper"], .9, 2)
    ink.fill("M2047 122L2073 122L2072 138L2048 138Z", p["warm"], 1.2)
    ink.shape("M2042 104L2060 84L2078 104Z", p["warm"], 1.1, 2)
    ink.add(f'<g class="glow"><path class="i" d="M2060 96L1880 60L1880 132Z" fill="{ink.gradient([(0, p["marker"], .0), (1, p["marker"], .75)], 0, 0, 1, 0)}" style="animation-delay:1.6s"/>'
            f'<circle class="i" cx="2060" cy="96" r="6" fill="{p["marker"]}" stroke="{p["ink"]}" stroke-width="1.6" style="animation-delay:1.4s"/></g>')
    # the sea, pale at the horizon and deep in front
    sea = ink.gradient([(0, p["wash"], 1), (.45, p["deep"], 1), (1, mix(p["deep"], p["accent"], .38), 1)])
    top = wave(rng, -40, LW + 40, HZ, 3.5, 150, .8)
    ink.add(f'<g class="wv" style="animation-duration:11s"><path class="i" d="{smooth(top)}L{LW + 40} {LH + 20}L-40 {LH + 20}Z" fill="{sea}" style="animation-delay:.3s"/>{ink.line(smooth(top), .1, 1.6, 2.4)}</g>')
    for k, (yy, amp, span, op, wd) in enumerate(((236, 2.5, 90, ".3", 1.5), (262, 3.5, 110, ".34", 1.7), (300, 5, 130, ".4", 1.9), (348, 6, 150, ".45", 2.1))):
        x = -40
        while x < LW:
            ln = rng.uniform(140, 320) * (1 + k * .25)
            ink.add(f'<g class="wv" style="animation-duration:{7 + k * 1.5:.1f}s;animation-delay:-{rng.uniform(0, 6):.1f}s">{ink.line(smooth(wave(rng, x, x + ln, yy + rng.uniform(-6, 6), amp, span * .6)), .8 + k * .15, .6, wd, None, op)}</g>')
            x += ln + rng.uniform(90, 260)
    for _ in range(34):                              # light on the water
        x, y = rng.uniform(980, 1500), rng.uniform(222, 290)
        ink.add(f'<g transform="translate({f(x)} {f(y)})"><g class="tw" style="animation-duration:{rng.uniform(1.6, 3.4):.1f}s;animation-delay:-{rng.uniform(0, 3):.1f}s">'
                f'<path class="i s" d="M-{f(rng.uniform(6, 16))} 0L{f(rng.uniform(6, 16))} 0" stroke="{p["paper"]}" stroke-width="2.4" style="animation-delay:1.2s"/></g></g>')
    # a sail far out, a buoy nearer
    ink.add(f'<g class="i" style="animation-delay:1.3s"><g class="bob" style="animation-duration:5s"><path d="M1236 212L1236 176L1262 208Z" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M1220 212L1270 212L1262 221L1228 221Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.8" stroke-linejoin="round"/></g></g>')
    ink.add(f'<g transform="translate(1004 318)"><g class="i" style="animation-delay:1.5s"><g class="bob"><path d="M-13 0L-9 -30L9 -30L13 0Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M-11 -14L11 -14L10 -22L-10 -22Z" fill="{p["paper"]}"/><path class="s" d="M0 -30L0 -44" stroke="{p["ink"]}" stroke-width="2.2"/><circle cx="0" cy="-48" r="5" fill="{p["marker"]}" stroke="{p["ink"]}" stroke-width="1.8"/></g></g></g>')
    # the boat, the fox aboard, and its reflection
    for k in range(4):
        ink.stroke(smooth(wave(rng, MX - 90 + k * 14, MX + 96 - k * 12, 322 + k * 13, 2.4, 44, .5)), 1.9 + k * .1, .4, 2.2, p["fur2"], ".42")
    boat(ink, MX, 296, 1.7, k=2.05)
    # a fish leaping
    flyer(ink, "M700 330Q790 190 880 330", 4, 7, f'<g transform="scale(1.5)">{fish_shape(p, p["warm"])}</g>')
    # rocks in front with sea grass, and the nearest waves breaking white
    for x, s in ((300, 54), (392, 34), (2080, 60), (2188, 38), (1180, 26)):
        rock(ink, x, 470 + rng.uniform(-8, 10), s, 1.0 + x / 3000)
    for gx, lf in ((250, 34), (350, 28), (440, 22), (2030, 34), (2140, 28), (2240, 24)):
        ink.vine([(gx, LH + 14), (gx + rng.uniform(-10, 10), 470), (gx + rng.uniform(-14, 14), 414)], at=1.3, speed=120, leaf=lf, sway=4, side=rng.choice((-1, 1)),
                 curl=0, width=2.3, gap=(17, 24), first=10, taper=.7, lean=(22, 44), extra=.25)
    front = wave(rng, -40, LW + 40, 478, 9, 190)
    ink.add(f'<g class="wv" style="animation-duration:6s"><path class="i" d="{smooth(front)}L{LW + 40} {LH + 20}L-40 {LH + 20}Z" fill="{mix(p["deep"], p["accent"], .5)}" fill-opacity=".8" style="animation-delay:.9s"/>'
            f'{ink.line(smooth(front), .7, 1.4, 2.6)}{ink.line(smooth([(a, b + 9) for a, b in front]), 1.1, 1.2, 3, p["paper"], ".7")}</g>')


def land_cat(ink):
    p, rng = ink.p, ink.rng
    band(ink, wave(rng, -40, LW + 40, 196, 20, 520), mix(p["leaf"][1], p["bg"], .7), .2)
    for x in (260, 420, 980, 1150, 1960, 2140):
        tree(ink, x, 214 + rng.uniform(-6, 8), rng.uniform(60, 84), .5, far=.62)
    band(ink, wave(rng, -40, LW + 40, 250, 16, 420), mix(p["leaf"][0], p["bg"], .4), .35)
    tree(ink, 640, 392, 330, .9)
    # a swing on the big tree
    ink.add(f'<g transform="translate(700 196)"><g class="i" style="animation-delay:1.8s"><g class="swing" style="transform-origin:0 0">'
            f'<path class="s" d="M-16 0L-16 122M16 0L16 122" stroke="{p["ink"]}" stroke-width="2"/><path d="M-24 122L24 122L24 131L-24 131Z" fill="{p["fur2"]}" stroke="{p["ink"]}" stroke-width="2" stroke-linejoin="round"/></g></g></g>')
    tree(ink, 2040, 380, 236, 1.1, p["leaf"][0])
    # the fence, ivy climbing it
    for x in range(820, 1980, 30):
        if 1500 < x < 1680:
            continue
        hh = 74 + rng.uniform(-4, 4)
        ink.pop(x, 372, f'<path d="M-8 0L-8 {f(-hh + 9)}L0 {f(-hh)}L8 {f(-hh + 9)}L8 0Z" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="2" stroke-linejoin="round"/>', 1.0 + x / 3000)
    ink.stroke(smooth(hand_line(rng, (810, 322), (1500, 322), 1.2, 80)), 1.4, .7, 2.2)
    ink.stroke(smooth(hand_line(rng, (1680, 322), (1990, 322), 1.2, 80)), 1.5, .5, 2.2)
    ink.vine([(840, 372), (870, 320), (960, 300), (1080, 316), (1190, 296), (1300, 312)], at=1.5, speed=300, leaf=30, sway=4, side=-1, curl=1, width=2.3, gap=(44, 64), extra=.3, stalk=.45)
    ink.vine([(1960, 372), (1930, 318), (1850, 302), (1760, 314)], at=1.7, speed=260, leaf=28, sway=4, side=1, curl=-1, width=2.3, gap=(40, 60), extra=.3, stalk=.45)
    for x, s in ((930, 34), (1290, 40), (1780, 36), (2240, 44), (330, 46)):
        bush(ink, x, 396 + rng.uniform(-4, 6), s, 1.3, berries=x % 3 == 0)
    # the lawn in front, full of flowers
    band(ink, wave(rng, -40, LW + 40, 392, 7, 300), ink.gradient([(0, p["wash"], 1), (1, p["deep"], 1)]), .5, outline=True, width=2.6)
    grasses(ink, 30, LW - 30, 398, 1.2, 52, (18, 34))
    colors = [p["warm"], p["marker"], p["belly"], p["accent"]]
    for x in list(range(120, 1440, 86)) + list(range(1760, 2330, 90)):
        flower(ink, x + rng.uniform(-24, 24), 410 + rng.uniform(-4, 30), rng.uniform(28, 52), 1.6 + rng.uniform(0, .8), rng.choice(colors))
    for x in (1120, 1264):                           # flower pots
        ink.pop(x, 452, f'<path d="M-17 0L-21 -30L21 -30L17 0Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/><path d="M-24 -30L24 -30L24 -38L-24 -38Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>', 1.7)
        flower(ink, x - 8, 414, 34, 2.0, p["marker"]), flower(ink, x + 9, 414, 44, 2.1, p["belly"])
    for a, b, c in ((300, 1100, 300), (1250, 2100, 270)):
        flyer(ink, smooth(wave(rng, a, b, c, 22, 170)), 3 + a / 900, 26 + a / 200, butterfly(p))
    sitter(ink, MX, 430, 1.9, k=1.75)


def land_lion(ink):
    p, rng = ink.p, ink.rng
    HZ = 256
    # the sun going down behind the plain, a far mountain with snow on it
    glow = ink.gradient([(0, p.get("glow", p["marker"]), .95), (.55, p.get("glow", p["marker"]), .35), (1, p.get("glow", p["marker"]), 0)], radial=True)
    ink.add(f'<circle class="i" cx="930" cy="{HZ - 14}" r="250" fill="{glow}" style="animation-delay:.2s"/>')
    ink.add(f'<g transform="translate(930 {HZ - 14})"><g class="spin"><path class="i s" d="{"".join(f"M{f(math.cos(a) * 124)} {f(math.sin(a) * 124)}L{f(math.cos(a) * (150 if k % 2 else 138))} {f(math.sin(a) * (150 if k % 2 else 138))}" for k, a in ((k, k * math.pi / 12) for k in range(24)))}" stroke="{p["ink"]}" stroke-width="2.2" stroke-opacity=".7" style="animation-delay:.9s"/></g>'
            f'<path class="i" d="{circle_path(0, 0, 108, rng, 14, .02)}" fill="{p.get("glow", p["marker"])}" style="animation-delay:.3s"/>{ink.line(circle_path(0, 0, 108, rng, 14, .02), .2, 1.3, 2.6)}</g>')
    mtn = "M1440 256L1560 178L1640 142L1820 138L1900 174L2060 256Z"
    ink.fill(mtn, mix(p["fur2"], p["bg"], .62), .4)
    ink.fill("M1640 142L1820 138L1856 154L1800 150L1770 164L1730 152L1690 166L1664 152L1618 154Z", p["belly"], .7)
    ink.stroke("M1440 256L1560 178L1640 142L1820 138L1900 174L2060 256", .4, 1.4, 2, opacity=".5")
    band(ink, wave(rng, -40, LW + 40, HZ, 4, 480), mix(p["leaf"][1], p["bg"], .45), .4, outline=".7")
    for x, hh in ((330, 96), (1260, 78), (1420, 60), (2230, 104)):
        flat_tree(ink, x, HZ + 14, hh, .8, far=.42)
    band(ink, wave(rng, -40, LW + 40, 300, 6, 420), ink.gradient([(0, p["wash"], 1), (1, p["deep"], 1)]), .6)
    flat_tree(ink, 560, 392, 250, 1.0)
    flat_tree(ink, 2060, 398, 280, 1.2)
    # the rock the lion sits on
    for x, y, s in ((MX - 110, 430, 62), (MX + 110, 432, 70), (MX, 426, 104)):
        rock(ink, x, y, s, 1.3, mix(p["fur2"], p["bg"], .55))
    band(ink, wave(rng, -40, LW + 40, 420, 8, 340), p["deep"], .8, outline=True, width=2.6)
    grasses(ink, 20, MX - 190, 428, 1.3, 58, (26, 56), wave_y=4), grasses(ink, MX + 200, LW - 20, 428, 1.3, 58, (26, 56), wave_y=4)
    grasses(ink, 20, LW - 20, 478, 1.5, 76, (34, 68))
    for x in (700, 1240, 1900):
        ink.extra(x, 380, 2.2, 2)
    for k, (a, b) in enumerate(((120, 150), (200, 120))):
        flyer(ink, smooth(wave(rng, -40, LW + 40, a, 16, 300)), 3 + k * 6, 46 + k * 9, flying_bird(p))
    sitter(ink, MX, 350, 2.0, k=1.7)


def land_owl(ink):
    p, rng = ink.p, ink.rng
    mountains(ink, -40, LW + 40, 270, 150, 240, mix(p["leaf"][2], p["bg"], .45), .2, snow=p["belly"])
    ink.add(f'<rect class="i" x="-40" y="190" width="{LW + 80}" height="110" fill="{ink.gradient([(0, p["bg"], 0), (.6, p["bg"], .75), (1, p["bg"], 0)])}" style="animation-delay:.6s"/>')
    mountains(ink, -40, LW + 40, 300, 96, 180, mix(p["leaf"][0], p["bg"], .3), .4)
    x = 10
    while x < LW:                                    # the far wood
        fir(ink, x, 318 + rng.uniform(-6, 8), rng.uniform(70, 124), .6 + rng.uniform(0, .5), far=.45)
        x += rng.uniform(34, 70)
    band(ink, wave(rng, -40, LW + 40, 318, 12, 520), mix(p["leaf"][2], p["bg"], .35), .7)
    # a cabin with a light on, smoke from its chimney
    hx, hy = 690, 392
    ink.shape(f"M{hx - 70} {hy}L{hx - 70} {hy - 62}L{hx + 70} {hy - 62}L{hx + 70} {hy}Z", p["fur2"], 1.0, 2.4)
    ink.shape(f"M{hx - 86} {hy - 58}L{hx} {hy - 122}L{hx + 86} {hy - 58}Z", mix(p["fur2"], p["ink"], .35), 1.1, 2.4)
    ink.shape(f"M{hx + 34} {hy - 96}L{hx + 34} {hy - 132}L{hx + 54} {hy - 132}L{hx + 54} {hy - 82}Z", p["fur2"], 1.2, 2.2)
    ink.add(f'<g class="glow"><circle class="i" cx="{hx - 30}" cy="{hy - 32}" r="52" fill="{ink.gradient([(0, p["warm"], .55), (1, p["warm"], 0)], radial=True)}" style="animation-delay:1.6s"/>'
            f'<path class="i" d="M{hx - 46} {hy - 16}L{hx - 46} {hy - 48}L{hx - 14} {hy - 48}L{hx - 14} {hy - 16}Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2" style="animation-delay:1.5s"/></g>')
    ink.stroke(f"M{hx - 30} {hy - 16}L{hx - 30} {hy - 48}M{hx - 46} {hy - 32}L{hx - 14} {hy - 32}", 1.7, .3, 1.6)
    ink.shape(f"M{hx + 14} {hy}L{hx + 14} {hy - 44}L{hx + 44} {hy - 44}L{hx + 44} {hy}Z", mix(p["fur2"], p["ink"], .4), 1.4, 2.2)
    for k in range(3):
        ink.add(f'<g transform="translate({hx + 44 + k * 4} {hy - 140 - k * 22})"><g class="bb" style="animation-duration:{5 + k:.1f}s;animation-delay:{1.8 + k * 1.4:.1f}s">'
                f'<path class="s" d="M0 0q9 -8 0 -16q-9 -8 0 -16" stroke="{p["soft"]}" stroke-width="2.4" stroke-opacity=".7"/></g></g>')
    for x, hh in ((180, 250), (300, 190), (410, 150), (500, 110), (880, 170), (980, 120), (2260, 240), (2150, 170)):
        fir(ink, x, 404 + rng.uniform(-4, 8), hh, 1.0 + x / 4000)
    # the old tree on the right, a branch of it for the owl
    trunk = f"M1800 {LH + 20}C1790 420 1808 300 1790 170C1786 110 1800 60 1808 -20L1900 -20C1890 60 1904 130 1900 200C1896 300 1916 420 1910 {LH + 20}Z"
    ink.shape(trunk, mix(p["fur2"], p["ink"], .28), .9, 2.8, 1.4)
    ink.stroke("M1826 110C1822 180 1836 260 1828 380M1868 100C1876 160 1862 240 1874 420M1846 200q6 20 0 44", 1.6, 1, 1.8, opacity=".45")
    for cx, cy, rx, ry in ((1700, 96, 150, 84), (1990, 104, 170, 92), (1850, 60, 190, 96), (1770, 150, 110, 56), (1950, 164, 120, 56)):
        d = blob(ink, cx, cy, rx, ry, 12, .12)
        ink.fill(d, mix(mix(p["leaf"][2], p["ink"], .12), p["bg"], .3 if ink.mode == "dark" else 0), 1.5)
        ink.fill(blob(ink, cx + rx * .25, cy + ry * .3, rx * .66, ry * .6), p["ink"], 1.7, ".12")
        ink.stroke(d, 1.3, 1.1, 2.5)
    branch = "M1800 262C1730 250 1660 262 1590 252C1540 246 1500 256 1450 246L1452 236C1500 244 1540 234 1592 240C1660 248 1730 236 1800 244Z"
    ink.shape(branch, mix(p["fur2"], p["ink"], .28), 1.2, 2.6)
    for bx, by, ang in ((1470, 240, -70), (1520, 244, -110), (1660, 248, -60), (1720, 244, -120), (1500, 250, 80), (1700, 258, 70)):
        outline, veins = ink.leaf(rng.uniform(24, 34), "round")
        ink.pop(bx, by, f'<path d="{outline}" fill="{rng.choice(p["leaf"])}" stroke="{p["ink"]}" stroke-width="1.8"/><path class="s" d="{veins}" stroke="{p["ink"]}" stroke-width="1" stroke-opacity=".6"/>', 1.8, ang, rng.uniform(3, 5))
    band(ink, wave(rng, -40, LW + 40, 404, 10, 420), ink.gradient([(0, p["wash"], 1), (1, p["deep"], 1)]), .8, outline=True, width=2.6)
    grasses(ink, 20, LW - 20, 410, 1.4, 60, (16, 30))
    for _ in range(46):                              # fireflies
        x, y = rng.uniform(40, LW - 40), rng.uniform(250, 470)
        ink.add(f'<g transform="translate({f(x)} {f(y)})"><g class="fly" style="animation-duration:{rng.uniform(5, 11):.1f}s;animation-delay:-{rng.uniform(0, 8):.1f}s"><g class="tw" style="animation-duration:{rng.uniform(1.4, 3):.1f}s;animation-delay:-{rng.uniform(0, 3):.1f}s">'
                f'<circle class="i" r="7" fill="{p["warm"]}" fill-opacity=".25" style="animation-delay:1.6s"/><circle class="i" r="2.6" fill="{p["warm"]}" style="animation-delay:1.6s"/></g></g></g>')
    animal(ink, MX, 239, 2.0, k=1.75)


def land_bear(ink):
    p, rng = ink.p, ink.rng
    mountains(ink, -40, LW + 40, 250, 170, 300, mix(p["soft"], p["bg"], .62), .2, snow=p["paper"])
    ink.add(f'<rect class="i" x="-40" y="170" width="{LW + 80}" height="110" fill="{ink.gradient([(0, p["bg"], 0), (.6, p["bg"], .7), (1, p["bg"], 0)])}" style="animation-delay:.6s"/>')
    x = 0
    while x < LW:
        fir(ink, x, 286 + rng.uniform(-8, 8), rng.uniform(80, 150), .5 + rng.uniform(0, .5), far=.5)
        x += rng.uniform(30, 64)
    band(ink, wave(rng, -40, LW + 40, 286, 12, 520), mix(p["leaf"][1], p["bg"], .35), .6)
    x = 0
    while x < LW:
        if not 1160 < x < 1400:
            fir(ink, x, 340 + rng.uniform(-8, 10), rng.uniform(120, 210), .8 + rng.uniform(0, .5), far=.2)
        x += rng.uniform(60, 120)
    band(ink, wave(rng, -40, LW + 40, 344, 10, 460), ink.gradient([(0, p["wash"], 1), (1, p["deep"], 1)]), .9, outline=True, width=2.6)
    # a stream coming down through the meadow
    water = mix(THEMES["fox"][ink.mode]["deep"], p["bg"], .15)
    stream = "M1250 344C1290 370 1210 392 1250 420C1300 452 1190 478 1140 540L1420 540C1400 480 1390 452 1350 424C1310 396 1340 372 1300 344Z"
    ink.shape(stream, water, 1.1, 2.4, 1.3)
    for a, b, c in ((1256, 380, 40), (1270, 430, 60), (1230, 480, 90)):
        ink.add(f'<g class="wv" style="animation-duration:4s">{ink.line(smooth(wave(rng, a, a + c, b, 2.5, 30, .4)), 1.8, .4, 1.8, p["paper"], ".8")}</g>')
    for x, y, s in ((1226, 420, 20), (1372, 446, 26), (1190, 500, 30), (1400, 500, 22)):
        rock(ink, x, y, s, 1.6)
    for x, hh in ((150, 280), (300, 200), (2250, 300), (2110, 210), (1960, 150)):
        fir(ink, x, 420 + rng.uniform(-4, 10), hh, 1.1)
    # a fallen log, mushrooms, ferns
    ink.shape("M640 436C640 410 664 404 690 404L900 408C924 408 934 420 934 436C934 452 922 462 900 462L690 462C660 462 640 458 640 436Z", p["fur2"], 1.4, 2.5)
    ink.shape("M880 435A20 27 0 1 0 920 435A20 27 0 1 0 880 435Z", p["belly"], 1.5, 2.2)
    ink.stroke("M889 435A11 15 0 1 0 911 435A11 15 0 1 0 889 435M700 420L790 424M720 446L840 448", 1.8, .5, 1.5, opacity=".5")
    for x in (560, 620, 960, 1060, 1500, 1740, 1820):
        s = rng.uniform(.9, 1.5)
        ink.pop(x, 452 + rng.uniform(-4, 14), f'<g transform="scale({f(s)})"><path d="M-3 0L-3 -10L3 -10L3 0Z" fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="1.6" stroke-linejoin="round"/>'
                f'<path d="M-12 -10C-12 -23 12 -23 12 -10Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.8" stroke-linejoin="round"/>'
                f'<circle cx="-4" cy="-15" r="1.7" fill="{p["belly"]}"/><circle cx="4" cy="-14" r="1.4" fill="{p["belly"]}"/></g>', 1.9)
    for x in (480, 1010, 1470, 1700, 1880, 2020):
        for k in range(5):
            outline, veins = ink.leaf(rng.uniform(34, 54), "fern")
            ink.pop(x, 456 + rng.uniform(-4, 10), f'<path d="{outline}" fill="{rng.choice(p["leaf"])}" stroke="{p["ink"]}" stroke-width="1.5" stroke-linejoin="round"/><path class="s" d="{veins}" stroke="{p["ink"]}" stroke-width="1.4"/>',
                    1.7, -90 + (k - 2) * 26 + rng.uniform(-8, 8), rng.uniform(3, 5))
    bush(ink, 1760, 440, 44, 1.6, berries=True), bush(ink, 400, 446, 50, 1.6, berries=True)
    grasses(ink, 20, 1130, 462, 1.6, 64, (16, 30)), grasses(ink, 1430, LW - 20, 462, 1.6, 64, (16, 30))
    flyer(ink, smooth(wave(rng, -40, LW + 40, 130, 14, 280)), 4, 50, flying_bird(p))
    sitter(ink, MX, 448, 2.0, k=1.72)


def land_penguin(ink):
    p, rng = ink.p, ink.rng
    ice, blue = p["paper"], mix(p["leaf"][1], p["bg"], .2)
    mountains(ink, -40, LW + 40, 236, 150, 260, mix(p["leaf"][0], p["bg"], .4), .2, snow=ice)
    # the sea between, ice drifting on it
    sea = ink.gradient([(0, mix(p["accent"], p["bg"], .55), 1), (1, mix(p["accent"], p["ink"], .25), 1)])
    ink.fill(f"M-40 236L{LW + 40} 236L{LW + 40} 330L-40 330Z", sea, .4)
    ink.stroke(smooth(hand_line(rng, (-40, 236), (LW + 40, 236), 1, 200)), .3, 1.4, 2.2)
    for k in range(3):
        x = -40
        while x < LW:
            ln = rng.uniform(100, 260)
            ink.add(f'<g class="wv" style="animation-duration:{8 + k * 2}s;animation-delay:-{rng.uniform(0, 6):.1f}s">{ink.line(smooth(wave(rng, x, x + ln, 254 + k * 24, 2.5, 60, .4)), 1, .5, 1.6, p["paper"], ".55")}</g>')
            x += ln + rng.uniform(120, 300)
    for x, w in ((230, 80), (560, 50), (1010, 96), (1380, 60), (2010, 90), (2250, 54)):
        y = rng.uniform(262, 300)
        ink.add(f'<g class="bob" style="animation-duration:{rng.uniform(4, 7):.1f}s"><path class="i" d="M{x - w} {f(y)}L{f(x - w * .6)} {f(y - 9)}L{f(x + w * .7)} {f(y - 10)}L{x + w} {f(y)}L{f(x + w * .6)} {f(y + 7)}L{f(x - w * .7)} {f(y + 7)}Z" fill="{ice}" stroke="{p["ink"]}" stroke-width="1.8" stroke-linejoin="round" style="animation-delay:1.2s"/></g>')
    # two great icebergs
    for bx, s, at in ((480, 1.0, .9), (2120, .82, 1.1)):
        pts = [(-150, 0), (-120, -70), (-70, -110), (-40, -84), (10, -168), (60, -120), (90, -140), (150, -40), (170, 0)]
        d = "M" + "L".join(f"{f(bx + a * s)} {f(318 + b * s)}" for a, b in pts) + "Z"
        ink.fill(d, ink.gradient([(0, ice, 1), (1, blue, 1)]), at + .2)
        ink.fill("M" + "L".join(f"{f(bx + a * s)} {f(318 + b * s)}" for a, b in ((10, -168), (60, -120), (90, -140), (150, -40), (170, 0), (40, 0), (30, -90))) + "Z", p["ink"], at + .4, ".09")
        ink.stroke(d, at, 1.3, 2.4)
        ink.stroke(f"M{f(bx - 70 * s)} {f(318 - 110 * s)}L{f(bx - 50 * s)} 318M{f(bx + 10 * s)} {f(318 - 168 * s)}L{f(bx + 30 * s)} {f(318 - 60 * s)}L{f(bx + 20 * s)} 318", at + .8, .6, 1.5, opacity=".4")
    # the snow in front
    band(ink, wave(rng, -40, LW + 40, 336, 16, 520), ink.gradient([(0, ice, 1), (1, p["wash"], 1)]), .7, outline=True, width=2.6)
    band(ink, wave(rng, -40, LW + 40, 420, 14, 440), ink.gradient([(0, p["wash"], 1), (1, p["deep"], 1)]), .9, outline=".5")
    # an igloo
    ix, iy = 800, 404
    dome = f"M{ix - 96} {iy}C{ix - 96} {iy - 112} {ix + 96} {iy - 112} {ix + 96} {iy}Z"
    shadow(ink, ix + 14, iy + 3, 116, 1.2)
    ink.fill(dome, ink.gradient([(0, ice, 1), (1, blue, 1)], 0, 0, 1, 1), 1.3)
    ink.stroke(dome, 1.1, 1, 2.6)
    ink.stroke(f"M{ix - 88} {iy - 34}L{ix + 88} {iy - 34}M{ix - 66} {iy - 62}L{ix + 66} {iy - 62}M{ix - 50} {iy}L{ix - 50} {iy - 34}M{ix} {iy - 34}L{ix} {iy - 62}M{ix + 50} {iy}L{ix + 50} {iy - 34}M{ix - 26} {iy - 62}L{ix - 26} {iy - 78}M{ix + 28} {iy - 62}L{ix + 28} {iy - 78}",
               1.8, .8, 1.5, opacity=".42")
    ink.shape(f"M{ix - 30} {iy}C{ix - 30} {iy - 46} {ix + 30} {iy - 46} {ix + 30} {iy}Z", mix(p["ink"], p["bg"], .3), 1.6, 2.4)
    # a hole in the ice and a flag
    ink.shape("M1250 452A46 13 0 1 0 1342 452A46 13 0 1 0 1250 452Z", mix(p["accent"], p["ink"], .2), 1.6, 2.2)
    flyer(ink, "M1296 452Q1310 380 1296 452", 5, 5, f'<g transform="rotate(-90) scale(1.1)">{fish_shape(p, p["warm"])}</g>')
    ink.stroke("M1150 450L1150 366", 1.8, .4, 2.4)
    ink.add(f'<g class="i" style="animation-delay:2s"><path class="sw" style="transform-origin:1150px 380px" d="M1150 366L1196 378L1150 392Z" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="2" stroke-linejoin="round"/></g>')
    for _ in range(70):
        ink.extra(rng.uniform(20, LW - 20), rng.uniform(-30, 330), .6, 1)
    sitter(ink, MX, 430, 2.0, k=1.8)
    sitter(ink, MX + 104, 440, 2.2, k=1.05, flip=True)
    sitter(ink, MX - 104, 444, 2.3, k=.9)


def land_tortoise(ink):
    p, rng = ink.p, ink.rng
    rockc = mix(p["accent"], p["bg"], .55)
    # mesas far off, in the heat
    for x, w, h, at in ((330, 260, 150, .2), (700, 150, 110, .3), (1320, 320, 130, .25), (1960, 200, 170, .3), (2240, 130, 100, .35)):
        d = (f"M{x - w * .62} 250L{x - w * .5} {250 - h * .3}L{x - w * .42} {250 - h * .34}L{x - w * .4} {250 - h}L{x + w * .38} {250 - h * 1.02}L{x + w * .42} {250 - h * .36}"
             f"L{x + w * .52} {250 - h * .3}L{x + w * .64} 250Z")
        ink.fill(d, mix(rockc, p["bg"], .25), at)
        ink.fill(f"M{x + w * .1} {250 - h}L{x + w * .38} {250 - h * 1.02}L{x + w * .42} {250 - h * .36}L{x + w * .52} {250 - h * .3}L{x + w * .64} 250L{x + w * .2} 250Z", p["ink"], at + .3, ".08")
        ink.stroke(d, at, 1.3, 2, opacity=".5")
        for k in range(1, 4):
            ink.stroke(smooth(hand_line(rng, (x - w * .4, 250 - h * (1 - k * .22)), (x + w * .4, 250 - h * (1.01 - k * .22)), .8, 60)), at + .6, .5, 1.2, opacity=".28")
    ink.add(f'<rect class="i" x="-40" y="190" width="{LW + 80}" height="80" fill="{ink.gradient([(0, p["bg"], 0), (.7, p["bg"], .7), (1, p["bg"], 0)])}" style="animation-delay:.6s"/>')
    band(ink, wave(rng, -40, LW + 40, 252, 14, 760), mix(p["deep"], p["bg"], .3), .4, outline=".5")
    dune = ink.gradient([(0, p["wash"], 1), (1, p["deep"], 1)])
    band(ink, wave(rng, -40, LW + 40, 316, 26, 900), dune, .6, outline=".7")
    for a, b, c in ((200, 700, 344), (1000, 1500, 356), (1750, 2250, 340)):
        for k in range(3):
            ink.stroke(smooth(wave(rng, a + k * 40, b - k * 60, c + k * 16, 4, 220, .6)), 1.2 + k * .1, .7, 1.4, opacity=".3")
    front = wave(rng, -40, LW + 40, 420, 14, 700)
    band(ink, front, ink.gradient([(0, p["deep"], 1), (1, mix(p["deep"], p["accent"], .22), 1)]), .9, outline=True, width=2.6)
    for x, y, hh, at in ((250, 428, 250, 1.2), (410, 440, 150, 1.4), (1010, 432, 190, 1.3), (2080, 430, 270, 1.3), (2230, 444, 140, 1.5), (1830, 438, 110, 1.6)):
        shadow(ink, x + hh * .18, y + 2, hh * .34, at)
        cactus(ink, x, y, hh, at)
    for x in (560, 880, 1180, 1360, 1800, 1950):     # prickly pears
        s = rng.uniform(26, 40)
        pads = "".join(f'<ellipse cx="{f(a * s)}" cy="{f(b * s)}" rx="{f(s * .42)}" ry="{f(s * .56)}" transform="rotate({r} {f(a * s)} {f(b * s)})" fill="{p["leaf"][0]}" stroke="{p["ink"]}" stroke-width="2"/>'
                       for a, b, r in ((0, -.55, 0), (-.5, -1.2, -24), (.5, -1.3, 22), (0, -1.9, 4)))
        ink.pop(x, 446 + rng.uniform(-6, 12), pads + f'<circle cx="{f(-.62 * s)}" cy="{f(-1.74 * s)}" r="{f(s * .14)}" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.3"/><circle cx="{f(.05 * s)}" cy="{f(-2.46 * s)}" r="{f(s * .14)}" fill="{p["warm"]}" stroke="{p["ink"]}" stroke-width="1.3"/>', 1.6, 0, rng.uniform(6, 9))
    for x, s in ((680, 30), (760, 18), (1330, 34), (1690, 22), (2330, 30), (120, 26)):
        rock(ink, x, 452 + rng.uniform(-6, 14), s, 1.6, rockc)
    grasses(ink, 40, LW - 40, 452, 1.7, 110, (16, 28))
    # a tumbleweed going by
    weed = "".join(f'<path class="s" d="{circle_path(rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(9, 17), rng, 8, .2)}" stroke="{p["fur2"]}" stroke-width="1.5"/>' for _ in range(5))
    ink.add(f'<g opacity="0"><g><g>{weed}<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="2.4s" repeatCount="indefinite"/></g></g>'
            f'<animateMotion path="M-60 400Q300 380 700 404T1500 396T{LW + 60} 404" dur="34s" begin="4s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.03;0.97;1" dur="34s" begin="4s" repeatCount="indefinite"/></g>')
    flyer(ink, smooth(wave(rng, -40, LW + 40, 110, 14, 300)), 5, 52, flying_bird(p))
    shadow(ink, MX + 8, 440, 110, 1.9)
    animal(ink, MX, 438, 2.0, k=2.0)


LANDS = dict(fox=land_fox, cat=land_cat, lion=land_lion, owl=land_owl, bear=land_bear, penguin=land_penguin, tortoise=land_tortoise)

# ── the two corners of the sky ──


def sky(ink, right):
    """What is in the sky beside the name: one picture for the left corner, one for the right."""
    p, rng, th, w, h = ink.p, ink.rng, ink.theme, ink.w, ink.h
    X = (lambda v: w - v) if right else (lambda v: v)
    if th == "fox":
        if right:
            cloud(ink, X(150), 86, 1.15, .3), cloud(ink, X(280), 190, .7, .6)
            bird(ink, X(70), 190, 1, 1), bird(ink, X(120), 228, .7, 1.2), bird(ink, X(250), 64, .6, 1.3)
        else:
            sun(ink, 110, 104, 50, .3)
            cloud(ink, 250, 170, .9, .7), bird(ink, 300, 70, .8, 1.2)
    elif th == "cat":
        guide = [(X(-10), -10), (X(70), 40), (X(150), 34), (X(210), 90), (X(190), 170), (X(240), 230)] if not right else [(X(-10), -10), (X(60), 60), (X(130), 70), (X(170), 140), (X(140), 220)]
        ink.vine(guide, at=.3, speed=300, leaf=36, sway=6, side=1 if right else -1, curl=-1 if right else 1, width=2.8, gap=(46, 70), extra=.35, first=40, stalk=.45)
        flyer(ink, smooth(wave(rng, 40, w - 40, 240, 16, 110)), 2.5, 16, butterfly(p))
    elif th == "lion":
        cloud(ink, X(140), 80, 1.0, .3), cloud(ink, X(270), 170, .66, .6)
        for k in range(5):
            bird(ink, X(70 + k * 44), 180 + (k % 3) * 22 - k * 6, .9 - k * .08, 1 + k * .1)
    elif th == "owl":
        if right:
            ink.add(f'<circle class="i" cx="{w - 140}" cy="110" r="130" fill="{ink.gradient([(0, p.get("glow", p["marker"]), .5), (1, p.get("glow", p["marker"]), 0)], radial=True)}" style="animation-delay:.3s"/>')
            moon(ink, w - 140, 110, 56, .3)
        for _ in range(26 if not right else 16):
            x, y = rng.uniform(14, w - 14), rng.uniform(14, h - 14)
            if right and math.hypot(x - (w - 140), y - 110) < 86:
                continue
            star(ink, x, y, rng.uniform(3, 8), .4 + rng.uniform(0, 1.4))
        if not right:
            flyer(ink, "M20 40L330 220", 5, 13, f'<path class="s" d="M0 0L-56 0" stroke="{p["warm"]}" stroke-width="2.6"/><circle r="3.4" fill="{p["warm"]}"/>')
    elif th == "bear":
        cloud(ink, X(140), 84, 1.1, .3), cloud(ink, X(280), 180, .7, .6)
        if right:
            sun(ink, w - 96, 190, 36, .5)
        for k in range(3):
            bird(ink, X(90 + k * 60), 230 - k * 24, .9 - k * .1, 1 + k * .1)
    elif th == "penguin":
        for k in range(4):
            ink.add(f'<g class="wv" style="animation-duration:{9 + k * 2}s;animation-delay:-{k * 2}s">{ink.line(smooth(wave(rng, 10, w - 10, 50 + k * 34, 16, 150)), .3 + k * .2, 1.2, 5 - k * .6, p["leaf"][k % 3], ".85")}</g>')
        for _ in range(22):
            ink.extra(rng.uniform(10, w - 10), rng.uniform(0, h - 60), .5, 1)
    else:
        if right:
            sun(ink, w - 120, 110, 52, .3)
        else:
            cloud(ink, 150, 90, .9, .4)
        for k in range(3):
            bird(ink, X(60 + k * 70), 200 + (k % 2) * 30, .9 - k * .1, 1 + k * .15)

# ───────────────────────────── SMALL PARTS ──────────────────────────


def plants(ink):
    """What grows along the top edge of a card (the card's edge is the bottom of this picture)."""
    rng, w, h, th = ink.rng, ink.w, ink.h, ink.theme
    from_left = rng.random() < .5
    span = rng.uniform(.5, .78) * w
    x0, x1 = (16, 16 + span) if from_left else (w - 16, w - 16 - span)
    base = h - 4
    guide = [(x0, base - 2), (x0 + (x1 - x0) * .35, base - 9), (x0 + (x1 - x0) * .7, base - 3), (x1, base - 10)]
    side = -1 if from_left else 1
    if th == "cat":
        ink.vine(guide, at=.2, speed=260, leaf=27, sway=4, side=side, both=False, curl=side, width=2.2, gap=(40, 60), lean=(40, 112), first=16, extra=.3, stalk=.45)
    elif th == "fox":
        ink.vine(guide, at=.2, speed=260, leaf=31, sway=4, side=side, both=False, curl=side, width=2.2, gap=(28, 44), lean=(62, 104), first=12, extra=.28)
    elif th in ("lion", "bear", "tortoise"):
        ink.stroke(smooth(hand_line(rng, (min(x0, x1), base), (max(x0, x1), base), 1.2, 60)), .2, .6, 2.2)
        x = min(x0, x1) + 14
        while x < max(x0, x1) - 10:
            if th == "tortoise" and rng.random() < .22:
                cactus(ink, x, base, rng.uniform(26, 40), .4 + x / 900)
            elif th == "bear" and rng.random() < .3:
                pine(ink, x, base, rng.uniform(30, 46), .4 + x / 900)
            else:
                tuft(ink, x, base, .4 + x / 900, rng.uniform(16, 34) if th == "lion" else rng.uniform(12, 20), rng.choice((3, 4, 5)),
                     "grass" if th != "tortoise" else "succulent")
            x += rng.uniform(34, 70)
        if th == "lion":
            ink.extra((x0 + x1) / 2, base - 30, 1.2, 2)
    elif th == "owl":
        ink.vine(guide, at=.2, speed=260, leaf=22, sway=3, side=side, both=True, curl=side, width=2.2, gap=(34, 52), lean=(40, 80), first=16, extra=.45)
    else:                                            # penguin: snow lying on the edge, flakes falling
        mound = wave(rng, min(x0, x1), max(x0, x1), base - 8, 5, 90)
        ink.add(f'<path class="i" d="{smooth(mound)}L{f(max(x0, x1))} {base}L{f(min(x0, x1))} {base}Z" fill="{ink.p["belly"]}" style="animation-delay:.4s"/>')
        ink.stroke(smooth(mound), .2, .8, 2.2)
        for _ in range(6):
            ink.extra(rng.uniform(min(x0, x1), max(x0, x1)), rng.uniform(-10, 6), .6, 1)


def line(ink):
    """The line that runs off to the right of a heading, with something of the theme on it."""
    rng, p, w, th = ink.rng, ink.p, ink.w, ink.theme
    y = ink.h * .62
    if th == "fox":
        pts = wave(rng, 6, w - 20, y, 6, 116)
        ink.stroke(smooth(pts), .2, 1.2, 2.3)
        ink.stroke(smooth(wave(rng, 120, 280, y + 20, 3, 60)), .8, .4, 1.6, opacity=".4")
        if rng.random() < .5:
            boat(ink, rng.uniform(260, w - 200), y - 10, 1.0, crew=False, k=.5)
        else:
            flyer(ink, smooth([(q[0], q[1] + 20) for q in pts]), 1.4, 40, fish_shape(p, p["warm"]))
        ink.extra(rng.uniform(100, w - 100), y + 20, 1.2, 2)
    elif th == "cat":
        ink.vine([(6, y), (w * .25, y - 8), (w * .5, y + 4), (w * .75, y - 10), (w - 30, y - 2)], at=.2, speed=520, leaf=25,
                 sway=5, side=-1, curl=1, width=2.2, gap=(70, 116), first=40, extra=.25, stalk=.45)
    elif th == "owl":
        pts = [(6 + k * (w - 40) / 8, y + rng.uniform(-14, 14)) for k in range(9)]
        ink.stroke("M" + "L".join(f"{f(a)} {f(b)}" for a, b in pts), .2, 1.2, 1.6, opacity=".55")
        for a, b in pts:
            star(ink, a, b, rng.uniform(4, 8), .3 + a / 900)
    elif th == "penguin":
        pts = wave(rng, 6, w - 20, y + 6, 7, 170)
        ink.stroke(smooth(pts), .2, 1.2, 2.3)
        for _ in range(7):
            ink.extra(rng.uniform(20, w - 20), rng.uniform(0, y - 20), .5, 1)
    else:
        ink.stroke(smooth(hand_line(rng, (6, y + 8), (w - 20, y + 6), 1.4, 70)), .2, 1.2, 2.3)
        x = 30
        while x < w - 40:
            if th == "tortoise" and rng.random() < .25:
                cactus(ink, x, y + 7, rng.uniform(24, 36), .4 + x / 900)
            elif th == "bear" and rng.random() < .35:
                pine(ink, x, y + 7, rng.uniform(26, 40), .4 + x / 900)
            else:
                tuft(ink, x, y + 7, .4 + x / 900, rng.uniform(14, 28), rng.choice((3, 4)), "succulent" if th == "tortoise" else "grass")
            x += rng.uniform(60, 130)
        if th == "lion":
            flyer(ink, f"M0 {f(y - 26)}L{w} {f(y - 34)}", 1.5, 36, flying_bird(p))


def strip(ink):
    """The ground above the footer: the theme's land, with a few of its things on it."""
    rng, p, w, h, th = ink.rng, ink.p, ink.w, ink.h, ink.theme
    y = 96
    if th == "fox":
        top = wave(rng, -40, w + 40, y, 6, 118)
        ink.add(f'<g class="wv"><path class="i" d="{smooth(top)}L{w + 40} {h + 10}L-40 {h + 10}Z" fill="{p["wash"]}" style="animation-delay:.4s"/>{ink.line(smooth(top), .2, 1.4, 2.6)}</g>')
        for gx in (60, 130, 320, 760, 1080, 1150):
            ink.vine([(gx, h + 10), (gx + rng.uniform(-8, 8), h - 30), (gx + rng.uniform(-10, 10), y + 24)], at=.6, speed=110, leaf=24, sway=4,
                     side=rng.choice((-1, 1)), curl=0, width=2.2, gap=(16, 22), first=10, taper=.7, lean=(22, 44), extra=.3)
        flyer(ink, smooth(wave(rng, -40, w + 40, y + 44, 8, 190)), 1.5, 44, fish_shape(p, p["warm"]))
        boat(ink, 880, y - 6, 1.0, crew=False, k=.7)
        return
    ground(ink, y, .2, 6 if th != "owl" else 14, 260, layers=1)
    if th == "cat":
        for x in range(40, w, 70):
            tuft(ink, x + rng.uniform(-20, 20), y + 2, .5 + x / 1200, rng.uniform(16, 28), rng.choice((3, 4, 5)))
        ink.t = dict(ink.t, extra="flowers")
        for x in (200, 480, 720, 1010):
            ink.extra(x, y - 10, 1.2, 1)
        ink.t = THEMES[th]
    elif th == "lion":
        acacia(ink, 180, y + 2, 78, .6)
        for x in range(300, w, 64):
            tuft(ink, x + rng.uniform(-18, 18), y + 3, .5 + x / 1200, rng.uniform(20, 38), rng.choice((4, 5, 6)))
    elif th == "owl":
        for x, hh in ((60, 80), (120, 56), (1080, 70), (1140, 96)):
            pine(ink, x, y + 6, hh, .6)
        for _ in range(9):
            star(ink, rng.uniform(220, 980), rng.uniform(8, 60), rng.uniform(3, 6), .6)
    elif th == "bear":
        for x in range(30, w, 86):
            pine(ink, x + rng.uniform(-16, 16), y + 4, rng.uniform(46, 96), .5 + x / 1500)
    elif th == "penguin":
        ink.shape("M120 104L156 44L188 70L214 30L262 104Z", p["belly"], .6, 2.4)
        for _ in range(12):
            ink.extra(rng.uniform(20, w - 20), rng.uniform(-10, 50), .6, 1)
    else:
        for x, hh in ((90, 84), (170, 50), (860, 62), (1120, 90)):
            cactus(ink, x, y + 4, hh, .6)
        for x in (300, 450, 620, 1000):
            tuft(ink, x, y + 6, .8, rng.uniform(12, 20), 3, "grass")


def sleeper(ink):
    """The animal asleep on a line: it sits on the top edge of a frame."""
    animal(ink, ink.w - 96, ink.h - 2, .3, asleep=True, k=1.0)

# ─────────────────────────────── CSS ────────────────────────────────


def css():
    """The colours of every theme and where its pictures are, as CSS variables."""
    out = ["/* Written by scripts/draw.py from THEMES. Do not edit: change the colours there and run it again. */"]
    for th, t in THEMES.items():
        for mode in ("light", "dark"):
            p = t[mode]
            vars_ = {
                "bg": p["bg"], "card": p["card"], "ink": p["ink"], "soft": p["soft"], "accent": p["accent"], "warm": p["warm"],
                "marker": p["marker"], "wash": p["wash"], "deep": p["deep"], "leaf-1": p["leaf"][0], "leaf-2": p["leaf"][1], "leaf-3": p["leaf"][2],
            }
            sel = f'html[data-theme="{th}"][data-mode="{mode}"]'
            if th == DEFAULT_THEME and mode == "light":
                sel = ":root, " + sel
            out.append(sel + " {\n" + "".join(f"  --{k}: {v};\n" for k, v in vars_.items()) + f"  color-scheme: {mode};\n}}")
    (ROOT / "src" / "app" / "themes.css").write_text("\n\n".join(out) + "\n", encoding="utf-8")
    themes = [dict(id=th, name=t["name"], swatch=[t["light"]["accent"], t["light"]["leaf"][0], t["light"]["warm"], t["light"]["fur"]]) for th, t in THEMES.items()]
    (ROOT / "src" / "resources" / "themes.json").write_text(json.dumps(dict(default=DEFAULT_THEME, themes=themes), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print("Drawing…")
    draw("land.svg", LW, LH, 11, lambda ink: LANDS[ink.theme](ink))
    draw("sky-a.svg", 380, 300, 13, lambda ink: sky(ink, False))
    draw("sky-b.svg", 380, 300, 17, lambda ink: sky(ink, True))
    draw("sleeper.svg", 240, 132, 21, sleeper)
    for n in range(4):
        draw(f"plants-{n}.svg", 600, 70, 31 + n * 7, plants)
    for n in range(3):
        draw(f"line-{n}.svg", 900, 84, 61 + n * 5, line)
    draw("ground.svg", 1200, 150, 91, strip)
    if not PREVIEW_T:
        css()
    print("Done.")
