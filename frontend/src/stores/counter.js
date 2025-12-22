import { ref, computed,watch } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const token = ref(null)
  const refreshToken = ref(null)
  const nickname = ref('')

  const isLoggedIn = computed(() => !!token.value)

  function login(newToken, newRefreshToken , newNickname) {
    token.value = newToken
    refreshToken.value = newRefreshToken
    nickname.value = newNickname
  }

  function logout() {
    token.value = null
    refreshToken.value = null
    nickname.value = ''
  }

  const savedSettings = JSON.parse(localStorage.getItem('user-settings') || '{}')
  
  const darkMode = ref(savedSettings.darkMode ?? false)
  const soundEffects = ref(savedSettings.soundEffects ?? true)
  const autoPlay = ref(savedSettings.autoPlay ?? true)
  const dailyGoal = ref(savedSettings.dailyGoal ?? 3)

  // 2. 설정이 바뀔 때마다 자동으로 localStorage에 저장 (Persistence)
  watch([darkMode, soundEffects, autoPlay, dailyGoal], () => {
    localStorage.setItem('user-settings', JSON.stringify({
      darkMode: darkMode.value,
      soundEffects: soundEffects.value,
      autoPlay: autoPlay.value,
      dailyGoal: dailyGoal.value
    }))
  }, { deep: true })

  // 3. 다크모드 적용 로직 (전역 클래스 토글)
  const applyTheme = () => {
    if (darkMode.value) {
      document.documentElement.classList.add('dark-theme')
    } else {
      document.documentElement.classList.remove('dark-theme')
    }
  }

  const toggleDarkMode = () => {
    darkMode.value = !darkMode.value
    applyTheme()
  }

  return { 
    isLoggedIn,
    nickname,
    login,
    logout,
    token,
    refreshToken,
    darkMode, 
    soundEffects, 
    autoPlay, 
    dailyGoal, 
    toggleDarkMode, 
    applyTheme
  }
},{
  persist:{
    key: 'auth-storage',
    paths:['token', 'refreshToken' ,'nickname'],
  }
}
)
