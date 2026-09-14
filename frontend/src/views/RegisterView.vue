<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { register } from '@/api/auth'


const router = useRouter()

const username = ref('')
const password = ref('')

const loading = ref(false)
const errorMessage = ref('')


async function handleRegister() {
  try {
    loading.value = true
    errorMessage.value = ''

    await register({
      username: username.value,
      password: password.value,
    })

    await router.push('/login')
  } catch (error) {
    console.error(error)

    if (error.response?.status === 409) {
      errorMessage.value = '用户名已存在'
    } else {
      errorMessage.value = '注册失败'
    }
  } finally {
    loading.value = false
  }
}
</script>


<template>
  <main>
    <h1>注册</h1>

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
      @click="handleRegister"
    >
      {{ loading ? '注册中...' : '注册' }}
    </button>

    <p v-if="errorMessage">
      {{ errorMessage }}
    </p>

    <RouterLink to="/login">
      已有账号？登录
    </RouterLink>
  </main>
</template>
