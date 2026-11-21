import type { Metadata } from "next";
import Link from "next/link";
import { Frame, Fx, Scene } from "@/components";
import { person } from "@/resources";
import { getProjects, workPath } from "@/utils/utils";

export const metadata: Metadata = {
  title: "Gallery",
  description: `Every product by ${person.name} as its site looks now.`,
  alternates: { canonical: "/gallery" },
};

export default function Gallery() {
  const shots = getProjects().filter((project) => project.metadata.images[0]);
  return (
    <>
      <div className="wrap">
        <header className="page-head">
          <Fx steady>
            <h1 className="wavy">Gallery</h1>
          </Fx>
          <p>Each product as its own site looks now: the pictures are taken again every week.</p>
        </header>
      </div>
      <Scene page="gallery" small />
      <div className="wrap">
        <div className="gallery">
          {shots.map((project) => (
            <Link key={project.slug} href={workPath(project.slug)} className="shot sketch">
              <Frame />
              <img
                className="frame"
                src={project.metadata.images[0]}
                alt={project.metadata.title}
                loading="lazy"
              />
              <h3>{project.metadata.title}</h3>
            </Link>
          ))}
        </div>
      </div>
    </>
  );
}
