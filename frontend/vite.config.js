import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // ADD THIS SECTION
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // Your Flask URL
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
