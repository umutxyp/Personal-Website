import { motion } from 'framer-motion';
import { TypeAnimation } from 'react-type-animation';
import { siteConfig } from '../lib/config';
import { HiDownload, HiArrowDown } from 'react-icons/hi';
import dynamic from 'next/dynamic';

const Scene3D = dynamic(() => import('./3d/Scene3D'), {
  ssr: false,
  loading: () => (
    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 animate-pulse" />
  ),
});

export default function HeroSection() {
  const scrollToNext = () => {
    window.scrollTo({
      top: window.innerHeight,
      behavior: 'smooth'
    });
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* 3D Background */}
      <div className="absolute inset-0 z-0 opacity-40">
        <Scene3D />
      </div>

      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-white/5 dark:via-black/5 to-white dark:to-black z-0" />

      {/* Content */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 z-10 pt-20">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-12">
          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="flex-1 text-center lg:text-left"
          >
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-lg md:text-xl font-medium text-blue-600 dark:text-blue-400 mb-4"
            >
              👋 Welcome to my portfolio
            </motion.p>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              style={{ fontWeight: 'var(--style-headingWeight)' }}
              className="text-4xl md:text-6xl lg:text-7xl mb-6"
            >
              <span 
                className="bg-clip-text text-transparent"
                style={{
                  backgroundImage: `linear-gradient(to right, var(--color-primary), var(--color-secondary), var(--color-accent))`,
                  textShadow: 'var(--style-glow)',
                }}
              >
                {siteConfig.personal.name}
              </span>
            </motion.h1>

            <div 
              style={{ 
                color: 'var(--color-text)',
                fontWeight: 'var(--style-headingWeight)',
              }}
              className="text-2xl md:text-3xl lg:text-4xl mb-6 h-20"
            >
              <TypeAnimation
                sequence={[
                  'Full-Stack Developer',
                  2000,
                  'Content Creator',
                  2000,
                  'Community Manager',
                  2000,
                  'Tech Enthusiast',
                  2000,
                ]}
                wrapper="span"
                speed={50}
                repeat={Infinity}
              />
            </div>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              style={{ color: 'var(--color-textSecondary)' }}
              className="text-lg md:text-xl mb-8 max-w-2xl mx-auto lg:mx-0"
              dangerouslySetInnerHTML={{ __html: siteConfig.about.intro }}
            />

            {/* Highlights */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="grid grid-cols-2 gap-4 mb-8 max-w-lg mx-auto lg:mx-0"
            >
              {siteConfig.about.highlights.map((highlight, index) => (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.05, y: -5 }}
                  style={{
                    backgroundColor: 'var(--color-surface)',
                    border: 'var(--style-cardBorder)',
                    boxShadow: 'var(--style-shadow)',
                    color: 'var(--color-text)',
                  }}
                  className="p-3 rounded-xl backdrop-blur-sm text-sm md:text-base"
                >
                  {highlight}
                </motion.div>
              ))}
            </motion.div>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              className="flex flex-wrap gap-4 justify-center lg:justify-start"
            >
              <motion.a
                href="#projects"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                style={{
                  background: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                  boxShadow: 'var(--style-shadow)',
                  fontWeight: 'var(--style-headingWeight)',
                }}
                onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--style-glow)'}
                onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'var(--style-shadow)'}
                className="px-6 py-3 sm:px-8 sm:py-4 text-white rounded-full transition-all text-sm sm:text-base"
              >
                View My Work
              </motion.a>

              {siteConfig.personal.resumeUrl && (
                <motion.a
                  href={siteConfig.personal.resumeUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  style={{
                    backgroundColor: 'var(--color-surface)',
                    color: 'var(--color-text)',
                    border: 'var(--style-cardBorder)',
                    boxShadow: 'var(--style-shadow)',
                    fontWeight: 'var(--style-headingWeight)',
                  }}
                  className="px-6 py-3 sm:px-8 sm:py-4 rounded-full transition-all flex items-center gap-2 text-sm sm:text-base"
                >
                  <HiDownload className="w-5 h-5" />
                  Download CV
                </motion.a>
              )}
            </motion.div>
          </motion.div>

          {/* Avatar */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="relative"
          >
            <motion.div
              animate={{
                scale: [1, 1.05, 1],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="relative w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96"
            >
              {/* Glow Effect */}
              <div 
                className="absolute inset-0 rounded-full opacity-20 blur-3xl animate-pulse"
                style={{
                  background: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                }}
              />
              
              {/* Avatar Image */}
              <div 
                className="relative w-full h-full rounded-full overflow-hidden border-4 shadow-2xl"
                style={{
                  borderColor: 'var(--color-surface)',
                  boxShadow: 'var(--style-glow)',
                }}
              >
                <img
                  src={siteConfig.personal.avatar}
                  alt={siteConfig.personal.name}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Animated Ring */}
              <div 
                className="absolute inset-0 rounded-full border-4 animate-spin-slow"
                style={{ borderColor: 'var(--color-primary)', opacity: 0.3 }}
              />
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Scroll Down Indicator */}
      <motion.button
        onClick={scrollToNext}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          style={{ color: 'var(--color-textSecondary)' }}
          onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-primary)'}
          onMouseLeave={(e) => e.currentTarget.style.color = 'var(--color-textSecondary)'}
          className="flex flex-col items-center gap-2 transition-colors"
        >
          <span className="text-sm font-medium">Scroll Down</span>
          <HiArrowDown className="w-6 h-6" />
        </motion.div>
      </motion.button>
    </section>
  );
}
