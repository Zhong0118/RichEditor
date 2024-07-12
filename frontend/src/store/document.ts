import { defineStore } from "pinia";
import { ref } from "vue";
import { Document } from "@/types/DocumentType.ts";

export const useDocumentStore = defineStore(
  "document",
  () => {
    const document = ref<Document>();
    const setDocument = (d: Document) => {
      document.value = d;
    };

    const getDid = () => {
      if (document.value) {
        return document.value.did;
      }
    }
    const changeTag = (tag: string) => {
      if (document.value) {
        document.value.tag = tag;
      }
    };

    const changeTitle = (title: string) => {
      if (document.value) {
        document.value.title = title;
      }
    };

    const changeShared = (share: boolean) => {
      if (document.value) {
        document.value.is_shared = share;
      }
    };

    const changeUpdateTime = (time: string) => {
      if (document.value) {
        document.value.updateTime = time;
      }
    };
    const delDocument = () => {
      document.value = void 0;
    };
    return {
      document,
      setDocument,
      delDocument,
      changeTitle,
      changeTag,
      changeShared,
      changeUpdateTime,
      getDid
    };
  },
  {
    persist: true,
  },
);
