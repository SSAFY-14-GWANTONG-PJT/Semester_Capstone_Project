import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '0.0.0.0',   // 도커 외부에서 접속 가능하게 함
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Django 서버 주소
        changeOrigin: true,
      }
    },
    watch: {
      usePolling: true // 파일 변경 감지 방식을 '폴링'으로 변경 (도커 필수 설정!)
    }
  }
})
