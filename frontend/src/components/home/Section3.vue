<script setup>
import Description from "@/components/home/small/Description.vue";
</script>

<template>
  <div id="doc" class="h-full bg-sky-100 pb-8 pl-[5%] pr-[5%] pt-8">
    <Description>
      <template #title1>文档类型</template>
      <template #title2>5大文档类型，让记录得心应手</template>
      <template #title3
        >专业强大的编辑器，支持5种文档类型，随心所欲开启顺滑的创作编辑体验</template
      >
    </Description>
    <div class="mt-4 flex flex-row gap-6">
      <div>
        <img src="@/assets/images/pic1.jpg" />
        <h3
          class="opposans text-center text-2xl font-bold text-[--admin-thead] mt-8"
        >
          文本编辑
        </h3>
      </div>
      <div>
        <img src="@/assets/images/pic10.jpg" />
        <h3
          class="opposans text-center text-2xl font-bold text-[--admin-thead] mt-8"
        >
          智能画布
        </h3>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
