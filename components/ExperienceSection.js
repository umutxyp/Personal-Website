import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { siteConfig } from '../lib/config';

export default function ExperienceSection() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section ref={ref} className="py-20" style={{ backgroundColor: 'var(--color-background)' }}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          className="text-center mb-16"
        >
          <h2 
            style={{ fontWeight: 'var(--style-headingWeight)' }}
            className="text-4xl md:text-5xl mb-4"
          >
            <span 
              className="bg-clip-text text-transparent"
              style={{
                backgroundImage: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
              }}
            >
              Experience
            </span>
          </h2>
          <p 
            style={{ color: 'var(--color-textSecondary)' }}
            className="text-xl max-w-2xl mx-auto"
          >
            My journey in tech and community building
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto">
          {siteConfig.experience.map((exp, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ delay: index * 0.2 }}
              className="relative mb-12 last:mb-0"
            >
              {/* Timeline Line */}
              {index !== siteConfig.experience.length - 1 && (
                <div 
                  className="absolute left-6 sm:left-8 top-16 sm:top-20 w-0.5 h-full -z-10"
                  style={{
                    background: `linear-gradient(to bottom, var(--color-primary), var(--color-secondary))`,
                  }}
                />
              )}

              <div className="flex gap-3 sm:gap-6">
                {/* Icon */}
                <motion.div
                  whileHover={{ scale: 1.1, rotate: 360 }}
                  transition={{ duration: 0.5 }}
                  style={{
                    background: `linear-gradient(135deg, var(--color-primary), var(--color-secondary))`,
                    boxShadow: 'var(--style-glow)',
                  }}
                  className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 rounded-full flex items-center justify-center text-2xl sm:text-3xl"
                >
                  {exp.icon}
                </motion.div>

                {/* Content */}
                <motion.div
                  whileHover={{ scale: 1.02, x: 10 }}
                  style={{
                    backgroundColor: 'var(--color-surface)',
                    border: 'var(--style-cardBorder)',
                    boxShadow: 'var(--style-shadow)',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--style-glow)'}
                  onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'var(--style-shadow)'}
                  className="flex-1 p-4 sm:p-6 rounded-2xl transition-all"
                >
                  <div className="flex flex-wrap items-start justify-between gap-2 sm:gap-4 mb-3">
                    <h3 
                      style={{ 
                        color: 'var(--color-text)',
                        fontWeight: 'var(--style-headingWeight)',
                      }}
                      className="text-lg sm:text-2xl"
                    >
                      {exp.title}
                    </h3>
                    <span 
                      style={{
                        backgroundColor: 'var(--color-primary)',
                        color: 'white',
                        fontWeight: 'var(--style-headingWeight)',
                        opacity: 0.9,
                      }}
                      className="px-3 py-1 sm:px-4 rounded-full text-xs sm:text-sm"
                    >
                      {exp.duration}
                    </span>
                  </div>
                  <p 
                    style={{ color: 'var(--color-textSecondary)' }}
                    className="leading-relaxed text-sm sm:text-base"
                  >
                    {exp.description}
                  </p>
                </motion.div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Goals Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.6 }}
          className="mt-20 max-w-4xl mx-auto"
        >
          <h3 
            style={{
              color: 'var(--color-text)',
              fontWeight: 'var(--style-headingWeight)',
            }}
            className="text-2xl sm:text-3xl text-center mb-6 sm:mb-8"
          >
            🎯 Goals & Vision
          </h3>
          <div className="grid sm:grid-cols-2 gap-3 sm:gap-4">
            {siteConfig.goals.map((goal, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={inView ? { opacity: 1, scale: 1 } : {}}
                transition={{ delay: 0.7 + index * 0.1 }}
                whileHover={{ scale: 1.05, y: -5 }}
                style={{
                  backgroundColor: 'var(--color-surface)',
                  border: 'var(--style-cardBorder)',
                  boxShadow: 'var(--style-shadow)',
                }}
                className="p-3 sm:p-4 rounded-xl"
              >
                <p 
                  style={{ color: 'var(--color-text)' }}
                  className="flex items-start gap-2 sm:gap-3 text-sm sm:text-base"
                >
                  <span style={{ color: 'var(--color-primary)', fontWeight: 'var(--style-headingWeight)' }}>•</span>
                  {goal}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
