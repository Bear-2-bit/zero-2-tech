<script setup>
import AppIcon from '@/components/AppIcon.vue'
import GrowthArtwork from '@/components/GrowthArtwork.vue'
</script>

<template>
  <main class="auth-page">
    <section class="auth-story">
      <RouterLink to="/login" class="brand"
        ><span class="brand-mark"><AppIcon name="sprout" :size="25" /></span
        ><span>zero<span class="brand-connector">2</span>tech</span></RouterLink
      >
      <div class="auth-story-content">
        <span class="eyebrow"><span class="tiny-dot"></span>A LITTLE PROGRESS, EVERY DAY</span>
        <h1>每一个大目标，<br />都始于<span>小小的一步。</span></h1>
        <p>让 AI 帮你理清方向，<br />用每一次行动，靠近想成为的自己。</p>
        <div class="auth-artwork"><GrowthArtwork /></div>
        <div class="auth-story-features">
          <span><AppIcon name="sparkles" :size="17" />AI 拆解目标</span
          ><span><AppIcon name="tasks" :size="17" />记录每一步</span
          ><span><AppIcon name="trend" :size="17" />看见成长</span>
        </div>
      </div>
      <span class="auth-story-footer">从零开始，步步向前。<span>ZERO TO POSSIBILITY</span></span>
    </section>
    <section class="auth-form-side">
      <div class="auth-form-wrap"><slot /></div>
      <footer class="auth-footer">zero-2-tech · 你的个人学习工作台</footer>
    </section>
  </main>
</template>
