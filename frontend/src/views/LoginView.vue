<script setup>
import AppIcon from '@/components/AppIcon.vue'
import AuthLayout from '@/components/AuthLayout.vue'
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

    await authStore.login(username.value, password.value)

    await router.push('/dashboard')
  } catch (error) {
    console.error(error)

    errorMessage.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthLayout>
    <span class="form-kicker">YOUR LEARNING SPACE</span>
    <h2 class="auth-title">欢迎回来<span class="greeting-dot">。</span></h2>
    <p class="auth-subtitle">登录你的工作台，继续下一步成长。</p>
    <form class="auth-form" @submit.prevent="handleLogin">
      <div class="field-group">
        <label for="login-username">用户名</label>
        <div class="input-with-icon">
          <AppIcon name="user" :size="18" /><input
            id="login-username"
            v-model="username"
            autocomplete="username"
            placeholder="输入你的用户名"
          />
        </div>
      </div>
      <div class="field-group">
        <label for="login-password">密码</label>
        <div class="input-with-icon">
          <AppIcon name="lock" :size="18" /><input
            id="login-password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            placeholder="输入你的密码"
          />
        </div>
      </div>
      <p v-if="errorMessage" class="alert-message" role="alert">
        <AppIcon name="alert" :size="17" />{{ errorMessage }}
      </p>
      <button class="button button-primary auth-submit" type="submit" :disabled="loading">
        <span v-if="loading" class="spinner"></span>{{ loading ? '登录中...' : '登录工作台'
        }}<AppIcon v-if="!loading" name="arrow" :size="18" />
      </button>
    </form>
    <p class="auth-switch">
      还没有账号？<RouterLink to="/register"
        >创建一个账号 <AppIcon name="arrow" :size="14"
      /></RouterLink>
    </p>
    <div class="auth-assurance">
      <AppIcon name="sprout" :size="16" />不必一下走很远，今天也可以前进一步。
    </div>
  </AuthLayout>
</template>
