/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#FAFAF9',
        ink: '#1C1F26',
        slate: '#5B6472',
        line: '#E4E2DC',
        signal: '#1F5F4A',
        'signal-dim': '#EAF1EE',
        amber: '#C08A2E',
        'amber-dim': '#FBF3E3',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Inter', 'sans-serif'],
        mono: ['"SF Mono"', '"Roboto Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
