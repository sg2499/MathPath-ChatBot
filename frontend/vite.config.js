import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/mathpath-chatbot.js`,
        chunkFileNames: `assets/mathpath-chatbot-chunk.js`,
        assetFileNames: `assets/mathpath-chatbot.[ext]`
      }
    }
  },
  server: {
    host: "0.0.0.0",
    port: 5173
  }
});
