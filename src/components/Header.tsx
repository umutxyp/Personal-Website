import Link from "next/link";
import { person } from "@/resources";
import { Nav } from "./Nav";
import { ThemePicker } from "./ThemePicker";

export function Header() {
  return (
    <header className="header">
      <div className="wrap">
        <Link href="/" className="brand">
          {/* biome-ignore lint/a11y/useAltText: the name is right beside it */}
          <img src="/logo.svg" width={30} height={30} alt="" />
          {person.name}
        </Link>
        <Nav className="nav" />
        <ThemePicker />
      </div>
      <Nav className="mobile-nav" />
    </header>
  );
}
