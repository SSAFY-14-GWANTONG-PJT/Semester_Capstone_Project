import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  // 1. 기존 상태(State) 유지
  const token = ref(null)
  const refreshToken = ref(null)
  const nickname = ref('')
  const email = ref('')
  const userId = ref(null)
  const experience = ref(0) // 기존 경험치 ref 사용
  const level = ref(1)      // 레벨 추가

  const isLoggedIn = computed(() => !!token.value)

  // 2. 레벨 시스템 데이터 (고정된 상수이므로 ref로 만들지 않아도 됩니다)
  const levelSystem = [
    { level: 1, max_exp: 100 },
    { level: 2, max_exp: 120 },
    { level: 3, max_exp: 140 },
    { level: 4, max_exp: 160 },
    { level: 5, max_exp: 180 },
    { level: 6, max_exp: 200 },
    { level: 7, max_exp: 220 },
    { level: 8, max_exp: 240 },
    { level: 9, max_exp: 260 },
    { level: 10, max_exp: 280 },
  ]

  // 3. Getters (Computed 사용)
  const currentMaxExp = computed(() => {
    const data = levelSystem.find(l => l.level === level.value)
    return data ? data.max_exp : 280 // 만렙 이후 기본값
  })

  const expPercentage = computed(() => {
    return Math.min((experience.value / currentMaxExp.value) * 100, 100)
  })

  // 4. Actions (함수 사용)
  
  // 레벨업 체크 함수 (경험치 획득 시 호출됨)
  const checkLevelUp = () => {
    // 현재 레벨의 최대치를 먼저 고정하고 계산을 시작해야 안전합니다.
    while (true) {
      const max = currentMaxExp.value
      if (experience.value >= max) {
        if (level.value >= 10) {
          experience.value = max
          break
        }
        experience.value -= max // 여분의 경험치를 남깁니다.
        level.value += 1
        alert(`축하합니다! 레벨 ${level.value}이(가) 되었습니다! 🎉`)
      } else {
        break
      }
    }
  }

  // 경험치 획득 함수 (컴포넌트에서 호출용)
  const gainExperience = (amount) => {
    experience.value += amount
    checkLevelUp()
  }

  function login(newToken, newRefreshToken, newNickname, newEmail) {
    token.value = newToken
    refreshToken.value = newRefreshToken
    nickname.value = newNickname
    email.value = newEmail
    try {
      const payload = JSON.parse(atob(newToken.split('.')[1]))
      userId.value = payload.user_id
    } catch (e) {
      console.error("토큰 파싱 실패", e)
    }
  }

  function logout() {
    token.value = null
    refreshToken.value = null
    nickname.value = ''
    userId.value = null
    email.value = ''
    experience.value = 0
    level.value = 1
  }

  // 설정 관련 로직 (기존 유지)
  const savedSettings = JSON.parse(localStorage.getItem('user-settings') || '{}')
  const darkMode = ref(savedSettings.darkMode ?? false)
  const soundEffects = ref(savedSettings.soundEffects ?? true)
  const autoPlay = ref(savedSettings.autoPlay ?? true)
  const dailyGoal = ref(savedSettings.dailyGoal ?? 3)

  watch([darkMode, soundEffects, autoPlay, dailyGoal], () => {
    localStorage.setItem('user-settings', JSON.stringify({
      darkMode: darkMode.value,
      soundEffects: soundEffects.value,
      autoPlay: autoPlay.value,
      dailyGoal: dailyGoal.value
    }))
  }, { deep: true })

  const applyTheme = () => {
    if (darkMode.value) document.documentElement.classList.add('dark-theme')
    else document.documentElement.classList.remove('dark-theme')
  }

  const toggleDarkMode = () => {
    darkMode.value = !darkMode.value
    applyTheme()
  }

  // 외부에서 사용할 수 있게 모두 반환
  return {
    isLoggedIn, nickname, email, userId, experience, level,
    currentMaxExp, expPercentage, // Getters
    gainExperience, login, logout, // Actions
    token, refreshToken, darkMode, soundEffects, autoPlay, dailyGoal,
    toggleDarkMode, applyTheme
  }
}, {
  persist: {
    key: 'auth-storage',
    // level과 experience도 브라우저를 새로고침해도 유지되도록 추가해야 합니다.
    paths: ['token', 'refreshToken', 'nickname', 'userId', 'level', 'experience'],
  }
})