<script lang="ts" setup>
const props = defineProps<{
  icon: string;
  title: string;
  text: string;
  action: Function;
  isActive?: Function;
}>();
</script>
<template>
  <el-tooltip :content="props.title" effect="dark" placement="left">
    <button
      :class="{ 'btn-active': props.isActive ? props.isActive() : null }"
      class="opposans btn btn-ghost mb-[2px] h-[30px] min-h-[30px] w-[30px] min-w-[30px] p-0"
      @click="props.action"
    >
      <i :class="`ri-${props.icon}`" class="text-[14px]"></i>
    </button>
  </el-tooltip>
</template>

<style lang="scss"></style>
