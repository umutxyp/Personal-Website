import { MDXRemote } from "next-mdx-remote/rsc";
import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

const slug = (children: ReactNode) =>
  String(children)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

const components = {
  a: ({ href = "", children, ...rest }: ComponentProps<"a">) =>
    href.startsWith("/") || href.startsWith("#") ? (
      <Link href={href}>{children}</Link>
    ) : (
      <a href={href} target="_blank" rel="noopener noreferrer" {...rest}>
        {children}
      </a>
    ),
  h2: ({ children }: ComponentProps<"h2">) => <h2 id={slug(children)}>{children}</h2>,
  h3: ({ children }: ComponentProps<"h3">) => <h3 id={slug(children)}>{children}</h3>,
  // biome-ignore lint/a11y/useAltText: the alt comes from the markdown
  img: (props: ComponentProps<"img">) => <img loading="lazy" {...props} />,
};

/** A case study's text, written by hand like the rest. */
export function Mdx({ source }: { source: string }) {
  return (
    <div className="prose">
      <MDXRemote source={source} components={components} />
    </div>
  );
}
