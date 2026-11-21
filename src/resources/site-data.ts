// Everything the site says about its owner. Change this file to make the site yours.
//
// Numbers in text are written as %project.key% tokens and filled from codeshare.me
// at render time (src/lib/live-stats.ts), so they stay current without edits here.
// **words** between two asterisks get a marker swipe behind them.

const siteData = {
  baseURL: "https://umutbayraktar.vercel.app",
  keywords: [
    "Umut Bayraktar",
    "Codeshare",
    "Codeshare Technology",
    "Full-stack developer",
    "AI systems researcher",
    "Content creator",
    "Next.js",
    "Discord bots",
    "Software studio",
    "Discord music bot",
    "Discord moderation bot",
    "Minecraft server list",
    "Discord server list",
    "Anime tracker",
    "AI chat",
    "Anti-censorship app",
    "Travel app",
  ],
  person: {
    firstName: "Umut",
    lastName: "Bayraktar",
    name: "Umut Bayraktar",
    roles: ["founder of Codeshare", "full-stack developer", "AI systems researcher"],
    role: "Founder of Codeshare · Full-Stack Developer · AI Systems Researcher",
    avatar: "/images/avatar.jpg",
    email: "umutbayraktar55@gmail.com",
    languages: ["Türkçe", "English"],
    biography:
      "Full-stack developer, AI systems researcher and content creator with 6+ years of building platforms end to end. Founder & CEO of Codeshare Technology, the software studio behind Beatra, Shroudly, Vanigo, Sylon, MCStat, JustAnime, JustDiscord and Dotrai.",
  },
  home: {
    about:
      "I'm **Umut** — full-stack developer, AI systems researcher and content creator with 6+ years of building platforms end to end. I'm the founder & CEO of **Codeshare Technology**, the software studio behind Beatra, Shroudly, Vanigo, Sylon, MCStat, JustAnime, JustDiscord and Dotrai. The company was incorporated in 2025, but most of the products are older than it — the first one dates back to 2020. The core of every product stays free, and I run all of it myself.",
    stats: [
      { value: "%studio.users%", label: "Discord users reached" },
      { value: "%studio.servers%", label: "Discord servers" },
      { value: "%studio.players%", label: "Minecraft players" },
      { value: "%github.stars%", label: "GitHub stars" },
    ],
    stack: [
      "TypeScript",
      "JavaScript",
      "Next.js",
      "React",
      "Tailwind",
      "Node.js",
      "PostgreSQL",
      "Prisma",
      "Redis",
      "MongoDB",
      "Docker",
      "Linux",
      "nginx",
      "Cloudflare",
    ],
  },
  studio: {
    name: "Codeshare Technology",
    url: "https://codeshare.me",
    tag: "software studio",
    description: "Software for online communities — with the core kept free.",
    logo: "/images/logos/codeshare.png",
    slug: "codeshare-technology",
    stats: [
      { value: "%studio.products%", label: "products live" },
      { value: "%studio.users%", label: "Discord users reached" },
      { value: "2020", label: "oldest account" },
      { value: "2025", label: "incorporated" },
    ],
  },
  // The products, in the order they are shown. `slug` is the case study under src/app/work/projects.
  products: [
    {
      name: "Beatra",
      url: "https://beatra.app",
      logo: "/images/logos/beatra.png",
      slug: "beatra-streaming-platform",
      description: "Music bot for Discord, with a web player — Spotify, YouTube, Apple Music and more.",
      stats: [
        { value: "%beatra.servers%", label: "servers" },
        { value: "%beatra.users%", label: "users" },
      ],
    },
    {
      name: "Shroudly",
      url: "https://github.com/umutxyp/Shroudly",
      logo: "/images/logos/shroudly.png",
      slug: "shroudly-anti-censorship",
      description: "Opens blocked YouTube, Instagram, X, Discord — no VPN; Windows 7–11, Mac, Linux, phones, TVs.",
      stats: [
        { value: "%shroudly.downloads%", label: "downloads" },
        { value: "%shroudly.stars%", label: "stars" },
      ],
    },
    {
      name: "Vanigo",
      url: "https://vanigo.app",
      logo: "/images/logos/vanigo.png",
      slug: "vanigo-travel-app",
      description: "Travel app with places, reviews, events and trips — plus a wallet that pays shops by local QR.",
      stats: [
        { value: "%vanigo.places%", label: "places" },
        { value: "%vanigo.languages%", label: "languages" },
      ],
    },
    {
      name: "Sylon",
      url: "https://sylon.app",
      logo: "/images/logos/sylon.png",
      slug: "sylon-discord-bot",
      description: "AI moderation for Discord that catches ads and scams in any language, even in images.",
      stats: [
        { value: "%sylon.servers%", label: "servers" },
        { value: "%sylon.users%", label: "users" },
        { value: "%sylon.uptime%", label: "uptime" },
      ],
    },
    {
      name: "MCStat",
      url: "https://mcstat.org",
      logo: "/images/logos/mcstat.png",
      slug: "mcstat-minecraft-server-list",
      description: "Real-time Minecraft server list with live player counts, vote rankings and player profiles.",
      stats: [
        { value: "%mcstat.servers%", label: "servers" },
        { value: "%mcstat.players%", label: "players" },
        { value: "%mcstat.skins%", label: "skins" },
      ],
    },
    {
      name: "JustAnime",
      url: "https://justanime.me",
      logo: "/images/logos/justanime.png",
      logoTile: "#15131d",
      slug: "justanime-anime-tracker",
      description: "Anime & manga tracker where every single episode gets its own rating and review.",
      stats: [
        { value: "%justanime.titles%", label: "titles" },
        { value: "%justanime.characters%", label: "characters" },
        { value: "%justanime.schedule%", label: "airing" },
      ],
    },
    {
      name: "JustDiscord",
      url: "https://justdiscord.org",
      logo: "/images/logos/justdiscord.png",
      slug: "justdiscord-server-bot-list",
      description: "Discord server & bot list built on trust — real reviews, verified owners, free emojis.",
      stats: [
        { value: "%justdiscord.servers%", label: "servers" },
        { value: "%justdiscord.bots%", label: "bots" },
        { value: "%justdiscord.emojis%", label: "emojis" },
      ],
    },
    {
      name: "Dotrai",
      url: "https://dotrai.com",
      logo: "/images/logos/dotrai.png",
      logoTile: "#0d0d0f",
      slug: "dotrai-ai-chat",
      description: "Free AI chat that searches the live web, runs real code and shows its reasoning.",
      stats: [],
    },
  ],
  social: [
    { name: "codeshare.me", link: "https://codeshare.me" },
    { name: "github", link: "https://github.com/umutxyp" },
    { name: "linkedin", link: "https://linkedin.com/in/umutxyp" },
    { name: "youtube", link: "https://youtube.com/@umutxyp" },
    { name: "instagram", link: "https://instagram.com/umutxyp" },
    { name: "tiktok", link: "https://tiktok.com/@umutxyp" },
    { name: "telegram", link: "https://t.me/umutxyp" },
    { name: "x", link: "https://twitter.com/devbayraktar" },
    { name: "facebook", link: "https://facebook.com/umutxyp" },
    { name: "discord", link: "https://discord.gg/FnU3Whr9ef" },
    { name: "email", link: "mailto:umutbayraktar55@gmail.com" },
  ],
  about: {
    intro:
      "I am a software developer, AI systems researcher and content creator. For over 6 years I have been building and running platforms end to end — writing the code, operating the servers they run on, and growing the communities around them. Today that work lives under **Codeshare Technology**, the software studio I founded: a Discord music bot reaching %beatra.users% users in %beatra.servers% servers, an anti-censorship app downloaded %shroudly.downloads% times, a travel app with a map of %vanigo.places% places, an AI moderation bot, a Minecraft data platform, a Discord directory, an anime tracker and an AI chat.",
    experiences: [
      {
        company: "Codeshare Technology",
        timeframe: "Feb 2020 — today",
        role: "Founder & CEO",
        link: "https://codeshare.me",
        achievements: [
          "Run Codeshare Technology Ltd (registered in England and Wales, no. 16672504), a small studio that builds software for online communities and runs it — no agency work, no consulting, nothing built for a client.",
          "Lead eight products — Beatra, Shroudly, Vanigo, Sylon, MCStat, JustAnime, JustDiscord and Dotrai — present in %studio.servers% Discord servers and reaching %studio.users% Discord users, from code to servers to the communities around them.",
          "Keep the core of every product free: Beatra plays music, Shroudly gets blocked sites loading again, MCStat gives its data away through an open API, and Dotrai answers questions.",
          "Built the first products in 2020 and incorporated the company in August 2025, once most of the products already existed and needed a company around them.",
        ],
      },
      {
        company: "Beatra",
        timeframe: "Nov 2020 — today",
        role: "Founder & Lead Developer",
        link: "https://beatra.app",
        achievements: [
          "First built in November 2020 and launched in 2021 as MusicMaker; shut it down in 2022 and brought it back in October 2025 as Beatra, on its original account.",
          "Built a music platform spanning Discord, the web player and Discord Activities, playing from YouTube, YouTube Music, Spotify, Apple Music, Deezer, SoundCloud, Tidal, Qobuz and Audius into one queue.",
          "Running in %beatra.servers% Discord servers for %beatra.users% users, with audio kept on its own voice servers so a busy moment elsewhere does not interrupt the song.",
          "Shipped Music Quiz, Taste Match, listening recaps, server and profile pages, a custom-bot tenant system and Premium from $1.49 a month.",
        ],
      },
      {
        company: "Shroudly",
        timeframe: "Oct 2025 — today",
        role: "Founder & Lead Developer",
        link: "https://github.com/umutxyp/Shroudly",
        achievements: [
          "Built a free, open-source anti-censorship app that opens blocked sites and apps without a VPN server in between — downloaded %shroudly.downloads% times, with %shroudly.stars% stars on GitHub.",
          "Shipped it for Windows 7 to 11, macOS, Linux, Android, Android TV and Google TV, iPhone, iPad and Apple TV, from one engine; it is on Google Play and the Mac App Store.",
          "Wrote an engine that learns which technique opens each site on each network, with encrypted DNS, optional ad blocking, and Tor as the last way out only when the user says yes.",
          "No account and no server of ours in between: the app counts only how many copies are running, with a random id made fresh at every start.",
        ],
      },
      {
        company: "Vanigo",
        timeframe: "Oct 2026 — today",
        role: "Founder & Lead Developer",
        link: "https://vanigo.app",
        achievements: [
          "Built a travel app for iPhone and Android: a map of %vanigo.places% places, reviews, events, day-by-day trips and questions answered by locals, in %vanigo.languages% languages.",
          "Added a travel toolkit — an offline currency converter, a guide to each country, local emergency numbers, transport apps and a card to show your driver — and end-to-end encrypted chat.",
          "Designed a self-custody wallet that pays shops by local QR from USDT or USDC through a licensed partner; QR payments are being switched on country by country.",
          "Wrote the app, its server, the website and the web map, and run all of it on Codeshare's own server.",
        ],
      },
      {
        company: "Sylon",
        timeframe: "Feb 2020 — today",
        role: "Founder & Lead Developer",
        link: "https://sylon.app",
        achievements: [
          "Started in February 2020 as Server Support, the oldest product I run; it became Sylon with its own site in April 2026.",
          "Built an AI moderation bot that catches Discord advertisements, invite links and scams in any language — including text hidden inside images — and writes every action it takes, with the reason, to a log channel.",
          "Shipped a join gate that screens accounts at the door, raid alerts with optional lockdown, harassment detection, a URL scanner, appeals, tickets with transcripts, leveling, giveaways, a suggestion board and role menus.",
          "Serving %sylon.servers% servers and %sylon.users% users with %sylon.uptime% uptime.",
        ],
      },
      {
        company: "MCStat",
        timeframe: "Dec 2025 — today",
        role: "Founder & Lead Developer",
        link: "https://mcstat.org",
        achievements: [
          "Built a Minecraft server list and data platform that pings every server around the clock and rolls the readings into a history, so a server page shows the last day, week, month and 90 days rather than a snapshot.",
          "Tracks %mcstat.servers% servers and %mcstat.players% player records, and keeps each player's recent skins and capes — %mcstat.skins% skins so far — because Mojang serves only the current one.",
          "Ranks players by activity points, by number of sessions and by how many different servers they play on, from sessions reported by servers that run the free MCStat plugin.",
          "Split the runtime into separate services so the website never restarts because the bot crashed, and shipped an open-source plugin, a Discord bot and a free API.",
        ],
      },
      {
        company: "JustAnime",
        timeframe: "Aug 2026 — today",
        role: "Founder & Lead Developer",
        link: "https://justanime.me",
        achievements: [
          "Built an anime and manga tracker where every single episode can be rated and reviewed, not just the series as a whole — over a catalogue of %justanime.titles% titles and %justanime.characters% character records.",
          "Shipped a library with episode-by-episode progress, studio following, recommendations, an airing calendar, charts, achievements and a social feed.",
          "Built JustAnime Sync, a browser extension that marks episodes and chapters as you finish them on 200+ streaming and reading sites, and keeps AniList and MyAnimeList lists in step.",
        ],
      },
      {
        company: "JustDiscord",
        timeframe: "Aug 2026 — today",
        role: "Founder & Lead Developer",
        link: "https://justdiscord.org",
        achievements: [
          "Built a Discord server and bot directory designed around trust: every listing carries a score out of 5 with reviews that explain the score, verified ownership is marked, and sponsored placements are always labelled.",
          "Ranks listings by community votes over a rolling 30-day window, so a server has to keep earning its place instead of coasting on a lead from years ago.",
          "Runs %justdiscord.servers% server listings and %justdiscord.bots% bot listings, plus %justdiscord.emojis% free emojis and stickers downloadable with no account.",
          "Shipped a bump every 12 hours, a public API with vote webhooks, and an official TypeScript SDK on npm.",
        ],
      },
      {
        company: "Dotrai",
        timeframe: "Mar 2025 — today",
        role: "Founder & Lead Developer",
        link: "https://dotrai.com",
        achievements: [
          "Built a free, browser-based AI chat that shows its working: live web search with the sources kept on the answer, and JavaScript run in a sandbox so the numbers are computed rather than guessed.",
          "Shipped file and image understanding, streaming responses, saved history across devices, memory you can review and delete, and incognito chats that are discarded when the next one begins.",
          "Available in 12 languages; new sign-ups are paused while its capacity is being sorted out.",
        ],
      },
    ],
    studies: [
      {
        name: "Web Design and Coding (Associate)",
        description: "Ankara University — modern web technology, UI/UX and AI-assisted front-end projects.",
      },
      {
        name: "Electrical & Electronic High Voltage",
        description:
          "Kepez Vocational and Technical Anatolian High School — a four-year program on circuit design, safety and energy transmission.",
      },
    ],
    technical: [
      {
        title: "Frontend",
        description: "React and Next.js at production scale — App Router, server components, i18n.",
        tags: ["React", "Next.js", "TypeScript", "JavaScript", "Tailwind CSS", "React Native", "Expo"],
      },
      {
        title: "Backend",
        description: "APIs, background workers, real-time gateways and Discord bots at shard scale.",
        tags: ["Node.js", "Express", "Socket.IO", "Discord.js", "Rust", "Lavalink"],
      },
      {
        title: "Data",
        description: "Schema design, migrations and caching for catalogues in the hundreds of thousands.",
        tags: ["PostgreSQL", "MongoDB", "Prisma", "Redis", "SQLite"],
      },
      {
        title: "Infrastructure",
        description: "Self-hosted production: I run the servers my products live on.",
        tags: ["Linux", "nginx", "systemd", "Docker", "Cloudflare", "Git", "Vercel"],
      },
      {
        title: "SEO & growth",
        description: "Sitemaps, structured data and crawler budgets for catalogues at 100K+ URLs.",
        tags: ["Technical SEO", "Structured data", "Internationalization", "Analytics"],
      },
      {
        title: "Community & content",
        description: "6+ years running communities and publishing to 44K+ followers.",
        tags: ["Community management", "Content creation", "Discord", "Instagram", "YouTube", "TikTok"],
      },
    ],
  },
  github: {
    username: "umutxyp",
    // Shown when the pinned repositories cannot be read from the GitHub profile.
    highlight: ["MusicBot", "Seo-Promt-Master", "Shroudly", "Discord-Bot-Website", "Personal-Website", "v14-discord-bot"],
    description: "Discord bots, SEO tooling and production-ready starters — open-sourced from the products I run.",
  },
};

export type SiteData = typeof siteData;
export type Product = (typeof siteData.products)[number];
export default siteData;
