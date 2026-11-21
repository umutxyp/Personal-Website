import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Frame, Heading, Mdx, Reveal } from "@/components";
import { fillStats, getLiveStats } from "@/lib/live-stats";
import { baseURL, person } from "@/resources";
import { formatDate } from "@/utils/formatDate";
import { getProjects } from "@/utils/utils";

export const revalidate = 86400;

export function generateStaticParams() {
  return getProjects().map((project) => ({ slug: project.slug }));
}

type Params = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { slug } = await params;
  const project = getProjects().find((item) => item.slug === slug);
  if (!project) return {};
  const description = fillStats(project.metadata.summary, await getLiveStats());
  const image = project.metadata.images[0] || `/api/og/generate?title=${encodeURIComponent(project.metadata.title)}`;
  return {
    title: project.metadata.title,
    description,
    alternates: { canonical: `/work/${slug}` },
    openGraph: { type: "article", title: project.metadata.title, description, url: `${baseURL}/work/${slug}`, images: [image] },
  };
}

export default async function Project({ params }: Params) {
  const { slug } = await params;
  const projects = getProjects();
  const project = projects.find((item) => item.slug === slug);
  if (!project) notFound();
  const stats = await getLiveStats();
  const { metadata } = project;
  const others = projects.filter((item) => item.slug !== slug).slice(0, 4);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    headline: metadata.title,
    description: fillStats(metadata.summary, stats),
    datePublished: metadata.publishedAt,
    url: `${baseURL}/work/${slug}`,
    author: { "@type": "Person", name: person.name, url: baseURL },
  };

  return (
    <article className="narrow">
      <header className="page-head">
        <h1 className="wavy">{metadata.title}</h1>
        <p>{fillStats(metadata.summary, stats)}</p>
        <div className="tags">
          <span className="tag small">since {formatDate(metadata.publishedAt)}</span>
          {metadata.link && (
            <a className="tag" href={metadata.link} rel="noopener">
              {metadata.link.replace(/^https?:\/\//, "")}
            </a>
          )}
        </div>
      </header>

      {metadata.images[0] && (
        <div className="cover sketch">
<Frame />
          <img src={metadata.images[0]} alt={`${metadata.title}, its site as it looks now`} />
        </div>
      )}

      <Mdx source={fillStats(project.content, stats)} />

      <Reveal as="section" className="section">
        <Heading line={2}>More work</Heading>
        <ul className="rows">
          {others.map((item) => (
            <li key={item.slug}>
              <div className="row-head">
                <Link href={`/work/${item.slug}`}>{item.metadata.title}</Link>
              </div>
              <p>{fillStats(item.metadata.summary, stats)}</p>
            </li>
          ))}
        </ul>
      </Reveal>
      {/* biome-ignore lint/security/noDangerouslySetInnerHtml: structured data */}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
    </article>
  );
}
