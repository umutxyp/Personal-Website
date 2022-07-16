const colors = require('tailwindcss/colors')
module.exports = {
  mode: 'jit',
  purge: ['./pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    fontFamily: {
      Poppins: ["Poppins", "sans-serif"]
    },
    extend: {
      colors: {
        ...colors
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}