"use client";

import { useSyncExternalStore } from "react";

// The theme lives on <html> as data-theme and data-mode (set before the first paint by the
// script in layout.tsx) and in localStorage. Components read it through useTheme().

const EVENT = "themechange";

function subscribe(callback: () => void) {
  window.addEventListener(EVENT, callback);
  return () => window.removeEventListener(EVENT, callback);
}

const read = () => `${document.documentElement.dataset.theme}/${document.documentElement.dataset.mode}`;

/** "fox/light", or null while the page is still being rendered on the server. */
export function useTheme(): string | null {
  return useSyncExternalStore(subscribe, read, () => null);
}

export function setTheme(next: { theme?: string; mode?: "light" | "dark" }) {
  const root = document.documentElement;
  if (next.theme) root.dataset.theme = next.theme;
  if (next.mode) root.dataset.mode = next.mode;
  try {
    if (next.theme) localStorage.setItem("theme", next.theme);
    if (next.mode) localStorage.setItem("mode", next.mode);
  } catch {
    // private windows may refuse storage; the choice then lasts for this page
  }
  window.dispatchEvent(new Event(EVENT));
}
