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
    class="opposans btn btn-ghost mb-[2px] h-[38px] min-h-[38px] w-[80px] min-w-[80px] p-0"
    @click="props.action"
  >
    <span :style="props.style" >{{props.text}}</span>
  </button>
</template>

<style lang="scss"></style>
