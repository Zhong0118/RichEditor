import { defineStore } from "pinia";
import { ref, computed, reactive } from "vue";

export const useUserStore = defineStore("user", () => {
  const userInfo = ref(1);
  return {userInfo}
});
