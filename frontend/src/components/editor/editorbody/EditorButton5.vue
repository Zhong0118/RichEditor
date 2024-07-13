<script lang="ts" setup>
const props = defineProps<{
  icon: string;
  text: string;
  // action: Function;
}>();
</script>
<template>
  <button
    class="opposans btn btn-ghost m-auto mb-[2px] h-[30px] min-h-[30px] w-full p-0"
  >
    <i :class="props.icon" class="text-[14px]"></i>
    <span>{{ props.text }}</span>
  </button>
</template>

<style lang="scss"></style>
