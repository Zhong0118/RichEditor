<script setup>
import { ref } from "vue";
import loginRigForForm from "@/components/login/loginRigForForm.vue";
import showPassword from "@/components/login/showPassword.vue";
import SvgIcon from "@/ui/svg-icon.vue";

const formType = "register";
const title = "欢迎";
const subtitle = "你需要使用你的邮箱进行注册";
const buttonText = "注册";

const email = ref("");
const isVisible = ref(false); // 初始状态，密码不可见

const handleVisibilityChange = (newValue) => {
  isVisible.value = newValue;
};

function registerIn(username, password) {
  console.log(username.value);
  console.log(password.value);
  console.log(email.value);
}
</script>

<template>
  <loginRigForForm
    :button-text="buttonText"
    :form-type="formType"
    :is-visible="isVisible"
    :subtitle="subtitle"
    :title="title"
    @getInfo="registerIn"
  >
    <label class="input-container form-control relative w-full">
      <div class="label">
        <span class="label-text text-xl text-[var(--login4)]">邮箱</span>
      </div>
      <div>
        <SvgIcon
            class="absolute left-2.5 top-1/2 translate-y-1/2 text-[20px] opacity-70"
            name="email"
          ></SvgIcon>
        <input
          v-model="email"
          class="input w-full grow pl-10"
          placeholder="Email"
          type="email"
        />
      </div>
    </label>
    <show-password @update:visible="handleVisibilityChange"></show-password>
  </loginRigForForm>
</template>

<style scoped></style>
