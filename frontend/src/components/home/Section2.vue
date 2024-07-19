<script setup>
import Description from "@/components/home/small/Description.vue";
import CardOne from "@/components/home/small/CardOne.vue";
import Button from "primevue/button";
import { reactive } from "vue";
import router from "@/router/index.js";

const card_list = reactive({
  card1: {
    img: "/src/assets/images/ai1.svg",
    t1: "摘要提取",
    t2: "速读内容概要，提炼核心观点",
  },
  card2: {
    img: "/src/assets/images/ai2.svg",
    t1: "文本润色",
    t2: "提升文字质量，优化语言表达",
  },
  card3: {
    img: "/src/assets/images/ai3.svg",
    t1: "内容续写",
    t2: "智能延续文章，展示无限创意",
  },
  card4: {
    img: "/src/assets/images/ai4.svg",
    t1: "一键翻译",
    t2: "快速语言转换，便捷沟通无界",
  },
  card5: {
    img: "/src/assets/images/ai5.svg",
    t1: "信息提取",
    t2: "OCR、语音多模态识别，有机整合内容",
  },
  card6: {
    img: "/src/assets/images/ai6.svg",
    t1: "智能模板",
    t2: "模板效率倍增，格式自动优化",
  },
  card7: {
    img: "/src/assets/images/ai7.svg",
    t1: "可视化数据",
    t2: "思维导图、表格、可视化表、画布不是梦",
  },
  card8: {
    img: "/src/assets/images/ai8.svg",
    t1: "随心提问",
    t2: "AI回答问题，知识一键即得",

  },
});

function toLogin() {
  router.push('/login')
}
</script>

<template>
  <div id="ai" class="bg-slate-50 pb-8 pl-[5%] pr-[5%] pt-8">
    <Description>
      <template #title1>AI介绍</template>
      <template #title2>AI智能助手</template>
      <template #title3
        >采用文心大模型和一系列飞桨AI小模型帮助完善知识库，提供高效精准的方式加速用户设计使用
      </template>
    </Description>
    <div class="mt-2 grid grid-cols-4 grid-rows-2 gap-[20px]">
      <CardOne v-for="card in card_list" :key="card.t1">
        <template #img>
          <img :src="card.img" alt="" class="ml-auto mr-auto w-[220px]" />
        </template>
        <template #t1>{{ card.t1 }}</template>
        <template #t2>{{ card.t2 }}</template>
      </CardOne>
    </div>

    <div class="mt-[40px] text-center">
      <Button
        icon="pi pi-arrow-right"
        iconPos="right"
        label="立即使用"
        outlined
        severity="info"
        @click="toLogin"
      />
    </div>
  </div>
</template>

<style scoped></style>
