import siteData from "@/resources/site-data";

/**
 * The pinned repositories are whatever is pinned on the GitHub profile itself.
 * The REST API does not expose pins and the GraphQL API needs a token, so the
 * public profile page is the source of truth: repin on GitHub and this follows.
 * Falls back to the list in site-data if the page cannot be read.
 */
export async function getPinnedNames(): Promise<string[]> {
  try {
    const response = await fetch(`https://github.com/${siteData.github.username}`, {
      headers: { Accept: "text/html", "User-Agent": "portfolio-app" },
      next: { revalidate: 3600 },
    });
    if (!response.ok) return siteData.github.highlight;
    const html = await response.text();
    const names = [...html.matchAll(/class="repo"[^>]*>([^<]+)</g)].map((match) => match[1].trim());
    const unique = [...new Set(names)];
    return unique.length > 0 ? unique : siteData.github.highlight;
  } catch (error) {
    console.error("Error fetching pinned repositories", error);
    return siteData.github.highlight;
  }
}
