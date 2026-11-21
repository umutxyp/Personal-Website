"use client";

import { type ReactNode, useEffect, useRef } from "react";

// What comes off the writing in each world: bubbles by the sea, petals in the garden, dust on
// the savanna, fireflies at night, leaves in the forest, snow on the ice, sand in the desert.
// `up` rises from the letters, `down` falls past them, `wind` is carried off to the side.
const WORLDS: Record<
  string,
  { kind: string; way: "up" | "down" | "wind"; size: [number, number] }
> = {
  fox: { kind: "bubble", way: "up", size: [6, 15] },
  cat: { kind: "petal", way: "up", size: [6, 10] },
  lion: { kind: "dust", way: "wind", size: [3, 6] },
  owl: { kind: "firefly", way: "up", size: [3, 5] },
  bear: { kind: "leaf", way: "down", size: [7, 12] },
  penguin: { kind: "snow", way: "down", size: [3, 7] },
  tortoise: { kind: "sand", way: "wind", size: [2, 4] },
};

const rand = (a: number, b: number) => a + Math.random() * (b - a);

function spawn(host: HTMLElement) {
  if (host.childElementCount > 40) return;
  const world = WORLDS[document.documentElement.dataset.theme ?? "fox"] ?? WORLDS.fox;
  const p = document.createElement("i");
  p.className = `fx-p fx-${world.kind}`;
  p.setAttribute("aria-hidden", "true");
  const [x, y, dx, dy] =
    world.way === "up"
      ? [rand(2, 98), rand(45, 95), rand(-24, 24), -rand(50, 130)]
      : world.way === "down"
        ? [rand(2, 98), rand(-10, 30), rand(-30, 30), rand(50, 110)]
        : [rand(-2, 80), rand(25, 90), rand(80, 190), -rand(5, 45)];
  const size = rand(...world.size);
  p.style.cssText = `--x:${x}%;--y:${y}%;--dx:${dx}px;--dy:${dy}px;--s:${size.toFixed(1)}px;--r:${rand(-320, 320).toFixed(0)}deg;--t:${rand(2.4, 4.8).toFixed(2)}s`;
  p.addEventListener("animationend", () => p.remove());
  host.appendChild(p);
}

/**
 * Writing the world comes off of. `steady` keeps it coming while the writing is on screen (the
 * big titles); otherwise there is a little when it first comes into view and when it is pointed at.
 */
export function Fx({
  children,
  steady = false,
  className = "",
}: { children: ReactNode; steady?: boolean; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const layer = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const host = layer.current;
    const box = ref.current;
    if (!host || !box || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    let timer: number | undefined;
    const burst = (n: number) => {
      for (let i = 0; i < n; i++) window.setTimeout(() => spawn(host), i * 70);
    };
    const observer = new IntersectionObserver(([entry]) => {
      window.clearInterval(timer);
      timer = undefined;
      if (!entry.isIntersecting) return;
      if (steady) timer = window.setInterval(() => !document.hidden && spawn(host), 380);
      else burst(6);
    });
    observer.observe(box);
    const point = () => burst(10);
    box.addEventListener("pointerenter", point);
    return () => {
      observer.disconnect();
      window.clearInterval(timer);
      box.removeEventListener("pointerenter", point);
    };
  }, [steady]);
  return (
    <div ref={ref} className={`fx ${className}`}>
      <span ref={layer} className="fx-layer" aria-hidden="true" />
      {children}
    </div>
  );
}
