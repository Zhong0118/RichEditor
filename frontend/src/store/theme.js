import { defineStore } from "pinia";
import { ref } from "vue";

export const useThemeStore = defineStore(
  "theme",
  () => {
    const theme = ref(false);
    const setTheme = (value) => {
      theme.value = value;
    };
    const delTheme = () => {
      theme.value = false;
    };

    return { theme, setTheme, delTheme };
  },
  {
    persist: true,
  },
);
