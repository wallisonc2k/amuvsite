/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/src/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Montserrat', 'sans-serif'],
      },
      colors: {
        'amuv-red': {
          100: '#FFECEE',
          200: '#FAD2D5',
          300: '#E98E95',
          400: '#E15B67',
          500: '#D82836',
          600: '#C41E2B',
          700: '#A2131F',
          800: '#7F0F19',
          900: '#5A0A12',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        float: 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
}
