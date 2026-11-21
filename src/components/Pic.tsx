"use client";

import { useTheme } from "./theme";

type Props = {
  /** The picture's name under public/scenes/<theme>/<mode>/, without ".svg". */
  name: string;
  width: number;
  height: number;
  className?: string;
  /** Load at once (the hero) instead of when it comes near the screen. */
  eager?: boolean;
};

/**
 * One of the theme's drawings. Its file depends on the theme and the mode, which only the
 * browser knows, so the space is kept and the picture arrives once the page is running.
 * Changing the theme swaps the file, and the new picture draws itself in again.
 */
export function Pic({ name, width, height, className = "", eager = false }: Props) {
  const theme = useTheme();
  return (
    <span className={`pic ${className}`} style={{ aspectRatio: `${width} / ${height}` }} aria-hidden="true">
      {theme && (
        // biome-ignore lint/a11y/noSvgWithoutTitle: decorative
        <img
          key={theme}
          src={`/scenes/${theme}/${name}.svg`}
          width={width}
          height={height}
          alt=""
          loading={eager ? "eager" : "lazy"}
          decoding="async"
        />
      )}
    </span>
  );
}
