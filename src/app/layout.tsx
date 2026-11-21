import "./themes.css";
import "./globals.css";

import type { Metadata, Viewport } from "next";
import { Gochi_Hand, Shantell_Sans } from "next/font/google";
import { Footer, Header } from "@/components";
import { baseURL, defaultTheme, person, siteData, themes } from "@/resources";

// The name is written in Gochi Hand, everything else in Shantell Sans: a marker and a pen.
const display = Gochi_Hand({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});
const text = Shantell_Sans({
  subsets: ["latin", "latin-ext"],
  axes: ["BNCE", "INFM", "SPAC"],
  variable: "--font-text",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(baseURL),
  title: { default: `${person.name} | ${person.role}`, template: `%s | ${person.name}` },
  description: person.biography,
  keywords: siteData.keywords,
  authors: [{ name: person.name, url: baseURL }],
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    siteName: person.name,
    title: `${person.name} | ${person.role}`,
    description: person.biography,
    url: baseURL,
    images: [
      {
        url: `/api/og/generate?title=${encodeURIComponent(person.name)}`,
        width: 1280,
        height: 720,
      },
    ],
  },
  twitter: { card: "summary_large_image" },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#e9f4fd" },
    { media: "(prefers-color-scheme: dark)", color: "#0d1826" },
  ],
};

// Runs before the first paint: the theme and the mode the visitor chose last time, or the
// default theme in the mode their system asks for. A link can carry a choice too
// (?theme=owl&mode=dark), which is then remembered like any other. The script is a fixed
// string: the themes it may choose from are read from <html data-themes>, and the default is
// the data-theme the server already wrote, so nothing is ever spliced into code.
const themeInit = `(function(){var d=document.documentElement,t,m,q=new URLSearchParams(location.search),ok=(d.getAttribute("data-themes")||"").split(" ");
try{if(ok.indexOf(q.get("theme"))>=0)localStorage.setItem("theme",q.get("theme"));if(q.get("mode")==="light"||q.get("mode")==="dark")localStorage.setItem("mode",q.get("mode"));
t=localStorage.getItem("theme");m=localStorage.getItem("mode")}catch(e){t=q.get("theme");m=q.get("mode")}
if(ok.indexOf(t)<0)t=d.getAttribute("data-theme");
if(m!=="light"&&m!=="dark")m=window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";
d.dataset.theme=t;d.dataset.mode=m})()`;

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: person.name,
  url: baseURL,
  image: `${baseURL}${person.avatar}`,
  jobTitle: person.role,
  description: person.biography,
  worksFor: { "@type": "Organization", name: siteData.studio.name, url: siteData.studio.url },
  sameAs: siteData.social.map((item) => item.link).filter((link) => link.startsWith("https://")),
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      data-theme={defaultTheme}
      data-themes={themes.map((theme) => theme.id).join(" ")}
      data-mode="light"
      className={`${display.variable} ${text.variable}`}
      suppressHydrationWarning
    >
      <head>
        {/* biome-ignore lint/security/noDangerouslySetInnerHtml: our own script, set before paint */}
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
        <noscript>
          <style>{".reveal{opacity:1;transform:none}"}</style>
        </noscript>
      </head>
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
        <script
          type="application/ld+json"
          // biome-ignore lint/security/noDangerouslySetInnerHtml: structured data
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </body>
    </html>
  );
}
