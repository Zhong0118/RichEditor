<script setup>
import {ref, reactive, onMounted, computed, markRaw} from "vue";

import Login from "@/components/login.vue";
import Register from "@/components/register.vue";
import Forget from "@/components/forget.vue";

const tabs = ref([
  markRaw(Login),
  markRaw(Register),
  markRaw(Forget),
])
const currentFormType = ref(tabs.value[0]);
const currentNum = ref(0);

function switchForm(formType) {
  if (formType === 'login') {
    currentFormType.value = tabs.value[0];
    currentNum.value = 0;
  } else if (formType === 'register') {
    currentFormType.value = tabs.value[1];
    currentNum.value = 1;
  } else {
    currentFormType.value = tabs.value[2];
    currentNum.value = 2;
    console.log("父组件响应")
  }
}

const findUrl = '@/assets/images/finding.svg'
const imageUrl = 'https://picsum.photos/800'
</script>

<template>
  <div class="wrapper relative box-border" style="background: var(--login); width: 100dvw; height: 100dvh">
    <div class="box">
      <div class="forms relative w-1/2 h-full flex flex-col items-center box-border">
        <div class="tips box-border">
          <span class="login-btn mr-5"
                :class="{'active-choose': currentNum === 0}"
                @click="switchForm('login')">login</span>
          <span class="register-btn"
                :class="{'active-choose': currentNum === 1}"
                @click="switchForm('register')">register</span>
        </div>
        <transition name="into" mode="out-in">
          <KeepAlive>
            <component :is="currentFormType" @toForgetForm="switchForm"></component>
          </KeepAlive>
        </transition>

      </div>
    </div>
  </div>

</template>

<style>
.box {
  width: 80vw;
  height: 80vh;
  background: url('https://picsum.photos/800') no-repeat fixed right top;
  background-size: 50% 100%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 30px;
  font-family: Ubuntu, sans-serif;
  overflow: hidden;
}

.box .forms {
  background-color: var(--login-b);
  border-radius: 30px 0 0 30px;
  color: rgb(255, 255, 255);
  overflow-y: auto;
}

.box .forms .tips {
  width: 70%;
  height: 10%;
  font-size: 25px;
  margin: 4vh;
}

.box .forms .tips span {
  cursor: pointer;
  padding-bottom: 5px;
  color: var(--login1);
}

.box .forms .tips span:hover {
  border-bottom: 4px solid var(--login3);
  color: var(--title-icon-color);
}

.box .forms .tips span.active-choose {
  border-bottom: 4px solid var(--login3);
  color: var(--title-icon-color);
}

.input-container input {
  background-color: var(--login2);
  color: var(--title-icon-color);
  font-size: 20px;
  border: 0;
}

@media (max-width: 1024px) {
  .box {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
  }

  .box .forms {
    width: 100%;
    border-radius: 0;
  }
}

@keyframes into {
  0% {
    transform: translateY(5vh);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}

.into-enter-active {
  animation: into 0.5s ease-in-out forwards;
}


</style>