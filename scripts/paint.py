#!/usr/bin/env python3
"""Paints the site's pictures: a world for every theme, by day and by night.

Each theme (a fox by the sea, a cat on an old wall, a lion on the savanna, …) is a real place
built in layers, far to near: sky and light, distant land, mist, the middle ground, the animal,
and the grass in front. The animals and birds are real outlines (see silhouettes/CREDITS.md);
everything else, trees and rock and water, is grown by the code below.

    public/scenes/<theme>/<mode>/world-N.svg   the place, seen from five spots (one per page)
    public/scenes/<theme>/<mode>/perch.svg     the animal, for the top edge of a frame
    public/scenes/<theme>/<mode>/grow-N.svg    what grows along the top of a card
    public/scenes/<theme>/<mode>/line-N.svg    the strip of far country beside a heading
    public/scenes/<theme>/<mode>/ground.svg    the land the footer is made of
    public/scenes/projects/<slug>.svg          what stands in the world on a project's page

and the colours of each theme as CSS variables in src/app/themes.css, so the pictures and the
page always agree. Nothing here needs installing:  python3 scripts/paint.py [theme …]
"""
import json
import math
import os
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "scripts" / "silhouettes"
OUT = Path(os.environ.get("PREVIEW_DIR") or ROOT / "public" / "scenes")

# ───────────────────────────── THE PAGE ─────────────────────────────
# The colours of the page itself in each theme: `ink` the text, `soft` quieter text, `accent`
# links and underlines, `warm` the one colour that stands out, `marker` behind a number,
# `wash`/`deep` quiet surfaces, `leaf` small decorations. The page's own background is the top
# of that theme's sky (SCENES below), so the picture and the page are one piece.

UI = {
    "fox": dict(
        name="Fox by the sea",
        light=dict(card="#ffffff", ink="#14273d", soft="#4d6379", accent="#2188e0", warm="#ff8559", marker="#bfe2ff", wash="#d6ecfa", deep="#bcdcf2", leaf=["#86cfe0", "#4fa9cc", "#b5e2ee"]),
        dark=dict(card="#101b27", ink="#e4eef8", soft="#9db1c6", accent="#47b8f5", warm="#ff9770", marker="#1d5c8f", wash="#10283c", deep="#15344e", leaf=["#2f86b3", "#51aad6", "#1f6790"]),
    ),
    "cat": dict(
        name="Cat in the ivy",
        light=dict(card="#ffffff", ink="#1f2a24", soft="#51605a", accent="#2f8f5b", warm="#d4572f", marker="#ffe38a", wash="#e6f2df", deep="#d3e8c9", leaf=["#8fc79c", "#63a97a", "#b7dcab"]),
        dark=dict(card="#131c18", ink="#ece8da", soft="#a9ad9f", accent="#7fd39b", warm="#ff8f63", marker="#5a4a12", wash="#16241c", deep="#1c2f24", leaf=["#4f9c69", "#6fbf86", "#3b7a52"]),
    ),
    "lion": dict(
        name="Lion on the savanna",
        light=dict(card="#ffffff", ink="#3a2a14", soft="#75624a", accent="#c07a16", warm="#e2572b", marker="#ffe08a", wash="#f8ebc8", deep="#f0dba6", leaf=["#e3c46a", "#c9a23f", "#efdc9c"]),
        dark=dict(card="#1e1910", ink="#f4ead6", soft="#b9aa8e", accent="#f0b545", warm="#ff8a5c", marker="#5c4410", wash="#261f10", deep="#322814", leaf=["#a8842c", "#cfa646", "#7d6220"]),
    ),
    "owl": dict(
        name="Owl at night",
        light=dict(card="#ffffff", ink="#241f47", soft="#5c5780", accent="#6a55d6", warm="#f2a23a", marker="#e2dcff", wash="#e9e5fb", deep="#d9d3f6", leaf=["#b4a8ec", "#8d7fd8", "#d6cff7"]),
        dark=dict(card="#151428", ink="#ebe8fb", soft="#a9a5c9", accent="#a99bff", warm="#ffc15e", marker="#3a3180", wash="#19173a", deep="#211e4a", leaf=["#5a4fae", "#7d70d6", "#40377f"]),
    ),
    "bear": dict(
        name="Bear in the forest",
        light=dict(card="#ffffff", ink="#26301f", soft="#5a654f", accent="#3c7d3a", warm="#c9532c", marker="#d9eebd", wash="#e2eed3", deep="#cfe2ba", leaf=["#7fb069", "#4f8a45", "#b6d59c"]),
        dark=dict(card="#151c16", ink="#e9edd9", soft="#a7b097", accent="#86c96e", warm="#ff8c5a", marker="#2c4a22", wash="#17251a", deep="#1d3021", leaf=["#3f7a3c", "#5fa055", "#2c5a2c"]),
    ),
    "penguin": dict(
        name="Penguin in the snow",
        light=dict(card="#ffffff", ink="#1b2e3c", soft="#55707f", accent="#1697b7", warm="#ff9a3d", marker="#cdeefa", wash="#e6f5fb", deep="#d2ecf6", leaf=["#bfe6f2", "#8fd0e6", "#e2f5fb"]),
        dark=dict(card="#101c22", ink="#e3f2f8", soft="#9bb6c2", accent="#5fd0ea", warm="#ffb056", marker="#17505f", wash="#122730", deep="#17333f", leaf=["#2c6f86", "#4a9db8", "#1d5568"]),
    ),
    "tortoise": dict(
        name="Tortoise in the desert",
        light=dict(card="#ffffff", ink="#3b2a1f", soft="#7a6455", accent="#c8642f", warm="#e8473a", marker="#ffd9ad", wash="#f9e6c9", deep="#f2d5ac", leaf=["#9cc7a0", "#6fa57a", "#c4dfc0"]),
        dark=dict(card="#1f1812", ink="#f4e7d8", soft="#bba794", accent="#f0915a", warm="#ff7466", marker="#5c3a18", wash="#281d13", deep="#352617", leaf=["#4c8a5a", "#6dae76", "#356543"]),
    ),
}
DEFAULT_THEME = "fox"

# ───────────────────────────── THE LIGHT ────────────────────────────
# What each world looks like by day (light) and by night (dark): the sky from the top of the
# page down to the horizon, the light in it, the colour of far things and of near ones, the
# water, and the light that catches the edge of whatever stands against it.

SCENES = {
    "fox": dict(
        light=dict(sky=["#e9f4fd", "#cde6fa", "#ffe6c2"], glow="#fff0c0", far="#a8cbe4", near="#16314c", rim="#ffdca0",
                   water=["#ffe7c4", "#93c4e4", "#2a6792", "#123a5c"], pop="#ff8559"),
        dark=dict(sky=["#0d1826", "#122741", "#214669"], glow="#e6eef8", far="#1f405e", near="#050c14", rim="#a9c9e8",
                  water=["#35648a", "#163a59", "#0b2238", "#06131f"], pop="#ffb36b"),
    ),
    "cat": dict(
        light=dict(sky=["#f2f8e8", "#e2f0d3", "#ffefc0"], glow="#fff4c2", far="#a8cf9c", near="#17301d", rim="#ffe9a2", pop="#e2572f"),
        dark=dict(sky=["#0c1510", "#102019", "#1a3427"], glow="#e9f1dd", far="#1f3b2c", near="#040906", rim="#bfe4c5", pop="#ffc66b"),
    ),
    "lion": dict(
        light=dict(sky=["#fff2d9", "#ffd9a1", "#ff9c55"], glow="#fff1b8", far="#e89c5e", near="#2f1708", rim="#ffd27c", pop="#ffe7a0"),
        dark=dict(sky=["#161109", "#231a0f", "#3b2a15"], glow="#f4e7c6", far="#3e2d18", near="#080502", rim="#e8cf98", pop="#ffcf7a"),
    ),
    "owl": dict(
        light=dict(sky=["#f0ebff", "#d8ccfb", "#f8c3da"], glow="#fff1f7", far="#a297d8", near="#1b1740", rim="#ffd2e6", pop="#ffc15e"),
        dark=dict(sky=["#0c0b1a", "#131130", "#23204d"], glow="#ebe8ff", far="#262458", near="#03030a", rim="#b8b1f2", pop="#ffd27a"),
    ),
    "bear": dict(
        light=dict(sky=["#f2f7ee", "#dfecdd", "#f9f0cf"], glow="#fff7d2", far="#a6c3aa", near="#12241a", rim="#f6e8aa",
                   water=["#f7efd0", "#b9d6c8", "#4f8474", "#1c3d34"], pop="#e8623a"),
        dark=dict(sky=["#0d1410", "#111f1a", "#1b3429"], glow="#e7f0e2", far="#1e3628", near="#030705", rim="#bcdcc3",
                  water=["#2f5a4a", "#17382e", "#0b2019", "#06120e"], pop="#ffc86b"),
    ),
    "penguin": dict(
        light=dict(sky=["#f2f9fe", "#dbf0fa", "#f5e8f3"], glow="#ffffff", far="#b2d6ea", near="#22475f", rim="#ffffff",
                   water=["#e6f5fb", "#7fc0da", "#1f7397", "#0f4763"], pop="#ff9a3d", ice="#f6fcff"),
        dark=dict(sky=["#07111a", "#0a1d2c", "#123349"], glow="#eaf6ff", far="#17384e", near="#03090e", rim="#9feadb",
                  water=["#1f5670", "#103349", "#081e2d", "#04101a"], pop="#7af0c8", ice="#9fc4d8"),
    ),
    "tortoise": dict(
        light=dict(sky=["#fff5e4", "#ffe2bc", "#ffbd84"], glow="#fff2c6", far="#e3a97a", near="#3a2012", rim="#ffd89c", pop="#e8473a"),
        dark=dict(sky=["#150f0b", "#20160f", "#35251a"], glow="#f5e7d0", far="#3b281b", near="#080402", rim="#e8c89c", pop="#ffb86b"),
    ),
}

W, H = 2400, 900

