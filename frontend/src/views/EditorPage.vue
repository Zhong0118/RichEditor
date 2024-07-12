<script setup>
import LeftNav from "@/components/editor/LeftNav.vue";
import EditorHeader from "@/components/editor/EditorHeader.vue";
import TiptapEditor from "@/components/editor/TiptapEditor.vue";
</script>

<template>
  <div class="flex flex-row">
    <div
      class="h-[100dvh] w-[16%] border-r-2 border-solid border-r-[--border-color]"
    >
      <LeftNav></LeftNav>
    </div>
    <div class="w-[84%] h-[100dvh]">
      <EditorHeader></EditorHeader>
      <TiptapEditor></TiptapEditor>
    </div>
  </div>
</template>

<style scoped></style>
