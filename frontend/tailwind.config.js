/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#070a12",
        panel: "rgba(255,255,255,0.08)",
        mint: "#5ef3b3",
        amber: "#f9c74f",
        coral: "#ff6b6b",
        sky: "#7dd3fc"
      },
      boxShadow: {
        glow: "0 0 70px rgba(94, 243, 179, 0.22)"
      }
    }
  },
  plugins: []
};
