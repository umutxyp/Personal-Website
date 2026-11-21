import { person, siteData } from "@/resources";
import { Pic } from "./Pic";
import { ThemeRow } from "./ThemePicker";

export function Footer() {
  return (
    <footer className="footer">
      <Pic name="ground" width={2400} height={260} className="ground" />
      <div className="footer-body">
        <div className="wrap">
          <h4>pick a world</h4>
          <ThemeRow />
          <p className="small">
            © {new Date().getFullYear()} {person.name} · drawn by hand, in code ·{" "}
            <a href={`https://github.com/${siteData.github.username}/Personal-Website`}>
              the source is open
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
