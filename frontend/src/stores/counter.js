import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  const token = ref(localStorage.getItem('token') || null)
  const nickname = ref(localStorage.getItem('nickname') || '')

  const isLoggedIn = computed(() => !!token.value)

  function login(newToken, newNickname) {
    token.value = newToken
    nickname.value = newNickname

    localStorage.setItem('token',newToken)
    localStorage.setItem('nickname',newNickname)
  }

  function logout() {
    token.value = null
    nickname.value = ''

    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
  }

  return { 
    count, 
    doubleCount, 
    increment, 
    isLoggedIn,
    nickname,
    login,
    logout,
    token
  }
})
