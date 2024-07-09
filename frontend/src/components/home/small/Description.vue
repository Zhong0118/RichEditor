<script setup></script>

<template>
  <div class="ml-auto mr-auto w-[60%]">
    <h4
      class="title1 opposans mb-2 text-center text-xl font-bold text-[--basic1]"
    >
      <slot name="title1"></slot>
    </h4>
    <h1
      class="title2 opposans mb-1 text-center text-4xl font-bold text-[--color-222]"
    >
      <slot name="title2"></slot>
    </h1>
    <p class="title3 opposans text-center text-[16px] font-extralight">
      <slot name="title3"></slot>
    </p>
  </div>
</template>

<style scoped></style>
