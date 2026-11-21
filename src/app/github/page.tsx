import type { Metadata } from "next";
import { Fx, Heading, Reveal, Scene } from "@/components";
import { getPinnedNames } from "@/lib/github";
import { compact, getRepos, type Repo } from "@/lib/live-stats";
import { siteData } from "@/resources";

export const revalidate = 3600;

export const metadata: Metadata = {
  title: "Open source",
  description: siteData.github.description,
  alternates: { canonical: "/github" },
};

const date = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", year: "numeric" });

function Rows({ repos }: { repos: Repo[] }) {
  return (
    <ul className="rows">
      {repos.map((repo) => (
        <li key={repo.id}>
          <div className="row-head">
            <a href={repo.html_url}>{repo.name}</a>
            <span className="stars">
              <i className="star" />
              {compact(repo.stargazers_count)}
            </span>
          </div>
          {repo.description && <p>{repo.description}</p>}
          <p className="meta">
            {[
              repo.language,
              `${compact(repo.forks_count)} forks`,
              `updated ${date.format(new Date(repo.updated_at))}`,
            ]
              .filter(Boolean)
              .join("  ·  ")}
          </p>
        </li>
      ))}
    </ul>
  );
}

export default async function GitHub() {
  const [repos, pinned] = await Promise.all([getRepos(), getPinnedNames()]);
  const first = pinned
    .map((name) => repos.find((repo) => repo.name === name))
    .filter((repo) => repo !== undefined);
  const rest = repos
    .filter((repo) => !first.includes(repo))
    .sort((a, b) => b.stargazers_count - a.stargazers_count);
  const stars = repos.reduce((sum, repo) => sum + repo.stargazers_count, 0);
  return (
    <>
      <div className="wrap">
        <header className="page-head">
          <Fx steady>
            <h1 className="wavy">Open source</h1>
          </Fx>
          <p>{siteData.github.description}</p>
          <div className="tags">
            <span className="tag small">{repos.length} repositories</span>
            <span className="tag small">
              <i className="star" />
              {compact(stars)} stars
            </span>
            <a className="tag" href={`https://github.com/${siteData.github.username}`}>
              github.com/{siteData.github.username}
            </a>
          </div>
        </header>
      </div>
      <Scene page="code" small />
      <div className="wrap">
        <section className="section">
          <Heading line={1}>Pinned</Heading>
          <Rows repos={first} />
        </section>
        {rest.length > 0 && (
          <Reveal as="section" className="section">
            <Heading line={2}>Everything else</Heading>
            <Rows repos={rest} />
          </Reveal>
        )}
      </div>
    </>
  );
}
