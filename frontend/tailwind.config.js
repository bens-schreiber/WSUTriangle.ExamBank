/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        "bg-primary": "#282c34",
        "bg-secondary": "#2f333d",
        "bg-tertiary": "#21252a",
        "bg-accent": "#696d76",
      }
    }
  },
  plugins: []
};