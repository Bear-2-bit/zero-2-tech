<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import {
  createTask,
  deleteTask,
  getTasks,
  updateTask,
} from '@/api/tasks'

import { decomposeGoal } from '@/api/ai'

import {
  deleteTaskStep,
  getTaskSteps,
  saveTaskSteps,
  updateTaskStep,
} from '@/api/taskSteps'


// =========================
// 基础对象
// =========================

const router = useRouter()
const authStore = useAuthStore()


// =========================
// Task 状态
// =========================

const tasks = ref([])

const title = ref('')
const description = ref('')

const loading = ref(false)
const errorMessage = ref('')


// =========================
// TaskStep / AI 状态
// =========================

// 已经保存到数据库中的学习步骤
// 结构：
// {
//   1: [...],
//   2: [...]
// }
const taskSteps = ref({})


// AI刚刚生成、但还没有保存的数据
const aiPreview = ref({})


// 当前哪个任务正在调用AI
const aiLoadingTaskId = ref(null)


// 当前哪个任务正在保存AI计划
const savingTaskId = ref(null)


// =========================
// 查询某个任务的学习步骤
// =========================

async function loadTaskSteps(taskId) {
  try {
    const response = await getTaskSteps(taskId)

    taskSteps.value[taskId] = response.data
  } catch (error) {
    console.error(error)

    errorMessage.value = '学习步骤加载失败'
  }
}


// =========================
// 查询任务列表
// =========================

async function loadTasks() {
  try {
    loading.value = true
    errorMessage.value = ''

    const response = await getTasks()

    tasks.value = response.data

    // 每个任务继续查询自己的学习步骤
    for (const task of tasks.value) {
      await loadTaskSteps(task.id)
    }
  } catch (error) {
    console.error(error)

    errorMessage.value = '任务加载失败'
  } finally {
    loading.value = false
  }
}


// =========================
// 创建任务
// =========================

