import { getPosts } from "@/utils/utils";
import { baseURL, blog, person } from "@/resources";
import { NextResponse } from "next/server";

/** Escapes text for XML element content and attribute values. */
function escapeXml(value: unknown): string {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

export async function GET() {
  const posts = getPosts(["src", "app", "blog", "posts"]);

  // Sort posts by date (newest first)
  const sortedPosts = posts.sort((a, b) => {
    return new Date(b.metadata.publishedAt).getTime() - new Date(a.metadata.publishedAt).getTime();
  });

  const blogTitle = escapeXml(blog.title);
  const blogLink = escapeXml(`${baseURL}/blog`);
  const author = escapeXml(`${person.email || "noreply@example.com"} (${person.name})`);

  // Generate RSS XML; every value is escaped before it goes into the XML.
  const rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${blogTitle}</title>
    <link>${blogLink}</link>
    <description>${escapeXml(blog.description)}</description>
    <language>en</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <atom:link href="${escapeXml(`${baseURL}/api/rss`)}" rel="self" type="application/rss+xml" />
    <managingEditor>${author}</managingEditor>
    <webMaster>${author}</webMaster>
    <image>
      <url>${escapeXml(`${baseURL}${person.avatar || "/images/avatar.jpg"}`)}</url>
      <title>${blogTitle}</title>
      <link>${blogLink}</link>
    </image>
    ${sortedPosts
      .map((post) => {
        const link = escapeXml(`${baseURL}/blog/${post.slug}`);
        return `
    <item>
      <title>${escapeXml(post.metadata.title)}</title>
      <link>${link}</link>
      <guid>${link}</guid>
      <pubDate>${escapeXml(new Date(post.metadata.publishedAt).toUTCString())}</pubDate>
      <description>${escapeXml(post.metadata.summary)}</description>
      ${post.metadata.image ? `<enclosure url="${escapeXml(`${baseURL}${post.metadata.image}`)}" type="image/jpeg" />` : ""}
      ${post.metadata.tag ? `<category>${escapeXml(post.metadata.tag)}</category>` : ""}
      <author>${author}</author>
    </item>`;
      })
      .join("")}
  </channel>
</rss>`;

  // Return the RSS XML with the appropriate content type
  return new NextResponse(rssXml, {
    headers: {
      "Content-Type": "application/xml",
      "Cache-Control": "public, max-age=3600, s-maxage=3600, stale-while-revalidate=86400",
    },
  });
}
