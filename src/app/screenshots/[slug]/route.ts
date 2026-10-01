import fs from "node:fs/promises";
import path from "node:path";
import chromium from "@sparticuz/chromium";
import puppeteer from "puppeteer-core";
import { getScreenshotProjects } from "@/utils/utils";

// Each project's cover is a live screenshot of its own site. The route is
// generated at build time and regenerated in the background once a week, so the
// Work page, case studies and gallery never show a stale product. No external
// service and no CI: Chromium runs inside the Vercel function.
export const dynamic = "force-static";
export const revalidate = 604800; // 7 days
export const maxDuration = 60;

// 16:10 at 2000x1250, the size every cover is published at.
const VIEWPORT = { width: 1600, height: 1000, deviceScaleFactor: 1.25 };
const JPEG_QUALITY = 80;

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36";

// Anything matching these is a bot check or a consent wall, not the site.
const BLOCKED_PAGE =
  /just a moment|attention required|verify you are human|checking your browser|before you continue to youtube/i;

// Cookie and consent banners that would otherwise sit on top of the capture.
const HIDE_OVERLAYS = `
  [id*="cookie" i], [class*="cookie" i], [id*="consent" i], [class*="consent" i],
  [aria-label*="cookie" i], #onetrust-banner-sdk, .cc-window, .cky-consent-container {
    display: none !important;
  }
`;

export function generateStaticParams() {
  return getScreenshotProjects().map(({ slug }) => ({ slug }));
}

async function launchBrowser() {
  // The build captures every project in parallel workers, and each one unpacks
  // Chromium to the same /tmp path. A worker that spawns it while another is
  // still writing gets ETXTBSY; waiting for the write to finish is enough.
  for (let attempt = 1; ; attempt++) {
    try {
      return await puppeteer.launch({
        args: await puppeteer.defaultArgs({ args: chromium.args, headless: "shell" }),
        executablePath: process.env.CHROMIUM_PATH || (await chromium.executablePath()),
        headless: "shell",
        defaultViewport: VIEWPORT,
      });
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ETXTBSY" || attempt === 10) throw error;
      await new Promise((resolve) => setTimeout(resolve, 1_000));
    }
  }
}

async function capture(url: string): Promise<Buffer> {
  const browser = await launchBrowser();

  try {
    const page = await browser.newPage();
    await page.setUserAgent({ userAgent: USER_AGENT });
    await page.emulateMediaFeatures([
      { name: "prefers-color-scheme", value: "dark" },
      { name: "prefers-reduced-motion", value: "reduce" },
    ]);

    const response = await page.goto(url, { waitUntil: "load", timeout: 25_000 });
    if (!response || response.status() >= 400) {
      throw new Error(`HTTP ${response?.status() ?? "no response"}`);
    }

    // Live counters and charts keep some sites from ever going fully idle.
    await page.waitForNetworkIdle({ idleTime: 500, timeout: 8_000 }).catch(() => {});
    await page.addStyleTag({ content: HIDE_OVERLAYS });
    await page.evaluate(() => window.scrollTo(0, 0));
    await new Promise((resolve) => setTimeout(resolve, 2_500));

    const title = await page.title();
    const text = await page.evaluate(() => document.body?.innerText.slice(0, 2_000) ?? "");
    if (
      BLOCKED_PAGE.test(title) ||
      BLOCKED_PAGE.test(text) ||
      new URL(page.url()).host.startsWith("consent.")
    ) {
      throw new Error(`landed on a bot check or consent page ("${title}")`);
    }

    return Buffer.from(await page.screenshot({ type: "jpeg", quality: JPEG_QUALITY }));
  } finally {
    await browser.close();
  }
}

export async function GET(_request: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const project = getScreenshotProjects().find((p) => p.slug === slug);
  if (!project) {
    return new Response("Not found", { status: 404 });
  }

  let image: Buffer;
  try {
    image = await capture(project.url);
  } catch (error) {
    // During a weekly refresh, throwing keeps the last good screenshot cached and
    // retries on a later request. At build time (or in dev) there is nothing cached
    // yet, so fall back to the cover image committed for the project.
    const canFallBack =
      process.env.NEXT_PHASE === "phase-production-build" || process.env.NODE_ENV === "development";
    console.error(`screenshot ${slug} <- ${project.url} failed: ${(error as Error).message}`);
    if (!canFallBack) throw error;
    image = await fs.readFile(path.join(process.cwd(), "public", project.fallback));
  }

  return new Response(new Uint8Array(image), {
    headers: { "Content-Type": "image/jpeg" },
  });
}
