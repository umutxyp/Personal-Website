import { cache, createElement, Fragment, type ReactNode } from "react";

// Every product number on this site comes from codeshare.me, the studio's own
// site: the stat tiles on its home page and on each project page. They are
// fetched at build time and refreshed weekly (ISR), so the numbers here move
// when the products do, with nothing typed in by hand.
//
// Text anywhere on the site refers to a number as a token, `%project.key%`
// (e.g. `%beatra.servers%`), and fillStats() swaps in the current value.

const SOURCE = "https://codeshare.me";
const REVALIDATE_SECONDS = 604800; // 7 days

// Where each project's tiles live, and which tile label each key reads. Keyed by
// label rather than position, so a reordered tile still lands in the right place.
const SOURCES = {
  studio: {
    path: "/",
    labels: {
      products: "Products live",
      servers: "Discord servers",
      users: "Discord users reached",
      players: "Minecraft players",
    },
  },
  beatra: {
    path: "/projects/beatra",
    labels: { servers: "Discord servers", users: "Discord users", playing: "Playing right now" },
  },
  sylon: {
    path: "/projects/sylon",
    labels: { servers: "Discord servers", users: "Discord users", uptime: "Uptime" },
  },
  mcstat: {
    path: "/projects/mcstat",
    labels: {
      servers: "Servers tracked",
      players: "Player records",
      skins: "Skins archived",
      capes: "Capes archived",
    },
  },
  justdiscord: {
    path: "/projects/justdiscord",
    labels: {
      servers: "Server listings",
      bots: "Bot listings",
      emojis: "Emojis and stickers",
      visitors: "Unique visitors",
    },
  },
  justanime: {
    path: "/projects/justanime",
    labels: {
      titles: "Anime and manga titles",
      characters: "Character records",
      schedule: "Airing schedule entries",
    },
  },
} as const;

type Sources = typeof SOURCES;
export type LiveStats = { [P in keyof Sources]: Record<keyof Sources[P]["labels"], string> };

// Last values read from codeshare.me (1 Oct 2026). Used for any tile that cannot
// be read, so a failed fetch never leaves a hole in the page.
const FALLBACK: LiveStats = {
  studio: { products: "6", servers: "41.1K", users: "2.9M", players: "463K" },
  beatra: { servers: "40.6K", users: "2.7M", playing: "80" },
  sylon: { servers: "490", users: "257K", uptime: "99.9%" },
  mcstat: { servers: "6,752", players: "463K", skins: "428K", capes: "73.0K" },
  justdiscord: { servers: "2,835", bots: "8,198", emojis: "96.8K", visitors: "18.4K" },
  justanime: { titles: "123K", characters: "176K", schedule: "1,190" },
};

const ENTITIES: Record<string, string> = { amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'", nbsp: " " };
const decode = (text: string) =>
  text.replace(/&(amp|lt|gt|quot|#39|nbsp);/g, (_, entity: string) => ENTITIES[entity]).trim();

/** Reads a page's stat tiles (`<dd>value</dd><dt>label</dt>`) into { label: value }. */
async function readTiles(path: string): Promise<Record<string, string>> {
  try {
    const response = await fetch(`${SOURCE}${path}`, {
      headers: { "User-Agent": "umutbayraktar.vercel.app (live stats)" },
      next: { revalidate: REVALIDATE_SECONDS },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const html = await response.text();
    const tiles: Record<string, string> = {};
    for (const [, value, label] of html.matchAll(/<dd[^>]*>([^<]+)<\/dd>\s*<dt[^>]*>([^<]+)<\/dt>/g)) {
      tiles[decode(label)] = decode(value);
    }
    return tiles;
  } catch (error) {
    console.error(`live stats: ${SOURCE}${path} unreadable, using last known values: ${(error as Error).message}`);
    return {};
  }
}

export const getLiveStats = cache(async (): Promise<LiveStats> => {
  const projects = Object.keys(SOURCES) as (keyof Sources)[];
  const pages = await Promise.all(projects.map((project) => readTiles(SOURCES[project].path)));

  const stats = structuredClone(FALLBACK);
  projects.forEach((project, i) => {
    const labels: Record<string, string> = SOURCES[project].labels;
    const values: Record<string, string> = stats[project];
    for (const [key, label] of Object.entries(labels)) {
      if (pages[i][label]) values[key] = pages[i][label];
    }
  });
  return stats;
});

const TOKEN = /%([a-z]+)\.([a-z]+)%/g;

/** Replaces `%project.key%` tokens with current values. Unknown tokens are left as is. */
export function fillStats(text: string, stats: LiveStats): string {
  return text.replace(TOKEN, (token, project: string, key: string) => {
    const values = (stats as Record<string, Record<string, string>>)[project];
    return values?.[key] ?? token;
  });
}

/**
 * fillStats() for text that is rendered, with `**bold**` turned into <strong>.
 * Anything that is not a string is returned unchanged.
 */
export function renderStats(content: ReactNode, stats: LiveStats): ReactNode {
  if (typeof content !== "string") return content;
  const parts = fillStats(content, stats).split(/\*\*(.+?)\*\*/g);
  return createElement(
    Fragment,
    null,
    ...parts.map((part, i) => (i % 2 === 1 ? createElement("strong", { key: i }, part) : part)),
  );
}
