import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from 'framer-motion';
import { HiMenu, HiX, HiMail } from 'react-icons/hi';
import { FaFacebook, FaInstagram } from 'react-icons/fa';
import { siteConfig } from '../lib/config';

export default function Header() {
  const router = useRouter();
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Projects', path: '/projects' },
    { name: 'Contact', path: '/contact' },
  ];

  const socialIcons = {
    facebook: FaFacebook,
    instagram: FaInstagram,
    email: HiMail,
  };

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      style={{
        backgroundColor: isScrolled ? 'var(--color-surface)' : 'transparent',
        backdropFilter: isScrolled ? 'blur(12px)' : 'none',
        boxShadow: isScrolled ? 'var(--style-shadow)' : 'none',
      }}
      className="fixed top-0 left-0 right-0 z-40 transition-all duration-300"
    >
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link href="/">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center gap-2 cursor-pointer"
            >
              <div 
                className="w-8 h-8 sm:w-10 sm:h-10 rounded-full flex items-center justify-center text-white font-bold text-base sm:text-xl"
                style={{
                  background: `linear-gradient(135deg, var(--color-primary), var(--color-secondary))`,
                  boxShadow: 'var(--style-glow)',
                }}
              >
                PH
              </div>
              <span 
                className="text-base sm:text-xl font-bold bg-clip-text text-transparent hidden xs:inline"
                style={{
                  backgroundImage: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                  fontWeight: 'var(--style-headingWeight)',
                }}
              >
                Petr Havel
              </span>
            </motion.div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <Link key={item.path} href={item.path}>
                <motion.a
                  whileHover={{ y: -2 }}
                  style={{
                    color: router.pathname === item.path ? 'var(--color-primary)' : 'var(--color-text)',
                    fontWeight: router.pathname === item.path ? 'var(--style-headingWeight)' : 'var(--style-fontWeight)',
                  }}
                  className="text-sm transition-colors cursor-pointer relative"
                >
                  {item.name}
                  {router.pathname === item.path && (
                    <motion.div
                      layoutId="underline"
                      style={{
                        background: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                        boxShadow: 'var(--style-glow)',
                      }}
                      className="absolute -bottom-1 left-0 right-0 h-0.5"
                    />
                  )}
                </motion.a>
              </Link>
            ))}
          </div>

          {/* Social Icons (Desktop) */}
          <div className="hidden lg:flex items-center gap-2">
            {Object.entries(siteConfig.social).slice(0, 4).map(([platform, url]) => {
              const Icon = socialIcons[platform];
              if (!Icon || !url) return null;
              return (
                <motion.a
                  key={platform}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.1, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  style={{
                    color: 'var(--color-textSecondary)',
                  }}
                  className="p-2 rounded-lg transition-colors"
                  onMouseEnter={(e) => {
                    e.currentTarget.style.color = 'var(--color-primary)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.color = 'var(--color-textSecondary)';
                  }}
                >
                  <Icon className="w-5 h-5" />
                </motion.a>
              );
            })}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{ color: 'var(--color-text)' }}
            className="md:hidden p-2 rounded-lg transition-colors"
          >
            {mobileMenuOpen ? (
              <HiX className="w-6 h-6" />
            ) : (
              <HiMenu className="w-6 h-6" />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            style={{
              backgroundColor: 'var(--color-surface)',
              borderTop: 'var(--style-cardBorder)',
            }}
            className="md:hidden"
          >
            <div className="container mx-auto px-4 py-4 space-y-2">
              {navItems.map((item) => (
                <Link key={item.path} href={item.path}>
                  <a
                    onClick={() => setMobileMenuOpen(false)}
                    style={{
                      backgroundColor: router.pathname === item.path ? 'var(--color-primary)' : 'transparent',
                      color: router.pathname === item.path ? 'white' : 'var(--color-text)',
                      fontWeight: router.pathname === item.path ? 'var(--style-headingWeight)' : 'var(--style-fontWeight)',
                      opacity: router.pathname === item.path ? 1 : 0.9,
                    }}
                    className="block px-4 py-3 rounded-lg transition-all cursor-pointer"
                  >
                    {item.name}
                  </a>
                </Link>
              ))}
              
              {/* Mobile Social Icons */}
              <div 
                style={{ borderTop: 'var(--style-cardBorder)' }}
                className="flex items-center gap-3 px-4 pt-4"
              >
                {Object.entries(siteConfig.social).map(([platform, url]) => {
                  const Icon = socialIcons[platform];
                  if (!Icon || !url) return null;
                  return (
                    <a
                      key={platform}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: 'var(--color-textSecondary)' }}
                      className="p-2 rounded-lg transition-all"
                      onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-primary)'}
                      onMouseLeave={(e) => e.currentTarget.style.color = 'var(--color-textSecondary)'}
                    >
                      <Icon className="w-5 h-5" />
                    </a>
                  );
                })}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
}
