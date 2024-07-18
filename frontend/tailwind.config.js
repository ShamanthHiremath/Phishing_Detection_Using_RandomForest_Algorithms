/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neonGreen: '#39ff14',
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
}