async function handleCreateTask() {
  if (!title.value.trim()) {
    errorMessage.value = '请输入任务标题'
    return
  }

  try {
    errorMessage.value = ''

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


// =========================
// 修改任务状态
// todo → doing → done → todo
// =========================

async function handleChangeStatus(task) {
  const nextStatus = {
    todo: 'doing',
    doing: 'done',
    done: 'todo',
  }

  try {
    errorMessage.value = ''

    await updateTask(task.id, {
      status: nextStatus[task.status],
    })

    await loadTasks()
  } catch (error) {
    console.error(error)

    errorMessage.value = '任务状态修改失败'
  }
}


// =========================
// 删除任务
// =========================

async function handleDeleteTask(id) {
  try {
    errorMessage.value = ''

    await deleteTask(id)

    await loadTasks()
  } catch (error) {
    console.error(error)

    errorMessage.value = '任务删除失败'
  }
}


// =========================
// AI 拆解任务
// =========================

async function handleAIDecompose(task) {
  try {
    aiLoadingTaskId.value = task.id
    errorMessage.value = ''

    // title + description 一起作为AI上下文
    const goal = task.description
      ? `${task.title}：${task.description}`
      : task.title

    const response = await decomposeGoal(goal)

    // 此时只是预览
    // 还没有写入 SQLite
    aiPreview.value[task.id] = response.data.steps
  } catch (error) {
    console.error(error)

    errorMessage.value = 'AI 拆解失败'
  } finally {
    aiLoadingTaskId.value = null
  }
}


// =========================
// 保存 AI 学习计划
// =========================

async function handleSaveAIPlan(taskId) {
  const steps = aiPreview.value[taskId]

  if (!steps?.length) {
    return
  }

  try {
    savingTaskId.value = taskId
    errorMessage.value = ''

    const response = await saveTaskSteps(
      taskId,
      steps
    )

    // 后端返回数据库中真正保存的 TaskStep
    taskSteps.value[taskId] = response.data

    // 清空AI预览
    aiPreview.value[taskId] = []
  } catch (error) {
    console.error(error)

    errorMessage.value = 'AI 学习计划保存失败'
  } finally {
    savingTaskId.value = null
  }
}


// =========================
// 切换学习步骤完成状态
// =========================

async function handleToggleStep(taskId, step) {
  try {
    errorMessage.value = ''

    const response = await updateTaskStep(
      taskId,
      step.id,
      {
        is_done: !step.is_done,
      }
    )

    const steps = taskSteps.value[taskId] || []

    const index = steps.findIndex(
      item => item.id === step.id
    )

    if (index !== -1) {
      steps[index] = response.data
    }
  } catch (error) {
    console.error(error)

    errorMessage.value = '学习步骤更新失败'
  }
}


// =========================
// 删除某个学习步骤
// =========================

async function handleDeleteStep(taskId, stepId) {
  try {
    errorMessage.value = ''

    await deleteTaskStep(
      taskId,
      stepId
    )

    taskSteps.value[taskId] =
      (taskSteps.value[taskId] || []).filter(
        step => step.id !== stepId
      )
  } catch (error) {
    console.error(error)

    errorMessage.value = '学习步骤删除失败'
  }
}


// =========================
// 退出登录
// =========================

async function handleLogout() {
  authStore.logout()

  await router.push('/login')
}


// =========================
// 页面第一次打开
// =========================

onMounted(() => {
  loadTasks()
})
</script>


<template>
  <!-- ====================== -->
  <!-- 顶部用户信息 -->
  <!-- ====================== -->

  <header>
    <span v-if="authStore.user">
      当前用户：{{ authStore.user.username }}
    </span>

    <button @click="handleLogout">
      退出登录
    </button>
  </header>


  <main>
    <h1>学习任务</h1>


    <!-- ====================== -->
    <!-- 创建任务 -->
    <!-- ====================== -->

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


    <!-- ====================== -->
    <!-- 全局状态 -->
    <!-- ====================== -->

    <p v-if="loading">
      加载中...
    </p>

    <p v-if="errorMessage">
      {{ errorMessage }}
    </p>


    <!-- ====================== -->
    <!-- 任务列表 -->
    <!-- ====================== -->

    <section v-if="!loading">
      <ul>

        <li
          v-for="task in tasks"
          :key="task.id"
        >

          <!-- 任务基本信息 -->

          <div>
            <strong>
              {{ task.title }}
            </strong>

            <span>
              {{ task.description }}
            </span>

            <span>
              状态：{{ task.status }}
            </span>
          </div>


          <!-- 任务操作 -->

          <div>
            <button
              @click="handleChangeStatus(task)"
            >
              修改状态
            </button>

            <button
              @click="handleDeleteTask(task.id)"
            >
              删除任务
            </button>

            <button
              :disabled="
                aiLoadingTaskId === task.id
              "
              @click="
                handleAIDecompose(task)
              "
            >
              {{
                aiLoadingTaskId === task.id
                  ? 'AI 拆解中...'
                  : 'AI 帮我拆解'
              }}
            </button>
          </div>


          <!-- ====================== -->
          <!-- AI 临时预览 -->
          <!-- ====================== -->

          <div
            v-if="
              aiPreview[task.id]?.length
            "
          >
            <h3>
              AI 建议
            </h3>

            <ol>
              <li
                v-for="(
                  step,
                  index
                ) in aiPreview[task.id]"
                :key="index"
              >
                {{ step }}
              </li>
            </ol>

            <button
              :disabled="
                savingTaskId === task.id
              "
              @click="
                handleSaveAIPlan(task.id)
              "
            >
              {{
                savingTaskId === task.id
                  ? '保存中...'
                  : '保存 AI 计划'
              }}
            </button>
          </div>


          <!-- ====================== -->
          <!-- 已保存的学习步骤 -->
          <!-- ====================== -->

          <div
            v-if="
              taskSteps[task.id]?.length
            "
          >
            <h3>
              学习步骤
            </h3>

            <ul>
              <li
                v-for="
                  step in taskSteps[task.id]
                "
                :key="step.id"
              >

                <label>
                  <input
                    type="checkbox"
                    :checked="step.is_done"
                    @change="
                      handleToggleStep(
                        task.id,
                        step
                      )
                    "
                  />

                  <span>
                    {{ step.content }}
                  </span>
                </label>

                <button
                  @click="
                    handleDeleteStep(
                      task.id,
                      step.id
                    )
                  "
                >
                  删除步骤
                </button>

              </li>
            </ul>
          </div>

        </li>

      </ul>
    </section>

  </main>
</template>
