<script setup>
defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 20 },
})
const paths = {
  sprout: ['M12 21v-9', 'M12 16C5 16 3 12 3 6c6 0 9 3 9 8', 'M12 12c0-6 3-9 9-9 0 6-3 9-9 9'],
  overview: ['M3 3h7v7H3z', 'M14 3h7v7h-7z', 'M3 14h7v7H3z', 'M14 14h7v7h-7z'],
  tasks: ['M9 5h12M9 12h12M9 19h12', 'm3 5 1 1 2-2M3 12h3M3 19h3'],
  chevron: ['m9 5 7 7-7 7'],
  arrow: ['M4 12h16m-6-6 6 6-6 6'],
  plus: ['M12 5v14M5 12h14'],
  sparkles: ['m12 3 2.4 6.6L21 12l-6.6 2.4L12 21l-2.4-6.6L3 12l6.6-2.4L12 3Z', 'M20 2v4m-2-2h4'],
  check: ['m5 12 4 4L19 6'],
  checkCircle: ['M21 11v1a9 9 0 1 1-5.3-8.2', 'm9 11 3 3L22 4'],
  circle: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z'],
  clock: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z', 'M12 7v5l3 2'],
  trend: ['m3 17 6-6 4 4 8-10', 'M15 5h6v6'],
  book: ['M12 5C9 3 5 3 2 4v15c3-1 7-1 10 1 3-2 7-2 10-1V4c-3-1-7-1-10 1Zm0 0v15'],
  logout: ['M9 4H4v16h5', 'M10 12h11m-4-4 4 4-4 4'],
  trash: ['M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7m4-7v7'],
  save: [
    'M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h12l4 4v12a2 2 0 0 1-2 2Z',
    'M7 3v6h10V3M7 21v-8h10v8',
  ],
  lock: ['M5 10h14v11H5z', 'M8 10V6a4 4 0 0 1 8 0v4M12 14v3'],
  user: ['M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z', 'M4 21v-2a8 8 0 0 1 16 0v2'],
  alert: ['M12 3 2 21h20L12 3Z', 'M12 9v5m0 3v.1'],
}
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    class="app-icon"
  >
    <path v-for="(path, index) in paths[name] || paths.circle" :key="index" :d="path" />
  </svg>
</template>
