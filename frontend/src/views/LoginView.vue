<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'


const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

const loading = ref(false)
const errorMessage = ref('')


async function handleLogin() {
  try {
    loading.value = true
    errorMessage.value = ''

    await authStore.login(
      username.value,
      password.value
    )

    await router.push('/tasks')
  } catch (error) {
    console.error(error)

    errorMessage.value =
      '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>


<template>
  <main>
    <h1>登录</h1>

    <input
      v-model="username"
      placeholder="用户名"
    />

    <input
      v-model="password"
      type="password"
      placeholder="密码"
    />

    <button
      :disabled="loading"
      @click="handleLogin"
    >
      {{ loading ? '登录中...' : '登录' }}
    </button>

    <p v-if="errorMessage">
      {{ errorMessage }}
    </p>

    <RouterLink to="/register">
      没有账号？注册
    </RouterLink>
  </main>
</template>
