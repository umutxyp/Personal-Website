import { useTheme } from '../contexts/ThemeContext';
import { themes } from '../lib/config';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { HiColorSwatch } from 'react-icons/hi';

export default function ThemeSwitcher() {
  const { theme, changeTheme, availableThemes } = useTheme();
  const [isOpen, setIsOpen] = useState(false);

  const themeIcons = {
    dark: '🌙',
    light: '☀️',
    neon: '⚡',
    sunset: '🌅',
    forest: '🌲'
  };

  return (
    <div className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            className="absolute bottom-14 sm:bottom-16 right-0 bg-white dark:bg-gray-800 rounded-xl sm:rounded-2xl shadow-2xl p-2 sm:p-3 min-w-[180px] sm:min-w-[200px]"
          >
            <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2 px-2">
              Choose Theme
            </p>
            <div className="space-y-1">
              {availableThemes.map((themeName) => (
                <button
                  key={themeName}
                  onClick={() => {
                    changeTheme(themeName);
                    setIsOpen(false);
                  }}
                  className={`
                    w-full px-3 py-2 sm:px-4 sm:py-2.5 rounded-lg sm:rounded-xl text-left transition-all duration-200
                    flex items-center gap-2 sm:gap-3 text-xs sm:text-sm font-medium
                    ${
                      theme === themeName
                        ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                        : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }
                  `}
                >
                  <span className="text-lg sm:text-xl">{themeIcons[themeName]}</span>
                  <span className="capitalize">{themes[themeName].name}</span>
                  {theme === themeName && (
                    <motion.span
                      layoutId="activeTheme"
                      className="ml-auto text-xs"
                    >
                      ✓
                    </motion.span>
                  )}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Toggle Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 
                   shadow-lg shadow-blue-500/50 flex items-center justify-center
                   text-white text-xl sm:text-2xl hover:shadow-xl transition-shadow"
      >
        <HiColorSwatch />
      </motion.button>
    </div>
  );
}
