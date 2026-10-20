<script setup>
import AppIcon from '@/components/AppIcon.vue'
import AuthLayout from '@/components/AuthLayout.vue'
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
  <AuthLayout>
    <span class="form-kicker">A NEW BEGINNING</span>
    <h2 class="auth-title">从这里，开始<span class="greeting-dot">。</span></h2>
    <p class="auth-subtitle">创建你的学习空间，让每一次积累都有迹可循。</p>
    <form class="auth-form" @submit.prevent="handleRegister">
      <div class="field-group">
        <label for="register-username">用户名 <span>3–50 个字符</span></label>
        <div class="input-with-icon">
          <AppIcon name="user" :size="18" /><input
            id="register-username"
            v-model="username"
            autocomplete="username"
            placeholder="给自己取一个名字"
          />
        </div>
      </div>
      <div class="field-group">
        <label for="register-password">密码 <span>6–100 个字符</span></label>
        <div class="input-with-icon">
          <AppIcon name="lock" :size="18" /><input
            id="register-password"
            v-model="password"
            type="password"
            autocomplete="new-password"
            placeholder="设置你的登录密码"
          />
        </div>
      </div>
      <p v-if="errorMessage" class="alert-message" role="alert">
        <AppIcon name="alert" :size="17" />{{ errorMessage }}
      </p>
      <button class="button button-primary auth-submit" type="submit" :disabled="loading">
        <span v-if="loading" class="spinner"></span>{{ loading ? '注册中...' : '创建学习空间'
        }}<AppIcon v-if="!loading" name="arrow" :size="18" />
      </button>
    </form>
    <p class="auth-switch">
      已经有账号了？<RouterLink to="/login"
        >直接登录 <AppIcon name="arrow" :size="14"
      /></RouterLink>
    </p>
    <div class="auth-assurance">
      <AppIcon name="sprout" :size="16" />每一段成长，都值得有一个开始。
    </div>
  </AuthLayout>
</template>
