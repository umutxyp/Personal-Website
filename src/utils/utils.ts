import fs from "fs";
import path from "path";
import matter from "gray-matter";

type Team = {
  name: string;
  role: string;
  avatar: string;
  linkedIn: string;
};

type Metadata = {
  title: string;
  publishedAt: string;
  summary: string;
  image?: string;
  images: string[];
  tag?: string;
  team: Team[];
  link?: string;
  /**
   * Manual position in the project list, lowest first. Projects are ordered by
   * how much traffic they actually carry, which the publish date does not track.
   * Anything without an order falls to the end and sorts by date.
   */
  order?: number;
  /** Set to false to keep a hand-made cover instead of a live screenshot. */
  screenshot?: boolean;
  /** Page to screenshot when it should differ from `link`. */
  screenshotUrl?: string;
};

import { notFound } from "next/navigation";

function getMDXFiles(dir: string) {
  if (!fs.existsSync(dir)) {
    return [];
  }

  return fs.readdirSync(dir).filter((file) => path.extname(file) === ".mdx");
}

function readMDXFile(filePath: string) {
  if (!fs.existsSync(filePath)) {
    notFound();
  }

  const rawContent = fs.readFileSync(filePath, "utf-8");
  const { data, content } = matter(rawContent);

  const metadata: Metadata = {
    title: data.title || "",
    publishedAt: data.publishedAt,
    summary: data.summary || "",
    image: data.image || "",
    images: data.images || [],
    tag: data.tag || [],
    team: data.team || [],
    link: data.link || "",
    order: typeof data.order === "number" ? data.order : undefined,
    screenshot: data.screenshot !== false,
    screenshotUrl: data.screenshotUrl || "",
  };

  return { metadata, content };
}

function getMDXData(dir: string) {
  const mdxFiles = getMDXFiles(dir);
  return mdxFiles.map((file) => {
    const { metadata, content } = readMDXFile(path.join(dir, file));
    const slug = path.basename(file, path.extname(file));

    return {
      metadata,
      slug,
      content,
    };
  });
}

export function getPosts(customPath = ["", "", "", ""]) {
  const postsDir = path.join(process.cwd(), ...customPath);
  return getMDXData(postsDir);
}

const PROJECTS_PATH = ["src", "app", "work", "projects"];

function hasLiveScreenshot(metadata: Metadata) {
  return metadata.screenshot !== false && Boolean(metadata.screenshotUrl || metadata.link) && Boolean(metadata.images[0]);
}

/**
 * Projects whose cover is a live screenshot of their site, served from
 * /screenshots/<slug> and refreshed weekly. `fallback` is the committed cover,
 * used at build time if the site cannot be captured.
 */
export function getScreenshotProjects() {
  return getMDXData(path.join(process.cwd(), ...PROJECTS_PATH))
    .filter(({ metadata }) => hasLiveScreenshot(metadata))
    .map(({ slug, metadata }) => ({
      slug,
      url: metadata.screenshotUrl || metadata.link || "",
      fallback: metadata.images[0],
    }));
}

/** Projects with their cover pointed at the live screenshot where there is one. */
export function getProjects() {
  return getMDXData(path.join(process.cwd(), ...PROJECTS_PATH)).map((project) => {
    if (!hasLiveScreenshot(project.metadata)) return project;
    const images = [`/screenshots/${project.slug}`, ...project.metadata.images.slice(1)];
    return { ...project, metadata: { ...project.metadata, images } };
  });
}
