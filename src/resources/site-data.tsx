const siteData = {
  meta: {
    baseURL: "https://umutbayraktar.vercel.app",
    keywords: [
      "Umut Bayraktar",
      "Codeshare",
      "Codeshare Technology",
      "Full-stack developer",
      "AI Systems Researcher",
      "Content Creator",
      "Community Management",
      "Social Media Management",
      "Next.js",
      "Discord bots",
      "Software studio",
      "Discord music bot",
      "Discord moderation bot",
      "Minecraft server list",
      "Discord server list",
      "Anime tracker",
      "AI chat",
    ],
  },
  person: {
    firstName: "Umut",
    lastName: "Bayraktar",
    name: "Umut Bayraktar",
    role: "AI Systems Researcher · Full-Stack Developer · Content Creator",
    avatar: "/images/avatar.jpg",
    email: "umutbayraktar55@gmail.com",
    phone: "",
    website: "https://umutbayraktar.vercel.app",
    timezone: "Asia/Hanoi",
    address: "Vietnam",
    languages: ["Türkçe", "English"],
    biography:
      "Professional software developer, AI systems researcher, and content creator with 6+ years of experience in full-stack development, community management, and social media. Founder & CEO of Codeshare Technology, the studio behind Beatra, Sylon, MCStat, JustDiscord, JustAnime, and Dotrai — six products reaching 2.9M Discord users.",
  },
  hero: {
    headline: "Full-Stack Developer, AI Researcher & Content Creator",
    subline: (
      <>
        6+ years building platforms that carry real traffic — a Discord music bot reaching 3M
        users in 40K servers, an AI moderation bot, a Minecraft data platform with 463K player
        records, a Discord discovery platform, an anime tracker, and an AI chat. Founder of{" "}
        <strong>Codeshare Technology</strong>, the studio they all live under.
      </>
    ),
    featured: {
      label: "Codeshare Technology",
      href: "https://codeshare.me",
      badge: "Software studio",
    },
    ctaPrimary: {
      label: "Explore Codeshare",
      href: "https://codeshare.me",
    },
    ctaSecondary: {
      label: "Watch Beatra in action",
      href: "https://beatra.app",
    },
    stats: [
      { value: "2.9M", label: "Discord users reached across Codeshare products" },
      { value: "3M", label: "Beatra users across 40K Discord servers" },
      { value: "463K", label: "Minecraft player records on MCStat" },
      { value: "44K+", label: "Followers across Instagram, YouTube & TikTok" },
    ],
  },
  newsletter: {
    display: false,
    title: "Build log",
    description: "Shipping notes from Beatra, Sylon, MCStat, JustDiscord, JustAnime, and Dotrai.",
  },
  social: [
    { name: "Instagram", icon: "instagram", link: "https://instagram.com/umutxyp" },
    { name: "YouTube", icon: "youtube", link: "https://youtube.com/@umutxyp" },
    { name: "TikTok", icon: "tiktok", link: "https://tiktok.com/@umutxyp" },
    { name: "umutxyp", icon: "discord", link: "https://discord.gg/FnU3Whr9ef" },
    { name: "GitHub", icon: "github", link: "https://github.com/umutxyp" },
    { name: "LinkedIn", icon: "linkedin", link: "https://linkedin.com/in/umutxyp" },
    { name: "Twitter", icon: "twitter", link: "https://twitter.com/devbayraktar" },
    { name: "Telegram", icon: "telegram", link: "https://t.me/umutxyp" },
    { name: "Facebook", icon: "facebook", link: "https://facebook.com/umutxyp" },
  ],
  about: {
    introTitle: "Who I am",
    introDescription:
      "I am a professional software developer, AI systems researcher, and content creator. For over 6 years I have been building and running platforms end to end — writing the code, operating the servers they run on, and growing the communities around them. Today that work lives under Codeshare Technology, the studio I founded: a Discord music bot reaching 3M users in 40,000 servers, an AI moderation bot in 500 servers, a Minecraft data platform tracking 6,752 servers and 463K player records, a Discord discovery platform with 11,000+ listings, an anime and manga tracker with 123K titles, and a free AI chat. The core of every product stays free, I run all of it on my own infrastructure, and I produce content across Instagram, YouTube, and TikTok for 44K+ followers.",
    experiences: [
      {
        company: "Codeshare Technology",
        timeframe: "Feb 2020 - Present",
        role: "Founder & CEO",
        achievements: [
          "Run Codeshare Technology Ltd (registered in England and Wales, no. 16672504), a small studio that builds software for online communities and runs it — no agency work, no consulting, nothing built for a client.",
          "Lead six products — Beatra, Sylon, MCStat, JustDiscord, JustAnime, and Dotrai — reaching 2.9M Discord users, from code to servers to the communities around them.",
          "Keep the core of every product free: Beatra plays music, Sylon guards a server, MCStat gives its data away through an open API, and Dotrai answers questions, none of it behind a payment.",
          "Built the first products in 2020 and incorporated the company in August 2025, once four of the six products already existed and needed a company around them.",
        ],
        images: [],
        link: "https://codeshare.me",
      },
      {
        company: "MCStat.org",
        timeframe: "Dec 2025 - Present",
        role: "Founder & Lead Developer",
        achievements: [
          "Built a real-time Minecraft server list and data platform with live player counts, uptime history, vote rankings, ping latency, per-country breakdowns, and an open API.",
          "Tracks 6,752 servers and holds 463K player records with name history, skin history, and a cape gallery — 428K skins archived.",
          "Split the runtime into separate services so the website never restarts because the bot crashed and the ping worker never competes with the web server for CPU.",
          "Shipped a Bukkit/proxy plugin that streams signed telemetry — sessions, TPS, vote links — straight from server owners' machines.",
        ],
        images: [],
        link: "https://mcstat.org",
      },
      {
        company: "Beatra",
        timeframe: "Nov 2020 - Present",
        role: "Founder & Lead Developer",
        achievements: [
          "First built in November 2020 and launched in 2021 as MusicMaker; shut it down in 2022 and brought it back in October 2025 as Beatra, on its original account.",
          "Built a multi-platform music streaming ecosystem spanning Discord, web, desktop, and Discord Activities, playing from YouTube, YouTube Music, Spotify, Apple Music, Deezer, SoundCloud, Tidal, Audius, and Qobuz.",
          "Scaled to 40K Discord servers and 3M users with synchronized playback, audio filters, smart autoplay, and 99% uptime.",
          "Shipped Beatra Wrapped, listening analytics, server and profile pages, a custom-bot tenant system, and a premium tier at $1.49/month.",
        ],
        images: [],
        link: "https://beatra.app",
      },
      {
        company: "JustDiscord",
        timeframe: "Aug 2026 - Present",
        role: "Founder & Lead Developer",
        achievements: [
          "Built a Discord server and bot discovery platform designed around trust: every listing carries a score out of 5 with reviews that explain the score, ownership is verified through Discord itself, and sponsored placements are always labelled.",
          "Runs a catalogue of 2,835 server listings and 8,198 bot listings, plus 96.8K free emojis and stickers installable straight to a server you own — with 18.4K unique visitors.",
          "Shipped an hourly bump system, a public API with vote webhooks, and an official zero-dependency TypeScript SDK on npm.",
        ],
        images: [],
        link: "https://justdiscord.org",
      },
      {
        company: "Sylon",
        timeframe: "Feb 2020 - Present",
        role: "Founder & Lead Developer",
        achievements: [
          "Started in February 2020 as Server Support, the oldest product I run; it became Sylon with its own site in April 2026.",
          "Built an AI moderation bot that catches Discord advertisements, invite links, and scams in any language — including text hidden inside images.",
          "Shipped a full moderation suite with cases and logs, a ticket system with HTML transcripts, server guard, anti-raid and anti-spam, leveling with custom rank cards, giveaways, role menus, and welcome automation.",
          "Serving 500 servers and 300K users with 99.9% uptime across all shards.",
        ],
        images: [],
        link: "https://sylon.app",
      },
      {
        company: "JustAnime",
        timeframe: "Aug 2026 - Present",
        role: "Founder & Lead Developer",
        achievements: [
          "Built an anime and manga tracker where every single episode can be rated and reviewed, not just the series as a whole — over a catalogue of 123K titles, 176K character records, and 1,190 airing schedule entries.",
          "Shipped studio following, user follows, seasonal calendars, trending charts, achievements, and community reviews.",
          "Built JustAnime Sync, a Chrome and Firefox extension that marks episodes and chapters as you watch or read on 200+ streaming and reading sites, and mirrors progress to linked AniList and MyAnimeList accounts.",
        ],
        images: [],
        link: "https://justanime.me",
      },
      {
        company: "Dotrai",
        timeframe: "Mar 2025 - Present",
        role: "Founder & Lead Developer",
        achievements: [
          "Built a free, browser-based AI chat that searches the live web, runs real code, and shows its reasoning.",
          "Shipped streaming responses, syntax-highlighted code help across languages, and conversations saved to the account so they continue on any device.",
          "Kept sign-up to an email and a password — no credit card, no setup, no download.",
        ],
        images: [],
        link: "https://dotrai.com",
      },
    ],
    studies: [
      {
        name: "Electrical & Electronic High Voltage",
        description:
          "Kepez Vocational and Technical Anatolian High School - four-year program focused on circuit design, safety, and energy transmission.",
      },
      {
        name: "Web Design and Coding (Associate)",
        description:
          "Ankara University - specializing in modern web tech, UI/UX, and AI-assisted front-end projects.",
      },
    ],
    technical: [
      {
        title: "Frontend Development",
        description: "React and Next.js at production scale — App Router, server components, i18n",
        images: [],
        tags: [
          { name: "React.js", icon: "react" },
          { name: "Next.js", icon: "nextjs" },
          { name: "JavaScript", icon: "javascript" },
          { name: "TypeScript", icon: "typescript" },
          { name: "Tailwind CSS", icon: "css" },
          { name: "HTML5", icon: "html" },
          { name: "CSS3", icon: "css" },
        ],
      },
      {
        title: "Backend Development",
        description: "APIs, background workers, real-time gateways, and Discord bots at shard scale",
        images: [],
        tags: [
          { name: "Node.js", icon: "nodejs" },
          { name: "Express.js", icon: "javascript" },
          { name: "Socket.IO", icon: "javascript" },
          { name: "Discord.js", icon: "discord" },
          { name: "Lavalink", icon: "code" },
          { name: "Go", icon: "code" },
        ],
      },
      {
        title: "Database & Data",
        description: "Schema design, migrations, and caching for catalogues in the tens of thousands",
        images: [],
        tags: [
          { name: "PostgreSQL", icon: "database" },
          { name: "MongoDB", icon: "database" },
          { name: "Prisma", icon: "database" },
          { name: "Redis", icon: "database" },
        ],
      },
      {
        title: "Infrastructure & DevOps",
        description: "Self-hosted production: I run the servers my products live on",
        images: [],
        tags: [
          { name: "Linux", icon: "terminal" },
          { name: "Nginx", icon: "terminal" },
          { name: "systemd", icon: "terminal" },
          { name: "Docker", icon: "code" },
          { name: "Cloudflare", icon: "code" },
          { name: "Git", icon: "github" },
          { name: "GitHub", icon: "github" },
          { name: "Vercel", icon: "vercel" },
        ],
      },
      {
        title: "SEO & Growth",
        description: "Sitemaps, structured data, and crawler budgets for catalogues at 100K+ URLs",
        images: [],
        tags: [
          { name: "Technical SEO", icon: "code" },
          { name: "Structured Data", icon: "code" },
          { name: "Internationalization", icon: "code" },
          { name: "Analytics", icon: "code" },
        ],
      },
      {
        title: "Community & Social Media",
        description: "6+ years running communities and publishing to 44K+ followers",
        images: [],
        tags: [
          { name: "Community Management", icon: "person" },
          { name: "Social Media Management", icon: "person" },
          { name: "Content Creation", icon: "person" },
          { name: "Digital Marketing", icon: "person" },
          { name: "Project Management", icon: "person" },
          { name: "Discord", icon: "discord" },
          { name: "Instagram", icon: "instagram" },
          { name: "YouTube", icon: "youtube" },
          { name: "TikTok", icon: "tiktok" },
        ],
      },
    ],
  },
  // Live screenshots of each product, refreshed weekly (src/app/screenshots).
  gallery: [
    "/screenshots/mcstat-minecraft-server-list",
    "/screenshots/beatra-streaming-platform",
    "/screenshots/justdiscord-server-bot-list",
    "/screenshots/sylon-discord-bot",
    "/screenshots/justanime-anime-tracker",
    "/screenshots/dotrai-ai-chat",
    "/screenshots/codeshare-technology",
    "/screenshots/creator-studio-automation",
  ],
  github: {
    username: "umutxyp",
    // Fallback only. The /github page scrapes the live pinned repositories from the
    // GitHub profile, so what is pinned there is what shows here.
    highlight: [
      "MusicBot",
      "Seo-Promt-Master",
      "Discord-Bot-Website",
      "Personal-Website",
      "slash-command-bot",
      "Shroudly",
    ],
    description:
      "Discord bots, SEO tooling, and production-ready starters — open-sourced from the products I run.",
  },
};

export default siteData;
