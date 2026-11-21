import type { Metadata } from "next";
import { Frame, Fx, Heading, Reveal, Scene } from "@/components";
import { getLiveStats, renderStats } from "@/lib/live-stats";
import { person, siteData } from "@/resources";

export const revalidate = 86400;

export const metadata: Metadata = {
  title: "About",
  description: person.biography,
  alternates: { canonical: "/about" },
};

export default async function About() {
  const stats = await getLiveStats();
  const { about } = siteData;
  return (
    <>
      <div className="wrap">
        <header className="page-head">
          <Fx steady>
            <h1 className="wavy">About</h1>
          </Fx>
          <p>{renderStats(about.intro, stats)}</p>
          <div className="tags">
            {person.languages.map((language) => (
              <span key={language} className="tag small">
                {language}
              </span>
            ))}
            <a className="tag" href={`mailto:${person.email}`}>
              write to me
            </a>
          </div>
        </header>
      </div>
      <Scene page="about" small />
      <div className="wrap">
        <section className="section">
          <Heading line={1}>Work</Heading>
          {about.experiences.map((job) => (
            <Reveal key={job.company} className="job sketch">
              <Frame />
              <div className="job-head">
                <h3>
                  <a href={job.link}>{job.company}</a>
                </h3>
                <span className="role">{job.role}</span>
                <span className="when">{job.timeframe}</span>
              </div>
              <ul>
                {job.achievements.map((line) => (
                  <li key={line}>{renderStats(line, stats)}</li>
                ))}
              </ul>
            </Reveal>
          ))}
        </section>

        <Reveal as="section" className="section">
          <Heading line={2}>What I work with</Heading>
          <div className="skills">
            {about.technical.map((skill) => (
              <div key={skill.title} className="skill sketch">
                <Frame />
                <h3>{skill.title}</h3>
                <p>{skill.description}</p>
                <div className="tags">
                  {skill.tags.map((tag) => (
                    <span key={tag} className="tag small">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Reveal>

        <Reveal as="section" className="section">
          <Heading line={0}>Studies</Heading>
          <ul className="rows">
            {about.studies.map((study) => (
              <li key={study.name}>
                <div className="row-head">
                  <b style={{ fontSize: 22 }}>{study.name}</b>
                </div>
                <p>{study.description}</p>
              </li>
            ))}
          </ul>
        </Reveal>
      </div>
    </>
  );
}
