<script setup>
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import AppIcon from '@/components/AppIcon.vue'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  authStore.logout()

  await router.push('/login')
}
</script>

<template>
  <div :class="['application', { 'has-sidebar': authStore.isLoggedIn }]">
    <aside v-if="authStore.isLoggedIn" class="sidebar">
      <RouterLink to="/dashboard" class="brand" aria-label="zero-2-tech 首页">
        <span class="brand-mark"><AppIcon name="sprout" :size="24" /></span>
        <span
          >zero<span class="brand-connector">2</span>tech<span class="brand-caption"
            >让学习，步步有迹。</span
          ></span
        >
      </RouterLink>
      <div class="workspace-label">个人学习空间 <span>WORKSPACE</span></div>
      <nav class="main-nav" aria-label="主导航">
        <RouterLink to="/dashboard"
          ><AppIcon name="overview" /><span>学习概览</span
          ><AppIcon class="nav-arrow" name="chevron" :size="15"
        /></RouterLink>
        <RouterLink to="/tasks"
          ><AppIcon name="tasks" /><span>学习任务</span
          ><AppIcon class="nav-arrow" name="chevron" :size="15"
        /></RouterLink>
      </nav>
      <div class="sidebar-note">
        <span class="note-spark"><AppIcon name="sparkles" :size="21" /></span>
        <h3>大目标，小步走</h3>
        <p>把想学的交给 AI，<br />把每一步留给自己。</p>
        <RouterLink to="/tasks">开始规划 <AppIcon name="arrow" :size="16" /></RouterLink>
        <span class="note-orbit" aria-hidden="true"></span>
      </div>
      <div class="sidebar-bottom">
        <div class="user-profile">
          <span class="avatar">{{
            (authStore.user?.username || 'U').slice(0, 1).toUpperCase()
          }}</span>
          <div class="user-copy">
            <strong>{{ authStore.user?.username || '学习者' }}</strong
            ><span>个人工作台</span>
          </div>
          <button
            class="icon-button logout-button"
            title="退出登录"
            aria-label="退出登录"
            @click="handleLogout"
          >
            <AppIcon name="logout" :size="18" />
          </button>
        </div>
        <span class="sidebar-footnote">一点积累，很多可能。<span>© zero-2-tech</span></span>
      </div>
    </aside>
    <div class="application-main">
      <header v-if="authStore.isLoggedIn" class="topbar">
        <div class="breadcrumb">
          <span>我的工作台</span><AppIcon name="chevron" :size="13" /><strong>{{
            $route.name === 'tasks' ? '学习任务' : '学习概览'
          }}</strong>
        </div>
        <span class="topbar-caption"><span class="tiny-dot"></span>专注当下，持续生长</span>
      </header>
      <RouterView />
    </div>
  </div>
</template>
