<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import VirtualScroller from "primevue/virtualscroller";
import DocCard from "@/components/editor/leftnav/DocCard.vue";
import Swal from "sweetalert2";
import emitter from "@/hooks/mitter.js";
import { useDocumentStore } from "@/store/document.ts";
import { useUserStore } from "@/store/user.ts";
import { useDocument } from "@/hooks/useDocument.js";
import { customAlphabet } from "nanoid";
import { Document, renameType } from "@/types/DocumentType.ts";
import { ElMessage } from "element-plus";

const documentStore = useDocumentStore();
const userStore = useUserStore();
const {
  documentsList,
  getAllDocuments,
  createDocument,
  create_did,
  update_tag,
  update_title,
  delete_doc,
  showTemplates,
  templatesList,
  applyTemplate,
} = useDocument();

const count = ref(0);
const share_id_string =
  "1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM";
const nanoid = customAlphabet(share_id_string, 8);
// const tag_color_list = ["", "badge-success", "badge-ghost", "badge-accent"];

const sortBy = ref("finishTimeDcs");
const searchQuery = ref("");

function changeSort(value: string) {
  sortBy.value = value;
}

const filterDocList = computed(() => {
  let tempList = [...documentsList.value];
  if (searchQuery.value !== "") {
    tempList = tempList.filter((doc: Document) =>
      doc.title.includes(searchQuery.value),
    );
  }
  return tempList.sort((a: Document, b: Document) => {
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
count.value = documentsList.value.length;
const renameDoc = (data: renameType) => {
  const doc = documentsList.value.find((doc: Document) => doc._id === data._id);
  if (doc) {
    doc.title = data.newTitle;
    const update = new Date().toISOString();
    doc.updateTime = update;
    update_title(data._id, data.newTitle, update);
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
      delete_doc(did);
      documentsList.value = documentsList.value.filter(
        (doc: Document) => doc._id !== did,
      );
      if (documentStore.document === undefined) {
        return;
      } else if (did === documentStore.getDid()) {
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
      placeholder: "最多输入8个字符", // 设置输入框占位符
    },
    customClass: {
      input: "w-[40%] ml-auto mr-auto", // 你的自定义类，需要在 CSS 中定义
    },
  }).then((result) => {
    if (result.isConfirmed) {
      const newTag = result.value; // 获取用户输入的新标签
      if (newTag) {
        const doc = documentsList.value.find(
          (doc: Document) => doc._id === did,
        );
        if (doc) {
          doc.tag = newTag; // 更新文档的标签
          documentStore.changeTag(newTag); // 更新当前文档的标签
          const update = new Date().toISOString();
          doc.updateTime = update;
          update_tag(did, newTag, update);
        }
      }
    }
  });
};
watch(filterDocList, (newDocList) => {
  count.value = newDocList.length;
});

const createShow = ref(false);
const createTitle = ref("");
const createTag = ref("");

const templateShow = ref(false);
const templateTitle = ref("");
const templateTag = ref("");

function createOneDoc() {
  createShow.value = true;
}

function createConfirm() {
  const title = createTitle.value;
  const tag = createTag.value;
  const share_id = nanoid();
  const createTime = new Date().toISOString();
  const uid = userStore.user?.uid;
  if (title === "" || title === " ") {
    ElMessage({
      message: "请输入标题",
      type: "warning",
    });
  } else {
    createShow.value = false;
    const doc: Document = {
      _id: "",
      updateTime: createTime,
      createTime: createTime,
      share_id: share_id,
      tag: tag,
      title: title,
      is_shared: false,
    };
    createDocument(uid, doc);
  }
}

const templateId = ref("")
function templateOneDoc() {
  templateShow.value = true;
  showTemplates();
}

function templateConfirm() {
  const title = templateTitle.value;
  const tag = templateTag.value;
  const share_id = nanoid();
  const createTime = new Date().toISOString();
  const selectedTemplate = templatesList.value.find(
    (template) => template._id === templateId.value,
  );
  if (!selectedTemplate) {
    ElMessage({
      message: "模板不存在",
      type: "error",
    });
    return;
  }

  if (!title.trim()) {
    ElMessage({
      message: "请输入标题",
      type: "warning",
    });
    return;
  }
  templateShow.value = false;
  const doc: Document = {
    _id: "",
    updateTime: createTime,
    createTime: createTime,
    share_id: share_id,
    tag: tag,
    title: title,
    content: selectedTemplate.content, // 使用找到的模板对象的 content
    is_shared: false,
  };
  applyTemplate(doc);
}

const virtualScroller = ref();
const scrollToCurrentDocumentRef = (currentDid: string) => {
  scrollToCurrentDocument(currentDid);
};

function scrollToCurrentDocument(currentDid: string) {
  const index = filterDocList.value.findIndex(
    (doc: Document) => doc._id === currentDid,
  );
  if (index !== -1) {
    virtualScroller.value.scrollToIndex(index);
  }
}

onMounted(() => {
  getAllDocuments();
  emitter.on("create-doc", createOneDoc);
  emitter.on("apply-template", templateOneDoc);
  emitter.on("locate-current", scrollToCurrentDocumentRef);
  emitter.on("header-delete-doc", deleteDoc);
  emitter.on("header-rename-doc", renameDoc);
  emitter.on("header-change-tag", changeTag);
});
onUnmounted(() => {
  emitter.off("create-doc", createOneDoc);
  emitter.off("apply-template", templateOneDoc);
  emitter.off("locate-current", scrollToCurrentDocumentRef);
  emitter.off("header-delete-doc", deleteDoc);
  emitter.off("header-rename-doc", renameDoc);
  emitter.off("header-change-tag", changeTag);
});
</script>

<template>
  <el-dialog v-model="createShow" title="创建文档" width="300">
    <el-form :model="true">
      <el-form-item label="文档标题">
        <el-input v-model="createTitle" autocomplete="off" />
      </el-form-item>
      <el-form-item label="文档标签">
        <el-input v-model="createTag" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="createShow = false">取消</el-button>
        <el-button type="primary" @click="createConfirm"> 确认</el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="templateShow" title="应用模板" width="300">
    <el-form :model="true">
      <el-form-item label="模板选择">
        <el-select v-model="templateId">
          <el-option
            v-for="template in templatesList"
            :key="template._id"
            :label="template.title"
            :value="template._id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="文档标题">
        <el-input v-model="templateTitle" autocomplete="off" />
      </el-form-item>
      <el-form-item label="文档标签">
        <el-input v-model="templateTag" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="templateShow = false">取消</el-button>
        <el-button type="primary" @click="templateConfirm"> 确认</el-button>
      </div>
    </template>
  </el-dialog>

  <div class="mt-4 flex h-auto flex-row gap-2">
    <label
      class="input input-bordered flex h-8 w-[82%] items-center gap-2 pl-2 pr-0.5 text-[12px]"
    >
      <i class="pi pi-search"></i>
      <input
        v-model="searchQuery"
        class="grow"
        placeholder="输入标题"
        type="text"
      />
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
