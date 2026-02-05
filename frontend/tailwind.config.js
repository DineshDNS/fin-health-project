/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],

  theme: {
    extend: {
      /* ---------------------------------
         COLOR TOKENS (LOCKED)
      --------------------------------- */
      colors: {
        /* Sidebar gradient colors */
        sidebarStart: "#FC4E33",
        sidebarMid: "#EE3B53",
        sidebarEnd: "#E12871",

        /* App background gradient colors */
        appBgStart: "#FBE0DB",
        appBgMid1: "#FDCFDB",
        appBgMid2: "#F0C2B8",
        appBgEnd: "#F49AA7",

        /* Card surface colors */
        cardCream: "#FFF8EE",      // main cards
        cardBlush: "#FFE4E8",      // business context
        cardGlass: "rgba(255,255,255,0.25)", // insights
      },

      /* ---------------------------------
         BACKGROUND GRADIENT TOKENS
      --------------------------------- */
      backgroundImage: {
        "sidebar-gradient":
          "linear-gradient(180deg, #4e0202 0%, #930d1f 50%, #8b043a 100%)",

        "app-gradient":
          "linear-gradient(135deg, #f78fbf 0%, #f7d0d7 35%, #fcddc6 65%, #f17382 100%)",
      },

      /* ---------------------------------
         SHADOW TOKENS
      --------------------------------- */
      boxShadow: {
        cardHero: "0 18px 45px rgba(0,0,0,0.18)",
        cardSoft: "0 10px 24px rgba(0,0,0,0.10)",
        cardGlass: "0 25px 60px rgba(0,0,0,0.20)",
      },

      /* ---------------------------------
         ANIMATIONS (Tailwind way)
      --------------------------------- */
      keyframes: {
        "pulse-soft": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.85" },
        },
      },

      animation: {
        "pulse-soft": "pulse-soft 2s ease-in-out infinite",
      },
    },
  },

  plugins: [],
};
