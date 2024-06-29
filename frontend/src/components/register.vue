<script setup>
import {ref, reactive, defineProps, defineEmits, computed} from "vue";
import loginRigForForm from "@/components/loginRigForForm.vue";
import showPassword from "@/components/showPassword.vue"

const formType = "register"
const title = "Register";
const subtitle = "You need to use your email to register";
const buttonText = "Register"

const email = ref("")

function registerIn(username, password) {
  console.log(username.value);
  console.log(password.value);
  console.log(email.value)
}

</script>

<template>
  <loginRigForForm
      :form-type="formType"
      :title="title" :subtitle="subtitle" :button-text="buttonText"
      @getInfo="registerIn">
    <label class="form-control w-full input-container relative">
      <div class="label">
        <span class="label-text text-xl" style="color: var(--login4);">Email</span>
      </div>
      <div>
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            class="h-5 w-5 opacity-70 absolute top-1/2 left-2.5 translate-y-1/2">
          <path
              d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z"/>
          <path
              d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z"/>
        </svg>
        <input
            type="email"
            placeholder="Email"
            class="input input-bordered input-info w-full grow pl-10" v-model="email"/>
      </div>
    </label>
    <show-password></show-password>
  </loginRigForForm>
</template>

<style scoped>
</style>