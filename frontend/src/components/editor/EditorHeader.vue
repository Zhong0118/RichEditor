<script lang="ts" setup>
import { useDocumentStore } from "@/store/document.ts";
import { computed, nextTick, ref } from "vue";
import { useUnSelect } from "@/hooks/useUnSelect.js";
import { useDocument } from "@/hooks/useDocument.js";
import emitter from "@/hooks/mitter.js";
import { renameType } from "@/types/DocumentType.ts";
import { useShare } from "@/hooks/useShare.js";
import { ElLoading } from "element-plus";

const { unSelect } = useUnSelect();

const { debounceUpdateDocumentInDB, exportTemplate } = useDocument();

const documentStore = useDocumentStore();
const currentDocument = computed(() => {
  if (documentStore.document === undefined) {
    return {
      _id: "NULL",
      title: "暂无文档",
      is_shared: false,
    };
  } else {
    return documentStore.document;
  }
});

const headerEditableTitle = ref();
const canRename = ref(false);
const handleDelete = (did: string) => {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    emitter.emit("header-delete-doc", did);
  }
};

const focusOnTitle = () => {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    canRename.value = true;
    nextTick(() => {
      headerEditableTitle.value.focus();
    });
  }
};

function cancelRename() {
  canRename.value = false;
  headerEditableTitle.value.textContent = currentDocument.value.title;
}

function confirmRename() {
  const newTitle = headerEditableTitle.value.textContent.trim();
  if (documentStore.document !== undefined) {
    documentStore.changeTitle(newTitle);
    const renameData: renameType = {
      _id: documentStore.document._id,
      newTitle: newTitle,
    };
    emitter.emit("header-rename-doc", renameData);
  }
}

function changeTag() {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    emitter.emit("header-change-tag", currentDocument.value._id);
  }
}

function locateCurrent() {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    emitter.emit("locate-current", currentDocument.value._id);
  }
}

const { shareDocument } = useShare();

function shareCheck() {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    shareDocument();
  }
}

const loading = ref(false);

function saveDocument() {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    const loadingInstance = ElLoading.service({
      lock: true,
      text: "保存中，请稍候...",
      background: "rgba(0, 0, 0, 0.7)",
    });
    loading.value = true;
    debounceUpdateDocumentInDB();
    loading.value = false;
    loadingInstance.close();
  }
}

async function exportATemplate() {
  if (
    currentDocument.value._id === "NULL" ||
    documentStore.document === undefined
  ) {
    unSelect();
  } else {
    const loadingInstance = ElLoading.service({
      lock: true,
      text: "导出中，请稍候...",
      background: "rgba(0, 0, 0, 0.7)",
    });
    loading.value = true;
    await exportTemplate();
    loading.value = false;
    loadingInstance.close();
  }
}
</script>

<template>
  <div
    class="flex h-[10%] w-full flex-row items-center justify-between border-b-2 border-solid border-b-[--border-color] bg-[--panel-color] pl-4 pr-4"
  >
    <h1
      ref="headerEditableTitle"
      :contenteditable="canRename"
      :title="currentDocument.title"
      class="opposans w-3/4 overflow-hidden whitespace-nowrap text-[32px] font-bold leading-[50px]"
      @blur="cancelRename"
      @keydown.enter.prevent="confirmRename()"
      @keydown.esc.prevent="cancelRename()"
    >
      {{ currentDocument.title }}
    </h1>
    <div class="flex flex-row">
      <div
        class="tooltip tooltip-bottom mr-2 rounded-[4px] hover:bg-[--basic3]"
        data-tip="定位到当前位置"
      >
        <i class="pi pi-map-marker p-2" @click.prevent="locateCurrent"></i>
      </div>

      <button
        class="opposans btn btn-primary mr-2 h-[30px] min-h-[32px] pl-3 pr-3"
        @click="saveDocument"
      >
        <i class="pi pi-save" style="font-size: 14px"></i>
        保存
      </button>
      <div
        class="tooltip tooltip-bottom mr-2 rounded-[4px] hover:bg-[--basic2]"
        data-tip="共享"
      >
        <i class="pi pi-external-link p-2" @click="shareCheck"></i>
      </div>
      <div
        class="tooltip tooltip-bottom mr-2 rounded-[4px] hover:bg-[--basic2]"
        data-tip="查找"
      >
        <i class="pi pi-filter p-2"></i>
      </div>

      <div class="dropdown dropdown-left dropdown-bottom content-center">
        <i
          class="pi pi-ellipsis-v rounded-[4px] p-2 hover:bg-[--basic2]"
          tabindex="0"
        ></i>
        <ul
          class="menu dropdown-content z-[1] w-32 rounded-[8px] bg-[--panel-color] p-2 shadow"
          tabindex="0"
        >
          <li><a class="opposans" @click="exportATemplate">导出为模板</a></li>
          <li><a class="opposans">导出为 pdf</a></li>
          <hr />
          <li @click="changeTag"><a class="opposans">修改标签</a></li>
          <li @click="focusOnTitle"><a class="opposans">重命名</a></li>
          <hr />
          <li @click="handleDelete(currentDocument._id)">
            <a class="opposans text-[--tododelete]">删除</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
