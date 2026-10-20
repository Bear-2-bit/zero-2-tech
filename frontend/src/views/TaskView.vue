<script setup>
import AppIcon from '@/components/AppIcon.vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import { createTask, deleteTask, getTasks, updateTask } from '@/api/tasks'

import { decomposeGoal } from '@/api/ai'

import { deleteTaskStep, getTaskSteps, saveTaskSteps, updateTaskStep } from '@/api/taskSteps'

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
    const goal = task.description ? `${task.title}：${task.description}` : task.title

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

    const response = await saveTaskSteps(taskId, steps)

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

    const response = await updateTaskStep(taskId, step.id, {
      is_done: !step.is_done,
    })

    const steps = taskSteps.value[taskId] || []

    const index = steps.findIndex((item) => item.id === step.id)

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

    await deleteTaskStep(taskId, stepId)

    taskSteps.value[taskId] = (taskSteps.value[taskId] || []).filter((step) => step.id !== stepId)
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
  <main class="workspace-page task-page">
    <div class="page-heading">
      <div>
        <span class="eyebrow">SMALL STEPS, REAL PROGRESS</span>
        <h1>我的学习任务<span class="heading-dot">.</span></h1>
        <p>把目标写下来，把成长落在每一步。</p>
      </div>
      <span class="page-pill"><AppIcon name="sparkles" :size="16" />有 AI 陪你，一步步来</span>
    </div>
    <p v-if="errorMessage" class="alert-message" role="alert">
      <AppIcon name="alert" :size="17" />{{ errorMessage }}
    </p>
    <div class="tasks-layout">
      <aside class="task-composer-column">
        <section class="panel task-composer">
          <span class="composer-icon"><AppIcon name="plus" :size="23" /></span>
          <h2>种下一个新目标</h2>
          <p>今天，你想学点什么？</p>
          <form @submit.prevent="handleCreateTask">
            <div class="field-group">
              <label for="task-title">学习目标 <span>必填</span></label
              ><input id="task-title" v-model="title" placeholder="例如：掌握 FastAPI 基础" />
            </div>
            <div class="field-group">
              <label for="task-description">补充描述 <span>选填</span></label
              ><textarea
                id="task-description"
                v-model="description"
                rows="4"
                placeholder="写下你的基础、想达到的程度，或计划投入的时间…"
              />
            </div>
            <button class="button button-primary composer-submit" type="submit">
              <AppIcon name="plus" :size="17" />创建学习任务
            </button>
          </form>
          <div class="composer-tip">
            <AppIcon name="sparkles" :size="16" /><span
              >目标越具体，AI 越能帮你找到清晰的学习路径。</span
            >
          </div>
        </section>
        <div class="task-margin-note">
          <span>“</span>
          <p>不积跬步，无以至千里。</p>
          <small>专注每一个当下的小进步。</small><AppIcon name="sprout" :size="30" />
        </div>
      </aside>
      <section class="task-list-section" aria-label="学习任务列表">
        <div class="task-list-heading">
          <h2>
            学习清单 <span>{{ tasks.length.toString().padStart(2, '0') }}</span>
          </h2>
          <span class="small-label">目标 · 计划 · 行动</span>
        </div>
        <div v-if="loading" class="loading-panel panel" role="status">
          <span class="spinner"></span>正在加载学习任务…
        </div>
        <div v-else-if="!tasks.length" class="panel empty-state">
          <span class="empty-icon"><AppIcon name="sprout" :size="40" /></span
          ><span class="eyebrow">EVERY JOURNEY STARTS SOMEWHERE</span>
          <h2>给成长，种下第一颗种子</h2>
          <p>在新目标里写下你想学的内容，<br />再让 AI 帮你把想法变成可执行的小步骤。</p>
          <label for="task-title" class="text-link"
            >写下我的第一个目标 <AppIcon name="arrow" :size="17"
          /></label>
        </div>
        <div v-else class="task-cards">
          <article
            v-for="(task, taskIndex) in tasks"
            :key="task.id"
            class="panel task-card"
            :class="'task-' + task.status"
          >
            <div class="task-card-heading">
              <span class="task-index">TASK {{ (taskIndex + 1).toString().padStart(2, '0') }}</span
              ><span class="status-badge" :class="'status-' + task.status"
                ><span></span
                >{{
                  { todo: '待开始', doing: '进行中', done: '已完成' }[task.status] || task.status
                }}</span
              >
            </div>
            <h3 class="task-title">{{ task.title }}</h3>
            <p v-if="task.description" class="task-description">{{ task.description }}</p>
            <div class="task-actions">
              <button
                class="button button-ai"
                :disabled="aiLoadingTaskId === task.id"
                @click="handleAIDecompose(task)"
              >
                <span v-if="aiLoadingTaskId === task.id" class="spinner"></span
                ><AppIcon v-else name="sparkles" :size="16" />{{
                  aiLoadingTaskId === task.id ? 'AI 正在拆解...' : 'AI 帮我拆解'
                }}</button
              ><button
                class="button button-secondary button-status"
                :title="'切换到' + { todo: '进行中', doing: '已完成', done: '待开始' }[task.status]"
                @click="handleChangeStatus(task)"
              >
                <AppIcon :name="task.status === 'doing' ? 'check' : 'clock'" :size="15" />{{
                  { todo: '开始学习', doing: '标记完成', done: '重新开始' }[task.status] ||
                  '修改状态'
                }}</button
              ><button
                class="icon-button task-delete"
                title="删除任务"
                :aria-label="'删除任务：' + task.title"
                @click="handleDeleteTask(task.id)"
              >
                <AppIcon name="trash" :size="17" />
              </button>
            </div>
            <div v-if="aiLoadingTaskId === task.id" class="ai-thinking" role="status">
              <span class="thinking-dots"><i></i><i></i><i></i></span>正在为你梳理可执行的学习路径…
            </div>
            <section v-if="aiPreview[task.id]?.length" class="ai-preview">
              <div class="ai-preview-heading">
                <span><AppIcon name="sparkles" :size="18" /><strong>AI 为你规划</strong></span
                ><span class="preview-label">预览 · 尚未保存</span>
              </div>
              <ol class="preview-steps">
                <li v-for="(step, index) in aiPreview[task.id]" :key="index">
                  <span>{{ (index + 1).toString().padStart(2, '0') }}</span>
                  <p>{{ step }}</p>
                </li>
              </ol>
              <div class="ai-preview-footer">
                <p>
                  {{
                    taskSteps[task.id]?.length
                      ? '保存后将替换当前学习步骤。'
                      : '觉得合适，就把计划留在这里。'
                  }}
                </p>
                <button
                  class="button button-primary button-small"
                  :disabled="savingTaskId === task.id"
                  @click="handleSaveAIPlan(task.id)"
                >
                  <span v-if="savingTaskId === task.id" class="spinner"></span
                  ><AppIcon v-else name="save" :size="15" />{{
                    savingTaskId === task.id ? '保存中...' : '保存 AI 计划'
                  }}
                </button>
              </div>
            </section>
            <section v-if="taskSteps[task.id]?.length" class="saved-steps">
              <div class="saved-steps-heading">
                <h4>我的执行步骤</h4>
                <span
                  >{{ taskSteps[task.id].filter((step) => step.is_done).length }} /
                  {{ taskSteps[task.id].length }} 已完成</span
                >
              </div>
              <div
                class="steps-progress"
                role="progressbar"
                :aria-valuenow="taskSteps[task.id].filter((step) => step.is_done).length"
                aria-valuemin="0"
                :aria-valuemax="taskSteps[task.id].length"
                aria-label="学习步骤完成进度"
              >
                <span
                  :style="{
                    width:
                      (taskSteps[task.id].filter((step) => step.is_done).length /
                        taskSteps[task.id].length) *
                        100 +
                      '%',
                  }"
                ></span>
              </div>
              <ul class="step-list">
                <li
                  v-for="step in taskSteps[task.id]"
                  :key="step.id"
                  :class="{ 'step-done': step.is_done }"
                >
                  <label class="step-checkbox"
                    ><input
                      type="checkbox"
                      :checked="step.is_done"
                      @change="handleToggleStep(task.id, step)"
                    /><span>{{ step.content }}</span></label
                  ><button
                    class="icon-button step-delete"
                    title="删除步骤"
                    :aria-label="'删除步骤：' + step.content"
                    @click="handleDeleteStep(task.id, step.id)"
                  >
                    <AppIcon name="trash" :size="15" />
                  </button>
                </li>
              </ul>
            </section>
            <div
              v-else-if="!aiPreview[task.id]?.length && aiLoadingTaskId !== task.id"
              class="no-steps"
            >
              <AppIcon name="sparkles" :size="15" />还没有执行步骤，让 AI 帮你迈出第一步。
            </div>
          </article>
        </div>
      </section>
    </div>
    <footer class="page-footer">
      <span>每一个勾选，都是努力留下的痕迹。</span
      ><button class="text-link subtle-logout" @click="handleLogout">
        退出登录<AppIcon name="logout" :size="14" />
      </button>
    </footer>
  </main>
</template>
