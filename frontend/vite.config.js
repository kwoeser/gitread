import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
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
    },
  },
});