<script lang="ts" setup>
import { computed, nextTick, ref } from "vue";
import { useDocumentStore } from "@/store/document.ts";
import { useDocument } from "@/hooks/useDocument.js";
import { Document, renameType } from "@/types/DocumentType.ts";
import { useShare } from "@/hooks/useShare.js";
import emitter from "@/hooks/mitter.js";

const { shareCancel } = useShare();

const { debounceGetContent, getContent } = useDocument();

const props = withDefaults(
  defineProps<{
    doc: Document;
    reNameDoc?: Function;
    deleteDoc?: Function;
  }>(),
  {
    reNameDoc: () => {},
    deleteDoc: () => {},
  },
);

const editableTitle = ref();
const docCard = ref();
const canRename = ref(false);

const documentStore = useDocumentStore();
const current = computed(() => {
  if (documentStore.document === undefined) {
    return false;
  } else {
    return documentStore.getDid() === props.doc._id;
  }
});

const emit = defineEmits(["delete-doc", "rename-doc"]);

const handleDelete = (_id: string) => {
  // 假设 parentEmit 是一个用于向父组件发送事件的方法
  emit("delete-doc", _id);
};

const focusOnTitle = () => {
  canRename.value = true;
  nextTick(() => {
    editableTitle.value.focus();
  });
};

function cancelRename() {
  canRename.value = false;
  editableTitle.value.textContent = props.doc.title;
}

function confirmRename() {
  const newTitle = editableTitle.value.textContent.trim();
  if (newTitle !== props.doc.title) {
    const renameData: renameType = {
      _id: props.doc._id,
      newTitle: newTitle,
    };
    emit("rename-doc", renameData);
    canRename.value = false;
  }
  if (current.value) {
    documentStore.changeTitle(newTitle);
  }
}

function selectDocument() {
  shareCancel();
  const d = {
    _id: props.doc._id,
    title: props.doc.title,
    share_id: props.doc.share_id,
    is_shared: props.doc.is_shared,
    createTime: props.doc.createTime,
    updateTime: props.doc.updateTime,
    tag: props.doc.tag,
    tag_color: props.doc.tag_color,
  };
  documentStore.setDocument(d);
    emitter.emit("change-content");
}

function splitTime(time: string) {
  return time.substring(0, 10);
}
</script>

<template>
  <div
    ref="docCard"
    :class="{ 'bg-[--small-doc]': current }"
    class="ml-1 mr-2 mt-2 flex w-[95%] flex-col justify-between rounded-[8px] border-[1px] border-solid border-[--border-color] p-1.5 hover:bg-[--small-doc]"
    @click.prevent="selectDocument"
  >
    <div class="flex flex-row justify-between">
      <h1
        ref="editableTitle"
        :contenteditable="canRename"
        :title="doc.title"
        class="opposans mb-2 w-[80%] max-w-[80%] content-center break-all text-xl font-semibold tracking-normal"
        @blur="cancelRename"
        @keydown.esc.prevent="cancelRename"
        @keydown.enter.prevent="confirmRename"
        @click.stop
      >
        {{ doc.title }}
      </h1>
      <div class="dropdown dropdown-left content-center" @click.stop>
        <i
          class="pi pi-ellipsis-v mb-2 rounded-[4px] p-2 hover:bg-[--basic2]"
          tabindex="0"
        ></i>
        <ul
          class="menu dropdown-content z-[1] w-32 rounded-[8px] bg-[--panel-color] p-2 shadow"
          tabindex="0"
        >
          <li @click="focusOnTitle"><a class="opposans">重命名</a></li>
          <li @click="handleDelete(props.doc._id)">
            <a class="opposans text-[--tododelete]">删除</a>
          </li>
        </ul>
      </div>
    </div>
    <div
      v-if="doc.tag"
      :title="doc.tag"
      class="opposans badge badge-ghost max-w-[60%] overflow-hidden whitespace-nowrap rounded-[8px] text-[12px] font-bold"
    >
      {{ doc.tag }}
    </div>
    <p class="select-none text-[12px] text-[--small-text]">
      {{ splitTime(doc.createTime) }}
      &nbsp|&nbsp
      {{ splitTime(doc.updateTime) }}
    </p>
  </div>
</template>

<style scoped></style>
