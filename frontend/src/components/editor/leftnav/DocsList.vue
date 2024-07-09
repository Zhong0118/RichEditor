<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import VirtualScroller from "primevue/virtualscroller";
import DocCard from "@/components/editor/leftnav/DocCard.vue";
import Swal from "sweetalert2";
import emitter from "@/hooks/mitter";
import { useDocumentStore } from "@/store/document";
import Mock from "mockjs";
import { Document, renameType } from "@/types/DocumentType";

const documentStore = useDocumentStore();

const count = ref(0);

function generateRandomDocuments(): Document[] {
  const randomDocument = () => ({
    did: Mock.Random.id(), // 生成随机 ID
    title: Mock.Random.cword(5, 10), // 生成随机长度的标题（5 到 10 个词）
    share_id: Mock.Random.string("lowercase"), // 生成随机小写字符串作为 share_id
    is_shared: Mock.Random.boolean(), // 随机布尔值表示是否共享
    createTime: Mock.Random.date("yyyy-MM-dd").toString(), // 生成随机日期作为创建时间
    updateTime: Mock.Random.date("yyyy-MM-dd").toString(), // 生成随机日期作为更新时间
    tag: Mock.Random.cword(1, 3), // 生成随机长度的标签（1 到 3 个词）
    content: Mock.Random.paragraph(), // 生成随机段落作为内容
    tag_color: Mock.Random.pick([
      "",
      "badge-success",
      "badge-ghost",
      "badge-accent",
    ]),
  });

  return Mock.mock({
    "list|15": [randomDocument], //
  }).list; // 返回生成的 Document 数组
}

const docList = ref<Document[]>([]);
docList.value = generateRandomDocuments();

const sortBy = ref("");
count.value = docList.value.length;
const searchQuery = ref("");

function changeSort(value: string) {
  sortBy.value = value;
}

const filterDocList = computed(() => {
  // 创建一个 docList 的副本并进行排序，而不是直接修改 docList
  return [...docList.value].sort((a, b) => {
    switch (sortBy.value) {
      case "titleAcs":
        return a.title.localeCompare(b.title);
      case "titleDcs":
        return b.title.localeCompare(a.title);
      case "createTimeAcs":
        return a.createTime.localeCompare(b.createTime);
      case "createTimeDcs":
        return b.createTime.localeCompare(a.createTime);
      case "finishTimeAcs":
        return a.updateTime.localeCompare(b.updateTime);
      case "finishTimeDcs":
        return b.updateTime.localeCompare(a.updateTime);
      case "tag":
        return a.tag.localeCompare(b.tag);
      default:
        return 0; // 保持原顺序
    }
  });
});
const renameDoc = (data: renameType) => {
  console.log(data);
  console.log(data.did);
  console.log(data.newTitle);
  const doc = docList.value.find((doc) => doc.did === data.did);
  if (doc) {
    doc.title = data.newTitle;
  }
};
const deleteDoc = (did: string) => {
  Swal.fire({
    text: "确定要删除该文档吗？",
    icon: "question",
    showConfirmButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    showCancelButton: true,
  }).then((result) => {
    if (result.isConfirmed) {
      docList.value = docList.value.filter((doc) => doc.did !== did);
      if (documentStore.document === undefined) {
        return;
      } else if (did === documentStore.document.did) {
        documentStore.delDocument();
      }
    }
  });
};
const changeTag = (did: string) => {
  Swal.fire({
    title: "请输入新标签",
    input: "text", // 显示输入框
    icon: "info",
    position: "top",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    reverseButtons: true, // 交换确认和取消按钮的位置
    inputAttributes: {
      maxlength: "8", // 设置最大长度限制，这里设置为20字符
      placeholder: "最多输入8个字符" // 设置输入框占位符
    },
    customClass: {
      input: "w-[40%] ml-auto mr-auto" // 你的自定义类，需要在 CSS 中定义
    },
  }).then((result) => {
    if (result.isConfirmed) {
      const newTag = result.value; // 获取用户输入的新标签
      if (newTag) {
        const doc = docList.value.find((doc) => doc.did === did);
        if (doc) {
          doc.tag = newTag; // 更新文档的标签
          documentStore.document.tag = newTag; // 更新当前文档的标签
        }
      }
    }
  });
};
watch(docList, (newDocList) => {
  count.value = newDocList.length;
});

function createOneDoc() {}

const virtualScroller = ref();
const scrollToCurrentDocumentRef = (currentDid: string) => {
  scrollToCurrentDocument(currentDid);
};

function scrollToCurrentDocument(currentDid: string) {
  const index = filterDocList.value.findIndex((doc) => doc.did === currentDid);
  if (index !== -1) {
    console.log(index);
    virtualScroller.value.scrollToIndex(index);
  }
}

onMounted(() => {
  emitter.on("create-doc", createOneDoc);
  emitter.on("locate-current", scrollToCurrentDocumentRef);
  emitter.on("header-delete-doc", deleteDoc);
  emitter.on("header-rename-doc", renameDoc);
  emitter.on("header-change-tag", changeTag);
});
onUnmounted(() => {
  emitter.off("create-doc", createOneDoc);
  emitter.off("locate-current", scrollToCurrentDocumentRef);
  emitter.off("header-delete-doc", deleteDoc);
  emitter.off("header-rename-doc", renameDoc);
  emitter.off("header-change-tag", changeTag);
});
</script>

<template>
  <div class="mt-4 flex h-auto flex-row gap-2">
    <label
      class="input input-bordered flex h-8 w-[82%] items-center gap-2 pl-2 pr-0.5 text-[12px]"
    >
      <i class="pi pi-search"></i>
      <input class="grow" placeholder="输入标题" type="text" v-model="searchQuery"/>
    </label>
    <div class="dropdown dropdown-bottom content-center">
      <i
        class="pi pi-sort-alt mb-2 rounded-[4px] p-2 hover:bg-[--basic2]"
        tabindex="0"
      ></i>
      <ul
        class="menu dropdown-content z-[1] w-36 rounded-[8px] bg-base-100 p-2 shadow"
        tabindex="0"
      >
        <li @click.prevent="changeSort('titleAcs')">
          <a class="opposans">标题升序</a>
        </li>
        <li @click.prevent="changeSort('titleDcs')">
          <a class="opposans">标题倒序</a>
        </li>
        <li @click.prevent="changeSort('createTimeAcs')">
          <a class="opposans">创造时间升序</a>
        </li>
        <li @click.prevent="changeSort('createTimeDcs')">
          <a class="opposans">创造时间倒序</a>
        </li>
        <li @click.prevent="changeSort('finishTimeAcs')">
          <a class="opposans">修改时间升序</a>
        </li>
        <li @click.prevent="changeSort('finishTimeDcs')">
          <a class="opposans">修改时间倒序</a>
        </li>
        <li @click.prevent="changeSort('tag')">
          <a class="opposans">按标签分类</a>
        </li>
      </ul>
    </div>
  </div>
  <VirtualScroller
    ref="virtualScroller"
    :autoSize="true"
    :item-size="100"
    :items="filterDocList"
    :numToleratedItems="1"
    class="h-[70%] w-full rounded-[8px] bg-[--color-fff]"
  >
    <template v-slot:item="{ item }">
      <DocCard :doc="item" @delete-doc="deleteDoc" @rename-doc="renameDoc">
      </DocCard>
    </template>
  </VirtualScroller>
  <div
    class="alidongfang absolute bottom-1 left-0 w-full border-t-2 border-solid border-t-[--border-color] pl-2"
  >
    总共 {{ count }} 项
  </div>
</template>

<style scoped></style>
