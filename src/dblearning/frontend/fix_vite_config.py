content = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
    watch: {
      usePolling: true,
      interval: 300,
    },
  }
})
"""
with open("D:/DemoCN2026/dblearning/frontend/vite.config.js", "w", encoding="utf-8") as f:
    f.write(content)
print("vite.config.js updated with usePolling")
