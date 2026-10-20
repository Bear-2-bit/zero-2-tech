<script setup>
import AppIcon from '@/components/AppIcon.vue'
import GrowthArtwork from '@/components/GrowthArtwork.vue'
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
  <main class="workspace-page dashboard-page">
    <div class="page-heading">
      <div>
        <span class="eyebrow">MY LEARNING OVERVIEW</span>
        <h1>学习概览<span class="heading-dot">.</span></h1>
        <p>每一小步，都是看得见的进步。</p>
      </div>
      <RouterLink to="/tasks" class="button button-primary"
        ><AppIcon name="plus" :size="17" />创建学习任务</RouterLink
      >
    </div>
    <section class="welcome-banner">
      <div class="welcome-copy">
        <span class="banner-label"><AppIcon name="sprout" :size="16" />GROW AT YOUR OWN PACE</span>
        <h2>把「想学」，变成「学会」。</h2>
        <p>
          从一个清晰的目标开始，让 AI 帮你拆解方向，<br
            class="desktop-break"
          />再用每一次行动，抵达更好的自己。
        </p>
        <RouterLink to="/tasks" class="button button-paper"
          >开始我的学习计划<AppIcon name="arrow" :size="17"
        /></RouterLink>
      </div>
      <GrowthArtwork />
    </section>
    <p v-if="errorMessage" class="alert-message" role="alert">
      <AppIcon name="alert" :size="17" />{{ errorMessage }}
    </p>
    <div v-if="loading" class="loading-panel" role="status">
      <span class="spinner"></span>正在整理你的学习进度…
    </div>
    <template v-else-if="!errorMessage">
      <section class="stats-grid" aria-label="学习统计">
        <article class="stat-card">
          <div class="stat-top">
            <span>总学习任务</span><span class="stat-icon"><AppIcon name="book" /></span>
          </div>
          <div class="stat-value">{{ dashboard.total_tasks }}<span>个任务</span></div>
          <p>每一个目标，都是新的可能</p>
          <span class="stat-bottom-line"></span>
        </article>
        <article class="stat-card">
          <div class="stat-top">
            <span>已完成任务</span
            ><span class="stat-icon stat-icon-olive"><AppIcon name="checkCircle" /></span>
          </div>
          <div class="stat-value">{{ dashboard.completed_tasks }}<span>个任务</span></div>
          <p>把努力，积累成自己的底气</p>
          <span class="stat-bottom-line olive"></span>
        </article>
        <article class="stat-card">
          <div class="stat-top">
            <span>任务完成率</span
            ><span class="stat-icon stat-icon-sand"><AppIcon name="trend" /></span>
          </div>
          <div class="stat-value">{{ dashboard.completion_rate }}<span>%</span></div>
          <div
            class="stat-progress"
            role="progressbar"
            :aria-valuenow="dashboard.completion_rate"
            aria-valuemin="0"
            aria-valuemax="100"
            aria-label="任务完成率"
          >
            <span :style="{ width: dashboard.completion_rate + '%' }"></span>
          </div>
          <p>
            {{ dashboard.total_tasks ? '持续向前，每一步都算数' : '创建第一个任务，开启你的进度' }}
          </p>
        </article>
      </section>
      <section class="dashboard-bottom">
        <article class="panel journey-panel">
          <div class="section-heading">
            <div>
              <span class="eyebrow">FROM GOAL TO ACTION</span>
              <h2>让学习，有迹可循</h2>
            </div>
            <span class="small-label">三个步骤，开始行动</span>
          </div>
          <div class="journey-steps">
            <div class="journey-step">
              <span class="journey-number">01</span
              ><span class="journey-icon"><AppIcon name="book" :size="22" /></span>
              <h3>写下你的目标</h3>
              <p>记录想学的知识、技能，<br />给成长一个明确的方向。</p>
            </div>
            <div class="journey-step">
              <span class="journey-number">02</span
              ><span class="journey-icon"><AppIcon name="sparkles" :size="22" /></span>
              <h3>让 AI 理清思路</h3>
              <p>把大目标拆成小步骤，<br />预览后，保存你的计划。</p>
            </div>
            <div class="journey-step">
              <span class="journey-number">03</span
              ><span class="journey-icon"><AppIcon name="checkCircle" :size="22" /></span>
              <h3>一步步，去完成</h3>
              <p>勾选每一个完成的步骤，<br />看见自己的点滴积累。</p>
            </div>
          </div>
        </article>
        <article class="next-step-panel">
          <span class="eyebrow">YOUR NEXT CHAPTER</span
          ><AppIcon class="next-step-leaf" name="sprout" :size="42" />
          <h2>{{ dashboard.total_tasks ? '下一步，继续向前。' : '你的第一步，从这里开始。' }}</h2>
          <p>
            {{
              dashboard.total_tasks
                ? '打开任务清单，选一个小步骤，给今天留下一点收获。'
                : '不用等到准备好一切。写下一个想学的目标，就是很好的开始。'
            }}
          </p>
          <RouterLink class="text-link" to="/tasks"
            >{{ dashboard.total_tasks ? '前往学习任务' : '创建第一个任务'
            }}<AppIcon name="arrow" :size="17"
          /></RouterLink>
        </article>
      </section>
    </template>
    <footer class="page-footer">
      <span>慢慢来，也是在向前。</span
      ><span>MADE FOR YOUR GROWTH <AppIcon name="sprout" :size="14" /></span>
    </footer>
  </main>
</template>
