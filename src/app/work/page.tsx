import type { Metadata } from "next";
import Link from "next/link";
import { Frame, Fx, Pic, Reveal, Scene } from "@/components";
import { fillStats, getLiveStats } from "@/lib/live-stats";
import { person } from "@/resources";
import { sortedProjects } from "@/utils/utils";

export const revalidate = 86400;

export const metadata: Metadata = {
  title: "Work",
  description: `Products and case studies from Codeshare Technology by ${person.name}`,
  alternates: { canonical: "/work" },
};

export default async function Work() {
  const stats = await getLiveStats();
  return (
    <>
      <div className="wrap">
        <header className="page-head">
          <Fx steady>
            <h1 className="wavy">Work</h1>
          </Fx>
          <p>What I have built and run, each with the story behind it.</p>
        </header>
      </div>
      <Scene page="work" small />
      <div className="wrap">
        <div className="shots">
          {sortedProjects().map((project, n) => (
            <Reveal key={project.slug}>
              <Link href={`/work/${project.slug}`} className="shot sketch">
                <Frame />
                <Pic name={`grow-${n % 4}`} width={600} height={80} className="grown" />
                <img
                  className="frame"
                  src={project.metadata.images[0]}
                  alt={`${project.metadata.title}, its site as it looks now`}
                  loading="lazy"
                />
                <h3>{project.metadata.title}</h3>
                <p>{fillStats(project.metadata.summary, stats)}</p>
              </Link>
            </Reveal>
          ))}
        </div>
      </div>
    </>
  );
}
