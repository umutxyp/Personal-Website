"use client";

import { type ReactNode, useEffect, useRef } from "react";

/** Its children come into view as the page is scrolled to them. */
export function Reveal({ children, className = "", as: Tag = "div" }: { children: ReactNode; className?: string; as?: "div" | "section" | "li" }) {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          element.classList.add("in");
          observer.disconnect();
        }
      },
      { rootMargin: "0px 0px -8% 0px" },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  return (
    // @ts-expect-error one ref for the three tags it can be
    <Tag ref={ref} className={`reveal ${className}`}>
      {children}
    </Tag>
  );
}
