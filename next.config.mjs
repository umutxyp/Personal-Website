/** @type {import('next').NextConfig} */
const nextConfig = {
  // Chromium for the live project screenshots (src/app/screenshots). Its Brotli
  // binaries and the project pages the route reads are loaded from disk at
  // runtime, so they are traced in explicitly.
  serverExternalPackages: ["@sparticuz/chromium", "puppeteer-core"],
  outputFileTracingIncludes: {
    // Keys are globs ("[slug]" would be a character class).
    "/screenshots/*": ["./node_modules/@sparticuz/chromium/bin/**", "./src/app/work/projects/**"],
    // The pages that list projects are regenerated in the background and read the same files.
    "/": ["./src/app/work/projects/**"],
    "/work": ["./src/app/work/projects/**"],
    "/work/*": ["./src/app/work/projects/**"],
    "/gallery": ["./src/app/work/projects/**"],
  },
  // Each screenshot is captured during the build; a slow site needs more than 60s.
  staticPageGenerationTimeout: 180,
  async redirects() {
    return [
      // Old case-study URL, kept so existing links still land on the Codeshare page.
      { source: "/work/code-share-marketplace", destination: "/work/codeshare-technology", permanent: true },
    ];
  },
};

export default nextConfig;
