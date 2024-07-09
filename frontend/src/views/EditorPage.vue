<script setup>
import LeftNav from "@/components/editor/LeftNav.vue";
import EditorHeader from "@/components/editor/EditorHeader.vue";
</script>

<template>
  <div class="flex-row flex">
    <div
      class="w-[16%] border-r-2 border-solid border-r-[--border-color] h-[100dvh]"
    >
      <LeftNav></LeftNav>
    </div>
    <div class="w-[84%]">
      <EditorHeader></EditorHeader>
    </div>
  </div>
</template>

<style scoped></style>
