import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/generate_readme_from_repo': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/download_readme': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/auth': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/repos': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/logout': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/login': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    },
  },
});
