
import { createApp } from 'vue'
import { createPinia } from 'pinia'

// 새로고침해도 store의 내용이 localstorage에 저장되게 하는 라이브러리
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'

import './assets/base.css'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

import '@/api/index.js'
app.mount('#app')
