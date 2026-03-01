import { defineStore } from 'pinia'
import { ref } from 'vue'
import { setToken, removeToken, getToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(getToken())
  const isLoggedIn = ref(!!token.value)

  // 设置用户信息
  function setUser(userData) {
    user.value = userData
  }

  // 设置令牌
  function setTokenValue(newToken) {
    token.value = newToken
    setToken(newToken)
    isLoggedIn.value = true
  }

  // 清除用户信息
  function clearUser() {
    user.value = null
    token.value = null
    isLoggedIn.value = false
    removeToken()
  }

  return {
    user,
    token,
    isLoggedIn,
    setUser,
    setTokenValue,
    clearUser
  }
})
