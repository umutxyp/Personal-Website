// ============================================
// 🎨 PORTFOLIO CONFIGURATION
// ============================================
// Manage all your site information from here!

export const siteConfig = {
  // Personal Information
  personal: {
    name: "Petr Havel",
    // username: '', // odstraněno
    // tagline: '', // odstraněno
    title: "Student Geoinformatiky, dálkového průzkumu Země a kartografie",
    age: 20, // případně uprav dle potřeby (nyní příklad)
    birthDate: "", // nevyplněno
    location: "Pospíšilova 5, Praha 3, 130 00",
    avatar: "",
    email: "havelpeta@gmail.com",
    resumeUrl: "#",
  },

  // About & Bio
  about: {
    intro: "Ahoj! Jsem <strong>Petr Havel</strong>, student geoinformatiky, dálkového průzkumu Země a kartografie na Univerzitě Karlově. Zajímám se o mapy, geografii, přírodu a moderní technologie v oblasti prostorových dat.",
    
    description: `Studuji geoinformatiku a kartografii na Univerzitě Karlově v Praze, kde se věnuji zpracování prostorových dat, satelitním snímkům, mapám a analýze přírodního prostředí. Mezi mé zájmy patří technologie dálkového průzkumu Země a moderní geografické informační systémy (GIS). Rád pracuji s mapami a fascinuje mě propojení IT s objevováním světa kolem nás.`,
    
    highlights: [
      "🗺️ Student geoinformatiky a kartografie",
      "🌍 Zájem o přírodu, mapy a dálkový průzkum Země",
      "💻 Nadšenec do IT a prostorových technologií",
      "🎓 Student na Univerzitě Karlově, Praha."
    ]
  },

  // Experience
  experience: [
    {
      title: "Code Share - Founder & Developer",
      duration: "2018 - Present",
      description: "Founded Code Share in 2018 as a Discord bot development community with 15,000 members focused on collaboration and learning (2018-2023). Transformed it into a global software marketplace (2023-2025), and currently operating as a comprehensive platform where developers can publish, sell, and gain popularity, alongside selling various digital products.",
      icon: "🚀"
    },
    {
      title: "Beatra - Creator & Publisher",
      duration: "Ongoing",
      description: "Developed and maintain Altaypı, one of Discord's most recognized open-source music bots, serving thousands of servers worldwide with high-quality audio streaming and extensive features.",
      icon: "🎵"
    },
    {
      title: "Full-Stack Development",
      duration: "7+ Years",
      description: "Building websites, desktop applications, APIs, and scripts using modern technologies. Expert in MongoDB, PostgreSQL, JavaScript, React, TypeScript, Go, Tailwind, Node.js, Next.js, Express, and Socket.IO.",
      icon: "💻"
    },
    {
      title: "Content Creation",
      duration: "5+ Years",
      description: "Creating technology and programming content on YouTube (14K+ subscribers), Instagram (30K+ followers), TikTok, and Twitter. Sharing tutorials, tips, and insights about software development and tech trends.",
      icon: "🎥"
    }
  ],

  // Social Media
  social: {
    facebook: "https://www.facebook.com/petr.havel.16121",
    instagram: "https://www.instagram.com/havel_petis/",
    email: "mailto:havelpeta@gmail.com",
  },

  // Skills & Technologies
  skills: {
    frontend: [
      { name: "React.js", level: 95, icon: "react.svg" },
      { name: "Next.js", level: 90, icon: "nextjs.svg" },
      { name: "JavaScript", level: 95, icon: "javascript.svg" },
      { name: "TypeScript", level: 85, icon: "typescript.svg" },
      { name: "Tailwind CSS", level: 90, icon: "tailwindcss.svg" },
      { name: "HTML5", level: 95, icon: "html.svg" },
      { name: "CSS3", level: 90, icon: "css.svg" },
    ],
    
    backend: [
      { name: "Node.js", level: 90, icon: "nodejs.svg" },
      { name: "Express.js", level: 85, icon: "expressjs.svg" },
      { name: "Socket.IO", level: 80, icon: "nodejs.svg" },
      { name: "Go", level: 75, icon: "github.svg" },
      { name: "MongoDB", level: 85, icon: "mongodb.svg" },
      { name: "PostgreSQL", level: 80, icon: "mysql.svg" },
    ],
    
    tools: [
      { name: "Git", level: 90, icon: "git.svg" },
      { name: "GitHub", level: 90, icon: "github.svg" },
      { name: "Linux", level: 85, icon: "linux.svg" },
      { name: "Windows", level: 90, icon: "github.svg" },
      { name: "Vercel", level: 85, icon: "nextjs.svg" },
      { name: "Heroku", level: 80, icon: "heroku.svg" },
      { name: "Glitch", level: 75, icon: "nodejs.svg" },
    ]
  },

  // Projects - Auto-fetched from GitHub
  githubUsername: "umutxyp",

  // Goals
  goals: [
    "Build innovative software solutions that impact thousands of users",
    "Grow Code Share into the world's leading developer marketplace",
    "Expand my content creation to reach 100K+ followers across platforms",
    "Contribute to open-source projects and help developers worldwide",
    "Master emerging technologies like AI, blockchain, and cloud computing",
    "Create educational content that inspires the next generation of developers"
  ],

  // SEO & Meta
  seo: {
    title: "Umut Bayraktar | Full-Stack Developer & Content Creator",
    description: "Full-stack developer, Code Share founder, and creator of Beatra. 44K+ social media followers. Specializing in web development, community building, and tech content creation.",
    keywords: "umutxyp, umut bayraktar, full-stack developer, react developer, next.js, content creator, code share, altaypı, discord bot, web development, antalya developer",
    ogImage: "/og-image.png",
    twitterHandle: "@devbayraktar"
  }
};

