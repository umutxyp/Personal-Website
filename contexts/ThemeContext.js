import { createContext, useContext, useEffect, useState } from 'react';
import { themes } from '../lib/config';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [currentTheme, setCurrentTheme] = useState('dark');
  const [mounted, setMounted] = useState(false);

  // Tema yükleme (localStorage'dan)
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setCurrentTheme(savedTheme);
    setMounted(true);
  }, []);

  // Tema değişikliğinde localStorage'a kaydet
  useEffect(() => {
    if (mounted) {
      localStorage.setItem('theme', currentTheme);
      applyTheme(currentTheme);
    }
  }, [currentTheme, mounted]);

  const applyTheme = (themeName) => {
    const theme = themes[themeName];
    if (!theme) return;

    const root = document.documentElement;
    
    // CSS değişkenlerini root'a uygula (renkler)
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value);
    });

    // CSS değişkenlerini root'a uygula (stiller)
    if (theme.styles) {
      Object.entries(theme.styles).forEach(([key, value]) => {
        root.style.setProperty(`--style-${key}`, value);
      });
    }

    // Body background ve text renklerini direkt uygula
    document.body.style.backgroundColor = theme.colors.background;
    document.body.style.color = theme.colors.text;
    document.body.style.fontWeight = theme.styles?.fontWeight || 'normal';

    // Dark mode class'ı ekle/çıkar
    if (themeName === 'dark' || themeName === 'neon' || themeName === 'sunset' || themeName === 'forest') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  };

  const changeTheme = (themeName) => {
    if (themes[themeName]) {
      setCurrentTheme(themeName);
    }
  };

  // Prevent flash of wrong theme
  if (!mounted) {
    return null;
  }

  return (
    <ThemeContext.Provider
      value={{
        theme: currentTheme,
        themeColors: themes[currentTheme]?.colors,
        availableThemes: Object.keys(themes),
        changeTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
