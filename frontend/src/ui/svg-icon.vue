<template>
  <div
    v-if="isExternal"
    :style="styleExternalIcon"
    class="svg-external-icon svg-icon"
  />
  <svg v-else :class="svgClass" aria-hidden="true">
    <use :xlink:href="iconName" />
  </svg>
</template>

<script name="SvgIcon" setup>
import { computed } from "vue";

const props = defineProps({
  // svg图片名称
  name: {
    type: String,
    required: true,
  },
});

//是否外部链接
const isExternal = computed(() => {
  return /^(https?:|mailto:|tel:)/.test(props.name);
});

//svg图片名称计算属性
const iconName = computed(() => {
  return `#icon-${props.name}`;
});

//svg样式名称计算属性
const svgClass = computed(() => {
  return "svg-icon";
});

const styleExternalIcon = computed(() => {
  return {
    mask: `url(${props.name}) no-repeat 50% 50%`,
    "-webkit-mask": `url(${props.name}) no-repeat 50% 50%`,
  };
});
</script>

<style scoped>
.svg-icon {
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  fill: currentColor;
  overflow: hidden;
}

.svg-external-icon {
  background-color: currentColor;
  mask-size: cover !important;
  display: inline-block;
}
</style>
