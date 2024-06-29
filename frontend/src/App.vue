<script setup>
import {RouterLink, RouterView} from 'vue-router'
import {reactive, ref} from 'vue';
import LoginPage from "@/views/LoginPage.vue";
</script>

<template>
  <LoginPage></LoginPage>
</template>

<style>
body {
  background: var(--login);
}
</style>
