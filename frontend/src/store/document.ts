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
        return document.value._id;
      }
    };
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

    // 在你的 useDocumentStore 中
    function setDocumentContent(content : any) {
      if (document.value) {
        document.value.content = content;
      }
    }

    return {
      document,
      setDocument,
      delDocument,
      changeTitle,
      changeTag,
      changeShared,
      changeUpdateTime,
      getDid,
      setDocumentContent,
    };
  },
  {
    persist: false,
  },
);
