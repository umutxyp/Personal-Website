import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { siteConfig } from '../lib/config';
import { useState } from 'react';

export default function SkillsSection() {
  const [activeCategory, setActiveCategory] = useState('frontend');
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const categories = [
    { id: 'frontend', label: 'Frontend', icon: '🎨' },
    { id: 'backend', label: 'Backend', icon: '⚙️' },
    { id: 'tools', label: 'Tools', icon: '🛠️' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <section ref={ref} id="skills" className="py-20" style={{ backgroundColor: 'var(--color-surface)' }}>
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
              Skills & Technologies
            </span>
          </h2>
          <p 
            style={{ color: 'var(--color-textSecondary)' }}
            className="text-xl max-w-2xl mx-auto"
          >
            Here are the technologies and tools I work with
          </p>
        </motion.div>

        {/* Category Tabs */}
        <div className="flex justify-center gap-2 sm:gap-4 mb-12 flex-wrap">
          {categories.map((category) => (
            <motion.button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              style={{
                background: activeCategory === category.id 
                  ? `linear-gradient(to right, var(--color-primary), var(--color-secondary))`
                  : 'var(--color-surface)',
                color: activeCategory === category.id ? 'white' : 'var(--color-text)',
                boxShadow: activeCategory === category.id ? 'var(--style-glow)' : 'var(--style-shadow)',
                border: activeCategory === category.id ? 'none' : 'var(--style-cardBorder)',
                fontWeight: activeCategory === category.id ? 'var(--style-headingWeight)' : 'var(--style-fontWeight)',
              }}
              className="px-4 py-2 sm:px-6 sm:py-3 rounded-full transition-all text-sm sm:text-base"
            >
              <span className="mr-1 sm:mr-2">{category.icon}</span>
              {category.label}
            </motion.button>
          ))}
        </div>

        {/* Skills Grid */}
        <motion.div
          key={activeCategory}
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          {siteConfig.skills[activeCategory]?.map((skill, index) => (
            <motion.div
              key={skill.name}
              variants={itemVariants}
              whileHover={{ y: -5, scale: 1.02 }}
              style={{ 
                background: 'var(--color-background)',
                border: 'var(--style-cardBorder)',
                boxShadow: 'var(--style-shadow)',
              }}
              onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--style-glow)'}
              onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'var(--style-shadow)'}
              className="p-6 rounded-2xl transition-all"
            >
              <div className="flex items-center gap-4 mb-4">
                <div 
                  className="w-12 h-12 rounded-lg p-2 flex items-center justify-center"
                  style={{
                    backgroundColor: 'var(--color-surface)',
                    boxShadow: 'var(--style-shadow)',
                  }}
                >
                  <img
                    src={`/assets/techs/${skill.icon}`}
                    alt={skill.name}
                    className="w-full h-full object-contain"
                  />
                </div>
                <div className="flex-1">
                  <h3 
                    style={{ 
                      color: 'var(--color-text)',
                      fontWeight: 'var(--style-headingWeight)',
                    }}
                    className="text-sm"
                  >
                    {skill.name}
                  </h3>
                  <p 
                    style={{ color: 'var(--color-textSecondary)' }}
                    className="text-sm"
                  >
                    {skill.level}% Proficiency
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div 
                className="relative h-2 rounded-full overflow-hidden"
                style={{ backgroundColor: 'var(--color-surface)' }}
              >
                <motion.div
                  initial={{ width: 0 }}
                  animate={inView ? { width: `${skill.level}%` } : {}}
                  transition={{ duration: 1, delay: index * 0.1 }}
                  style={{
                    background: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                  }}
                  className="absolute inset-y-0 left-0 rounded-full"
                />
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
