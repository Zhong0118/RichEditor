<template>
  <ul class="menu w-full rounded-box">
    <li v-for="heading in headings" :key="heading.id" :class="`level-${heading.level}`">
      <a class="opposans">{{ heading.text }}</a>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    headings: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>

.level-1 { @apply text-2xl font-black; }
.level-2 { @apply text-xl font-extrabold pl-2; }
.level-3 { @apply text-lg font-bold pl-4; }
.level-4 { @apply text-base font-semibold pl-6; }
/* 根据需要继续定义其他级别 */
</style>