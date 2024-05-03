/** @type {import('tailwindcss').Config} */
export default {
    content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      maxHeight: {
        fitted: "calc(100vh - 80px)"
      },
      height: {
        chat: "calc(100vh - 100px)"
      }
    },
  },
  plugins: [],
}

