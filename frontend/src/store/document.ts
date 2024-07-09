import { defineStore } from "pinia";
import { ref } from "vue";
import {Document} from "@/types/DocumentType";



export const useDocumentStore = defineStore(
  "document",
  () => {
    const document = ref<Document>();
    const setDocument = (d: Document) => {
      document.value = d;
    }
    const delDocument = () => {
      document.value = void 0;
    }
    return { document, setDocument, delDocument };
  },
  {
    persist: true,
  },
);
