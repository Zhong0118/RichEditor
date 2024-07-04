<script setup>
import { defineEmits, ref } from "vue";
import loginRigForForm from "@/components/login/loginRigForForm.vue";
import showPassword from "@/components/login/showPassword.vue";

const formType = "login";
const title = "你好";
const subtitle = "请输入你的用户名和密码";
const buttonText = "登录";

const isVisible = ref(false); // 初始状态，密码不可见

const handleVisibilityChange = (newValue) => {
  isVisible.value = newValue;
};

const emit = defineEmits(["toForgetForm"]);
const onForgetPasswordClick = () => {
  emit("toForgetForm", "forget-pwd");
};

function loginIn(username, password) {
  console.log(username.value);
  console.log(password.value);
}
</script>
<template>
  <loginRigForForm
    :button-text="buttonText"
    :form-type="formType"
    :is-visible="isVisible"
    :subtitle="subtitle"
    :title="title"
    @get-info="loginIn"
  >
    <show-password @update:visible="handleVisibilityChange">
      <span class="forget-pwd-btn cursor-pointer" @click="onForgetPasswordClick"
        >忘记密码？</span
      >
    </show-password>
  </loginRigForForm>
</template>

<style scoped></style>