# 🚀 Umut Bayraktar - Portfolio Website

<div align="center">

![Portfolio](https://img.shields.io/badge/Portfolio-2.0-blue?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14.0-black?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-18.2-61dafb?style=for-the-badge&logo=react)
![Three.js](https://img.shields.io/badge/Three.js-r159-black?style=for-the-badge&logo=three.js)
![Tailwind](https://img.shields.io/badge/Tailwind-3.3-38bdf8?style=for-the-badge&logo=tailwind-css)

**Modern portfolio website with stunning 3D animations, multi-theme support, and cutting-edge design**

[Live Demo](https://umutbayraktar.vercel.app) · [Report Bug](https://github.com/umutxyp/Personal-Website/issues) · [Request Feature](https://github.com/umutxyp/Personal-Website/issues)

</div>

---

## ✨ Features

### 🎨 **Multi-Theme System**
- 🌙 **Dark Mode** - Eye-friendly dark theme
- ☀️ **Light Mode** - Clean and bright appearance
- ⚡ **Neon Mode** - Vibrant and energetic colors
- 🌅 **Sunset Mode** - Warm and relaxing tones
- 🌲 **Forest Mode** - Nature-inspired green theme
- 💾 LocalStorage theme persistence

### 🎭 **3D Animations & Effects**
- 🌟 Interactive 3D scene with Three.js
- ⭐ Animated particle system (2000+ particles)
- 🔮 Rotating and morphing 3D sphere
- 🎪 Smooth page transitions with Framer Motion
- 🎨 Scroll-triggered animations
- ✨ Hover effects and micro-interactions

### 📱 **Responsive Design**
- 📱 Mobile-first approach (320px - 1440px+)
- 💻 Tablet optimization
- 🖥️ Desktop widescreen support
- 🔄 Perfect display on all devices

### ⚙️ **Centralized Configuration**
- 📝 Single config file (`lib/config.js`) for all site content
- 👤 Personal information
- 💼 Experience & career timeline
- 🛠️ Skills & technologies
- 🚀 Projects (GitHub integration)
- 📧 Contact information
- 🎯 Goals & achievements

### 🔥 **GitHub Integration**
- 🔗 Auto-fetch repositories from GitHub API
- ⭐ Sort projects by star count
- 🖼️ OpenGraph preview images
- 🏷️ Language-based filtering
- 📊 Display stats (stars, forks)

### ⚡ **Performance Optimized**
- 🚀 Next.js 14 with SSG & SSR
- 📦 Optimized bundle size (~130 kB)
- 🎯 Code splitting & lazy loading
- 🔧 Production-ready build
- 📈 SEO optimized

---

## 🛠️ Tech Stack

### Frontend
- **React.js 18.2.0** - UI Library
- **Next.js 14.0.3** - React Framework
- **Tailwind CSS 3.3.5** - Utility-first CSS
- **Framer Motion 10.16.4** - Animation Library
- **Three.js + React Three Fiber** - 3D Graphics
- **TypeScript** - Type Safety

### Backend & Tools
- **Node.js** - Runtime Environment
- **Express.js** - API Routes
- **MongoDB & PostgreSQL** - Databases
- **Socket.IO** - Real-time Features
- **Vercel** - Deployment Platform
- **Git & GitHub** - Version Control

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- npm or yarn package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/umutxyp/Personal-Website.git
cd Personal-Website
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Configure your settings**

Edit `lib/config.js` with your information:
```javascript
export const siteConfig = {
  personal: {
    name: "Your Name",
    username: "yourusername",
    email: "your@email.com",
    // ... more settings
  },
  // ... other configurations
}
```

4. **Run development server**
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

5. **Build for production**
```bash
npm run build
npm start
# or
yarn build
yarn start
```

---

## 📁 Project Structure

```
portfolio/
├── components/          # React components
│   ├── NewHeader.js     # Navigation header
│   ├── HeroSection.js   # Landing section with 3D background
│   ├── SkillsSection.js # Skills & technologies display
│   ├── ExperienceSection.js # Career timeline
│   ├── ProjectsSection.js   # GitHub projects gallery
│   ├── ContactSection.js    # Contact information
│   └── ThemeSwitcher.js     # Theme selection UI
├── pages/               # Next.js pages
│   ├── _app.jsx         # App wrapper
│   ├── _document.jsx    # HTML document
│   ├── index.jsx        # Home page
│   ├── projects.jsx     # Projects page
│   ├── contact.jsx      # Contact page
│   └── api/             # API routes
│       └── github-repos.js  # GitHub API integration
├── lib/                 # Utilities
│   ├── config.js        # 🎯 MAIN CONFIGURATION FILE
│   └── swr.js           # SWR hooks
├── contexts/            # React contexts
│   └── ThemeContext.js  # Theme management
├── public/              # Static assets
│   └── assets/
│       └── techs/       # Technology icons
└── styles/              # Global styles
    └── globals.css      # CSS variables & utilities
```

---

## ⚙️ Configuration Guide

All site content is managed in `lib/config.js`:

### Personal Information
```javascript
personal: {
  name: "Your Name",
  username: "yourusername",
  email: "your@email.com",
  location: "Your City, Country",
  // ...
}
```

### Skills & Technologies
```javascript
skills: {
  frontend: [
    { name: "React.js", level: 95, icon: "react.svg" },
    // ...
  ],
  backend: [...],
  tools: [...]
}
```

### GitHub Integration
```javascript
githubUsername: "yourusername"  // Your GitHub username
```

### Themes
Customize theme colors in `themes` object:
```javascript
themes: {
  dark: {
    colors: { primary: "#3B82F6", ... },
    styles: { fontWeight: "normal", ... }
  },
  // ...
}
```

---

## 🎨 Theme Customization

Each theme has:
- **Colors**: Primary, secondary, accent, background, surface, text
- **Styles**: Font weights, shadows, glows, borders

Themes use CSS variables for real-time switching:
```css
var(--color-primary)
var(--color-secondary)
var(--style-glow)
var(--style-shadow)
```

---

## 📦 Build Output

```
Route (pages)                              Size     First Load JS
┌ ○ /                                      9.99 kB         138 kB
├ ○ /contact                               2.41 kB         127 kB
└ ○ /projects                              1.54 kB         129 kB
+ First Load JS shared by all              130 kB
  ├ chunks/framework.js                    45.2 kB
  ├ chunks/main.js                         31.8 kB
  └ chunks/pages/_app.js                   46.4 kB
```

---

## 🌐 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to [Vercel](https://vercel.com)
3. Deploy with one click

### Manual Deployment

```bash
npm run build
npm start
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project at [github.com/umutxyp/Personal-Website](https://github.com/umutxyp/Personal-Website)
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Umut Bayraktar**

- Website: [umutbayraktar.vercel.app](https://umutbayraktar.vercel.app)
- GitHub: [@umutxyp](https://github.com/umutxyp)
- Instagram: [@umutxyp](https://instagram.com/umutxyp)
- YouTube: [@umutxyp](https://youtube.com/umutxyp)
- Twitter: [@devbayraktar](https://twitter.com/devbayraktar)
- Discord: [Join Server](https://discord.gg/NrkMaPRc73)

---

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - React Framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS Framework
- [Three.js](https://threejs.org/) - 3D Graphics
- [Framer Motion](https://www.framer.com/motion/) - Animation Library
- [Vercel](https://vercel.com/) - Deployment Platform

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by Umut Bayraktar

</div>
