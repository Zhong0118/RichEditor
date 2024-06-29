<script setup>
import {ref, reactive, defineProps, defineEmits, computed} from "vue";
import loginRigForForm from "@/components/loginRigForForm.vue";
import showPassword from "@/components/showPassword.vue"


const formType = "login"
const title = "Hello";
const subtitle = "Type your username and password";
const buttonText = "Login"

const emit = defineEmits(['toForgetForm']);
const onForgetPasswordClick = () => {
  emit('toForgetForm', 'forget-pwd');
};

function loginIn(username, password) {
  console.log(username.value);
  console.log(password.value);
}
</script>
<template>
  <loginRigForForm
      :form-type="formType"
      :title="title" :subtitle="subtitle" :button-text="buttonText"
      @getInfo="loginIn">
    <show-password>
      <span class="forget-pwd-btn cursor-pointer" style="color: var(--login1);"
            @click="onForgetPasswordClick">forget password</span>
    </show-password>

  </loginRigForForm>
</template>

<style scoped>

@media (max-width: 1024px) {
  .other-select {
    justify-content: flex-end !important;
  }

  .other-select .rem-pwd {
    display: none;
  }
}

</style>