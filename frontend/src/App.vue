<script setup>
import { RouterView, useRoute } from "vue-router";
import { onMounted, watch } from "vue";
onMounted(() => {
  const route = useRoute();
  const setTitle = (to) => {
    document.title = to.meta.title || '默认标题 - 我的网站';
  };
  setTitle(route);
  watch(() => route.path, () => {
    setTitle(route);
  });
});
</script>

<template>
  <RouterView />
</template>

<style></style>
