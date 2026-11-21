"use client";

import type { CSSProperties } from "react";
import { scenes } from "@/resources";
import { useTheme } from "./theme";

type Page = keyof typeof scenes.pages;
type Project = keyof typeof scenes.projects;

/**
 * The theme's world, from the spot that belongs to this page: the whole width of the screen,
 * cropped to it from the bottom, and kept by the part that matters (the animal, or on a
 * project's page the animal and the project's own thing). The page's background is the top of
 * the sky, so the picture fades into the page with no edge.
 */
export function Scene({
  page,
  project,
  small = false,
}: { page?: Page; project?: string; small?: boolean }) {
  const theme = useTheme();
  const known =
    project && project in scenes.projects ? scenes.projects[project as Project] : undefined;
  const spot = known ?? scenes.pages[page ?? "code"];
  const file = known ? `project-${project}` : `world-${spot.v}`;
  return (
    <div
      className={`scene${small ? " small" : ""}`}
      style={{ "--focus": `${spot.focus * 100}%` } as CSSProperties}
      aria-hidden="true"
    >
      {theme && (
        <img
          key={theme}
          src={`/scenes/${theme}/${file}.svg`}
          alt=""
          decoding="async"
          fetchPriority={page === "home" ? "high" : "auto"}
        />
      )}
    </div>
  );
}
