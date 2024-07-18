<script lang="ts" setup>
import { useUserStore } from "@/store/user.ts";
import { useDocumentStore } from "@/store/document.ts";
import Divider from "primevue/divider";
import { ref, watch } from "vue";
import { useThemeStore } from "@/store/theme.js";
import emitter from "@/hooks/mitter.js";
import Swal from "sweetalert2";
import { customAlphabet } from "nanoid";
import http from "@/utils/requests.js";

const share_id_string =
  "1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM";
const nanoid = customAlphabet(share_id_string, 6);

const userStore = useUserStore();
const documentStore = useDocumentStore();
const user = userStore.user;
const userName = user?.username;
const userId = user?.uid;
let userAvatar = user?.avatar;
const userVip = ref(user?.vip);
userAvatar = userAvatar?.replace("@", "/src");

const vipUrl1 = ref("/src/assets/avatar/vip1.svg");
const vipUrl2 = ref("/src/assets/avatar/vip2.svg");
const vipUrl = userVip.value ? vipUrl2 : vipUrl1;

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

function chooseOneTemplate() {
  emitter.emit("apply-template");
}

const code = ref("");

function showQRCodeAndVerify() {
  code.value = nanoid();
  const qrCodeContainer = document.createElement("div");
  qrCodeContainer.style.display = "flex"; // 居中显示二维码
  qrCodeContainer.style.justifyContent = "center";
  // 设置二维码的属性和内容
  new QRCode(qrCodeContainer, {
    text: code.value,
    width: 128,
    height: 128,
  });
  qrCodeContainer.title = '';
  setTimeout(() => {
    Swal.fire({
      title: "扫描二维码支付",
      html: qrCodeContainer.outerHTML,
      input: "text",
      inputPlaceholder: "输入购买码",
      focusConfirm: false,
      inputAttributes: {
        maxlength: "6", // 设置最大长度限制，这里设置为20字符
      },
      customClass: {
        input: "w-[40%] ml-auto mr-auto", // 你的自定义类，需要在 CSS 中定义
      },
      showCancelButton: true, // 显示取消按钮
      confirmButtonText: "购买",
      reverseButtons: true,
      preConfirm: () => {
        const userEnteredCode = Swal.getInput()?.value;
        // 比较用户输入的验证码与生成的验证码
        if (userEnteredCode?.toLowerCase() === code.value.toLowerCase()) {
          vipUrl.value = vipUrl2.value;
          userVip.value = true;
          http.request({
            method: "POST",
            url: "/api/setvip",
            data: {
              uid: userId,
            },
          });
        } else {
          // 验证码不正确，显示错误提示
          Swal.showValidationMessage("购买码输入错误，请重新输入");
          return false;
        }
      },
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "购买成功",
          text: "您已经是尊贵的VIP用户了",
          icon: "success",
          timer: 1500,
        });
      }
    });
  }, 100); // 小延迟确保 DOM 更新
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
          v-show="!userVip"
          class="opposans link link-primary content-center text-[14px] no-underline"
          @click.prevent="showQRCodeAndVerify"
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
            <a class="opposans" @click.prevent="chooseOneTemplate"
              ><i class="ri-article-line"></i>模板选择</a
            >
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
