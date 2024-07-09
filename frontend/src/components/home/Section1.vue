<script setup></script>

<template>
  <div
    id="index"
    class="grid h-[480px] grid-cols-2 grid-rows-1 bg-sky-100 pl-[5%] pr-[5%] pt-8"
  >
    <div class="relative m-auto w-[62%]">
      <h4
        class="index-title1 mb-[20px] text-4xl font-extrabold text-[--admin-thead]"
      >
        BD Note
      </h4>
      <h2
        class="index-title2 alidongfang mb-[1px] text-5xl font-thin text-[--color-222]"
      >
        划时代AI
        <br />智能富文本编辑器
      </h2>
      <div
        class="index-title3 reeyregular text-center text-xl text-[--admin-botton-hover]"
      >
        Let's note and enjoy the AI happily
      </div>
      <p
        class="index-title4 opposans ml-1 mr-1 mt-[10px] text-[14px] font-extralight"
      >
        基于百度飞桨AI studio与文心ERNIE模型，<br />让您在创作中享受到智能助力，帮助构建最适合您的知识库。
      </p>
      <img
        alt=""
        class="section1-jump absolute -top-[20%] right-[0] w-10"
        loading="lazy"
        src="@/assets/icons/section1_1.svg"
      />
      <img
        alt=""
        class="section1-jump absolute -bottom-[30%] -left-[10%] w-10"
        loading="lazy"
        src="@/assets/icons/section1_2.svg"
      />
    </div>
    <div class="m-auto">aaa</div>
  </div>
</template>

<style scoped>
.section1-jump {
  animation: jump 2s ease-in-out infinite alternate;
}

@keyframes jump {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(20px);
  }
}
</style>
