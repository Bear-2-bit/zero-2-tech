<script setup>
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'


const router = useRouter()
const authStore = useAuthStore()


async function handleLogout() {
  authStore.logout()

  await router.push('/login')
}
</script>


<template>
  <div>
    <header v-if="authStore.isLoggedIn">
      <nav>
        <RouterLink to="/dashboard">
          Dashboard
        </RouterLink>

        <RouterLink to="/tasks">
          学习任务
        </RouterLink>

        <span v-if="authStore.user">
          {{ authStore.user.username }}
        </span>

        <button @click="handleLogout">
          退出登录
        </button>
      </nav>
    </header>

    <RouterView />
  </div>
</template>
