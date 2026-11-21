import Link from "next/link";
import { Frame, Fx, Heading, Pic, ProjectCard, Reveal, Scene } from "@/components";
import { getPinnedNames } from "@/lib/github";
import { compact, fillStats, getLiveStats, getRepos, renderStats } from "@/lib/live-stats";
import { person, siteData } from "@/resources";
import { getProjects } from "@/utils/utils";

// The numbers on this page are read from codeshare.me and GitHub; once a day is plenty.
export const revalidate = 86400;

export default async function Home() {
  const [stats, repos, pinned] = await Promise.all([getLiveStats(), getRepos(), getPinnedNames()]);
  const written = new Set(getProjects().map((project) => project.slug));
  const { home, studio, products } = siteData;
  const openSource = pinned
    .map((name) => repos.find((repo) => repo.name === name))
    .filter((repo) => repo !== undefined)
    .slice(0, 6);

  return (
    <>
      <section className="hero">
        <div className="hero-text">
          <Fx steady>
            <h1>{person.name}</h1>
          </Fx>
          <span className="underline" aria-hidden="true">
            <i />
            <i />
          </span>
          <ul className="roles">
            {person.roles.map((role) => (
              <li key={role}>{role}</li>
            ))}
          </ul>
        </div>
        <Scene page="home" />
      </section>

      <div className="wrap">
        <nav className="links" aria-label="Elsewhere">
          {siteData.social.map((item) => (
            <a key={item.name} className="tag" href={item.link} rel="me noopener">
              {item.name}
            </a>
          ))}
        </nav>

        <Reveal as="section" className="section">
          <Heading line={0}>About</Heading>
          <p className="note">{renderStats(home.about, stats)}</p>
          <p className="more">
            <Link className="link" href="/about">
              the longer story
            </Link>
          </p>
          <div className="stats">
            {home.stats.map((stat) => (
              <div className="stat" key={stat.label}>
                <b>
                  <mark>{fillStats(stat.value, stats)}</mark>
                </b>
                <span>{stat.label}</span>
              </div>
            ))}
          </div>
        </Reveal>

        <Reveal as="section" className="section">
          <Heading line={1}>Projects</Heading>
          <div className="studio sketch">
            <Frame />
            <Pic name="grow-3" width={600} height={80} className="grown" />
            <Pic name="perch" width={260} height={170} className="perch" />
            <div className="studio-head">
              <img src={studio.logo} width={120} height={128} alt="" />
              <div>
                <h3>{studio.name}</h3>
                <p>
                  <a href={studio.url}>{studio.url.replace("https://", "")}</a> · {studio.tag}
                </p>
              </div>
            </div>
            <p>{studio.description}</p>
            <ul className="products">
              {products.map((product) => (
                <li key={product.name}>
                  <a className="tag small" href={product.url}>
                    {product.name}
                  </a>
                </li>
              ))}
            </ul>
            <div className="figures">
              {studio.stats.map((stat) => (
                <span key={stat.label}>
                  <b>
                    <mark>{fillStats(stat.value, stats)}</mark>
                  </b>{" "}
                  {stat.label}
                </span>
              ))}
            </div>
          </div>

          <div className="cards">
            {products.map((product, n) => (
              <ProjectCard
                key={product.name}
                name={product.name}
                url={product.url}
                logo={product.logo}
                logoTile={"logoTile" in product ? product.logoTile : undefined}
                href={written.has(product.slug) ? `/work/${product.slug}` : product.url}
                description={product.description}
                stats={product.stats.map((stat) => ({
                  value: fillStats(stat.value, stats),
                  label: stat.label,
                }))}
                plants={n}
              />
            ))}
          </div>
        </Reveal>

        <Reveal as="section" className="section">
          <Heading line={2}>Tech stack</Heading>
          <ul className="stack">
            {home.stack.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </Reveal>

        <Reveal as="section" className="section">
          <Heading line={0} id="open-source">
            Open source
          </Heading>
          <ul className="rows">
            {openSource.map((repo) => (
              <li key={repo.id}>
                <div className="row-head">
                  <a href={repo.html_url}>{repo.name}</a>
                  <span className="stars">
                    <i className="star" />
                    {compact(repo.stargazers_count)}
                  </span>
                </div>
                {repo.description && <p>{repo.description}</p>}
              </li>
            ))}
          </ul>
          <p className="more" style={{ marginTop: 18 }}>
            <Link className="link" href="/github">
              all of it
            </Link>
          </p>
        </Reveal>
      </div>
    </>
  );
}
