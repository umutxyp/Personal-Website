import mdx from "@next/mdx";

const withMDX = mdx({
  extension: /\.mdx?$/,
  options: {},
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ["ts", "tsx", "md", "mdx"],
  transpilePackages: ["next-mdx-remote"],
  // Chromium for the live project screenshots (src/app/screenshots). Its Brotli
  // binaries and the project pages the route reads are loaded from disk at
  // runtime, so they are traced in explicitly.
  serverExternalPackages: ["@sparticuz/chromium", "puppeteer-core"],
  outputFileTracingIncludes: {
    // Keys are globs ("[slug]" would be a character class).
    "/screenshots/*": ["./node_modules/@sparticuz/chromium/bin/**", "./src/app/work/projects/**"],
  },
  // Each screenshot is captured during the build; a slow site needs more than 60s.
  staticPageGenerationTimeout: 180,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "www.google.com",
        pathname: "**",
      },
    ],
  },
  async redirects() {
    return [
      // Old case-study URL, kept so existing links still land on the Codeshare page.
      {
        source: "/work/code-share-marketplace",
        destination: "/work/codeshare-technology",
        permanent: true,
      },
    ];
  },
  sassOptions: {
    compiler: "modern",
    silenceDeprecations: ["legacy-js-api"],
  },
};

export default withMDX(nextConfig);