# ───────────────────────────── GEOMETRY ─────────────────────────────


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def mix(a, b, t):
    """Colour a with a share t of colour b."""
    a, b = (("#" + "".join(ch * 2 for ch in x[1:])) if len(x) == 4 else x for x in (a, b))
    ca, cb = (int(a[i:i + 2], 16) for i in (1, 3, 5)), (int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{round(x + (y - x) * max(0, min(1, t))):02x}" for x, y in zip(ca, cb))


def ridge(rng, x0, x1, y, amp, rough=.55, n=7, sharp=0.0):
    """A line of land as the earth makes it: broken again and again, each time more finely."""
    pts, a = [(x0, 0.0), (x1, 0.0)], 1.0
    for _ in range(n):
        new = []
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            new += [(ax, ay), ((ax + bx) / 2, (ay + by) / 2 + rng.uniform(-a, a))]
        pts, a = new + [pts[-1]], a * rough
    lo, hi = min(p[1] for p in pts), max(p[1] for p in pts)
    out = []
    for x, v in pts:
        v = (v - lo) / ((hi - lo) or 1) * 2 - 1
        if sharp:
            v = v * (1 - sharp) + (1 - 2 * abs(v)) * sharp
        out.append((x, y + v * amp))
    return out


def poly(pts, close=None):
    d = "M" + "L".join(f"{round(x)} {round(y)}" for x, y in pts)
    return d + (f"L{round(pts[-1][0])} {close}L{round(pts[0][0])} {close}Z" if close is not None else "")


def at_x(pts, x):
    """How high the line is at x."""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if ax <= x <= bx:
            return ay + (by - ay) * (x - ax) / ((bx - ax) or 1)
    return pts[-1][1]


def smooth(points, closed=False):
    n = len(points)
    get = (lambda i: points[i % n]) if closed else (lambda i: points[max(0, min(n - 1, i))])
    d = [f"M{f(points[0][0])} {f(points[0][1])}"]
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        d.append(f"C{f(p1[0] + (p2[0] - p0[0]) / 6)} {f(p1[1] + (p2[1] - p0[1]) / 6)} "
                 f"{f(p2[0] - (p3[0] - p1[0]) / 6)} {f(p2[1] - (p3[1] - p1[1]) / 6)} {f(p2[0])} {f(p2[1])}")
    return "".join(d) + ("Z" if closed else "")

# ── things that grow, as their outlines ──


def spruce(rng, h=200):
    """A spruce: boughs in tiers, drooping, never quite even."""
    n = 11
    left, right = [], []
    for i in range(1, n + 1):
        t = i / n
        y = -h + t * h * .93
        w = (t ** .85) * h * .19 * rng.uniform(.82, 1.14)
        left += [(-w, y + rng.uniform(3, 8)), (-w * rng.uniform(.38, .5), y + h * .93 / n * .55)]
        w = (t ** .85) * h * .19 * rng.uniform(.82, 1.14)
        right += [(w, y + rng.uniform(3, 8)), (w * rng.uniform(.38, .5), y + h * .93 / n * .55)]
    pts = [(0, -h)] + left + [(-h * .02, -h * .07), (-h * .02, 0), (h * .02, 0), (h * .02, -h * .07)] + right[::-1]
    return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"


def round_blob(cx, cy, r):
    return f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0Z"


def oak(rng, h=200):
    """A broad tree, grown the way one grows: a trunk that forks and forks again, leaves where the twigs end.
    Returns two outlines, the wood and the leaves."""
    wood, leaves = [], []

    def branch(x, y, ang, length, width, depth):
        x2, y2 = x + math.sin(ang) * length, y - math.cos(ang) * length
        w2, nx, ny = width * .66, math.cos(ang), math.sin(ang)
        wood.append(((x - nx * width / 2, y - ny * width / 2), (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2), (x + nx * width / 2, y + ny * width / 2)))
        if depth <= 2:
            for _ in range(5 if depth else 8):
                leaves.append((x2 + rng.gauss(0, 13), y2 + rng.gauss(0, 10), rng.uniform(7, 14)))
        if depth == 0:
            return
        n = 2 if rng.random() < .65 else 3
        for i in range(n):
            turn = rng.uniform(.28, .7) * (1 if i % 2 else -1) if n == 2 or i < 2 else rng.uniform(-.15, .15)
            branch(x2, y2, ang * .8 + turn, length * rng.uniform(.64, .8), w2, depth - 1)

    branch(0, 0, rng.uniform(-.06, .06), 62, 15, 4)
    top = min(y - r for _, y, r in leaves)
    k = h / -top
    d1 = "".join("M" + "L".join(f"{f(x * k)} {f(y * k)}" for x, y in q) + "Z" for q in wood)
    d2 = "".join(round_blob(x * k, y * k, r * k) for x, y, r in leaves)
    return [d1, d2]


def acacia(rng, h=200):
    """An acacia: a leaning trunk, boughs reaching out, a crown as flat as a table."""
    d = (f"M{f(-h * .025)} 0C{f(-h * .01)} {f(-h * .3)} {f(-h * .06)} {f(-h * .5)} {f(-h * .01)} {f(-h * .68)}L{f(h * .03)} {f(-h * .68)}C{f(-h * .01)} {f(-h * .5)} {f(h * .05)} {f(-h * .3)} {f(h * .035)} 0Z"
         f"M0 {f(-h * .52)}C{f(-h * .18)} {f(-h * .62)} {f(-h * .34)} {f(-h * .66)} {f(-h * .5)} {f(-h * .78)}L{f(-h * .46)} {f(-h * .8)}C{f(-h * .32)} {f(-h * .7)} {f(-h * .16)} {f(-h * .68)} {f(h * .01)} {f(-h * .58)}Z"
         f"M{f(h * .01)} {f(-h * .5)}C{f(h * .2)} {f(-h * .6)} {f(h * .36)} {f(-h * .66)} {f(h * .52)} {f(-h * .8)}L{f(h * .48)} {f(-h * .82)}C{f(h * .34)} {f(-h * .72)} {f(h * .18)} {f(-h * .68)} {f(h * .01)} {f(-h * .58)}Z")
    crown = ""
    for _ in range(26):
        x = rng.uniform(-h * .62, h * .62)
        y = -h * .8 - (1 - (x / (h * .68)) ** 2) * h * .1 + rng.uniform(-h * .025, h * .03)
        rx, ry = h * rng.uniform(.1, .17), h * rng.uniform(.035, .055)
        crown += f"M{f(x - rx)} {f(y)}a{f(rx)} {f(ry)} 0 1 0 {f(2 * rx)} 0a{f(rx)} {f(ry)} 0 1 0 {f(-2 * rx)} 0Z"
    return [d, crown]


def saguaro(rng, h=200):
    """A saguaro: one tall column and an arm or two, each leaving the trunk level and turning up."""
    w = h * .08

    def column(x, y0, y1, r):
        return f"M{f(x - r)} {f(y0)}L{f(x - r)} {f(y1 + r)}a{f(r)} {f(r)} 0 0 1 {f(2 * r)} 0L{f(x + r)} {f(y0)}Z"

    d = column(0, 0, -h, w)
    for side, y, up in ((-1, rng.uniform(.3, .44), rng.uniform(.26, .36)), (1, rng.uniform(.44, .58), rng.uniform(.2, .3))):
        if side == 1 and rng.random() < .25:
            continue
        r, R = w * .7, w * 1.5
        x, yc = side * h * rng.uniform(.2, .26), -h * y
        cx, cy = x - side * R, yc - R                    # the middle of the turn
        if side == 1:
            d += f"M0 {f(yc - r)}L{f(cx + 1)} {f(yc - r)}L{f(cx + 1)} {f(yc + r)}L0 {f(yc + r)}Z"
            d += f"M{f(cx + R + r)} {f(cy - 1)}L{f(cx + R + r)} {f(cy)}A{f(R + r)} {f(R + r)} 0 0 1 {f(cx)} {f(cy + R + r)}L{f(cx)} {f(cy + R - r)}A{f(R - r)} {f(R - r)} 0 0 0 {f(cx + R - r)} {f(cy)}L{f(cx + R - r)} {f(cy - 1)}Z"
        else:
            d += f"M0 {f(yc + r)}L{f(cx - 1)} {f(yc + r)}L{f(cx - 1)} {f(yc - r)}L0 {f(yc - r)}Z"
            d += f"M{f(cx)} {f(cy + R + r)}A{f(R + r)} {f(R + r)} 0 0 1 {f(cx - R - r)} {f(cy)}L{f(cx - R - r)} {f(cy - 1)}L{f(cx - R + r)} {f(cy - 1)}L{f(cx - R + r)} {f(cy)}A{f(R - r)} {f(R - r)} 0 0 0 {f(cx)} {f(cy + R - r)}Z"
        d += column(x, cy, -h * (y + up), r)
    return d


def tuft(rng, h=60, n=9, spread=.5, lean=0.0):
    """A clump of grass: thin blades, each bent its own way."""
    d = ""
    for _ in range(n):
        x0 = rng.uniform(-h * .14, h * .14)
        tip = x0 + rng.uniform(-spread, spread) * h + lean * h
        hh = h * rng.uniform(.45, 1)
        w = h * rng.uniform(.018, .034)
        d += f"M{f(x0 - w)} 0Q{f((x0 + tip) / 2 - w * 2)} {f(-hh * .6)} {f(tip)} {f(-hh)}Q{f((x0 + tip) / 2 + w * 2)} {f(-hh * .55)} {f(x0 + w)} 0Z"
    return d


def kelp(rng, h=160):
    """A stem of sea weed, leafy to both sides."""
    d, w = "", h * .02
    pts = [(math.sin(t * 3.4 + rng.uniform(0, 1)) * h * .07 * t, -h * t) for t in (k / 8 for k in range(9))]
    d += "M" + "L".join(f"{f(x - w)} {f(y)}" for x, y in pts) + "L" + "L".join(f"{f(x + w)} {f(y)}" for x, y in reversed(pts)) + "Z"
    for k, (x, y) in enumerate(pts[1:-1]):
        s = 1 if k % 2 else -1
        l, b = h * rng.uniform(.14, .2), h * rng.uniform(.035, .05)
        d += f"M{f(x)} {f(y)}Q{f(x + s * l * .5)} {f(y - b * 1.6)} {f(x + s * l)} {f(y - b * 2.4)}Q{f(x + s * l * .55)} {f(y + b * .2)} {f(x)} {f(y)}Z"
    return d


def rock_shape(rng, w=120, h=70):
    pts = [(-w * .5, 0), (-w * .46, -h * .4), (-w * .3, -h * rng.uniform(.7, .9)), (-w * .05, -h * rng.uniform(.86, 1)), (w * .22, -h * rng.uniform(.74, .92)),
           (w * .42, -h * .46), (w * .5, 0)]
    return "M" + "L".join(f"{f(x + rng.uniform(-3, 3))} {f(y)}" for x, y in pts) + "Z"

# ─────────────────────────────── PAINT ──────────────────────────────

STYLE = """
.sc-pz{transform:translate(calc(var(--mx,0)*var(--z)*-46px),calc(var(--my,0)*var(--z)*-14px + var(--sy,0)*(1 - var(--z))*70px));transition:transform .45s cubic-bezier(.2,.8,.2,1)}
.sc-in{opacity:0;animation:sc-in 1.3s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes sc-in{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
.sc-tw{animation:sc-tw 3s ease-in-out infinite alternate}
@keyframes sc-tw{from{opacity:.2}to{opacity:1}}
.sc-drift{animation:sc-drift 70s ease-in-out infinite alternate}
@keyframes sc-drift{from{transform:translateX(-50px)}to{transform:translateX(70px)}}
.sc-sway{animation:sc-sway 4.5s ease-in-out infinite alternate}
@keyframes sc-sway{from{transform:rotate(-2.4deg)}to{transform:rotate(2.8deg)}}
.sc-wind{animation:sc-wind 4.5s ease-in-out infinite alternate}
@keyframes sc-wind{from{transform:skewX(-3deg)}to{transform:skewX(5deg)}}
.sc-br{animation:sc-br 3.6s ease-in-out infinite alternate}
@keyframes sc-br{from{transform:scale(1,1)}to{transform:scale(1.004,1.016)}}
.sc-bob{animation:sc-bob 5s ease-in-out infinite alternate}
@keyframes sc-bob{from{transform:translateY(1.5px) rotate(-1.6deg)}to{transform:translateY(-2.5px) rotate(1.4deg)}}
.sc-fall{animation:sc-fall 9s linear infinite}
@keyframes sc-fall{0%{transform:translate(0,-60px);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translate(60px,420px);opacity:0}}
.sc-rise{animation:sc-rise 7s ease-in infinite}
@keyframes sc-rise{0%{transform:translateY(20px);opacity:0}20%{opacity:.9}100%{transform:translateY(-90px);opacity:0}}
.sc-float{animation:sc-float 9s ease-in-out infinite alternate}
@keyframes sc-float{from{transform:translate(-14px,6px)}to{transform:translate(16px,-8px)}}
.sc-beam{animation:sc-beam 9s ease-in-out infinite alternate}
@keyframes sc-beam{from{transform:rotate(-16deg);opacity:.25}to{transform:rotate(12deg);opacity:.75}}
.sc-wave{animation:sc-wave 9s ease-in-out infinite alternate}
@keyframes sc-wave{from{transform:translateX(-22px)}to{transform:translateX(22px)}}
.sc-aur{animation:sc-aur 13s ease-in-out infinite alternate}
@keyframes sc-aur{from{transform:translateX(-60px) scaleY(.86);opacity:.5}to{transform:translateX(50px) scaleY(1.12);opacity:.95}}
.sc-still *{animation-play-state:paused!important}
@media (prefers-reduced-motion:reduce){.sc *{animation:none!important;transition:none!important}.sc .sc-in{opacity:1}}
"""


class Scene:
    """One picture being painted: far things first, then nearer and nearer."""

    def __init__(self, theme, mode, w, h, seed, uid):
        self.theme, self.mode, self.w, self.h, self.uid = theme, mode, w, h, uid
        self.c = SCENES[theme][mode]
        self.night = mode == "dark"
        self.rng = random.Random(seed)
        self.defs, self.out, self.syms, self.n, self.blurs = [], [], {}, 0, {}
        self.t = 0.0                                 # when the layer being painted comes in
        self.prop = None                             # what a project page adds in front

    def id(self):
        self.n += 1
        return f"{self.uid}{self.n}"

    def add(self, s):
        self.out.append(s)

    def grad(self, stops, x1, y1, x2, y2):
        i = self.id()
        self.defs.append(f'<linearGradient id="{i}" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}">'
                         + "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + "</linearGradient>")
        return f"url(#{i})"

    def glow(self, color, cx, cy, r, strength=1.0, at=None):
        i = self.id()
        self.defs.append(f'<radialGradient id="{i}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}">'
                         f'<stop offset="0" stop-color="{color}" stop-opacity="{.95 * strength:.2f}"/><stop offset=".35" stop-color="{color}" stop-opacity="{.4 * strength:.2f}"/>'
                         f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        self.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#{i})"/>')

    def blur(self, std):
        if std not in self.blurs:
            i = self.id()
            self.defs.append(f'<filter id="{i}" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="{std}"/></filter>')
            self.blurs[std] = f"url(#{i})"
        return self.blurs[std]

    def open(self, z, at=None):
        """Begins a layer: z is how near it is (0 the sky, 1 right in front), for the way it moves with the pointer."""
        self.t = self.t + .16 if at is None else at
        self.add(f'<g class="sc-pz" style="--z:{z}"><g class="sc-in" style="animation-delay:{self.t:.2f}s">')

    def close(self):
        self.add("</g></g>")

    def tone(self, d):
        """The colour of land at depth d: 0 is far and takes the colour of the air, 1 is under your feet."""
        return mix(self.c["far"], self.c["near"], d ** 1.15)

    def land(self, pts, d, lit=.22, bottom=None):
        """A layer of land, a little lighter where the light falls on its top."""
        top = min(p[1] for p in pts)
        col = self.tone(d)
        fill = self.grad([(0, mix(col, self.c["rim"], lit * (1 - d * .5)), 1), (.5, col, 1), (1, mix(col, self.c["near"], .35), 1)], 0, top, 0, top + 260)
        self.add(f'<path d="{poly(pts, bottom or self.h + 40)}" fill="{fill}"/>')

    def shape(self, key, d, vw, vh):
        """Registers an outline once so it can be set down many times."""
        if key not in self.syms:
            i = self.id()
            self.syms[key] = (i, vw, vh)
            paths = "".join(f'<path d="{one}"/>' for one in ([d] if isinstance(d, str) else d))
            self.defs.append(f'<symbol id="{i}" viewBox="{f(-vw / 2)} {f(-vh)} {f(vw)} {f(vh)}" overflow="visible">{paths}</symbol>')
        return self.syms[key]

    def silhouette(self, name):
        if name not in self.syms:
            raw = (ART / f"{name}.svg").read_text()
            vw, vh = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', raw).groups())
            inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1)
            i = self.id()
            self.syms[name] = (i, vw, vh)
            self.defs.append(f'<symbol id="{i}" viewBox="0 0 {f(vw)} {f(vh)}">{inner}</symbol>')
        return self.syms[name]

    def use(self, key, x, base, h, fill, flip=False, opacity=None, sway=None):
        """A registered outline with its foot at (x, base), h tall."""
        i, vw, vh = self.syms[key]
        w = h * vw / vh
        op = f' opacity="{opacity}"' if opacity else ""
        use = f'<use href="#{i}" x="{f(-w / 2)}" y="{f(-h)}" width="{f(w)}" height="{f(h)}" fill="{fill}"{op}/>'
        if sway:
            use = f'<g class="sc-sway" style="animation-duration:{sway:.1f}s;animation-delay:-{self.rng.uniform(0, 6):.1f}s">{use}</g>'
        return f'<g transform="translate({f(x)} {f(base)}){" scale(-1 1)" if flip else ""}">{use}</g>'

    def put(self, *a, **k):
        self.add(self.use(*a, **k))

    def wind(self, items, y):
        """Lets the wind into a row of things rooted along y: three gusts, out of step."""
        rng = self.rng
        for g in range(3):
            part = "".join(items[g::3])
            if part:
                self.add(f'<g class="sc-wind" style="transform-origin:0 {f(y)}px;animation-duration:{rng.uniform(3.4, 5.6):.1f}s;animation-delay:-{rng.uniform(0, 6):.1f}s">{part}</g>')

    def animal(self, name, x, base, h, flip=False, light=1, shadow=True):
        """A real animal's outline, dark against the light, the light catching one edge of it."""
        i, vw, vh = self.silhouette(name)
        w = h * vw / vh
        c = self.c
        body = mix(c["near"], "#000000", .25)
        m = self.id()
        use = f'<use href="#{i}" x="{f(-w / 2)}" y="{f(-h)}" width="{f(w)}" height="{f(h)}"'
        k = h * .028 * light * (-1 if flip else 1)
        self.defs.append(f'<mask id="{m}">{use} fill="#fff"/></mask>')
        shade = self.grad([(0, mix(body, c["rim"], .16), 1), (1, body, 1)], 0, -h, 0, 0)
        sh = (f'<ellipse cx="{f(w * .04)}" cy="2" rx="{f(w * .46)}" ry="{f(max(4, h * .035))}" fill="#000" fill-opacity="{.5 if self.night else .32}" filter="{self.blur(6)}"/>' if shadow else "")
        self.add(f'<g transform="translate({f(x)} {f(base)}){" scale(-1 1)" if flip else ""}">{sh}<g class="sc-br">'
                 f'<g mask="url(#{m})">{use} fill="{c["rim"]}"/><g transform="translate({f(-k)} {f(h * .022)})">{use} fill="{shade}"/></g></g></g></g>')

    # ── the sky ──

    def sun(self, x, y, r):
        """The sun by day, the moon by night, and the light around it."""
        c = self.c
        self.glow(c["glow"], x, y, r * (7 if not self.night else 5.2), .9 if not self.night else .55)
        self.glow(c["glow"], x, y, r * 2.6, 1)
        if self.night:
            i = self.id()
            self.defs.append(f'<clipPath id="{i}"><circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/></clipPath>')
            self.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{c["glow"]}"/><g clip-path="url(#{i})" fill="{mix(c["glow"], c["sky"][1], .55)}" fill-opacity=".34">'
                     + "".join(f'<circle cx="{f(x + a * r)}" cy="{f(y + b * r)}" r="{f(s * r)}"/>' for a, b, s in ((-.3, -.25, .26), (.25, .1, .2), (-.1, .42, .16), (.42, -.4, .12), (-.52, .2, .1)))
                     + f'</g><circle cx="{f(x + r * .5)}" cy="{f(y - r * .3)}" r="{f(r * 1.25)}" fill="{c["sky"][1]}" fill-opacity=".0"/>')
        else:
            self.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{mix(c["glow"], "#ffffff", .5)}"/>')

    def stars(self, y1, n=150):
        rng, c = self.rng, self.c
        for g in range(3):
            dots = "".join(f'<circle cx="{f(rng.uniform(0, self.w))}" cy="{f(rng.uniform(0, y1) ** 1.0)}" r="{f(rng.choice((.9, 1.1, 1.3, 1.6, 2.1)))}"/>' for _ in range(n // 3))
            self.add(f'<g class="sc-tw" fill="{c["glow"]}" style="animation-duration:{2.4 + g * 1.3:.1f}s;animation-delay:-{g * 1.1:.1f}s">{dots}</g>')

    def cloud(self, x, y, s, opacity=.85):
        """A cloud: soft, lit from above, drifting."""
        rng, c = self.rng, self.c
        col = mix(c["glow"], "#ffffff", .6) if not self.night else mix(c["glow"], c["sky"][1], .78)
        parts = "".join(f'<ellipse cx="{f(rng.uniform(-120, 120) * s)}" cy="{f(rng.uniform(-18, 14) * s)}" rx="{f(rng.uniform(60, 120) * s)}" ry="{f(rng.uniform(18, 34) * s)}"/>' for _ in range(7))
        self.add(f'<g transform="translate({f(x)} {f(y)})"><g class="sc-drift" style="animation-duration:{rng.uniform(50, 90):.0f}s;animation-delay:-{rng.uniform(0, 40):.0f}s">'
                 f'<g fill="{col}" fill-opacity="{opacity}" filter="{self.blur(9)}">{parts}</g></g></g>')

    def mist(self, y, h, strength=.7):
        """Air lying in the hollows between one layer of land and the next."""
        c = self.c
        col = mix(c["sky"][2], c["glow"], .3)
        g = self.grad([(0, col, 0), (.55, col, strength), (1, col, 0)], 0, y, 0, y + h)
        self.add(f'<g class="sc-drift" style="animation-duration:90s"><rect x="-120" y="{f(y)}" width="{self.w + 240}" height="{f(h)}" fill="{g}"/></g>')

    def birds(self, n, x0, x1, y0, y1, dur=60, size=1.0):
        """Birds a long way off, crossing the sky."""
        rng, c = self.rng, self.c
        for k in range(n):
            y, s = rng.uniform(y0, y1), size * rng.uniform(.7, 1.2)
            d1, d2 = f"M{f(-9 * s)} 0Q{f(-4.5 * s)} {f(-6 * s)} 0 0Q{f(4.5 * s)} {f(-6 * s)} {f(9 * s)} 0", f"M{f(-9 * s)} {f(-3 * s)}Q{f(-4.5 * s)} {f(2 * s)} 0 0Q{f(4.5 * s)} {f(2 * s)} {f(9 * s)} {f(-3 * s)}"
            t = dur * rng.uniform(.8, 1.3)
            self.add(f'<g><path d="{d1}" fill="none" stroke="{c["near"]}" stroke-width="{f(1.8 * s)}" stroke-linecap="round" stroke-opacity=".8">'
                     f'<animate attributeName="d" values="{d1};{d2};{d1}" dur="{rng.uniform(.5, .8):.2f}s" repeatCount="indefinite"/></path>'
                     f'<animateMotion path="M{f(x0)} {f(y)}Q{f((x0 + x1) / 2)} {f(y - rng.uniform(20, 70))} {f(x1)} {f(y + rng.uniform(-30, 30))}" dur="{t:.0f}s" begin="-{rng.uniform(0, t):.0f}s" repeatCount="indefinite"/></g>')

    def specks(self, n, y0, y1, color, r=(1.4, 3), kind="float", glow=False):
        """Small things in the air: fireflies, snow, dust in the light."""
        rng = self.rng
        for _ in range(n):
            x, y, rad = rng.uniform(0, self.w), rng.uniform(y0, y1), rng.uniform(*r)
            dot = f'<circle r="{f(rad)}" fill="{color}"/>' + (f'<circle r="{f(rad * 3.2)}" fill="{color}" fill-opacity=".22"/>' if glow else "")
            cls = {"float": "sc-float", "fall": "sc-fall", "rise": "sc-rise"}[kind]
            tw = f'<g class="sc-tw" style="animation-duration:{rng.uniform(1.4, 3.2):.1f}s;animation-delay:-{rng.uniform(0, 3):.1f}s">{dot}</g>' if glow else dot
            self.add(f'<g transform="translate({f(x)} {f(y)})"><g class="{cls}" style="animation-duration:{rng.uniform(6, 13):.1f}s;animation-delay:-{rng.uniform(0, 12):.1f}s">{tw}</g></g>')

    # ── the ground ──

    def forest(self, line, key, hmin, hmax, step, d, x0=None, x1=None, sink=6, sway=False):
        """Trees along a line of land, each its own height."""
        rng = self.rng
        x = (x0 if x0 is not None else -40) + rng.uniform(0, step)
        col = self.tone(d)
        while x < (x1 if x1 is not None else self.w + 40):
            hh = rng.uniform(hmin, hmax)
            self.put(key, x, at_x(line, x) + sink, hh, mix(col, self.c["near"], rng.uniform(0, .18)), flip=rng.random() < .5,
                     sway=rng.uniform(5, 9) if sway else None)
            x += step * rng.uniform(.55, 1.5)

    def grass(self, line, d, step=34, h=(26, 58), x0=-20, x1=None, lean=0.0):
        """Grass along a line of land, moving in the wind."""
        rng = self.rng
        col = self.tone(d)
        for k in range(7):
            self.shape(f"tuft{k}/{lean}", tuft(random.Random(40 + k), 60, (6, 8, 10)[k % 3], lean=lean), 120, 60)
        x, items = x0, []
        while x < (x1 or self.w + 20):
            items.append(self.use(f"tuft{rng.randrange(7)}/{lean}", x, at_x(line, x) + 4, rng.uniform(*h), mix(col, self.c["near"], rng.uniform(0, .3)), flip=lean == 0 and rng.random() < .5))
            x += step * rng.uniform(.5, 1.5)
        self.wind(items, sum(p[1] for p in line) / len(line) + 4)

    def water(self, y, sun_x=None, bottom=None):
        """Still or moving water from y down: paler far off, light lying on it under the sun."""
        rng, c = self.rng, self.c
        bottom = bottom or self.h + 40
        wc = c["water"]
        self.add(f'<rect x="-80" y="{f(y)}" width="{self.w + 160}" height="{f(bottom - y)}" fill="{self.grad([(0, wc[0], 1), (.16, wc[1], 1), (.6, wc[2], 1), (1, wc[3], 1)], 0, y, 0, bottom)}"/>')
        if sun_x is not None:                        # the path of light towards the sun
            for g in range(3):
                bars = ""
                for _ in range(26):
                    t = rng.uniform(0, 1) ** 1.5
                    yy = y + 4 + t * (bottom - y) * .78
                    half = 16 + t * 190
                    ww = rng.uniform(.25, 1) * half
                    xx = sun_x + rng.uniform(-half, half)
                    bars += f'<rect x="{f(xx - ww / 2)}" y="{f(yy)}" width="{f(ww)}" height="{f(1.6 + t * 3.2)}" rx="1.6"/>'
                self.add(f'<g class="sc-tw" fill="{c["glow"]}" fill-opacity="{.75 if not self.night else .55}" style="animation-duration:{2.2 + g * .9:.1f}s;animation-delay:-{g:.1f}s">{bars}</g>')
        for g in range(3):                           # the swell
            lines = ""
            for _ in range(22):
                t = rng.uniform(0, 1) ** 1.3
                yy = y + 8 + t * (bottom - y) * .9
                xx, ln = rng.uniform(-40, self.w), 30 + t * 160 * rng.uniform(.5, 1.4)
                lines += f"M{f(xx)} {f(yy)}q{f(ln / 4)} {f(-2 - t * 3)} {f(ln / 2)} 0t{f(ln / 2)} 0"
            self.add(f'<g class="sc-wave" style="animation-duration:{7 + g * 2.5:.1f}s;animation-delay:-{g * 2:.0f}s"><path d="{lines}" fill="none" stroke="{mix(wc[0], c["glow"], .4)}" '
                     f'stroke-opacity="{.3 if not self.night else .2}" stroke-width="1.6" stroke-linecap="round"/></g>')

    def render(self, extra_style=""):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" class="sc" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" fill="none" preserveAspectRatio="xMidYMax slice">'
                f'<style>{STYLE.strip()}{extra_style}</style><defs>{"".join(self.defs)}</defs>{"".join(self.out)}</svg>\n')
# ───────────────────────────── THE WORLDS ───────────────────────────
# Each world is painted from the back: sky, far land, the middle distance, the place where the
# animal is, and what grows right in front. `v` is which page the picture is for (0 home,
# 1 about, 2 work and gallery, 3 open source and the case studies): the same world from
# another spot, the animal in another pose.

CAST = {
    "fox": [("fox-stand", False), ("fox-walk", True), ("fox-sit2", False), ("fox-sit", True), ("fox-stand", True)],
    "cat": [("cat-stand", False), ("cat-walk", True), ("cat-sit", False), ("cat-stand", True), ("cat-walk", False)],
    "lion": [("lion", False), ("lion-walk", True), ("leopard", False), ("lion", True), ("lion-walk", False)],
    "owl": [("owl", False), ("owl-2", True), ("owl-3", False), ("owl", True), ("owl-2", False)],
    "bear": [("bear", False), ("bear-2", True), ("bear-walk", False), ("bear", True), ("bear-2", False)],
    "penguin": [("penguin", False), ("penguin-side", True), ("penguin-3", False), ("penguin-4", True), ("penguin", True)],
    "tortoise": [("tortoise-2", False), ("tortoise", True), ("tortoise-3", False), ("tortoise-2", True), ("tortoise", False)],
}
PAGES = ["home", "about", "work", "code", "gallery"]   # world-0 … world-4
SPOT = [1560, 860, 1640, 780, 1240]                  # where the animal is, for each page
SUN = [1810, 600, 1390, 1040, 1500]                  # and where the light is


def common_sky(S, v, y, r, clouds=4, moon=None, stars_to=520, sun_x=None):
    S.open(.02, .0)
    night = S.night if moon is None else moon
    if S.night:
        S.stars(stars_to)
    keep, S.night = S.night, night
    S.sun(SUN[v] if sun_x is None else sun_x, y, r)
    S.night = keep
    for k in range(clouds):
        S.cloud(S.rng.uniform(100, S.w - 100), S.rng.uniform(70, y + 40), S.rng.uniform(.7, 1.5), .8 if not S.night else .55)
    S.close()


def front(S, y=858, grass=(44, 110), step=30, lean=0.0, ferns=0):
    """The nearest ground, dark, with what grows on it."""
    S.open(1.0)
    line = ridge(S.rng, -60, S.w + 60, y, 20, .5)
    S.land(line, 1.0, .05)
    S.grass(line, 1.0, step, grass, lean=lean)
    for _ in range(ferns):
        x = S.rng.uniform(40, S.w - 40)
        S.silhouette("fern")
        S.put("fern", x, at_x(line, x) + 6, S.rng.uniform(70, 130), S.tone(1), flip=S.rng.random() < .5, sway=S.rng.uniform(4, 7))
    if S.prop:
        S.prop(S, line)
    S.close()
    return line


def paint_fox(S, v):
    c, rng, HZ = S.c, S.rng, 520
    sx, ax = SUN[v], SPOT[v]
    common_sky(S, v, HZ - (70 if not S.night else 250), 54 if not S.night else 44)
    # islands on the horizon, a lighthouse on one of them
    S.open(.07)
    lx = 420 if ax > 1200 else 2010
    for x0, x1, amp in ((lx - 330, lx + 300, 34), ((1500 if lx < 1200 else 300), (2260 if lx < 1200 else 900), 22)):
        isl = [(x, HZ + 6 - max(0, (y - HZ) * -1)) for x, y in ridge(rng, x0, x1, HZ - amp * .5, amp * .5, .5, 5)]
        isl = [(x, min(HZ + 4, HZ - abs(math.sin((x - x0) / (x1 - x0) * math.pi)) * amp + (y - HZ) * .3)) for x, y in isl]
        S.land(isl, .1, .3, HZ + 8)
    ly = HZ - 30
    S.add(f'<path d="M{lx - 11} {ly}L{lx - 8} {ly - 84}L{lx + 8} {ly - 84}L{lx + 11} {ly}Z" fill="{mix(S.tone(.2), c["glow"], .5)}"/>'
          f'<path d="M{lx - 9.6} {ly - 40}L{lx - 8.8} {ly - 62}L{lx + 8.8} {ly - 62}L{lx + 9.6} {ly - 40}Z" fill="{c["pop"]}"/>'
          f'<path d="M{lx - 11} {ly - 84}L{lx - 11} {ly - 98}L{lx} {ly - 110}L{lx + 11} {ly - 98}L{lx + 11} {ly - 84}Z" fill="{S.tone(.5)}"/>')
    beam = S.grad([(0, c["glow"], .85 if S.night else .5), (1, c["glow"], 0)], 0, 0, 520, 0)
    S.add(f'<g transform="translate({lx} {ly - 91})"><g class="sc-beam"><path d="M0 0L520 -70L520 70Z" fill="{beam}"/></g>'
          f'<g class="sc-beam" style="animation-delay:-4.5s"><g transform="scale(-1 1)"><path d="M0 0L520 -70L520 70Z" fill="{beam}" fill-opacity=".6"/></g></g>'
          f'<circle r="6" fill="{c["glow"]}"/></g>')
    S.close()
    S.open(.12)
    S.water(HZ, sx)
    # a sail far out
    bx = 1180 if ax > 1200 else 1500
    S.add(f'<g transform="translate({bx} {HZ + 9})"><g class="sc-bob"><path d="M-26 0L26 0L18 9L-18 9Z" fill="{S.tone(.75)}"/><path d="M-2 -3L-2 -52L22 -6Z" fill="{mix(c["glow"], S.tone(.2), .2)}"/>'
          f'<path d="M-6 -3L-6 -40L-22 -5Z" fill="{mix(c["glow"], S.tone(.3), .35)}"/></g></g>')
    S.close()
    # the headland the fox sits on
    S.open(.6)
    left = ax < 1200
    head = [(x, y - (max(0, (x - 1150) if not left else (1250 - x)) / 1300) ** .8 * 250) for x, y in ridge(rng, -60, S.w + 60, 800, 26, .5)]
    S.land(head, .7, .3)
    S.grass(head, .7, 40, (18, 44))
    for rx in ((260, 420, 610) if not left else (1790, 1960, 2140)):
        S.add(f'<g transform="translate({rx} {at_x(head, rx) + 10})"><path d="{rock_shape(rng, rng.uniform(110, 220), rng.uniform(60, 110))}" fill="{S.tone(.85)}"/></g>')
    S.silhouette("gull"), S.silhouette("gull-2")
    gx = 420 if not left else 1960
    S.put("gull", gx, at_x(head, gx) - 62, 44, S.tone(1), flip=left)
    S.put("gull-2", gx + (190 if not left else -170), at_x(head, gx + (190 if not left else -170)) - 46, 36, S.tone(1), flip=not left)
    name, flip = CAST["fox"][v]
    S.animal(name, ax, at_x(head, ax) + 5, 168, flip=flip != left)
    S.close()
    S.birds(7, -60, S.w + 60, 120, 380, 70)
    front(S, 868, (30, 76), 26)


def paint_cat(S, v):
    c, rng = S.c, S.rng
    ax = SPOT[v]
    common_sky(S, v, 330 if not S.night else 210, 58 if not S.night else 46)
    for k, seed in enumerate((3, 8, 21)):
        S.shape(f"oak{k}", oak(random.Random(seed)), 250, 200)
    S.open(.08)
    far = ridge(rng, -60, S.w + 60, 500, 46, .5)
    S.land(far, .04, .35)
    for k in range(3):
        S.forest(far, f"oak{k}", 50, 96, 330, .12)
    S.close()
    S.open(.14)
    S.mist(470, 150, .6)
    S.close()
    S.open(.25)
    mid = ridge(rng, -60, S.w + 60, 580, 40, .5)
    S.land(mid, .3, .3)
    for k in range(3):
        S.forest(mid, f"oak{k}", 130, 230, 760, .38, sway=True)
    S.close()
    S.open(.36)
    S.mist(560, 110, .4)
    S.close()
    # the garden, and the old wall across it
    S.open(.55)
    base = ridge(rng, -60, S.w + 60, 724, 12, .5)
    S.land(base, .62, .26)
    bx = ax - 760 if ax > 1200 else ax + 780
    S.put("oak1", bx, at_x(base, bx) + 8, 500, S.tone(.74), sway=12)
    S.put("oak2", bx + (1500 if ax < 1200 else -1560), at_x(base, bx) + 8, 380, S.tone(.7), sway=10, flip=True)
    wy, x, top = 626, -70, []
    while x < S.w + 70:                              # its top, stone by stone
        w, y = rng.uniform(46, 92), wy + rng.uniform(-5, 5)
        top += [(x, y), (x + w - 3, y + rng.uniform(-1.5, 1.5))]
        x += w
    stone = mix(S.tone(.5), "#b3a995" if not S.night else c["far"], .6 if not S.night else .35)
    face = S.grad([(0, mix(stone, c["rim"], .5), 1), (.12, mix(stone, c["rim"], .2), 1), (1, mix(stone, c["near"], .5), 1)], 0, wy - 6, 0, wy + 120)
    S.add(f'<path d="{poly(top, 760)}" fill="{face}"/>')
    joints = ""
    for r in range(4):
        y, x = wy + 22 + r * 24, -60 + (r % 2) * 40
        while x < S.w + 60:
            w = rng.uniform(50, 110)
            joints += f"M{f(x)} {f(y + rng.uniform(-2, 2))}h{f(w - 12)}M{f(x + w - 6)} {f(y - 20)}v16"
            x += w
    S.add(f'<path d="{joints}" stroke="{c["near"]}" stroke-opacity=".26" stroke-width="2" stroke-linecap="round"/>')
    name, flip = CAST["cat"][v]
    S.animal(name, ax, at_x(top, ax) + 4, 148, flip=flip)
    ivy = []                                         # ivy coming over it
    for x in sorted(rng.uniform(-40, S.w + 40) for _ in range(13)):
        if abs(x - ax) < 150:
            continue
        wide, deep, leaves = rng.uniform(60, 150), rng.uniform(50, 104), ""
        for _ in range(int(wide * deep / 150)):
            t = rng.uniform(0, 1) ** 1.6
            lx, ly, r = rng.gauss(0, wide * .3 * (1 - t * .6)), -8 + t * deep, rng.uniform(4.5, 8.5)
            leaves += f"M{f(lx)} {f(ly - r)}q{f(r * 1.1)} {f(r * .1)} {f(r * .9)} {f(r)}q{f(-r * .4)} {f(r * .7)} {f(-r * .9)} {f(r * .9)}q{f(-r * .5)} {f(-r * .2)} {f(-r * .9)} {f(-r * .9)}q{f(-.1 * r)} {f(-r)} {f(r * .9)} {f(-r)}Z"
        ivy.append(f'<g transform="translate({f(x)} {f(at_x(top, x))})"><path d="{leaves}" fill="{mix(S.tone(.62), c["near"], rng.uniform(0, .3))}"/></g>')
    S.add("".join(ivy))
    S.close()
    S.open(.78)
    lawn = ridge(rng, -60, S.w + 60, 790, 18, .5)
    S.land(lawn, .82, .2)
    S.grass(lawn, .82, 30, (20, 46))
    flowers = []
    for _ in range(54):
        x = rng.uniform(20, S.w - 20)
        y, hh, col = at_x(lawn, x) + rng.uniform(4, 44), rng.uniform(26, 56), rng.choice((c["pop"], c["glow"], mix(c["pop"], c["glow"], .5), "#ffffff" if not S.night else c["rim"]))
        flowers.append(f'<g transform="translate({f(x)} {f(y)})"><path d="M0 0Q{f(rng.uniform(-4, 4))} {f(-hh * .5)} 0 {f(-hh)}" stroke="{S.tone(.98)}" stroke-width="2"/>'
                       + "".join(f'<circle cx="{f(math.cos(a) * 5)}" cy="{f(-hh + math.sin(a) * 5)}" r="4.2" fill="{col}"/>' for a in (k * 1.2566 for k in range(5)))
                       + f'<circle cy="{f(-hh)}" r="2.6" fill="{S.tone(.9)}"/></g>')
    S.wind(flowers, 810)
    S.close()
    S.open(.85)
    S.specks(26, 420, 800, c["pop"] if S.night else c["glow"], (2, 3.6), "float", glow=True)
    S.close()
    S.birds(4, -60, S.w + 60, 100, 300, 80, .8)
    front(S, 868, (40, 96), 24)


def paint_lion(S, v):
    c, rng, HZ = S.c, S.rng, 560
    ax = SPOT[v]
    common_sky(S, v, HZ - (34 if not S.night else 290), 112 if not S.night else 52, clouds=3)
    S.shape("acacia", acacia(random.Random(4), 200), 300, 200)
    S.shape("acacia2", acacia(random.Random(11), 200), 300, 200)
    for n in ("giraffe", "giraffe-2", "elephant", "zebra"):
        S.silhouette(n)
    # a mountain a long way off, snow on its flat top
    S.open(.05)
    mx = 620 if ax > 1200 else 1780
    mt = [(mx - 560, HZ + 4), (mx - 330, HZ - 96), (mx - 170, HZ - 168), (mx - 60, HZ - 196), (mx + 110, HZ - 200), (mx + 190, HZ - 170), (mx + 380, HZ - 84), (mx + 600, HZ + 4)]
    S.land(mt, 0, .4, HZ + 10)
    S.add(f'<path d="M{mx - 170} {HZ - 168}L{mx - 60} {HZ - 196}L{mx + 110} {HZ - 200}L{mx + 190} {HZ - 170}L{mx + 140} {HZ - 176}L{mx + 96} {HZ - 160}L{mx + 40} {HZ - 178}L{mx - 20} {HZ - 158}L{mx - 80} {HZ - 172}Z" fill="{c["glow"]}" fill-opacity=".8"/>')
    S.close()
    S.open(.1)
    plain = ridge(rng, -60, S.w + 60, HZ, 7, .5)
    S.land(plain, .14, .34)
    S.forest(plain, "acacia2", 56, 104, 330, .2, sink=2)
    herd = 1150 if ax > 1200 else 1260
    for k, (n, hh, dx) in enumerate((("giraffe", 86, 0), ("giraffe-2", 70, 96), ("elephant", 54, -230), ("elephant", 40, -150), ("zebra", 32, 250), ("zebra", 30, 310))):
        S.put(n, herd + dx, at_x(plain, herd + dx) + 3, hh, S.tone(.3), flip=k % 2 == 0)
    S.close()
    S.open(.16)
    S.mist(HZ - 60, 130, .55)
    S.close()
    S.open(.32)
    p2 = ridge(rng, -60, S.w + 60, 650, 14, .5)
    S.land(p2, .42, .3)
    S.forest(p2, "acacia", 170, 260, 620, .5, sink=3, sway=True)
    S.grass(p2, .42, 46, (14, 30))
    S.close()
    S.open(.58)
    p3 = ridge(rng, -60, S.w + 60, 738, 16, .5)
    S.land(p3, .7, .24)
    tx = 420 if ax > 1200 else 2010
    S.put("acacia2", tx, at_x(p3, tx) + 8, 470, S.tone(.82), sway=12)
    # the rocks the lion stands on
    gy = at_x(p3, ax)
    for dx, w, h in ((-150, 240, 96), (150, 260, 110), (0, 360, 150)):
        col = S.tone(.86)
        S.add(f'<g transform="translate({ax + dx} {f(gy + 18)})"><path d="{rock_shape(rng, w, h)}" fill="{S.grad([(0, mix(col, c["rim"], .32), 1), (.6, col, 1)], 0, -h, 0, 0)}"/></g>')
    name, flip = CAST["lion"][v]
    S.animal(name, ax, gy + 18 - 146, 176, flip=flip)
    S.grass(p3, .7, 30, (30, 64), lean=.12)
    S.close()
    S.open(.8)
    S.specks(34, 380, 820, c["glow"], (1.2, 2.6), "float")
    S.close()
    S.birds(9, -60, S.w + 60, 150, 420, 64)
    front(S, 870, (60, 140), 20, lean=.16)


def paint_owl(S, v):
    c, rng = S.c, S.rng
    ax = SPOT[v]
    side = 1 if ax < 1900 else -1                     # the dead tree is on this side of the owl; the moon on the other
    common_sky(S, v, 250, 60, clouds=3, moon=True, stars_to=560, sun_x=ax - side * 520)
    if not S.night:
        S.open(.02, .1)
        S.stars(420, 60)
        S.close()
    S.shape("spruce", spruce(random.Random(2)), 90, 200)
    S.shape("spruce2", spruce(random.Random(9)), 90, 200)
    S.open(.05)
    S.land(ridge(rng, -60, S.w + 60, 520, 150, .58, 7, .5), 0, .5)
    S.close()
    S.open(.1)
    S.land(ridge(rng, -60, S.w + 60, 566, 96, .58, 7, .4), .14, .36)
    S.mist(500, 150, .6)
    S.close()
    S.open(.2)
    f1 = ridge(rng, -60, S.w + 60, 610, 22, .5)
    S.land(f1, .3, .2)
    S.forest(f1, "spruce", 60, 120, 30, .3)
    S.close()
    S.open(.28)
    S.mist(590, 120, .5)
    S.close()
    S.open(.4)
    f2 = ridge(rng, -60, S.w + 60, 676, 24, .5)
    S.land(f2, .52, .18)
    S.forest(f2, "spruce2", 120, 210, 50, .52)
    # a cabin with a light on
    hx = 560 if ax > 1200 else 1820
    hy = at_x(f2, hx) + 12
    S.add(f'<path d="M{hx - 62} {f(hy)}L{hx - 62} {f(hy - 52)}L{hx - 76} {f(hy - 52)}L{hx} {f(hy - 108)}L{hx + 26} {f(hy - 89)}L{hx + 26} {f(hy - 112)}L{hx + 44} {f(hy - 112)}L{hx + 44} {f(hy - 76)}L{hx + 76} {f(hy - 52)}L{hx + 62} {f(hy - 52)}L{hx + 62} {f(hy)}Z" fill="{S.tone(.78)}"/>')
    S.glow(c["pop"], hx - 22, hy - 28, 90, .8)
    S.add(f'<g class="sc-tw" style="animation-duration:4s"><rect x="{hx - 36}" y="{f(hy - 42)}" width="28" height="28" fill="{c["pop"]}"/></g>'
          f'<path d="M{hx - 22} {f(hy - 42)}v28M{hx - 36} {f(hy - 28)}h28" stroke="{S.tone(.9)}" stroke-width="2.4"/>')
    for k in range(3):
        S.add(f'<g transform="translate({hx + 35 + k * 5} {f(hy - 118 - k * 26)})"><g class="sc-rise" style="animation-duration:{6 + k}s;animation-delay:-{k * 2}s">'
              f'<ellipse rx="{12 + k * 5}" ry="{8 + k * 3}" fill="{mix(c["glow"], c["sky"][1], .5)}" fill-opacity=".4" filter="{S.blur(6)}"/></g></g>')
    S.close()
    S.open(.55)
    S.specks(40, 480, 840, c["pop"], (1.6, 3), "float", glow=True)
    S.close()
    S.open(.72)
    f3 = ridge(rng, -60, S.w + 60, 790, 22, .5)
    S.land(f3, .82, .14)
    S.forest(f3, "spruce", 260, 420, 170, .84, x0=-40, x1=ax - 420, sway=True)
    S.forest(f3, "spruce2", 260, 420, 170, .84, x0=ax + 560, sway=True)
    S.close()
    # the dead tree the owl is on
    S.open(.9)
    side = 1 if ax < 1900 else -1
    tx, by = ax + side * 230, 470
    col = mix(c["near"], "#000000", .2)
    trunk = (f"M{tx - 44} {S.h + 40}C{tx - 30} 760 {tx - 40} 620 {tx - 24} 500C{tx - 16} 430 {tx - 30} 370 {tx - 36} 300L{tx - 14} 296C{tx - 6} 350 {tx + 6} 380 {tx + 12} 330"
             f"L{tx + 28} 334C{tx + 26} 400 {tx + 34} 440 {tx + 30} 520C{tx + 24} 640 {tx + 44} 770 {tx + 56} {S.h + 40}Z")
    branch = (f"M{tx - 20 * side} {by + 30}C{tx - side * 90} {by + 12} {tx - side * 190} {by + 20} {tx - side * 330} {by - 6}L{tx - side * 430} {by - 30}L{tx - side * 428} {by - 22}"
              f"L{tx - side * 330} {by + 6}C{tx - side * 200} {by + 34} {tx - side * 100} {by + 30} {tx - 20 * side} {by + 56}Z"
              f"M{tx - side * 300} {by - 2}L{tx - side * 372} {by - 70}L{tx - side * 366} {by - 72}L{tx - side * 286} {by + 2}Z")
    S.add(f'<path d="{trunk}{branch}" fill="{S.grad([(0, mix(col, c["rim"], .3), 1), (1, col, 1)], tx - 60, 0, tx + 60, 0)}"/>')
    name, flip = CAST["owl"][v]
    S.animal(name, ax + side * 8, by + 6, 138, flip=flip, shadow=False)
    S.close()
    S.silhouette("owl-fly")
    S.add(f'<g transform="translate({ax - side * 520 + (330 if ax - side * 520 < 1200 else -330)} 330)"><g class="sc-float" style="animation-duration:11s">')
    S.put("owl-fly", 0, 0, 50, S.tone(.7))
    S.add("</g></g>")
    front(S, 868, (36, 86), 26, ferns=9)


def paint_bear(S, v):
    c, rng = S.c, S.rng
    ax, LK = SPOT[v], 620
    common_sky(S, v, 300 if not S.night else 200, 56 if not S.night else 46)
    S.shape("spruce", spruce(random.Random(5)), 90, 200)
    S.shape("spruce2", spruce(random.Random(12)), 90, 200)
    for n in ("stag", "stag-2", "hare"):
        S.silhouette(n)
    S.open(.05)
    S.land(ridge(rng, -60, S.w + 60, 500, 170, .6, 7, .55), 0, .55)
    S.close()
    S.open(.1)
    S.land(ridge(rng, -60, S.w + 60, 548, 96, .58, 7, .4), .14, .34)
    S.mist(480, 150, .65)
    S.close()
    S.open(.2)
    f1 = ridge(rng, -60, S.w + 60, LK - 14, 14, .5)
    S.land(f1, .3, .2, LK + 6)
    S.forest(f1, "spruce", 60, 124, 28, .32)
    S.close()
    # the lake
    S.open(.26)
    S.water(LK, SUN[v], 760)
    refl = S.grad([(0, S.tone(.32), .55), (1, S.tone(.32), 0)], 0, LK, 0, LK + 90)
    S.add(f'<rect x="-80" y="{LK}" width="{S.w + 160}" height="90" fill="{refl}"/>')
    sx = 1000 if ax > 1200 else 1420
    S.put("stag", sx, LK + 3, 60, S.tone(.5), flip=ax > 1200)
    S.put("stag-2", sx + 80, LK + 4, 48, S.tone(.5), flip=ax < 1200)
    S.close()
    S.open(.34)
    S.mist(LK - 30, 90, .45)
    S.close()
    S.open(.6)
    shore = ridge(rng, -60, S.w + 60, 742, 18, .5)
    S.land(shore, .72, .22)
    S.forest(shore, "spruce2", 240, 420, 150, .76, x0=-40, x1=min(ax, 1200) - 330, sway=True)
    S.forest(shore, "spruce", 240, 420, 150, .76, x0=max(ax, 1200) + 380, sway=True)
    for _ in range(9):
        x = rng.uniform(20, S.w - 20)
        S.add(f'<g transform="translate({f(x)} {f(at_x(shore, x) + 8)})"><path d="{rock_shape(rng, rng.uniform(40, 110), rng.uniform(22, 50))}" fill="{S.tone(.86)}"/></g>')
    name, flip = CAST["bear"][v]
    S.animal(name, ax, at_x(shore, ax) + 6, 176, flip=flip)
    hx = ax - 460 if ax > 1200 else ax + 470
    S.put("hare", hx, at_x(shore, hx) + 5, 40, S.tone(1), flip=ax > 1200)
    S.grass(shore, .72, 38, (16, 36))
    S.close()
    S.open(.8)
    S.specks(22, 520, 840, c["pop"] if S.night else c["glow"], (1.6, 3), "float", glow=S.night)
    S.close()
    S.birds(6, -60, S.w + 60, 120, 360, 76)
    front(S, 868, (34, 80), 26, ferns=12)


def iceberg(S, x, y, s, flip=False):
    c = S.c
    pts = [(-170, 0), (-140, -66), (-96, -120), (-60, -92), (-10, -196), (36, -150), (72, -168), (130, -70), (180, 0)]
    k = -1 if flip else 1
    body = "M" + "L".join(f"{f(x + a * s * k)} {f(y + b * s)}" for a, b in pts) + "Z"
    shade = "M" + "L".join(f"{f(x + a * s * k)} {f(y + b * s)}" for a, b in ((-10, -196), (36, -150), (72, -168), (130, -70), (180, 0), (30, 0), (20, -100))) + "Z"
    ice = c["ice"]
    S.add(f'<path d="{body}" fill="{S.grad([(0, ice, 1), (1, mix(ice, c["water"][2], .45), 1)], 0, y - 200 * s, 0, y)}"/><path d="{shade}" fill="{c["water"][3]}" fill-opacity=".26"/>'
          f'<path d="M{f(x - 170 * s)} {f(y)}L{f(x + 180 * s)} {f(y)}L{f(x + 120 * s)} {f(y + 70 * s)}L{f(x - 110 * s)} {f(y + 60 * s)}Z" fill="{ice}" fill-opacity=".16"/>')


def paint_penguin(S, v):
    c, rng = S.c, S.rng
    ax, SEA = SPOT[v], 560
    ice = c["ice"]
    common_sky(S, v, 330 if not S.night else 170, 50 if not S.night else 34, clouds=3)
    if S.night:                                      # the lights in the sky
        S.open(.03, .2)
        for k, col in enumerate(("#5cf2c0", "#49b8ff", "#b07cff", "#5cf2c0")):
            top = ridge(rng, -200, S.w + 200, 150 + k * 46, 60, .5, 5)
            d = poly(top) + "L" + "L".join(f"{round(x)} {round(y + 190 + rng.uniform(-30, 30))}" for x, y in reversed(top)) + "Z"
            S.add(f'<g class="sc-aur" style="animation-duration:{11 + k * 3}s;animation-delay:-{k * 3}s;transform-origin:1200px 200px"><path d="{d}" '
                  f'fill="{S.grad([(0, col, 0), (.3, col, .5), (1, col, 0)], 0, 120 + k * 46, 0, 380 + k * 46)}" filter="{S.blur(14)}"/></g>')
        S.close()
    for n in ("penguin", "penguin-side", "penguin-3", "penguin-4", "seal", "polar-bear"):
        S.silhouette(n)
    S.open(.05)
    m = ridge(rng, -60, S.w + 60, 500, 150, .6, 7, .55)
    top = min(p[1] for p in m)
    S.add(f'<path d="{poly(m, SEA + 10)}" fill="{S.grad([(0, ice, 1), (.5, mix(ice, c["far"], .55), 1), (1, c["far"], 1)], 0, top, 0, SEA)}"/>')
    S.close()
    S.open(.1)
    S.mist(470, 110, .5)
    S.close()
    S.open(.16)
    S.water(SEA, SUN[v], 720)
    iceberg(S, 520 if ax > 1200 else 1900, SEA + 54, 1.0)
    iceberg(S, 2060 if ax > 1200 else 420, SEA + 40, .7, True)
    for _ in range(8):
        x, y, w = rng.uniform(40, S.w - 40), rng.uniform(SEA + 26, SEA + 130), rng.uniform(50, 130)
        S.add(f'<g transform="translate({f(x)} {f(y)})"><g class="sc-bob" style="animation-duration:{rng.uniform(4, 7):.1f}s"><path d="M{f(-w)} 0L{f(-w * .6)} -8L{f(w * .7)} -9L{f(w)} 0L{f(w * .6)} 7L{f(-w * .7)} 7Z" fill="{ice}"/>'
              f'<path d="M{f(-w)} 0L{f(w)} 0L{f(w * .6)} 7L{f(-w * .7)} 7Z" fill="{c["water"][3]}" fill-opacity=".22"/></g></g>')
    fx = 1120 if ax > 1200 else 1380
    S.add(f'<g transform="translate({fx} {SEA + 96})"><g class="sc-bob"><path d="M-120 0L-70 -10L84 -11L124 0L80 9L-90 9Z" fill="{ice}"/>')
    S.put("seal", 0, -6, 34, S.tone(.9))
    S.add("</g></g>")
    S.close()
    S.open(.55)
    snow = ridge(rng, -60, S.w + 60, 730, 22, .5)
    top = min(p[1] for p in snow)
    S.add(f'<path d="{poly(snow, S.h + 40)}" fill="{S.grad([(0, ice, 1), (.4, mix(ice, c["far"], .3), 1), (1, mix(ice, c["far"], .75), 1)], 0, top, 0, top + 240)}"/>')
    for dx, n, hh, fl in ((0, CAST["penguin"][v][0], 164, CAST["penguin"][v][1]), (118, "penguin-3", 112, True), (-112, "penguin-4", 96, False), (210, "penguin-side", 124, True)):
        S.animal(n, ax + dx, at_x(snow, ax + dx) + 6, hh, flip=fl)
    S.close()
    S.open(.8)
    S.specks(70, 60, 780, ice, (1.4, 3.2), "fall")
    S.close()
    S.open(1.0)
    drift = ridge(rng, -60, S.w + 60, 862, 24, .5)
    top = min(p[1] for p in drift)
    S.add(f'<path d="{poly(drift, S.h + 40)}" fill="{S.grad([(0, mix(ice, c["far"], .2), 1), (1, mix(ice, c["near"], .55), 1)], 0, top, 0, S.h)}"/>')
    if S.prop:
        S.prop(S, drift)
    S.close()


def mesa(S, x, y, w, h, d):
    """A table of rock: a skirt of fallen stone, a wall, a top that is nearly level."""
    c, rng = S.c, S.rng
    j = lambda a: rng.uniform(-a, a)
    left = [(x - w * .86, y), (x - w * .66, y - h * .17), (x - w * .52, y - h * .34)] + [(x - w * .47 + j(5), y - h * t) for t in (.48, .64, .8, .93)]
    top = [(x - w * .43, y - h), (x - w * .22, y - h * rng.uniform(.99, 1.03)), (x - w * .06, y - h), (x - w * .03, y - h * rng.uniform(.91, .95)),
           (x + w * .2, y - h * rng.uniform(.92, .96)), (x + w * .24, y - h * rng.uniform(.84, .88)), (x + w * .38, y - h * .86)]
    right = [(x + w * .43 + j(5), y - h * t) for t in (.76, .62, .48)] + [(x + w * .5, y - h * .34), (x + w * .68, y - h * .16), (x + w * .9, y)]
    col = S.tone(d)
    S.add(f'<path d="{poly(left + top + right)}Z" fill="{S.grad([(0, mix(col, c["rim"], .5), 1), (.5, col, 1), (1, mix(col, c["sky"][2], .45), 1)], 0, y - h, 0, y)}"/>')
    dark = [top[2], top[3], top[4], top[5], top[6]] + right + [(x + w * .16, y), (x + w * .1, y - h * .34), (x + w * .04, y - h * .6)]
    S.add(f'<path d="{poly(dark)}Z" fill="{c["near"]}" fill-opacity=".13"/>')
    cracks = "".join(f"M{f(x + w * t)} {f(y - h * rng.uniform(.86, .95))}l{f(j(4))} {f(h * rng.uniform(.2, .5))}" for t in (-.36, -.24, -.12, .1, .3))
    S.add(f'<path d="{cracks}" stroke="{c["near"]}" stroke-opacity=".14" stroke-width="2" stroke-linecap="round"/>')


def paint_tortoise(S, v):
    c, rng = S.c, S.rng
    ax = SPOT[v]
    common_sky(S, v, 250 if not S.night else 220, 60 if not S.night else 66, clouds=2, stars_to=600)
    if S.night:                                      # the band of stars across the sky
        S.open(.02, .2)
        S.add(f'<g transform="rotate(-16 1200 300)"><rect x="-400" y="170" width="3200" height="260" fill="{S.grad([(0, c["glow"], 0), (.5, c["glow"], .1), (1, c["glow"], 0)], 0, 170, 0, 430)}"/></g>')
        S.stars(600, 150)
        S.close()
    S.shape("saguaro", saguaro(random.Random(6)), 130, 200)
    S.shape("saguaro2", saguaro(random.Random(13)), 130, 200)
    for n in ("camel", "camel-2", "soar", "soar-2"):
        S.silhouette(n)
    S.open(.05)
    for x, w, h in ((300, 300, 190), (760, 170, 130), (1380, 380, 160), (2040, 240, 210)):
        mesa(S, x, 560, w, h, .02)
    S.close()
    S.open(.1)
    S.mist(470, 130, .6)
    for x, w, h in ((1020, 210, 110), (1720, 180, 140), (2300, 200, 120), (40, 220, 130)):
        mesa(S, x, 590, w, h, .16)
    S.close()
    S.open(.22)
    d1 = ridge(rng, -60, S.w + 60, 610, 34, .42)
    S.land(d1, .26, .5)
    cx = 1050 if ax > 1200 else 1300
    for k in range(4):
        S.put("camel" if k % 2 else "camel-2", cx + k * 74, at_x(d1, cx + k * 74) + 3, 46 - k * 2, S.tone(.5), flip=ax < 1200)
    S.close()
    S.open(.4)
    d2 = ridge(rng, -60, S.w + 60, 690, 40, .42)
    S.land(d2, .5, .46)
    S.forest(d2, "saguaro", 110, 190, 420, .6, sink=4)
    for k in range(3):                               # the wind's marks on the sand
        S.add(f'<path d="{smooth([(x, y + 26 + k * 20) for x, y in ridge(rng, 200 + k * 300, 1500 + k * 300, at_x(d2, 900), 8, .5, 4)])}" stroke="{c["near"]}" stroke-opacity=".12" stroke-width="2" fill="none"/>')
    S.close()
    S.open(.68)
    g = ridge(rng, -60, S.w + 60, 786, 18, .45)
    S.land(g, .8, .34)
    S.forest(g, "saguaro2", 300, 440, 520, .86, x0=-40, x1=ax - 360, sink=6)
    S.forest(g, "saguaro", 300, 440, 520, .86, x0=ax + 380, sink=6)
    for _ in range(10):
        x = rng.uniform(20, S.w - 20)
        if abs(x - ax) > 190:
            S.add(f'<g transform="translate({f(x)} {f(at_x(g, x) + 8)})"><path d="{rock_shape(rng, rng.uniform(40, 120), rng.uniform(20, 56))}" fill="{S.tone(.9)}"/></g>')
    name, flip = CAST["tortoise"][v]
    S.animal(name, ax, at_x(g, ax) + 6, 108, flip=flip)
    S.grass(g, .8, 110, (14, 30))
    S.close()
    for k, (x, y) in enumerate(((760, 250), (1460, 200))):
        S.add(f'<g transform="translate({x} {y})"><g class="sc-float" style="animation-duration:{14 + k * 5}s">')
        S.put("soar" if k else "soar-2", 0, 0, 22 + k * 6, S.tone(.75))
        S.add("</g></g>")
    S.open(.85)
    S.specks(24, 420, 840, c["glow"], (1.2, 2.4), "float")
    S.close()
    front(S, 872, (20, 52), 70)


WORLDS = dict(fox=paint_fox, cat=paint_cat, lion=paint_lion, owl=paint_owl, bear=paint_bear, penguin=paint_penguin, tortoise=paint_tortoise)

# ───────────────────────────── SMALL PARTS ──────────────────────────


def perch(S):
    """The animal on a line: it stands on the top edge of a frame."""
    name, flip = CAST[S.theme][0]
    h = {"tortoise": 76, "bear": 118, "lion": 122}.get(S.theme, 128)
    S.animal(name, S.w * .55, S.h - 3, h, flip=not flip)
    S.add(f'<g transform="translate({S.w * .14} {S.h - 1})"><g class="sc-sway"><path d="{tuft(S.rng, 34, 8)}" fill="{S.tone(.9)}"/></g></g>'
          f'<g transform="translate({S.w * .9} {S.h - 1})"><g class="sc-sway" style="animation-delay:-2s"><path d="{tuft(S.rng, 26, 7)}" fill="{S.tone(.9)}"/></g></g>')


def grow(S):
    """What grows along the top edge of a card."""
    rng, th, base = S.rng, S.theme, S.h - 1
    x0, x1 = (rng.uniform(10, 60), rng.uniform(300, 430)) if rng.random() < .5 else (rng.uniform(190, 300), S.w - rng.uniform(10, 60))
    line = [(x0, base), (x1, base)]
    if th == "penguin":
        snow = ridge(rng, x0 - 30, x1 + 30, base - 6, 6, .5, 5)
        S.add(f'<path d="{poly(snow, S.h)}" fill="{mix(S.c["ice"], S.c["far"], .35)}"/>')
    else:
        S.grass(line, .9, 22, (14, 38), x0, x1)
    props = {"fox": ("gull", 34), "cat": ("cat-walk", 40), "lion": ("zebra", 40), "owl": ("owl-3", 44), "bear": ("hare", 34), "penguin": ("penguin-4", 44), "tortoise": ("tortoise-2", 30)}[th]
    S.silhouette(props[0])
    S.put(props[0], rng.uniform(x0 + 60, x1 - 60), base, props[1], S.tone(1), flip=rng.random() < .5)
    if th in ("owl", "bear"):
        S.shape("spruce", spruce(random.Random(5)), 90, 200)
        for _ in range(3):
            S.put("spruce", rng.uniform(x0, x1), base, rng.uniform(34, 62), S.tone(.8))
    elif th == "tortoise":
        S.shape("saguaro", saguaro(random.Random(6)), 130, 200)
        for _ in range(2):
            S.put("saguaro", rng.uniform(x0, x1), base, rng.uniform(40, 62), S.tone(.8))
    elif th == "lion":
        S.shape("acacia", acacia(random.Random(4), 200), 300, 200)
        S.put("acacia", rng.uniform(x0 + 60, x1 - 60), base, 62, S.tone(.8))
    elif th == "fox":
        for _ in range(4):
            x = rng.uniform(x0, x1)
            S.add(f'<g transform="translate({f(x)} {base})"><g class="sc-sway"><path d="{kelp(rng, rng.uniform(34, 58))}" fill="{S.tone(.7)}"/></g></g>')


def horizon(S):
    """The line that runs off a heading: a strip of far country, fading at both ends."""
    rng, c = S.rng, S.c
    m = S.id()
    S.defs.append(f'<linearGradient id="{m}g"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                  f'<mask id="{m}"><rect width="{S.w}" height="{S.h}" fill="url(#{m}g)"/></mask>')
    S.add(f'<g mask="url(#{m})">')
    y = S.h - 14
    S.add(f'<path d="{poly(ridge(rng, -20, S.w + 20, y - 18, 16, .55, 6, .3), S.h)}" fill="{S.tone(.12)}"/>')
    near = ridge(rng, -20, S.w + 20, y, 6, .5, 5)
    S.add(f'<path d="{poly(near, S.h)}" fill="{S.tone(.5)}"/>')
    key = {"owl": "spruce", "bear": "spruce", "lion": "acacia", "tortoise": "saguaro", "cat": "oak"}.get(S.theme)
    if key:
        maker = dict(spruce=(spruce, 90), acacia=(acacia, 300), saguaro=(saguaro, 130), oak=(oak, 190))[key]
        S.shape(key, maker[0](random.Random(5), 200), maker[1], 200)
        S.forest(near, key, 16, 40, 70 if key != "spruce" else 26, .55, 0, S.w, sink=2)
    S.add("</g>")
    S.birds(3, -20, S.w + 20, 10, 40, 50, .6)


def strip(S):
    """The land above the footer."""
    rng = S.rng
    a = ridge(rng, -60, S.w + 60, 130, 28, .5)
    S.open(.3, 0)
    S.land(a, .3, .3)
    key = {"owl": "spruce", "bear": "spruce", "lion": "acacia", "tortoise": "saguaro", "cat": "oak"}.get(S.theme)
    if key:
        maker = dict(spruce=(spruce, 90), acacia=(acacia, 300), saguaro=(saguaro, 130), oak=(oak, 190))[key]
        S.shape(key, maker[0](random.Random(5), 200), maker[1], 200)
        S.forest(a, key, 60, 120, 150 if key != "spruce" else 60, .4)
    S.close()
    S.open(.7, .2)
    b = ridge(rng, -60, S.w + 60, 186, 16, .5)
    S.land(b, .8, .2)
    S.grass(b, .8, 26, (20, 50))
    name, flip = CAST[S.theme][1]
    S.animal(name, 1900, at_x(b, 1900) + 5, 96 if S.theme != "tortoise" else 60, flip=flip)
    S.close()
    S.open(1.0, .4)
    c = ridge(rng, -60, S.w + 60, 236, 8, .5)
    S.add(f'<path d="{poly(c, S.h + 40)}" fill="{S.c["near"]}"/>')
    S.grass(c, 1.0, 24, (16, 40))
    S.close()


# ───────────────────────────── THE PROJECTS ─────────────────────────
# A project's page shows the theme's world with one thing in it that belongs to that project,
# standing in front, across from the animal: a gramophone for the music bot, a gate thrown open
# for the app that opens blocked sites, a balloon and a signpost for the travel app, …


def solid(S, y0, y1):
    """The fill of a thing in front: dark, the light catching its top."""
    c = S.c
    body = mix(c["near"], "#000000", .2)
    return S.grad([(0, mix(body, c["rim"], .22), 1), (.35, body, 1), (1, body, 1)], 0, y0, 0, y1)


def note(S, x, y, k, delay):
    c = S.c
    return (f'<g transform="translate({f(x)} {f(y)})"><g class="sc-rise" style="animation-duration:{6 + k % 3}s;animation-delay:-{delay:.1f}s">'
            f'<g transform="rotate({(-14, 10, -4)[k % 3]})" fill="{c["pop"]}"><ellipse rx="9" ry="6.5" transform="rotate(-22)"/><rect x="6.5" y="-38" width="3" height="38"/>'
            + ('<path d="M9.5 -38q12 6 9 20q-2 -9 -9 -11Z"/>' if k % 2 else '<rect x="6.5" y="-38" width="26" height="5"/><rect x="29.5" y="-38" width="3" height="32"/><ellipse cx="26" cy="-6" rx="9" ry="6.5" transform="rotate(-22 26 -6)"/>')
            + "</g></g></g>")


def p_beatra(S, x, y):
    """A gramophone on an old crate, the music coming out of it."""
    fill = solid(S, y - 280, y)
    S.add(f'<path d="M{x - 66} {y}L{x - 62} {y - 104}L{x + 62} {y - 104}L{x + 66} {y}Z" fill="{fill}"/>'
          f'<path d="M{x - 50} {y - 74}h100M{x - 50} {y - 40}h100" stroke="{S.c["rim"]}" stroke-opacity=".18" stroke-width="3"/>'
          f'<ellipse cx="{x}" cy="{y - 108}" rx="54" ry="8" fill="{fill}"/>'
          f'<path d="M{x - 8} {y - 112}L{x + 2} {y - 124}C{x + 30} {y - 168} {x + 66} {y - 214} {x + 140} {y - 276}C{x + 168} {y - 246} {x + 178} {y - 200} {x + 170} {y - 166}C{x + 104} {y - 156} {x + 52} {y - 134} {x + 16} {y - 108}Z" fill="{fill}"/>'
          f'<path d="M{x + 140} {y - 276}C{x + 168} {y - 246} {x + 178} {y - 200} {x + 170} {y - 166}" stroke="{S.c["rim"]}" stroke-opacity=".5" stroke-width="3" fill="none"/>')
    S.glow(S.c["pop"], x + 160, y - 222, 110, .35)
    S.add("".join(note(S, x + 150 + S.rng.uniform(-50, 60), y - 240 - S.rng.uniform(0, 120), k, k * 1.3) for k in range(7)))


def p_shroudly(S, x, y):
    """A fence across the land and its gate thrown open, light coming through."""
    c = S.c
    S.glow(c["glow"], x, y - 90, 260, .9)
    S.add(f'<path d="M{x - 66} {y + 8}L{x + 66} {y + 8}L{x + 190} {y + 60}L{x - 190} {y + 60}Z" fill="{S.grad([(0, c["glow"], .55), (1, c["glow"], 0)], 0, y, 0, y + 60)}"/>')
    fill = solid(S, y - 200, y)
    posts = ""
    for side in (-1, 1):
        for k in range(1, 6):
            px = x + side * (70 + k * 46)
            posts += f"M{px - 7} {y + 4}L{px - 7} {y - 112}L{px} {y - 122}L{px + 7} {y - 112}L{px + 7} {y + 4}Z"
        posts += f"M{x + side * 70 - side * 0} {y - 96}L{x + side * 320} {y - 96}L{x + side * 320} {y - 84}L{x + side * 70} {y - 84}Z".replace("--", "")
        posts += f"M{x + side * 70} {y - 46}L{x + side * 320} {y - 46}L{x + side * 320} {y - 34}L{x + side * 70} {y - 34}Z"
        gx = x + side * 70
        posts += f"M{gx - 11} {y + 6}L{gx - 11} {y - 168}L{gx + 11} {y - 168}L{gx + 11} {y + 6}ZM{gx - 16} {y - 168}L{gx + 16} {y - 168}L{gx} {y - 184}Z"
    S.add(f'<path d="{posts}" fill="{fill}"/>')
    hx = x + 70                                       # the gate, swung out towards us
    S.add(f'<g stroke="{mix(c["near"], "#000000", .2)}" stroke-width="9" stroke-linecap="round" fill="none">'
          f'<path d="M{hx} {y - 150}L{hx + 96} {y - 176}M{hx} {y - 20}L{hx + 96} {y - 8}M{hx + 96} {y - 176}L{hx + 96} {y - 8}M{hx} {y - 20}L{hx + 96} {y - 176}"/>'
          + "".join(f'<path d="M{hx + t * 96:.0f} {y - 150 - t * 26:.0f}L{hx + t * 96:.0f} {y - 20 + t * 12:.0f}" stroke-width="5"/>' for t in (.25, .5, .75)) + "</g>")


def p_vanigo(S, x, y):
    """A signpost pointing every way, and a balloon on its way somewhere."""
    c = S.c
    fill = solid(S, y - 300, y)
    boards = ""
    for k, (h, ang, ln) in enumerate(((268, -8, 150), (222, 172, 130), (176, -2, 120), (130, 186, 104))):
        boards += (f'<g transform="translate({x} {y - h}) rotate({ang})"><path d="M-6 -15L{ln - 18} -15L{ln} 0L{ln - 18} 15L-6 15Z" fill="{fill}"/>'
                   f'<path d="M6 -4h{ln * .55:.0f}M6 4h{ln * .38:.0f}" stroke="{c["rim"]}" stroke-opacity=".28" stroke-width="3" stroke-linecap="round"/></g>')
    S.add(f'<path d="M{x - 8} {y + 4}L{x - 6} {y - 296}L{x} {y - 304}L{x + 6} {y - 296}L{x + 8} {y + 4}Z" fill="{fill}"/>{boards}')
    bx, by = (x - 300 if x > 1200 else x + 300), 330
    i = S.id()
    env = "M-22 100C-60 70 -95 20 -95 -32C-95 -92 -52 -128 0 -128C52 -128 95 -92 95 -32C95 20 60 70 22 100Z"
    base = mix(c["glow"], c["far"], .35 if not S.night else .6)
    stripe = mix(c["pop"], c["far"], .2 if not S.night else .45)
    S.defs.append(f'<clipPath id="{i}"><path d="{env}"/></clipPath>')
    S.add(f'<g transform="translate({bx} {by})"><g class="sc-float" style="animation-duration:16s"><g transform="scale(.8)">'
          f'<path d="{env}" fill="{base}"/><g clip-path="url(#{i})" fill="{stripe}"><path d="M0 -130C-44 -90 -44 60 0 104C44 60 44 -90 0 -130Z"/>'
          f'<path d="M-96 -130C-140 -90 -140 60 -96 104C-80 60 -80 -90 -96 -130Z"/><path d="M96 -130C80 -90 80 60 96 104C140 60 140 -90 96 -130Z"/>'
          f'<rect x="-100" y="-40" width="200" height="140" fill="{c["near"]}" fill-opacity=".14"/></g>'
          f'<path d="M-22 100L-14 128M22 100L14 128" stroke="{c["near"]}" stroke-width="2.5"/><rect x="-17" y="126" width="34" height="24" rx="3" fill="{mix(c["near"], c["far"], .25)}"/>'
          f'</g></g></g>')


def p_sylon(S, x, y):
    """A watchtower keeping an eye on the land, its light sweeping across."""
    c = S.c
    fill = solid(S, y - 360, y)
    dark = mix(c["near"], "#000000", .2)
    S.add(f'<g stroke="{dark}" stroke-linecap="round"><path d="M{x - 78} {y + 4}L{x - 44} {y - 240}M{x + 78} {y + 4}L{x + 44} {y - 240}" stroke-width="12"/>'
          f'<path d="M{x - 70} {y - 50}L{x + 62} {y - 130}M{x + 70} {y - 50}L{x - 62} {y - 130}M{x - 58} {y - 140}L{x + 52} {y - 220}M{x + 58} {y - 140}L{x - 52} {y - 220}M{x - 72} {y - 50}h144M{x - 60} {y - 135}h120" stroke-width="5"/></g>'
          f'<path d="M{x - 64} {y - 236}L{x + 64} {y - 236}L{x + 64} {y - 250}L{x - 64} {y - 250}ZM{x - 56} {y - 250}L{x - 56} {y - 312}L{x + 56} {y - 312}L{x + 56} {y - 250}Z" fill="{fill}"/>'
          f'<rect x="{x - 40}" y="{y - 300}" width="80" height="34" fill="{c["pop"]}"/>'
          f'<path d="M{x - 80} {y - 310}L{x} {y - 356}L{x + 80} {y - 310}Z" fill="{fill}"/>')
    S.glow(c["pop"], x, y - 283, 90, .7)
    beam = S.grad([(0, c["glow"], .8 if S.night else .45), (1, c["glow"], 0)], 0, 0, 760, 0)
    S.add(f'<g transform="translate({x} {y - 283}) rotate({-168 if x > 1200 else -12})"><g class="sc-beam" style="animation-duration:7s"><path d="M0 0L760 -70L760 70Z" fill="{beam}"/></g></g>')


def p_mcstat(S, x, y):
    """A hill made of blocks, a blocky tree on it, a few blocks floating up."""
    c = S.c
    s, a, b = 40, 40 * .866, 40 * .5
    top_c = mix(S.tone(.7), "#7fbf5a" if not S.night else "#3d6b3a", .45)
    side_l, side_r = S.tone(.86), mix(S.tone(1), "#000000", .2)
    leaf_t, leaf_l, leaf_r = mix(top_c, c["rim"], .25), mix(top_c, c["near"], .35), mix(top_c, c["near"], .6)
    wood = [mix(S.tone(.7), "#8a5a33", .4), mix(S.tone(.85), "#6b4423", .4), mix(S.tone(1), "#4a2e17", .3)]
    blocks = [(i, j, 0, "g") for i in range(3) for j in range(3)] + [(i, j, 1, "g") for i in range(2) for j in range(2)] + [(0, 0, 2, "w"), (0, 0, 3, "w"), (0, 0, 4, "w")]
    blocks += [(i, j, k, "l") for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (5, 6) if not (k == 6 and abs(i) + abs(j) == 2)] + [(0, 0, 7, "l")]
    blocks.sort(key=lambda q: (q[2], q[0] + q[1]))
    X, Y = x, y - s - b - 4 * b
    out = ""
    for i, j, k, kind in blocks:
        cx, cy = X + (i - j) * a, Y + (i + j) * b - k * s
        t, l, r = {"g": (top_c, side_l, side_r), "w": wood, "l": (leaf_t, leaf_l, leaf_r)}[kind]
        out += (f'<path d="M{f(cx)} {f(cy - b)}L{f(cx + a)} {f(cy)}L{f(cx)} {f(cy + b)}L{f(cx - a)} {f(cy)}Z" fill="{t}"/>'
                f'<path d="M{f(cx - a)} {f(cy)}L{f(cx)} {f(cy + b)}L{f(cx)} {f(cy + b + s)}L{f(cx - a)} {f(cy + s)}Z" fill="{l}"/>'
                f'<path d="M{f(cx)} {f(cy + b)}L{f(cx + a)} {f(cy)}L{f(cx + a)} {f(cy + s)}L{f(cx)} {f(cy + b + s)}Z" fill="{r}"/>')
    S.add(out)
    for k in range(5):
        fx, fy, q = x + S.rng.uniform(-160, 160), y - 330 - S.rng.uniform(0, 120), S.rng.uniform(5, 9)
        S.add(f'<g transform="translate({f(fx)} {f(fy)})"><g class="sc-float" style="animation-duration:{S.rng.uniform(5, 9):.1f}s;animation-delay:-{k * 1.7:.1f}s">'
              f'<path d="M0 {f(-q)}L{f(q * .87)} {f(-q / 2)}L0 0L{f(-q * .87)} {f(-q / 2)}Z" fill="{c["pop"]}"/><path d="M{f(-q * .87)} {f(-q / 2)}L0 0L0 {f(q)}L{f(-q * .87)} {f(q / 2)}Z" fill="{mix(c["pop"], c["near"], .3)}"/>'
              f'<path d="M0 0L{f(q * .87)} {f(-q / 2)}L{f(q * .87)} {f(q / 2)}L0 {f(q)}Z" fill="{mix(c["pop"], c["near"], .5)}"/></g></g>')


def p_justanime(S, x, y):
    """A gate of the old kind under a cherry tree in flower, its petals coming down."""
    c = S.c
    red = mix("#d23a2a" if not S.night else "#a8332a", c["near"], .25 if not S.night else .45)
    pink = "#f4a7c2" if not S.night else "#b56a8a"
    tx = x + (150 if x < 1200 else -150)
    sak = oak(random.Random(17), 420)
    S.add(f'<g transform="translate({tx} {y + 6})"><path d="{sak[0]}" fill="{solid(S, -420, 0)}"/><g class="sc-sway" style="animation-duration:8s"><path d="{sak[1]}" fill="{pink}"/></g></g>')
    S.add(f'<g fill="{red}"><path d="M{x - 86} {y + 4}L{x - 80} {y - 236}L{x - 64} {y - 236}L{x - 60} {y + 4}ZM{x + 60} {y + 4}L{x + 64} {y - 236}L{x + 80} {y - 236}L{x + 86} {y + 4}Z"/>'
          f'<path d="M{x - 112} {y - 196}L{x + 112} {y - 196}L{x + 112} {y - 180}L{x - 112} {y - 180}Z"/>'
          f'<path d="M{x - 150} {y - 250}Q{x} {y - 236} {x + 150} {y - 250}L{x + 140} {y - 232}Q{x} {y - 220} {x - 140} {y - 232}Z"/>'
          f'<path d="M{x - 10} {y - 230}L{x + 10} {y - 230}L{x + 10} {y - 196}L{x - 10} {y - 196}Z"/></g>'
          f'<path d="M{x - 160} {y - 258}Q{x} {y - 244} {x + 160} {y - 258}L{x + 156} {y - 248}Q{x} {y - 236} {x - 156} {y - 248}Z" fill="{mix(c["near"], "#000000", .3)}"/>')
    for k in range(26):
        px, py = tx + S.rng.uniform(-260, 260), y - S.rng.uniform(180, 520)
        S.add(f'<g transform="translate({f(px)} {f(py)})"><g class="sc-fall" style="animation-duration:{S.rng.uniform(7, 12):.1f}s;animation-delay:-{S.rng.uniform(0, 12):.1f}s">'
              f'<ellipse rx="5" ry="3" transform="rotate({S.rng.uniform(0, 180):.0f})" fill="{pink}"/></g></g>')


def p_justdiscord(S, x, y):
    """A camp: tents with their lamps lit and a fire in the middle, people's places side by side."""
    c = S.c
    fill = solid(S, y - 180, y)
    lamp = c["pop"]
    for dx, w, h in ((-200, 170, 130), (190, 190, 150), (-20 if x < 1200 else 20, 120, 92)):
        tx = x + dx
        S.add(f'<path d="M{tx - w / 2:.0f} {y + 4}L{tx} {y - h}L{tx + w / 2:.0f} {y + 4}Z" fill="{fill}"/>'
              f'<path d="M{tx - w * .14:.0f} {y + 4}L{tx} {y - h * .55:.0f}L{tx + w * .14:.0f} {y + 4}Z" fill="{lamp}" fill-opacity=".9"/>'
              f'<path d="M{tx} {y - h}L{tx - 10} {y - h - 16}M{tx} {y - h}L{tx + 10} {y - h - 16}" stroke="{mix(c["near"], "#000", .2)}" stroke-width="4"/>')
        S.glow(lamp, tx, y - h * .2, w * .6, .4)
    fx = x - 10 if x < 1200 else x + 10
    fx += 0
    fy = y + 30
    S.glow(c["pop"], fx, fy - 30, 160, .8)
    S.add(f'<path d="M{fx - 40} {fy}L{fx + 36} {fy - 18}L{fx + 40} {fy - 8}L{fx - 36} {fy + 10}ZM{fx + 40} {fy}L{fx - 36} {fy - 18}L{fx - 40} {fy - 8}L{fx + 36} {fy + 10}Z" fill="{fill}"/>'
          f'<g class="sc-tw" style="animation-duration:.6s"><path d="M{fx - 22} {fy - 10}C{fx - 30} {fy - 40} {fx - 6} {fy - 50} {fx} {fy - 84}C{fx + 10} {fy - 54} {fx + 32} {fy - 40} {fx + 22} {fy - 10}Z" fill="{c["pop"]}"/></g>'
          f'<path d="M{fx - 10} {fy - 10}C{fx - 14} {fy - 26} {fx - 2} {fy - 34} {fx + 2} {fy - 52}C{fx + 8} {fy - 34} {fx + 16} {fy - 24} {fx + 10} {fy - 10}Z" fill="{c["glow"]}"/>')
    for k in range(10):
        S.add(f'<g transform="translate({f(fx + S.rng.uniform(-20, 20))} {f(fy - 70)})"><g class="sc-rise" style="animation-duration:{S.rng.uniform(2.5, 4.5):.1f}s;animation-delay:-{S.rng.uniform(0, 4):.1f}s">'
              f'<circle r="2.4" fill="{c["glow"]}"/></g></g>')


def p_dotrai(S, x, y):
    """A telescope on its legs, turned to stars that join into a figure."""
    c = S.c
    fill = solid(S, y - 260, y)
    dark = mix(c["near"], "#000000", .2)
    px, py = x, y - 170
    S.add(f'<path d="M{px} {py}L{px - 70} {y + 4}M{px} {py}L{px + 64} {y + 4}M{px} {py}L{px + 8} {y + 6}" stroke="{dark}" stroke-width="8" stroke-linecap="round"/>'
          f'<g transform="translate({px} {py}) rotate({-32 if x > 1200 else -148})"><path d="M-80 -11L70 -18L70 18L-80 11Z" fill="{fill}"/><rect x="70" y="-22" width="22" height="44" rx="4" fill="{fill}"/>'
          f'<rect x="-104" y="-7" width="26" height="14" fill="{fill}"/><path d="M-60 -9L40 -14" stroke="{c["rim"]}" stroke-opacity=".4" stroke-width="3"/></g>')
    sx = x - 380 if x > 1200 else x + 380
    pts = [(sx - 230, 320), (sx - 140, 262), (sx - 40, 290), (sx + 40, 236), (sx + 150, 258), (sx + 210, 330), (sx + 90, 352), (sx - 40, 290)]
    col = c["glow"] if S.night else mix(c["glow"], "#ffffff", .5)
    S.add(f'<path d="{poly(pts)}" stroke="{col}" stroke-opacity="{.5 if S.night else .7}" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>')
    for k, (sx2, sy2) in enumerate(pts[:-1]):
        S.add(f'<g class="sc-tw" style="animation-duration:{2 + k % 3 * .7:.1f}s;animation-delay:-{k * .4:.1f}s"><circle cx="{sx2}" cy="{sy2}" r="{6 if k % 3 == 0 else 4.2}" fill="{col}"/>'
              f'<circle cx="{sx2}" cy="{sy2}" r="16" fill="{col}" fill-opacity=".25"/></g>')


def p_codeshare(S, x, y):
    """The workshop: a house with its windows lit late, smoke from the chimney, its sign over the door."""
    c = S.c
    fill = solid(S, y - 330, y)
    S.add(f'<path d="M{x - 150} {y + 4}L{x - 150} {y - 150}L{x - 172} {y - 150}L{x - 20} {y - 290}L{x + 60} {y - 216}L{x + 60} {y - 286}L{x + 94} {y - 286}L{x + 94} {y - 184}L{x + 132} {y - 150}L{x + 110} {y - 150}L{x + 110} {y + 4}Z" fill="{fill}"/>')
    for wx in (x - 116, x + 46):
        S.glow(c["pop"], wx + 20, y - 92, 100, .6)
        S.add(f'<g class="sc-tw" style="animation-duration:5s"><rect x="{wx}" y="{y - 120}" width="40" height="52" fill="{c["pop"]}"/></g>'
              f'<path d="M{wx + 20} {y - 120}v52M{wx} {y - 94}h40" stroke="{mix(c["near"], "#000", .2)}" stroke-width="4"/>')
    S.add(f'<rect x="{x - 40}" y="{y - 110}" width="50" height="114" fill="{mix(c["near"], "#000", .35)}"/>'
          f'<rect x="{x - 56}" y="{y - 160}" width="82" height="34" rx="4" fill="{mix(c["near"], "#000", .35)}"/>'
          f'<path d="M{x - 30} {y - 152}l-12 9l12 9M{x} {y - 152}l12 9l-12 9M{x - 9} {y - 133}l6 -22" stroke="{c["pop"]}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    for k in range(4):
        S.add(f'<g transform="translate({x + 77 + k * 6} {y - 300 - k * 30})"><g class="sc-rise" style="animation-duration:{6 + k}s;animation-delay:-{k * 1.6:.1f}s">'
              f'<ellipse rx="{14 + k * 6}" ry="{9 + k * 4}" fill="{mix(c["glow"], c["sky"][1], .5)}" fill-opacity=".45" filter="{S.blur(6)}"/></g></g>')


def p_creator(S, x, y):
    """A camera on its tripod, rolling, turned on the place."""
    c = S.c
    fill = solid(S, y - 260, y)
    dark = mix(c["near"], "#000000", .2)
    k = -1 if x > 1200 else 1
    px, py = x, y - 160
    S.add(f'<path d="M{px} {py}L{px - 72} {y + 4}M{px} {py}L{px + 70} {y + 4}M{px} {py}L{px} {y + 6}" stroke="{dark}" stroke-width="8" stroke-linecap="round"/>'
          f'<g transform="translate({px} {py - 10}){" scale(-1 1)" if k < 0 else ""}"><rect x="-70" y="-74" width="120" height="70" rx="8" fill="{fill}"/>'
          f'<path d="M50 -60L96 -74L96 -4L50 -18Z" fill="{fill}"/><circle cx="-40" cy="-96" r="24" fill="{fill}"/><circle cx="10" cy="-96" r="24" fill="{fill}"/>'
          f'<circle cx="-40" cy="-96" r="8" fill="{c["rim"]}" fill-opacity=".25"/><circle cx="10" cy="-96" r="8" fill="{c["rim"]}" fill-opacity=".25"/>'
          f'<rect x="-30" y="-6" width="40" height="10" fill="{fill}"/></g>')
    S.add(f'<g class="sc-tw" style="animation-duration:.9s"><circle cx="{px - k * 52}" cy="{py - 70}" r="6" fill="#ff3b30"/><circle cx="{px - k * 52}" cy="{py - 70}" r="16" fill="#ff3b30" fill-opacity=".3"/></g>')


PROJECTS = {
    "codeshare-technology": (p_codeshare, 0), "beatra-streaming-platform": (p_beatra, 1), "shroudly-anti-censorship": (p_shroudly, 2),
    "vanigo-travel-app": (p_vanigo, 3), "sylon-discord-bot": (p_sylon, 4), "mcstat-minecraft-server-list": (p_mcstat, 0),
    "justanime-anime-tracker": (p_justanime, 1), "justdiscord-server-bot-list": (p_justdiscord, 2), "dotrai-ai-chat": (p_dotrai, 3),
    "creator-studio-automation": (p_creator, 4),
}


def prop_x(v):
    return SPOT[v] - 700 if SPOT[v] > 1200 else SPOT[v] + 700

# ─────────────────────────────── WRITING ────────────────────────────


def world(theme, mode, v, project=None):
    S = Scene(theme, mode, W, H, seed=sum(ord(ch) for ch in theme) * 31 + v * 7, uid=f"{theme[0]}{mode[0]}{v}")
    c = S.c
    if project:
        fn = PROJECTS[project][0]
        S.prop = lambda S, line: fn(S, prop_x(v), at_x(line, prop_x(v)) + 6)
    S.add(f'<rect width="{W}" height="{H}" fill="{S.grad([(0, c["sky"][0], 1), (.45, c["sky"][1], 1), (1, c["sky"][2], 1)], 0, 0, 0, 600)}"/>')
    WORLDS[theme](S, v)
    return S.render()


def small(theme, mode, w, h, seed, fn, lift=False):
    """A small picture that sits on the page itself. At night the page is as dark as the land, so
    things on it are painted in the colour of moonlit land instead."""
    S = Scene(theme, mode, w, h, seed, uid=f"{theme[0]}{mode[0]}s{seed}")
    if lift and S.night:
        c = dict(S.c)
        c["far"], c["near"] = mix(c["sky"][0], c["far"], .9), mix(c["far"], c["glow"], .34)
        S.c = c
    fn(S)
    return S.render()


def css():
    """The colours of every theme as CSS variables, and the list of themes for the picker."""
    out = ["/* Written by scripts/paint.py from UI and SCENES. Do not edit: change the colours there and run it again. */"]
    for th, t in UI.items():
        for mode in ("light", "dark"):
            p, sc = t[mode], SCENES[th][mode]
            vars_ = {
                "bg": sc["sky"][0], "card": p["card"], "ink": p["ink"], "soft": p["soft"], "accent": p["accent"], "warm": p["warm"],
                "marker": p["marker"], "wash": p["wash"], "deep": p["deep"], "leaf-1": p["leaf"][0], "leaf-2": p["leaf"][1], "leaf-3": p["leaf"][2],
                "sky-1": sc["sky"][1], "sky-2": sc["sky"][2], "glow": sc["glow"], "pop": sc["pop"],
                "ground": sc["near"], "ground-ink": mix(sc["near"], "#ffffff", .86), "ground-soft": mix(sc["near"], "#ffffff", .6),
            }
            sel = f'html[data-theme="{th}"][data-mode="{mode}"]'
            if th == DEFAULT_THEME and mode == "light":
                sel = ":root, " + sel
            out.append(sel + " {\n" + "".join(f"  --{k}: {v};\n" for k, v in vars_.items()) + f"  color-scheme: {mode};\n}}")
    (ROOT / "src" / "app" / "themes.css").write_text("\n\n".join(out) + "\n", encoding="utf-8")
    themes = [dict(id=th, name=t["name"], swatch=[SCENES[th]["light"]["sky"][1], SCENES[th]["light"]["sky"][2], SCENES[th]["light"]["pop"], SCENES[th]["light"]["near"]]) for th, t in UI.items()]
    scenes = dict(pages={name: dict(v=v, focus=round(SPOT[v] / W, 3)) for v, name in enumerate(PAGES)},
                  projects={slug: dict(v=v, focus=round((SPOT[v] + prop_x(v)) / 2 / W, 3)) for slug, (_, v) in PROJECTS.items()})
    (ROOT / "src" / "resources" / "themes.json").write_text(json.dumps(dict(default=DEFAULT_THEME, themes=themes, scenes=scenes), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    only = sys.argv[1:] or list(SCENES)
    for theme in only:
        for mode in ("light", "dark"):
            d = OUT / theme / mode
            d.mkdir(parents=True, exist_ok=True)
            for v in range(len(PAGES)):
                (d / f"world-{v}.svg").write_text(world(theme, mode, v))
            for slug in PROJECTS:
                (d / f"project-{slug}.svg").write_text(world(theme, mode, PROJECTS[slug][1], slug))
            (d / "perch.svg").write_text(small(theme, mode, 260, 170, 21, perch, True))
            for n in range(4):
                (d / f"grow-{n}.svg").write_text(small(theme, mode, 600, 80, 31 + n * 7, grow, True))
            for n in range(3):
                (d / f"line-{n}.svg").write_text(small(theme, mode, 900, 84, 61 + n * 5, horizon, True))
            (d / "ground.svg").write_text(small(theme, mode, 2400, 260, 91, strip))
            print(theme, mode)
    if not os.environ.get("PREVIEW_DIR"):
        css()
