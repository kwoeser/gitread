import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const API_URL  = "https://gitread.onrender.com/"

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/generate_readme_from_repo': {
        target: API_URL,
        changeOrigin: true,
      },
      '/download_readme': {
        target: API_URL,
        changeOrigin: true,
      },
      '/auth': {
        target: API_URL,
        changeOrigin: true,
      },
      '/repos': {
        target: API_URL,
        changeOrigin: true,
      },
      '/logout': {
        target: API_URL,
        changeOrigin: true,
      },
      '/login': {
        target: API_URL,
        changeOrigin: true,
      }
    },
  },
});
