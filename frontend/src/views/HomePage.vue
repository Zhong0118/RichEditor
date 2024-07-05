<script setup>
import Header from "@/components/home/Header.vue";
import Section1 from "@/components/home/Section1.vue";
import Section2 from "@/components/home/Section2.vue";
import Section3 from "@/components/home/Section3.vue";
import Section4 from "@/components/home/Section4.vue";
import Section5 from "@/components/home/Section5.vue";
import Footer from "@/components/home/Footer.vue";
import { onMounted, onUnmounted, reactive, ref } from "vue";
import SvgIcon from "@/ui/svg-icon.vue";

const sections = reactive({
  index: "首页",
  ai: "AI介绍",
  doc: "文档类型",
  efficiency: "效率提升",
  inspiration: "灵感迸发",
  footer: "联系",
});

const top = ref(false);

function handleScroll() {
  top.value = window.scrollY >= 100;
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <Header :sections="sections"></Header>
  <Section1></Section1>
  <Section2></Section2>
  <Section3></Section3>
  <Section4></Section4>
  <Section5></Section5>
  <Footer></Footer>
  <a v-show="top" :class="{'active': top}" class="back-top-btn" href="#index">
    <SvgIcon name="lamb-top"></SvgIcon>
  </a>
</template>

<style scoped>
.back-top-btn {
  position: fixed;
  bottom: 4rem;
  right: 2rem;
  background-color: var(--doing2);
  font-size: 1rem;
  padding: 0.5rem;
  z-index: 10;
  opacity: 0;
  visibility: hidden;
  transition: 0.5s;
  border-radius: 0.5rem;
}

.back-top-btn.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(-0.67rem);
}
</style>
