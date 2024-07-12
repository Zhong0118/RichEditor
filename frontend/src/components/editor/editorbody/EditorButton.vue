<script lang="ts" setup>
const props = defineProps<{
  icon: string;
  title: string;
  action: Function;
  isActive?: Function;
}>();
</script>
<template>
  <el-tooltip effect="dark" :content="props.title" placement="top">
    <button
      :class="{ 'btn-active': props.isActive ? props.isActive() : null }"
      class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[32px] min-w-[32px] p-0"
      @click="props.action"
    >
      <i :class="`ri-${props.icon}`" class="text-[18px]"></i>
    </button>
  </el-tooltip>
</template>

<style lang="scss"></style>
