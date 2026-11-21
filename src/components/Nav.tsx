"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { nav } from "@/resources";

export function Nav({ className }: { className: string }) {
  const pathname = usePathname();
  return (
    <nav className={className} aria-label="Pages">
      {nav.map(({ path, label }) => {
        const current = path === "/" ? pathname === "/" : pathname.startsWith(path);
        return (
          <Link key={path} href={path} aria-current={current ? "page" : undefined}>
            {label}
          </Link>
        );
      })}
    </nav>
  );
}
