import '../styles/globals.css';
import Head from 'next/head';
import { ThemeProvider } from '../contexts/ThemeContext';
import { AnimatePresence, motion } from 'framer-motion';
import { useRouter } from 'next/router';
import { siteConfig } from '../lib/config';
import ThemeSwitcher from '../components/ThemeSwitcher';
import NewHeader from '../components/NewHeader';

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  return (
    <>
      <Head>
        <title>{siteConfig.seo.title}</title>
        <meta name="description" content={siteConfig.seo.description} />
        <meta name="keywords" content={siteConfig.seo.keywords} />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        
        {/* Open Graph */}
        <meta property="og:title" content={siteConfig.seo.title} />
        <meta property="og:description" content={siteConfig.seo.description} />
        <meta property="og:image" content={siteConfig.seo.ogImage} />
        <meta property="og:type" content="website" />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content={siteConfig.seo.twitterHandle} />
        <meta name="twitter:title" content={siteConfig.seo.title} />
        <meta name="twitter:description" content={siteConfig.seo.description} />
        <meta name="twitter:image" content={siteConfig.seo.ogImage} />
        
        <link rel="icon" href={siteConfig.personal.avatar} />
        
        {/* Fonts */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </Head>

      <ThemeProvider>
        <div className="min-h-screen transition-colors duration-300">
          <NewHeader />
          
          <AnimatePresence mode="wait">
            <motion.div
              key={router.pathname}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Component {...pageProps} />
            </motion.div>
          </AnimatePresence>

          {/* Footer */}
          <footer 
            style={{ 
              backgroundColor: 'var(--color-background)',
              borderTop: 'var(--style-cardBorder)',
            }}
            className="transition-all duration-300"
          >
            <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10 lg:py-12">
              <div className="flex flex-col md:flex-row items-center justify-between gap-4 sm:gap-6">
                <div className="text-center md:text-left">
                  <p 
                    style={{ color: 'var(--color-text)' }}
                    className="flex items-center gap-2 justify-center md:justify-start text-sm sm:text-base"
                  >
                    <span>Made with</span>
                    <span 
                      className="animate-pulse"
                      style={{ color: 'var(--color-accent)' }}
                    >
                      ❤️
                    </span>
                    <span>by umutxyp</span>
                  </p>
                  <p 
                    style={{ color: 'var(--color-textSecondary)' }}
                    className="text-xs sm:text-sm mt-1 sm:mt-2"
                  >
                    © {new Date().getFullYear()} All rights reserved.
                  </p>
                </div>

                <div className="flex items-center gap-3 sm:gap-4">
                  <a
                    href={siteConfig.social.discordServer || '#'}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      background: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                      fontWeight: 'var(--style-headingWeight)',
                    }}
                    className="px-4 py-2 sm:px-6 sm:py-3 text-white rounded-lg transition-all flex items-center gap-2 text-sm sm:text-base"
                    onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--style-glow)'}
                    onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
                  >
                    <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515a.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0a12.64 12.64 0 0 0-.617-1.25a.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057a19.9 19.9 0 0 0 5.993 3.03a.078.078 0 0 0 .084-.028a14.09 14.09 0 0 0 1.226-1.994a.076.076 0 0 0-.041-.106a13.107 13.107 0 0 1-1.872-.892a.077.077 0 0 1-.008-.128a10.2 10.2 0 0 0 .372-.292a.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127a12.299 12.299 0 0 1-1.873.892a.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028a19.839 19.839 0 0 0 6.002-3.03a.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.956-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.955-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.946 2.418-2.157 2.418z"/>
                    </svg>
                    <span className="hidden xs:inline">Join Discord</span>
                    <span className="xs:hidden">Discord</span>
                  </a>
                </div>
              </div>
            </div>
          </footer>

          {/* Theme Switcher */}
          <ThemeSwitcher />
        </div>
      </ThemeProvider>
    </>
  );
}

export default MyApp;
