<script setup>
import { ref } from "vue";
import loginRigForForm from "@/components/login/loginRigForForm.vue";
import showPassword from "@/components/login/showPassword.vue";

const formType = "register";
const title = "Register";
const subtitle = "You need to use your email to register";
const buttonText = "Register";

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
        <span class="label-text text-xl text-[var(--login4)]">Email</span>
      </div>
      <div>
        <svg
          class="absolute left-2.5 top-1/2 h-5 w-5 translate-y-1/2 opacity-70"
          fill="currentColor"
          viewBox="0 0 16 16"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z"
          />
          <path
            d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z"
          />
        </svg>
        <input
          v-model="email"
          class="input input-bordered input-info w-full grow pl-10"
          placeholder="Email"
          type="email"
        />
      </div>
    </label>
    <show-password @update:visible="handleVisibilityChange"></show-password>
  </loginRigForForm>
</template>

<style scoped></style>
