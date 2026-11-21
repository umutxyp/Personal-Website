import { cache, createElement, Fragment, type ReactNode } from "react";
import siteData from "@/resources/site-data";

// Every product number on this site comes from codeshare.me, the studio's own
// site: the figures on its home page and on each project page. They are fetched
// at build time and refreshed daily (ISR), so the numbers here move when the
// products do, with nothing typed in by hand. GitHub stars come from GitHub.
//
// Text anywhere on the site refers to a number as a token, `%project.key%`
// (e.g. `%beatra.servers%`), and fillStats() swaps in the current value.

const SOURCE = "https://codeshare.me";
const REVALIDATE_SECONDS = 86400; // a day

// Where each project's figures live, and which label each key reads. Keyed by
// label rather than position, so a reordered figure still lands in the right place.
const SOURCES = {
  studio: {
    path: "/about",
    labels: { products: "Products live", users: "Discord users reached" },
  },
  home: {
    path: "/",
    labels: { servers: "Discord servers", players: "Minecraft players" },
  },
  beatra: {
    path: "/projects/beatra",
    labels: { servers: "Discord servers", users: "Discord users" },
  },
  shroudly: {
    path: "/projects/shroudly",
    labels: { downloads: "Downloads", stars: "GitHub stars" },
  },
  vanigo: {
    path: "/projects/vanigo",
    labels: { places: "Places on the map", languages: "Languages" },
  },
  sylon: {
    path: "/projects/sylon",
    labels: { servers: "Discord servers", users: "Discord users", uptime: "Uptime" },
  },
  mcstat: {
    path: "/projects/mcstat",
    labels: { servers: "Servers tracked", players: "Player records", skins: "Skins archived", capes: "Capes archived" },
  },
  justdiscord: {
    path: "/projects/justdiscord",
    labels: { servers: "Server listings", bots: "Bot listings", emojis: "Emojis and stickers", visitors: "Unique visitors" },
  },
  justanime: {
    path: "/projects/justanime",
    labels: { titles: "Anime and manga titles", characters: "Character records", schedule: "Airing schedule entries" },
  },
} as const;

type Sources = typeof SOURCES;
type Scraped = { [P in keyof Sources]: Record<keyof Sources[P]["labels"], string> };
export type LiveStats = Record<string, Record<string, string>>;

// Last values read (21 Nov 2026). Used for any figure that cannot be read, so a
// failed fetch never leaves a hole in the page.
const FALLBACK: Scraped = {
  studio: { products: "8", users: "3.7M" },
  home: { servers: "45.2K", players: "43.9K" },
  beatra: { servers: "49.7K", users: "3.2M" },
  shroudly: { downloads: "145,929", stars: "585" },
  vanigo: { places: "66M", languages: "30" },
  sylon: { servers: "919", users: "504K", uptime: "99.9%" },
  mcstat: { servers: "6,781", players: "44.3K", skins: "124K", capes: "8.4K" },
  justdiscord: { servers: "1,495", bots: "8,110", emojis: "96.8K", visitors: "17.6K" },
  justanime: { titles: "164K", characters: "182K", schedule: "2,135" },
};
const GITHUB_FALLBACK = "3.3K";

const ENTITIES: Record<string, string> = { amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'", "#x27": "'", nbsp: " " };
const decode = (text: string) => text.replace(/&(amp|lt|gt|quot|#39|#x27|nbsp);/g, (_, entity: string) => ENTITIES[entity]);
// A figure: "6", "2.9M", "6,752", "99.9%", but not step numbers ("01").
const VALUE = /^(?!0\d)\d[\d.,]{0,8}[KMB]?\+?%?$/;

/**
 * Reads a page's figures into { label: value }. Every figure on codeshare.me is a
 * value followed by its label, so the page is read as lines of text and each value
 * is paired with the line after it.
 */
async function readFigures(path: string): Promise<Record<string, string>> {
  try {
    const response = await fetch(`${SOURCE}${path}`, {
      headers: { "User-Agent": "umutbayraktar.vercel.app (live stats)" },
      next: { revalidate: REVALIDATE_SECONDS },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const html = (await response.text()).replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, "");
    const lines = decode(html.replace(/<[^>]+>/g, "\n"))
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
    const figures: Record<string, string> = {};
    lines.forEach((line, i) => {
      const label = lines[i + 1];
      if (VALUE.test(line) && label && /^[A-Za-z][A-Za-z &]{2,40}$/.test(label) && !(label in figures)) {
        figures[label] = line;
      }
    });
    return figures;
  } catch (error) {
    console.error(`live stats: ${SOURCE}${path} unreadable, using last known values: ${(error as Error).message}`);
    return {};
  }
}

/** 2840 → "2.8K", 3200000 → "3.2M", the way codeshare.me writes numbers. */
export function compact(n: number): string {
  for (const [size, unit] of [[1_000_000, "M"], [1_000, "K"]] as const) {
    if (n >= size) return `${(n / size).toFixed(1).replace(/\.0$/, "")}${unit}`;
  }
  return String(n);
}

export type Repo = {
  id: number;
  name: string;
  html_url: string;
  description: string | null;
  stargazers_count: number;
  forks_count: number;
  language: string | null;
  updated_at: string;
  fork: boolean;
};

/** The owner's public repositories, from the GitHub API. */
export const getRepos = cache(async (): Promise<Repo[]> => {
  try {
    const response = await fetch(`https://api.github.com/users/${siteData.github.username}/repos?per_page=100&type=owner&sort=updated`, {
      headers: { Accept: "application/vnd.github+json", "User-Agent": "portfolio-app" },
      next: { revalidate: 3600 },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return ((await response.json()) as Repo[]).filter((repo) => !repo.fork);
  } catch (error) {
    console.error(`live stats: GitHub repositories unreadable: ${(error as Error).message}`);
    return [];
  }
});

export const getLiveStats = cache(async (): Promise<LiveStats> => {
  const projects = Object.keys(SOURCES) as (keyof Sources)[];
  const [repos, ...pages] = await Promise.all([getRepos(), ...projects.map((project) => readFigures(SOURCES[project].path))]);

  const stats: LiveStats = structuredClone(FALLBACK);
  projects.forEach((project, i) => {
    for (const [key, label] of Object.entries(SOURCES[project].labels as Record<string, string>)) {
      if (pages[i][label]) stats[project][key] = pages[i][label];
    }
  });
  // the studio's own numbers are spread over two pages of codeshare.me
  stats.studio = { ...stats.studio, ...stats.home };
  const stars = repos.reduce((sum, repo) => sum + repo.stargazers_count, 0);
  stats.github = { stars: stars ? compact(stars) : GITHUB_FALLBACK };
  return stats;
});

const TOKEN = /%([a-z]+)\.([a-z]+)%/g;

/** Replaces `%project.key%` tokens with current values. Unknown tokens are left as is. */
export function fillStats(text: string, stats: LiveStats): string {
  return text.replace(TOKEN, (token, project: string, key: string) => stats[project]?.[key] ?? token);
}

/**
 * fillStats() for text that is rendered: `**words**` get a marker swipe behind them.
 */
export function renderStats(content: string, stats: LiveStats): ReactNode {
  const parts = fillStats(content, stats).split(/\*\*(.+?)\*\*/g);
  return createElement(
    Fragment,
    null,
    ...parts.map((part, i) => (i % 2 === 1 ? createElement("mark", { key: i }, part) : part)),
  );
}
