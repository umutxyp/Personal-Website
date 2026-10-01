// Captures a fresh screenshot of every project's live site and writes it over the
// project's cover image, so the Work page, case studies and gallery always show
// what each product looks like today.
//
// Runs weekly from .github/workflows/project-screenshots.yml. Locally:
//   npm i --no-save playwright && npx playwright install chromium
//   node scripts/capture-screenshots.mjs [slug ...]
//
// Which page is captured comes from each project's MDX frontmatter:
//   link            the page that is captured
//   screenshotUrl   optional, captures this page instead of `link`
//   screenshot      set to false to keep a hand-made cover
//   images[0]       where the capture is written (must be a .jpg)
//
// A capture that fails, or that lands on a bot challenge instead of the site,
// leaves the existing image in place.

import fs from "node:fs/promises";
import path from "node:path";
import matter from "gray-matter";
import { chromium } from "playwright";

const PROJECTS_DIR = path.join("src", "app", "work", "projects");
const PUBLIC_DIR = "public";

// 16:10 at 2000x1250, the size every cover image is published at.
const VIEWPORT = { width: 1600, height: 1000 };
const DEVICE_SCALE_FACTOR = 1.25;
const JPEG_QUALITY = 80;

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36";

// Anything matching these is a bot check or a consent wall, not the site.
const BLOCKED_PAGE = /just a moment|attention required|verify you are human|checking your browser|before you continue to youtube/i;

// Cookie and consent banners that would otherwise sit on top of the capture.
const HIDE_OVERLAYS = `
  [id*="cookie" i], [class*="cookie" i], [id*="consent" i], [class*="consent" i],
  [aria-label*="cookie" i], #onetrust-banner-sdk, .cc-window, .cky-consent-container {
    display: none !important;
  }
`;

async function loadProjects(onlySlugs) {
  const files = (await fs.readdir(PROJECTS_DIR)).filter((file) => file.endsWith(".mdx"));
  const projects = [];

  for (const file of files) {
    const slug = path.basename(file, ".mdx");
    if (onlySlugs.length > 0 && !onlySlugs.includes(slug)) continue;

    const { data } = matter(await fs.readFile(path.join(PROJECTS_DIR, file), "utf-8"));
    const url = data.screenshotUrl || data.link;
    const image = data.images?.[0];

    if (data.screenshot === false || !url || !image) continue;
    if (!image.endsWith(".jpg")) {
      console.warn(`skip ${slug}: cover ${image} is not a .jpg`);
      continue;
    }

    projects.push({ slug, url, output: path.join(PUBLIC_DIR, image) });
  }

  return projects;
}

async function capture(browser, { url, output }) {
  const context = await browser.newContext({
    viewport: VIEWPORT,
    deviceScaleFactor: DEVICE_SCALE_FACTOR,
    colorScheme: "dark",
    locale: "en-US",
    userAgent: USER_AGENT,
    reducedMotion: "reduce",
  });

  try {
    const page = await context.newPage();
    const response = await page.goto(url, { waitUntil: "load", timeout: 60_000 });

    if (!response || response.status() >= 400) {
      throw new Error(`HTTP ${response?.status() ?? "no response"}`);
    }

    // Live counters and charts keep some sites from ever going fully idle.
    await page.waitForLoadState("networkidle", { timeout: 15_000 }).catch(() => {});
    await page.addStyleTag({ content: HIDE_OVERLAYS });
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(3_000);

    const title = await page.title();
    const text = await page.evaluate(() => document.body?.innerText.slice(0, 2_000) ?? "");
    if (BLOCKED_PAGE.test(title) || BLOCKED_PAGE.test(text) || /^consent\./.test(new URL(page.url()).host)) {
      throw new Error(`landed on a bot check or consent page ("${title}")`);
    }

    const buffer = await page.screenshot({ type: "jpeg", quality: JPEG_QUALITY });
    await fs.mkdir(path.dirname(output), { recursive: true });
    await fs.writeFile(`${output}.tmp`, buffer);
    await fs.rename(`${output}.tmp`, output);

    return `${Math.round(buffer.length / 1024)} KB`;
  } finally {
    await context.close();
  }
}

const projects = await loadProjects(process.argv.slice(2));
const browser = await chromium.launch(
  process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {},
);
const results = [];

for (const project of projects) {
  try {
    const detail = await capture(browser, project);
    results.push({ ...project, ok: true, detail });
    console.log(`ok   ${project.slug} <- ${project.url} (${detail})`);
  } catch (error) {
    results.push({ ...project, ok: false, detail: error.message });
    console.error(`FAIL ${project.slug} <- ${project.url}: ${error.message}`);
  }
}

await browser.close();

if (process.env.GITHUB_STEP_SUMMARY) {
  const rows = results.map(
    (r) => `| ${r.ok ? "✅" : "❌"} | ${r.slug} | ${r.url} | ${r.detail.replace(/\|/g, "\\|")} |`,
  );
  await fs.appendFile(
    process.env.GITHUB_STEP_SUMMARY,
    ["### Project screenshots", "", "| | Project | Page | Result |", "|:-:|:--|:--|:--|", ...rows, ""].join("\n"),
  );
}

// One unreachable site keeps its old image; only fail when nothing could be captured.
if (results.length > 0 && results.every((r) => !r.ok)) {
  process.exit(1);
}
