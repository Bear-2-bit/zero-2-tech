<script setup>
import { onMounted, ref } from 'vue'

import {
  createTask,
  deleteTask,
  getTasks,
  updateTask,
} from '@/api/tasks'


const tasks = ref([])

const title = ref('')
const description = ref('')

const loading = ref(false)
const errorMessage = ref('')


async function loadTasks() {
  try {
    loading.value = true
    errorMessage.value = ''

    const response = await getTasks()

    tasks.value = response.data
  } catch (error) {
    console.error(error)
    errorMessage.value = '任务加载失败'
  } finally {
    loading.value = false
  }
}


async function handleCreateTask() {
  if (!title.value.trim()) {
    return
  }

  try {
    await createTask({
      title: title.value,
      description: description.value,
    })

    title.value = ''
    description.value = ''

    await loadTasks()
  } catch (error) {
    console.error(error)
    errorMessage.value = '任务创建失败'
  }
}


async function handleChangeStatus(task) {
  const nextStatus = {
    todo: 'doing',
    doing: 'done',
    done: 'todo',
  }

  try {
    await updateTask(task.id, {
      status: nextStatus[task.status],
    })

    await loadTasks()
  } catch (error) {
    console.error(error)
    errorMessage.value = '任务状态修改失败'
  }
}


async function handleDeleteTask(id) {
  try {
    await deleteTask(id)

    await loadTasks()
  } catch (error) {
    console.error(error)
    errorMessage.value = '任务删除失败'
  }
}


onMounted(() => {
  loadTasks()
})
</script>


<template>
  <main>
    <h1>学习任务</h1>

    <section>
      <input
        v-model="title"
        placeholder="任务标题"
      />

      <input
        v-model="description"
        placeholder="任务描述"
      />

      <button @click="handleCreateTask">
        创建任务
      </button>
    </section>

    <p v-if="loading">
      加载中...
    </p>

    <p v-if="errorMessage">
      {{ errorMessage }}
    </p>

    <section v-if="!loading">
      <ul>
        <li
          v-for="task in tasks"
          :key="task.id"
        >
          <strong>{{ task.title }}</strong>

          <span>
            {{ task.description }}
          </span>

          <span>
            {{ task.status }}
          </span>

          <button @click="handleChangeStatus(task)">
            修改状态
          </button>

          <button @click="handleDeleteTask(task.id)">
            删除
          </button>
        </li>
      </ul>
    </section>
  </main>
</template>
