import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { siteConfig } from '../lib/config';
import { HiMail } from 'react-icons/hi';
import { 
  FaFacebook, FaInstagram, FaYoutube, FaGithub, 
  FaTelegram, FaTwitter, FaLinkedin 
} from 'react-icons/fa';

export default function ContactSection() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const socialIcons = {
    facebook: FaFacebook,
    instagram: FaInstagram,
    youtube: FaYoutube,
    github: FaGithub,
    telegram: FaTelegram,
    twitter: FaTwitter,
    linkedin: FaLinkedin,
  };

  return (
    <section ref={ref} id="contact" className="py-20" style={{ backgroundColor: 'var(--color-background)' }}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Email Info Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.2 }}
            style={{
              background: `linear-gradient(135deg, var(--color-primary), var(--color-secondary))`,
              boxShadow: 'var(--style-glow)',
            }}
            className="p-6 sm:p-8 lg:p-10 rounded-2xl text-white mb-8 text-center"
          >
            <h3 
              style={{ fontWeight: 'var(--style-headingWeight)' }}
              className="text-2xl sm:text-3xl lg:text-4xl mb-4"
            >
              Let's Connect!
            </h3>
            <p className="mb-6 opacity-90 text-base sm:text-lg">
              I'm always open to discussing new projects, creative ideas, or opportunities.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8">
              <div className="flex items-center gap-3">
                <HiMail className="w-6 h-6 sm:w-7 sm:h-7" />
                <a href={`mailto:${siteConfig.personal.email}`} className="hover:underline text-lg sm:text-xl font-medium">
                  {siteConfig.personal.email}
                </a>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-2xl sm:text-3xl">📍</span>
                <span className="text-lg sm:text-xl">{siteConfig.personal.location}</span>
              </div>
            </div>
          </motion.div>

          {/* Social Media Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.4 }}
          >
            <h3 
              style={{ 
                color: 'var(--color-text)',
                fontWeight: 'var(--style-headingWeight)',
              }}
              className="text-2xl sm:text-3xl mb-6 text-center"
            >
              Follow Me On Social Media
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
              {Object.entries(siteConfig.social).map(([platform, url]) => {
                const Icon = socialIcons[platform];
                if (!Icon || !url) return null;
                return (
                  <motion.a
                    key={platform}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.05, y: -5 }}
                    whileTap={{ scale: 0.95 }}
                    style={{
                      backgroundColor: 'var(--color-surface)',
                      border: 'var(--style-cardBorder)',
                      boxShadow: 'var(--style-shadow)',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = `linear-gradient(135deg, var(--color-primary), var(--color-secondary))`;
                      e.currentTarget.style.color = 'white';
                      e.currentTarget.style.boxShadow = 'var(--style-glow)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'var(--color-surface)';
                      e.currentTarget.style.color = 'var(--color-text)';
                      e.currentTarget.style.boxShadow = 'var(--style-shadow)';
                    }}
                    className="flex flex-col items-center gap-3 sm:gap-4 p-6 sm:p-8 rounded-2xl transition-all"
                  >
                    <Icon 
                      style={{ color: 'inherit' }}
                      className="w-10 h-10 sm:w-12 sm:h-12 transition-colors" 
                    />
                    <span 
                      style={{ color: 'inherit', fontWeight: 'var(--style-headingWeight)' }}
                      className="text-sm sm:text-base capitalize"
                    >
                      {platform}
                    </span>
                  </motion.a>
                );
              })}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
