<script setup>
import { onMounted, ref } from 'vue'

import { getDashboard } from '@/api/dashboard'


const dashboard = ref({
  total_tasks: 0,
  completed_tasks: 0,
  completion_rate: 0,
})

const loading = ref(false)
const errorMessage = ref('')


async function loadDashboard() {
  try {
    loading.value = true
    errorMessage.value = ''

    const response = await getDashboard()

    dashboard.value = response.data
  } catch (error) {
    console.error(error)

    errorMessage.value = 'Dashboard 加载失败'
  } finally {
    loading.value = false
  }
}


onMounted(() => {
  loadDashboard()
})
</script>


<template>
  <main>
    <h1>学习概览</h1>

    <p v-if="loading">
      加载中...
    </p>

    <p v-if="errorMessage">
      {{ errorMessage }}
    </p>

    <section v-if="!loading">
      <div>
        <h2>总任务</h2>
        <strong>
          {{ dashboard.total_tasks }}
        </strong>
      </div>

      <div>
        <h2>已完成</h2>
        <strong>
          {{ dashboard.completed_tasks }}
        </strong>
      </div>

      <div>
        <h2>完成率</h2>
        <strong>
          {{ dashboard.completion_rate }}%
        </strong>
      </div>
    </section>
  </main>
</template>
