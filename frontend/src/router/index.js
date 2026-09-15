import {
  createRouter,
  createWebHistory,
} from 'vue-router'

import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TaskView from '@/views/TaskView.vue'
import { useAuthStore } from '@/stores/auth'
import DashboardView from '@/views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(
    import.meta.env.BASE_URL
  ),

  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },

    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },

    {
      path: '/tasks',
      name: 'tasks',
      component: TaskView,

      meta: {
        requiresAuth: true,
      },
    },

     {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        requiresAuth: true,
      },
    },
  ],
})


router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!to.meta.requiresAuth) {
    return true
  }

  if (!authStore.token) {
    return '/login'
  }

  if (!authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch {
      return '/login'
    }
  }

  return true
})


export default router
