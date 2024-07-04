import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";

import { createPinia } from "pinia";
import piniaPluginPersist from 'pinia-plugin-persistedstate'
import router from "./router";

import { createVuestic } from "vuestic-ui";
import svgIcon from "@/ui/svg-icon.vue"; // 作为通用组件直接用
import "@/assets/icons/svg-icon.js";
import "virtual:svg-icons-register";
import "vuestic-ui/styles/essential.css";
import "vuestic-ui/styles/typography.css";
import "material-design-icons-iconfont/dist/material-design-icons.min.css";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersist)

app.use(pinia);
app.use(router);
app.component("svg-icon", svgIcon);
app.use(
  createVuestic({
    config: {
      colors: {
        variables: {
          primary: "#23e066",
          secondary: "#002c85",
          success: "#40e583",
          info: "#2c82e0",
          danger: "#e34b4a",
          warning: "#ffc200",
          gray: "#babfc2",
          dark: "#34495e",
          yourCustomColor: "#d0f55d",
        },
      },
    },
  }),
);
app.mount("#app");
