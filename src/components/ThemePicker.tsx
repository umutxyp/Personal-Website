"use client";

import { useEffect, useRef, useState } from "react";
import { themes } from "@/resources";
import { Frame } from "./Frame";
import { setTheme, useTheme } from "./theme";

const MODES = ["light", "dark"] as const;

/** The list of themes with their colours, and day or night. */
function Choices({ current, row = false }: { current: string | null; row?: boolean }) {
  const [theme, mode] = (current ?? "/").split("/");
  if (row) {
    return (
      <div className="theme-row">
        {themes.map((t) => (
          <button key={t.id} type="button" className="tag" aria-pressed={t.id === theme} onClick={() => setTheme({ theme: t.id })}>
            <i className="dot" style={{ background: t.swatch[0] }} />
            {t.name}
          </button>
        ))}
        {MODES.map((m) => (
          <button key={m} type="button" className="tag small" aria-pressed={m === mode} onClick={() => setTheme({ mode: m })}>
            {m === "light" ? "day" : "night"}
          </button>
        ))}
      </div>
    );
  }
  return (
    <>
      <h4>pick a world</h4>
      <ul className="theme-list">
        {themes.map((t) => (
          <li key={t.id}>
            <button type="button" className="theme-choice" aria-pressed={t.id === theme} onClick={() => setTheme({ theme: t.id })}>
              {t.name}
              <span className="swatches">
                {t.swatch.map((color) => (
                  <i key={color} style={{ background: color }} />
                ))}
              </span>
            </button>
          </li>
        ))}
      </ul>
      <div className="modes">
        {MODES.map((m) => (
          <button key={m} type="button" className="tag small" aria-pressed={m === mode} onClick={() => setTheme({ mode: m })}>
            {m === "light" ? "day" : "night"}
          </button>
        ))}
      </div>
    </>
  );
}

/** The button in the header that opens the list. */
export function ThemePicker() {
  const current = useTheme();
  const [open, setOpen] = useState(false);
  const box = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const close = (event: Event) => {
      if (event instanceof KeyboardEvent ? event.key === "Escape" : !box.current?.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener("pointerdown", close);
    document.addEventListener("keydown", close);
    return () => {
      document.removeEventListener("pointerdown", close);
      document.removeEventListener("keydown", close);
    };
  }, [open]);

  return (
    <div className="picker" ref={box}>
      <button type="button" className="tag picker-button" aria-expanded={open} aria-haspopup="dialog" onClick={() => setOpen(!open)}>
        <i className="dot" />
        theme
      </button>
      {open && (
        <div className="picker-panel sketch" role="dialog" aria-label="Theme">
          <Frame />
          <Choices current={current} />
        </div>
      )}
    </div>
  );
}

/** The same choice laid out as a row of labels, for the footer. */
export function ThemeRow() {
  return <Choices current={useTheme()} row />;
}
