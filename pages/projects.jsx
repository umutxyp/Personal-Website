import { motion } from 'framer-motion';
import ProjectsSection from '../components/ProjectsSection';

export default function Projects() {
  return (
    <div className="pt-20">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          background: `linear-gradient(135deg, var(--color-primary), var(--color-secondary))`,
          boxShadow: 'var(--style-shadow)',
        }}
        className="py-8 sm:py-10 lg:py-12 text-white"
      >
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 
            style={{ 
              fontWeight: 'var(--style-headingWeight)',
              textShadow: 'var(--style-glow)',
            }}
            className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl mb-3 sm:mb-4"
          >
            My Projects
          </h1>
          <p className="text-base sm:text-lg lg:text-xl opacity-90 max-w-2xl mx-auto">
            Explore my portfolio of web applications, tools, and creative projects
          </p>
        </div>
      </motion.div>
      
      <ProjectsSection />
    </div>
  );
}
