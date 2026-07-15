/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./article-sopk-keto.html'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Playfair Display Variable"', 'serif'],
        serif: ['"Cormorant Variable"', 'serif'],
        sans: ['"Outfit Variable"', 'sans-serif'],
        mono: ['"JetBrains Mono Variable"', 'monospace'],
      },
      colors: {
        cream: 'rgb(var(--color-bg-primary-rgb) / <alpha-value>)',
        sand: 'rgb(var(--color-bg-secondary-rgb) / <alpha-value>)',
        ink: 'rgb(var(--color-text-primary-rgb) / <alpha-value>)',
        body: 'rgb(var(--color-text-body-rgb) / <alpha-value>)',
        muted: 'rgb(var(--color-text-muted-rgb) / <alpha-value>)',
        gold: 'rgb(var(--color-accent-primary-rgb) / <alpha-value>)',
        caramel: 'rgb(var(--color-accent-secondary-rgb) / <alpha-value>)',
        sage: 'rgb(var(--color-accent-health-rgb) / <alpha-value>)',
        rose: 'rgb(var(--color-accent-beauty-rgb) / <alpha-value>)',
        mist: 'rgb(var(--color-accent-wellness-rgb) / <alpha-value>)',
      },
      boxShadow: {
        card: 'var(--shadow-card)',
        hover: 'var(--shadow-card-hover)',
        elevated: 'var(--shadow-elevated)',
      },
    },
  },
  plugins: [],
};
