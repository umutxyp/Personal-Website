import type { MetadataRoute } from "next";
import { baseURL, nav } from "@/resources";
import { getProjects } from "@/utils/utils";

export default function sitemap(): MetadataRoute.Sitemap {
  const today = new Date().toISOString().split("T")[0];
  const pages = nav.map(({ path }) => ({ url: `${baseURL}${path === "/" ? "" : path}`, lastModified: today }));
  const work = getProjects().map((project) => ({ url: `${baseURL}/work/${project.slug}`, lastModified: project.metadata.publishedAt }));
  return [...pages, ...work];
}