// Theme Colors (For each theme)
export const themes = {
  dark: {
    name: "Dark",
    colors: {
      primary: "#3B82F6",
      secondary: "#8B5CF6",
      accent: "#06B6D4",
      background: "#0F172A",
      surface: "#1E293B",
      text: "#F1F5F9",
      textSecondary: "#94A3B8",
    },
    styles: {
      fontWeight: "normal",
      headingWeight: "700",
      shadow: "0 4px 6px -1px rgba(0, 0, 0, 0.3)",
      glow: "0 0 20px rgba(59, 130, 246, 0.3)",
      cardBorder: "1px solid rgba(148, 163, 184, 0.1)",
    }
  },
  
  light: {
    name: "Light",
    colors: {
      primary: "#2563EB",
      secondary: "#7C3AED",
      accent: "#0891B2",
      background: "#F8FAFC",
      surface: "#FFFFFF",
      text: "#0F172A",
      textSecondary: "#64748B",
    },
    styles: {
      fontWeight: "normal",
      headingWeight: "600",
      shadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
      glow: "0 0 15px rgba(37, 99, 235, 0.2)",
      cardBorder: "1px solid rgba(226, 232, 240, 1)",
    }
  },
  
  neon: {
    name: "Neon",
    colors: {
      primary: "#FF00FF",
      secondary: "#00FFFF",
      accent: "#FFFF00",
      background: "#000000",
      surface: "#0A0A0A",
      text: "#FFFFFF",
      textSecondary: "#B3B3B3",
    },
    styles: {
      fontWeight: "500",
      headingWeight: "800",
      shadow: "0 0 10px rgba(255, 0, 255, 0.5)",
      glow: "0 0 30px rgba(255, 0, 255, 0.6), 0 0 60px rgba(0, 255, 255, 0.4)",
      cardBorder: "2px solid rgba(255, 0, 255, 0.3)",
    }
  },

  sunset: {
    name: "Sunset",
    colors: {
      primary: "#F97316",
      secondary: "#EC4899",
      accent: "#FBBF24",
      background: "#18181B",
      surface: "#27272A",
      text: "#FAFAFA",
      textSecondary: "#A1A1AA",
    },
    styles: {
      fontWeight: "normal",
      headingWeight: "700",
      shadow: "0 10px 25px -5px rgba(249, 115, 22, 0.3)",
      glow: "0 0 25px rgba(249, 115, 22, 0.4)",
      cardBorder: "1px solid rgba(249, 115, 22, 0.2)",
    }
  },

  forest: {
    name: "Forest",
    colors: {
      primary: "#10B981",
      secondary: "#14B8A6",
      accent: "#84CC16",
      background: "#064E3B",
      surface: "#065F46",
      text: "#ECFDF5",
      textSecondary: "#6EE7B7",
    },
    styles: {
      fontWeight: "normal",
      headingWeight: "700",
      shadow: "0 4px 6px -1px rgba(16, 185, 129, 0.3)",
      glow: "0 0 20px rgba(16, 185, 129, 0.4)",
      cardBorder: "1px solid rgba(16, 185, 129, 0.2)",
    }
  }
};

export default siteConfig;



