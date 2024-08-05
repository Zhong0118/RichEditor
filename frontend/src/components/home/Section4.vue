<script setup>
import Description from "@/components/home/small/Description.vue";
import CardOne from "@/components/home/small/CardOne.vue";
import { reactive } from "vue";
const card_list = reactive({
  card1: {
    img: "/src/assets/images/pic2.jpg",
    t1: "划词交流",
  },
  card2: {
    img: "/src/assets/images/pic3.jpg",
    t1: "AI问答",
  },
  card3: {
    img: "/src/assets/images/pic4.jpg",
    t1: "智能排版",
  },
  card4: {
    img: "/src/assets/images/pic5.jpg",
    t1: "OCR转换",
  },
  card5: {
    img: "/src/assets/images/pic6.jpg",
    t1: "语音转换",
  },
  card6: {
    img: "/src/assets/images/pic7.jpg",
    t1: "表格操作",
  },
  card7: {
    img: "/src/assets/images/pic8.jpg",
    t1: "pdf导出",
  },
  card8: {
    img: "/src/assets/images/pic9.jpg",
    t1: "多功能模板",
  },

  card9: {
    img: "/src/assets/images/pic14.jpg",
    t1: "共享合作",
  },

  card10: {
    img: "/src/assets/images/pic15.jpg",
    t1: "智能UML",
  },

  card11: {
    img: "/src/assets/images/pic16.jpg",
    t1: "思维提炼",
  },

  card12: {
    img: "/src/assets/images/pic17.jpg",
    t1: "热力展示",
  },
});
</script>

<template>
  <div id="efficiency" class="h-full bg-slate-50 pb-8 pl-[5%] pr-[5%] pt-8">
    <Description>
      <template #title1>效率提升</template>
      <template #title2>12大效率工具，让高效成为习惯</template>
      <template #title3>内嵌多种先进效率工具，多渠道内容一键收藏，创作效率指数提升</template>
    </Description>
      <div class="mt-2 grid grid-cols-2 grid-rows-4 gap-[20px]">
      <CardOne v-for="card in card_list" :key="card.t1">
        <template #img>
          <img :src="card.img" alt="" class="ml-auto mr-auto w-[600px] mb-8" />
        </template>
        <template #t1>{{ card.t1 }}</template>
      </CardOne>
    </div>
  </div>
</template>

<style scoped></style>
