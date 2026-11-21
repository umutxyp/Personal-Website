import Link from "next/link";
import type { ReactNode } from "react";
import { Frame } from "./Frame";
import { Pic } from "./Pic";

type Props = {
  name: string;
  url: string;
  logo: string;
  logoTile?: string;
  href: string;
  description: ReactNode;
  stats: { value: string; label: string }[];
  /** Which of the four drawings grows on its top edge. */
  plants: number;
};

/** A product in a hand-drawn frame, the theme's plants growing along its top. */
export function ProjectCard({
  name,
  url,
  logo,
  logoTile,
  href,
  description,
  stats,
  plants,
}: Props) {
  return (
    <Link href={href} className="card sketch">
      <Frame />
      <Pic name={`grow-${plants % 4}`} width={600} height={80} className="grown" />
      <div className="card-head">
        <span className="logo" style={logoTile ? { background: logoTile } : undefined}>
          <img src={logo} width={54} height={54} alt="" loading="lazy" />
        </span>
        <div>
          <h3>{name}</h3>
          <span>{url.replace(/^https?:\/\//, "")}</span>
        </div>
      </div>
      <p>{description}</p>
      {stats.length > 0 && (
        <div className="figures">
          {stats.map((stat) => (
            <span key={stat.label}>
              <mark>{stat.value}</mark> {stat.label}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
