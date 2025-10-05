import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { siteConfig } from '../lib/config';
import { HiExternalLink, HiCode, HiX, HiStar } from 'react-icons/hi';
import { FaGithub } from 'react-icons/fa';

export default function ProjectsSection() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });
  const [selectedProject, setSelectedProject] = useState(null);
  const [filter, setFilter] = useState('all');
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  // GitHub repos'u çek
  useEffect(() => {
    fetch('/api/github-repos')
      .then(res => res.json())
      .then(data => {
        // GitHub'dan gelen projeleri formatla
        const formattedProjects = data.map(repo => ({
          id: repo.id,
          title: repo.name,
          description: repo.description || 'No description provided',
          image: repo.image, // GitHub OpenGraph image
          tags: [], // Sadece language kullanacağız, topics gösterme
          liveUrl: repo.homepage || null,
          githubUrl: repo.url,
          stars: repo.stars,
          forks: repo.forks,
          language: repo.language,
          updatedAt: repo.updatedAt,
        }));
        setProjects(formattedProjects);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch GitHub repos:', err);
        setLoading(false);
      });
  }, []);

  // Sadece programlama dillerini filtre olarak göster
  const allLanguages = ['all', ...new Set(projects.map(p => p.language).filter(Boolean))];

  // Filter projeleri dile göre
  const filteredProjects = filter === 'all' 
    ? projects 
    : projects.filter(p => p.language?.toLowerCase() === filter.toLowerCase());

  return (
    <section ref={ref} id="projects" className="py-20" style={{ backgroundColor: 'var(--color-surface)' }}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          className="text-center mb-16"
        >
          <h2 style={{ fontWeight: 'var(--style-headingWeight)' }} className="text-4xl md:text-5xl mb-4">
            <span 
              className="bg-clip-text text-transparent"
              style={{ backgroundImage: `linear-gradient(to right, var(--color-primary), var(--color-secondary))` }}
            >
              GitHub Projects {loading && '⏳'}
            </span>
          </h2>
          <p style={{ color: 'var(--color-textSecondary)' }} className="text-xl max-w-2xl mx-auto">
            {loading ? 'Loading from GitHub...' : `${projects.length} repositories sorted by ⭐ stars`}
          </p>
        </motion.div>

        {/* Filter Tags - Sadece Diller */}
        <div className="flex flex-wrap justify-center gap-2 sm:gap-3 mb-8 sm:mb-12">
          {allLanguages.map((lang) => (
            <motion.button
              key={lang}
              onClick={() => setFilter(lang)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              style={{
                background: filter === lang 
                  ? `linear-gradient(to right, var(--color-primary), var(--color-secondary))`
                  : 'var(--color-surface)',
                color: filter === lang ? 'white' : 'var(--color-text)',
                boxShadow: filter === lang ? 'var(--style-glow)' : 'var(--style-shadow)',
                border: filter === lang ? 'none' : 'var(--style-cardBorder)',
                fontWeight: filter === lang ? 'var(--style-headingWeight)' : 'var(--style-fontWeight)',
              }}
              className="px-3 py-1.5 sm:px-4 sm:py-2 rounded-full text-xs sm:text-sm transition-all"
            >
              {lang === 'all' ? '🌐 All' : `💻 ${lang}`}
            </motion.button>
          ))}
        </div>

        {/* Projects Grid */}
        <motion.div
          layout
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          <AnimatePresence>
            {filteredProjects.map((project, index) => (
              <motion.div
                key={project.id}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
                onClick={() => setSelectedProject(project)}
                className="group relative cursor-pointer"
              >
                <div 
                  style={{
                    backgroundColor: 'var(--color-background)',
                    boxShadow: 'var(--style-shadow)',
                    border: 'var(--style-cardBorder)',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--style-glow)'}
                  onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'var(--style-shadow)'}
                  className="relative h-64 rounded-2xl overflow-hidden transition-all"
                >
                  {/* GitHub OpenGraph Image */}
                  {project.image && (
                    <img 
                      src={project.image} 
                      alt={project.title}
                      className="absolute inset-0 w-full h-full object-cover"
                      onError={(e) => {
                        // Fallback gradient if image fails
                        e.target.style.display = 'none';
                      }}
                    />
                  )}
                  
                  {/* Fallback gradient if no image */}
                  {!project.image && (
                    <div 
                      className="absolute inset-0"
                      style={{
                        background: `linear-gradient(135deg, var(--color-primary), var(--color-secondary))`,
                      }}
                    />
                  )}
                  
                  {/* Star Count Badge */}
                  <div 
                    className="absolute top-4 left-4 z-10 px-3 py-1 text-white rounded-full text-xs font-bold flex items-center gap-1"
                    style={{ 
                      backgroundColor: 'rgba(0, 0, 0, 0.7)',
                      backdropFilter: 'blur(8px)',
                      fontWeight: 'var(--style-headingWeight)',
                    }}
                  >
                    <HiStar className="text-yellow-400" /> {project.stars || 0}
                  </div>

                  {/* Language Badge */}
                  {project.language && (
                    <div 
                      className="absolute top-4 right-4 z-10 px-3 py-1 text-white rounded-full text-xs"
                      style={{ 
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        backdropFilter: 'blur(8px)',
                        fontWeight: 'var(--style-headingWeight)',
                      }}
                    >
                      {project.language}
                    </div>
                  )}

                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
                    <div className="text-white">
                      <p className="text-sm mb-2">Click to view details</p>
                      <div className="flex gap-2">
                        {project.liveUrl && (
                          <span className="flex items-center gap-1 text-xs">
                            <HiExternalLink /> Live Demo
                          </span>
                        )}
                        {project.githubUrl && (
                          <span className="flex items-center gap-1 text-xs">
                            <FaGithub /> {project.forks || 0} Forks
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Card Content */}
                <div className="mt-3 sm:mt-4">
                  <h3 
                    style={{ 
                      color: 'var(--color-text)',
                      fontWeight: 'var(--style-headingWeight)',
                    }}
                    className="text-lg sm:text-xl mb-2"
                  >
                    {project.title}
                  </h3>
                  <p 
                    style={{ color: 'var(--color-textSecondary)' }}
                    className="text-xs sm:text-sm mb-2 sm:mb-3 line-clamp-2"
                  >
                    {project.description}
                  </p>

                  {/* Sadece forks sayısını göster */}
                  <div className="flex items-center gap-3 text-xs">
                    {project.forks > 0 && (
                      <span 
                        style={{ color: 'var(--color-textSecondary)' }}
                        className="flex items-center gap-1"
                      >
                        <FaGithub /> {project.forks} forks
                      </span>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      </div>

      {/* Project Detail Modal */}
      <AnimatePresence>
        {selectedProject && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedProject(null)}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          >
            <motion.div
              initial={{ scale: 0.9, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 50 }}
              onClick={(e) => e.stopPropagation()}
              className="rounded-xl sm:rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl"
              style={{ backgroundColor: 'var(--color-surface)' }}
            >
              <button
                onClick={() => setSelectedProject(null)}
                style={{ 
                  backgroundColor: 'var(--color-surface)',
                  color: 'var(--color-text)',
                }}
                className="absolute top-4 right-4 p-2 rounded-full transition-all z-10"
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--color-primary)'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--color-surface)'}
              >
                <HiX className="w-6 h-6" />
              </button>

              {/* Project Image */}
              {selectedProject.image && (
                <div className="w-full h-48 sm:h-64 overflow-hidden rounded-t-xl sm:rounded-t-2xl">
                  <img 
                    src={selectedProject.image} 
                    alt={selectedProject.title}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}

              <div className="p-4 sm:p-6 lg:p-8">
                <div className="flex items-start justify-between gap-2 sm:gap-4 mb-3 sm:mb-4">
                  <h2 
                    style={{ 
                      color: 'var(--color-text)',
                      fontWeight: 'var(--style-headingWeight)',
                    }}
                    className="text-xl sm:text-2xl lg:text-3xl"
                  >
                    {selectedProject.title}
                  </h2>
                  
                  {/* Star & Language */}
                  <div className="flex gap-2">
                    <span 
                      className="flex items-center gap-1 px-3 py-1 rounded-full text-sm"
                      style={{
                        backgroundColor: 'var(--color-background)',
                        color: 'var(--color-text)',
                        fontWeight: 'var(--style-headingWeight)',
                      }}
                    >
                      <HiStar className="text-yellow-400" /> {selectedProject.stars || 0}
                    </span>
                    {selectedProject.language && (
                      <span 
                        className="px-3 py-1 rounded-full text-sm"
                        style={{
                          backgroundColor: 'var(--color-primary)',
                          color: 'white',
                        }}
                      >
                        {selectedProject.language}
                      </span>
                    )}
                  </div>
                </div>

                <p 
                  style={{ color: 'var(--color-textSecondary)' }}
                  className="mb-6 leading-relaxed"
                >
                  {selectedProject.description}
                </p>

                {/* Stats */}
                {(selectedProject.stars > 0 || selectedProject.forks > 0) && (
                  <div className="grid grid-cols-2 gap-3 sm:gap-4 mb-4 sm:mb-6">
                    <div 
                      className="text-center p-3 sm:p-4 rounded-xl"
                      style={{
                        backgroundColor: 'var(--color-background)',
                        border: 'var(--style-cardBorder)',
                      }}
                    >
                      <div 
                        style={{ 
                          color: 'var(--color-primary)',
                          fontWeight: 'var(--style-headingWeight)',
                        }}
                        className="text-2xl"
                      >
                        ⭐ {selectedProject.stars || 0}
                      </div>
                      <div style={{ color: 'var(--color-textSecondary)' }} className="text-sm">
                        Stars
                      </div>
                    </div>
                    <div 
                      className="text-center p-4 rounded-xl"
                      style={{
                        backgroundColor: 'var(--color-background)',
                        border: 'var(--style-cardBorder)',
                      }}
                    >
                      <div 
                        style={{ 
                          color: 'var(--color-primary)',
                          fontWeight: 'var(--style-headingWeight)',
                        }}
                        className="text-2xl"
                      >
                        🔱 {selectedProject.forks || 0}
                      </div>
                      <div style={{ color: 'var(--color-textSecondary)' }} className="text-sm">
                        Forks
                      </div>
                    </div>
                  </div>
                )}

                {/* Links */}
                <div className="flex gap-4">
                  {selectedProject.liveUrl && (
                    <a
                      href={selectedProject.liveUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        background: `linear-gradient(to right, var(--color-primary), var(--color-secondary))`,
                        fontWeight: 'var(--style-headingWeight)',
                      }}
                      className="flex-1 px-6 py-3 text-white rounded-xl flex items-center justify-center gap-2 transition-all"
                      onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--style-glow)'}
                      onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
                    >
                      <HiExternalLink className="w-5 h-5" />
                      Live Demo
                    </a>
                  )}
                  {selectedProject.githubUrl && (
                    <a
                      href={selectedProject.githubUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        backgroundColor: 'var(--color-background)',
                        color: 'var(--color-text)',
                        border: 'var(--style-cardBorder)',
                        fontWeight: 'var(--style-headingWeight)',
                      }}
                      className="flex-1 px-6 py-3 rounded-xl flex items-center justify-center gap-2 transition-all"
                      onMouseEnter={(e) => {
                        e.currentTarget.style.backgroundColor = 'var(--color-primary)';
                        e.currentTarget.style.color = 'white';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.backgroundColor = 'var(--color-background)';
                        e.currentTarget.style.color = 'var(--color-text)';
                      }}
                    >
                      <FaGithub className="w-5 h-5" />
                      View Code
                    </a>
                  )}
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
