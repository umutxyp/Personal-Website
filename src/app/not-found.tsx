import Link from "next/link";
import { Pic } from "@/components";

export default function NotFound() {
  return (
    <div className="wrap">
      <header className="page-head">
        <h1 className="wavy">Nothing here</h1>
        <p>This page wandered off. The rest of the site is where you left it.</p>
        <div className="tags">
          <Link className="tag" href="/">
            back home
          </Link>
        </div>
      </header>
      <Pic name="perch" width={260} height={170} className="lost" />
    </div>
  );
}
