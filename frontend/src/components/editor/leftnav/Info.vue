<script lang="ts" setup>
import { useUserStore } from "@/store/user.ts";
import { useDocumentStore } from "@/store/document.ts";
import Divider from "primevue/divider";
import { onMounted, ref, watch } from "vue";
import { useThemeStore } from "@/store/theme.js";
import emitter from "@/hooks/mitter.js";
const userStore = useUserStore();
const documentStore = useDocumentStore();
const user = userStore.user;
const userName = user?.username;
const userId = user?.uid;
let userAvatar = user?.avatar;
userAvatar = userAvatar?.replace("@", "/src");

const vipUrl = ref("/src/assets/avatar/vip1.svg");

const themeStore = useThemeStore();
const toggleTheme = ref(themeStore.theme);

watch(toggleTheme, (newVal) => {
  themeStore.setTheme(newVal);
  const htmlElement = document.documentElement;
  htmlElement.setAttribute("data-theme", newVal ? "dark" : "emerald");
});

function logout() {
  userStore.delUser();
  themeStore.delTheme();
  documentStore.delDocument();
  window.location.href = "/home";
}

function createOneDoc() {
  emitter.emit("create-doc");
}

function chooseOneTemplate(){
  emitter.emit("apply-template")
}

</script>

<template>
  <div class="flex flex-row border-b-[2px] p-[4px]">
    <div class="mr-2 flex flex-col text-center">
      <div class="dropdown">
        <div class="avatar w-[72px]" role="button" tabindex="0">
          <div class="rounded-full">
            <img :src="userAvatar" alt="Tailwind CSS Navbar component" />
          </div>
        </div>
        <ul
          class="menu dropdown-content z-[1] mt-2 w-44 rounded-[8px] bg-base-100 p-2 shadow"
          tabindex="0"
        >
          <li>
            <a class="opposans">
              <i class="pi pi-calendar-clock"></i>个人热力图</a
            >
          </li>
          <li>
            <a class="opposans"><i class="pi pi-cog"></i>设置</a>
          </li>
          <hr class="mb-1 mt-1" />
          <li>
            <label class="flex cursor-pointer gap-2">
              <i class="pi pi-sun"></i>
              <input
                v-model="toggleTheme"
                class="theme-controller toggle"
                type="checkbox"
              /><i class="pi pi-moon"></i>
            </label>
          </li>
          <hr class="mb-1 mt-1" />
          <li>
            <a class="opposans" @click="logout"
              ><i class="pi pi-sign-out"></i>退出登录</a
            >
          </li>
        </ul>
      </div>
      <p class="mt-2">{{ userName }}</p>
    </div>
    <div class="mt-4 flex flex-col">
      <div class="flex flex-row gap-0.5">
        <img :src="vipUrl" alt="icon-vip" class="w-8" />
        <Divider layout="vertical" type="dashed" />
        <a
          class="opposans link link-primary content-center text-[14px] no-underline"
          >开通会员
        </a>
      </div>
      <div class="dropdown mb-auto mt-auto">
        <div
          class="btn btn-primary h-[36px] min-h-[30px]"
          role="button"
          tabindex="0"
        >
          <i class="pi pi-plus-circle"></i>创建笔记
        </div>
        <ul
          class="menu dropdown-content z-[1] mt-2 w-44 rounded-[8px] bg-base-100 p-2 shadow"
          tabindex="0"
        >
          <li>
            <a class="opposans" @click.prevent="createOneDoc">
              <i class="ri-file-add-line"></i>文档创建</a
            >
          </li>
          <hr class="mb-1 mt-1" />
          <li>
            <a class="opposans" @click.prevent="chooseOneTemplate"><i class="ri-article-line"></i>模板选择</a>
          </li>
          <hr class="mb-1 mt-1" />
          <li>
            <a class="opposans"><i class="ri-mind-map"></i>思维导图</a>
          </li>
          <li>
            <a class="opposans"><i class="ri-gallery-line"></i>智能画布</a>
          </li>
          <li>
            <a class="opposans"><i class="ri-flow-chart"></i>UML图</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
