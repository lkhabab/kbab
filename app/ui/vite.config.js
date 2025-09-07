// app/ui/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/static/agri3d/',          // مهم جداً
  build: {
    outDir: '../static/agri3d',     // يطلّع الناتج مباشرة داخل Flask static
    emptyOutDir: true,
    assetsDir: 'assets'
  },
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/auth': 'http://127.0.0.1:5000',
      '/api':  'http://127.0.0.1:5000'
    }
  }
})
