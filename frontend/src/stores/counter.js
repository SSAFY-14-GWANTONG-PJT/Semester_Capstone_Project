import { ref, computed } from 'vue'
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

  return { 
    isLoggedIn,
    nickname,
    login,
    logout,
    token,
    refreshToken
  }
},{
  persist:{
    key: 'auth-storage',
    paths:['token', 'refreshToken' ,'nickname'],
  }
}
)
