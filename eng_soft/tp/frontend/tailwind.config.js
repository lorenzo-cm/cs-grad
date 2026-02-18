/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      screens: {
        'xs': '475px', // Adding an extra small breakpoint
      },
    },
  },
  plugins: [
    require('tailwind-scrollbar-hide'),
  ],
}
