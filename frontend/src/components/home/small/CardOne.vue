<script setup></script>

<template>
  <div class="flex-col">
    <slot name="img"></slot>
    <h3 class="opposans text-center text-2xl font-bold text-[--admin-thead]">
      <slot name="t1"></slot>
    </h3>
    <p class="opposans text-center text-[14px] font-extralight">
      <slot name="t2"></slot>
    </p>
  </div>
</template>

<style scoped></style>
