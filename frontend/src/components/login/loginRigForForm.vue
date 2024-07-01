<script setup>
import { defineEmits, defineProps, ref } from "vue";

const username = ref("");
const password = ref("");
const props = defineProps({
  formType: String,
  title: String,
  subtitle: String,
  buttonText: String,
  isVisible: Boolean,
});

const emit = defineEmits(["getInfo"]);
const returnInfo = () => {
  emit("getInfo", username, password);
};
</script>

<template>
  <div :class="{ formType }" class="wholeForm">
    <div class="form-title">
      <h1 class="mb-[10px] text-5xl font-bold">{{ title }}</h1>
      <h4>{{ subtitle }}</h4>
    </div>
    <div class="form mt-4">
      <label class="input-container form-control relative w-full">
        <div class="label">
          <span class="label-text text-xl" style="color: var(--login4)"
            >Username</span
          >
        </div>
        <div>
          <svg
            class="absolute left-2.5 top-1/2 h-5 w-5 translate-y-1/2 opacity-70"
            fill="currentColor"
            viewBox="0 0 16 16"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z"
            />
          </svg>
          <input
            v-model="username"
            class="input input-bordered input-info w-full pl-10"
            placeholder="Username"
            type="text"
          />
        </div>
      </label>
      <label class="input-container form-control relative w-full">
        <div class="label">
          <span class="label-text text-xl text-[var(--login4)]">Password</span>
        </div>
        <div>
          <svg
            class="absolute left-2.5 top-1/2 h-5 w-5 translate-y-1/2 opacity-70"
            fill="currentColor"
            viewBox="0 0 16 16"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              clip-rule="evenodd"
              d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
              fill-rule="evenodd"
            />
          </svg>
          <input
            v-model="password"
            :type="isVisible ? 'text' : 'password'"
            class="input input-bordered input-info w-full pl-10"
            placeholder="Password"
          />
        </div>
      </label>

      <slot />
      <button
        class="playfair-display btn btn-primary btn-wide mt-6 font-bold"
        style="font-size: 20px"
        @click.prevent="returnInfo()"
      >
        {{ buttonText }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.wholeForm {
  width: 70%;
  top: 18%;
  position: absolute;
}
</style>
