import "@/assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";

import { createPinia } from "pinia";
import persist from 'pinia-plugin-persistedstate';
import router from "./router";

import svgIcon from "@/ui/svg-icon.vue"; // 作为通用组件直接用
import "@/assets/icons/svg-icon.js";
import "material-design-icons-iconfont/dist/material-design-icons.min.css";
import 'remixicon/fonts/remixicon.css';
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import "primeicons/primeicons.css";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App);
const pinia = createPinia();
pinia.use(persist);

app.use(pinia);
app.use(router);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
});
app.use(ElementPlus);
app.component("svg-icon", svgIcon);
app.mount("#app");
