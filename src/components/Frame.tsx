"use client";

import { useEffect, useId, useRef, useState } from "react";

// A small seeded random generator, so a frame keeps its shape between renders.
function mulberry(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

type Point = [number, number];

/** A smooth path through the points (Catmull-Rom as cubic Béziers). */
function smooth(points: Point[]) {
  const at = (i: number) => points[Math.max(0, Math.min(points.length - 1, i))];
  const f = (n: number) => n.toFixed(1);
  let d = `M${f(points[0][0])} ${f(points[0][1])}`;
  for (let i = 0; i < points.length - 1; i++) {
    const [p0, p1, p2, p3] = [at(i - 1), at(i), at(i + 1), at(i + 2)];
    d += `C${f(p1[0] + (p2[0] - p0[0]) / 6)} ${f(p1[1] + (p2[1] - p0[1]) / 6)} ${f(p2[0] - (p3[0] - p1[0]) / 6)} ${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])} ${f(p2[1])}`;
  }
  return d;
}

/** A rounded box drawn in one go, the way a pen does it: nearly straight, closing a little past its start. */
function handBox(w: number, h: number, r: number, seed: number) {
  const random = mulberry(seed);
  const jit = (amount: number) => (random() * 2 - 1) * amount;
  const wobble = 1.5;
  const pts: Point[] = [];
  const side = (ax: number, ay: number, bx: number, by: number) => {
    const length = Math.hypot(bx - ax, by - ay);
    const n = Math.max(1, Math.round(length / 70));
    const bow = jit(wobble * 1.3);
    for (let i = 1; i < n; i++) {
      const t = i / n;
      const off = jit(wobble) + bow * Math.sin(Math.PI * t);
      pts.push([ax + (bx - ax) * t - ((by - ay) / length) * off, ay + (by - ay) * t + ((bx - ax) / length) * off]);
    }
  };
  const corner = (cx: number, cy: number, from: number) => {
    const a = ((from + 45) * Math.PI) / 180;
    pts.push([cx + Math.cos(a) * r + jit(0.8), cy + Math.sin(a) * r + jit(0.8)]);
  };
  const x = 1.5;
  const y = 1.5;
  const W = w - 3;
  const H = h - 3;
  pts.push([x + r + 14, y + jit(1)], [x + r + 40, y + jit(1)]);
  side(x + r + 40, y, x + W - r, y);
  pts.push([x + W - r, y + jit(1)]);
  corner(x + W - r, y + r, -90);
  pts.push([x + W + jit(1), y + r]);
  side(x + W, y + r, x + W, y + H - r);
  pts.push([x + W + jit(1), y + H - r]);
  corner(x + W - r, y + H - r, 0);
  pts.push([x + W - r, y + H + jit(1)]);
  side(x + W - r, y + H, x + r, y + H);
  pts.push([x + r, y + H + jit(1)]);
  corner(x + r, y + H - r, 90);
  pts.push([x + jit(1), y + H - r]);
  side(x, y + H - r, x, y + r);
  pts.push([x + jit(1), y + r]);
  corner(x + r, y + r, 180);
  pts.push([x + r, y + jit(0.5)], [x + r + 16, y - 0.2 + jit(0.5)], [x + r + 30, y - 1.2 + jit(0.4)]);
  return smooth(pts);
}

/**
 * The ink frame of a `.sketch` box. It measures the box it sits in and draws a frame of exactly
 * that size by hand, a little differently for every box, which then draws itself in. Until the
 * page is running, the box keeps a plain border so nothing jumps.
 */
export function Frame({ radius = 20 }: { radius?: number }) {
  const ref = useRef<SVGSVGElement>(null);
  const id = useId();
  const [size, setSize] = useState<{ w: number; h: number } | null>(null);

  useEffect(() => {
    const parent = ref.current?.parentElement;
    if (!parent) return;
    const measure = () => setSize({ w: parent.offsetWidth, h: parent.offsetHeight });
    const observer = new ResizeObserver(measure);
    observer.observe(parent);
    parent.dataset.framed = "";
    return () => observer.disconnect();
  }, []);

  const seed = [...id].reduce((sum, char, i) => sum + char.charCodeAt(0) * (i + 7), 11);
  return (
    <svg ref={ref} className="frame-ink" width={size?.w ?? 0} height={size?.h ?? 0} aria-hidden="true">
      {size && size.w > 60 && size.h > 40 && <path pathLength={1} d={handBox(size.w, size.h, Math.min(radius, size.h / 3), seed)} />}
    </svg>
  );
}
