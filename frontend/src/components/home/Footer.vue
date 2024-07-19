<script setup></script>

<template>
  <div id="footer" class="bg-base-200">
    <footer class="footer bg-base-200 p-10 pl-[5%] pr-[5%] text-base-content">
      <aside class="ml-auto mr-auto">
        <img class="h-[60px]" src="../../../public/titleIcon.svg"  alt=""/>
        <br />
        <div class="flex flex-row justify-between w-[150px]">
          <a
            class="social-link"
            href="https://github.com/Zhong0118/RichEditor"
            rel="noopener noreferrer"
            target="_blank"
          >
            <img
              alt="github"
              class="h-[24px]"
              src="@/assets/icons/github.svg"
            />
          </a>
          <a
            class="social-link"
            href="mailto:Zx21372128@gmail.com"
            rel="noopener noreferrer"
            target="_blank"
          >
            <img alt="gmail" class="h-[24px]" src="@/assets/icons/gmail.svg" />
          </a>
          <a
            class="social-link"
            href="https://space.bilibili.com/409889260"
            rel="noopener noreferrer"
            target="_blank"
          >
            <img
              alt="bilibili"
              class="h-[24px]"
              src="@/assets/icons/bilibili.svg"
            />
          </a>
          <a
            class="social-link"
            href="https://blog.csdn.net/CROSS__over?spm=1000.2115.3001.5343"
            rel="noopener noreferrer"
            target="_blank"
          >
            <img alt="csdn" class="h-[24px]" src="@/assets/icons/csdn.svg" />
          </a>
        </div>
      </aside>
      <nav class="ml-auto mr-auto special-font">
        <h6 class="footer-title text-[16px]">服务</h6>
        <a class="link-hover link">文本编辑</a>
        <a class="link-hover link">OCR读取</a>
        <a class="link-hover link">智能润色</a>
        <a class="link-hover link">模板设计</a>
      </nav>
      <nav class="ml-auto mr-auto special-font">
        <h6 class="footer-title text-[16px]">交互</h6>
        <a class="link-hover link">About us</a>
        <a class="link-hover link">Contact</a>
        <a class="link-hover link">Jobs</a>
        <a class="link-hover link">Press kit</a>
      </nav>
      <nav class="ml-auto mr-auto special-font">
        <h6 class="footer-title text-[16px]">主页</h6>
        <a class="link-hover link" href="#ai">简介</a>
        <a class="link-hover link" href="#doc">文档类型</a>
        <a class="link-hover link" href="#efficiency">效率提升</a>
        <a class="link-hover link" href="#inspiration">灵感迸发</a>
        <a class="link-hover link" href="#footer">联系</a>
      </nav>
    </footer>
    <div class="ml-[5%] mr-[5%] h-[1px] bg-neutral-700"></div>
    <footer
      class="footer footer-center rounded bg-base-200 p-10 pl-[5%] pr-[5%] text-base-content"
    >
      <aside>
        <p>
          Copyright © 2024 - 版权所有归属
          Zhong0118&nbsp;&nbsp;&nbsp;<b>|</b>&nbsp;&nbsp;&nbsp;联系方式：Zx21372128@163.com
        </p>
      </aside>
    </footer>
  </div>
</template>

<style scoped>
.special-font * {
  font-family: OPPOSans, sans-serif;
  font-weight: 400;
}
</style>
