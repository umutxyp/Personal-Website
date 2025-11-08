# Umut Bayraktar - Portfolio

Modern, high-performance portfolio website built with Next.js 15, Once UI, and TypeScript. Showcasing projects, experience, and technical expertise as a Full-Stack Developer and Founder of CodeShare Technology Ltd.

## ✨ Features

- **🚀 Next.js 15** - Latest React framework with App Router
- **🎨 Once UI System** - Beautiful, accessible component library
- **📱 Fully Responsive** - Optimized for all devices
- **🌙 Dark/Light Mode** - Theme switching with system preference detection
- **⚡ Static Generation** - Blazing fast page loads
- **📝 MDX Support** - Write content with React components
- **🎯 TypeScript** - Full type safety
- **🔍 SEO Optimized** - Meta tags, Open Graph, Schema.org
- **📊 GitHub Integration** - Auto-fetch and display repositories

## 🛠️ Tech Stack

- **Framework:** Next.js 15.3
- **UI Library:** Once UI System 1.4
- **Language:** TypeScript 5.8
- **Styling:** SCSS Modules
- **Content:** MDX
- **Icons:** React Icons
- **Deployment:** Vercel

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/umutxyp/Personal-Website.git

# Navigate to project directory
cd Personal-Website

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## 🚀 Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
npm run export   # Export static site
```

## 📁 Project Structure

```
├── public/
│   └── images/          # Static images
├── src/
│   ├── app/             # Next.js App Router pages
│   │   ├── about/       # About page
│   │   ├── work/        # Projects showcase
│   │   ├── gallery/     # Image gallery
│   │   ├── github/      # GitHub repos
│   │   └── api/         # API routes
│   ├── components/      # React components
│   ├── resources/       # Configuration & content
│   │   ├── content.tsx  # Page content
│   │   ├── site-data.tsx # Site data & metadata
│   │   └── once-ui.config.ts # UI configuration
│   ├── types/           # TypeScript types
│   └── utils/           # Utility functions
└── package.json
```

## ⚙️ Configuration

### Site Data
Edit `src/resources/site-data.tsx` to update:
- Personal information
- Social links
- Projects
- Work experience
- GitHub username

### UI Theme
Customize theme in `src/resources/once-ui.config.ts`:
- Colors (brand, accent, neutral)
- Typography
- Border styles
- Effects

### Routes
Enable/disable pages in `src/resources/once-ui.config.ts`:
```typescript
const routes = {
  "/": true,
  "/about": true,
  "/work": true,
  "/blog": false,
  "/gallery": true,
  "/github": true,
};
```

## 📄 Adding Projects

1. Create a new MDX file in `src/app/work/projects/`:
```mdx
---
title: "Project Name"
publishedAt: "2024-01-01"
summary: "Short description"
images: ["/images/projects/project.png"]
team: []
link: "https://project.com"
---

Project content here...
```

2. The project will automatically appear on the work page.

## 🎨 Customization

### Colors
Update theme colors in `once-ui.config.ts`:
- `brand`: Primary brand color
- `accent`: Accent/secondary color
- `neutral`: Gray scale tones

### Fonts
Configured in `once-ui.config.ts` using Next.js Font optimization:
- Heading: Geist
- Body: Geist
- Code: Geist Mono

## 🌐 Deployment

### Vercel (Recommended)
1. Push to GitHub
2. Import project in Vercel
3. Deploy automatically

### Manual Build
```bash
npm run build
npm start
```

## 📊 GitHub Integration

The `/github` page automatically fetches your public repositories. Update your GitHub username in `src/resources/site-data.tsx`:

```typescript
github: {
  username: "umutxyp",
  highlight: ["CodeShare", "Beatra", "MusicBot"],
}
```

## 🔧 Environment Variables

Optional: Create `.env.local` for password protection:
```env
PAGE_ACCESS_PASSWORD=your_password
```

Enable protected routes in `once-ui.config.ts`:
```typescript
const protectedRoutes = {
  "/about": true
};
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Connect

- **Website:** [umutbayraktar.vercel.app](https://umutbayraktar.vercel.app)
- **GitHub:** [@umutxyp](https://github.com/umutxyp)
- **LinkedIn:** [umutxyp](https://linkedin.com/in/umutxyp)
- **Twitter:** [@devbayraktar](https://twitter.com/devbayraktar)
- **Email:** umutbayraktar55@gmail.com

---

Built with ❤️ by [Umut Bayraktar](https://github.com/umutxyp) | Powered by [Next.js](https://nextjs.org) & [Once UI](https://once-ui.com)
