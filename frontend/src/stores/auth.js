import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import {
  getMe,
  login as loginRequest,
} from '@/api/auth'


export const useAuthStore = defineStore('auth', () => {
  const token = ref(
    localStorage.getItem('access_token')
  )

  const user = ref(null)


  const isLoggedIn = computed(() => {
    return Boolean(token.value)
  })


  async function login(username, password) {
    const response = await loginRequest({
      username,
      password,
    })

    token.value = response.data.access_token

    localStorage.setItem(
      'access_token',
      token.value
    )

    await fetchCurrentUser()
  }


  async function fetchCurrentUser() {
    if (!token.value) {
      user.value = null
      return
    }

    try {
      const response = await getMe()

      user.value = response.data
    } catch (error) {
      logout()
      throw error
    }
  }


  function logout() {
    token.value = null
    user.value = null

    localStorage.removeItem(
      'access_token'
    )
  }


  return {
    token,
    user,
    isLoggedIn,

    login,
    logout,
    fetchCurrentUser,
  }
})
