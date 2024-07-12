<script lang="ts" setup>
const props = defineProps<{
  text: string;
  style: string;
  action: Function;
  isActive?: Function;
}>();
</script>
<template>
  <button
    :class="{ 'btn-active': props.isActive ? props.isActive() : null }"
    class="opposans btn btn-ghost mb-[2px] h-[30px] min-h-[30px] w-[100px] min-w-[100px] p-0"
    @click="props.action"
  >
    <span :style="props.style" class="text-[14px]">{{props.text}}</span>
  </button>
</template>

<style lang="scss"></style>
