<script lang="ts" setup>
import ButtonGroup from "primevue/buttongroup";
import { marked } from "marked";
import Button from "primevue/button";
import { useUserStore } from "@/store/user.js";
import { ElLoading, ElMessage, ElMessageBox, UploadFile } from "element-plus";
import {
  BubbleMenu,
  EditorContent,
  useEditor,
  VueNodeViewRenderer,
} from "@tiptap/vue-3";
// 表格
import Table from "@tiptap/extension-table";
import TableCell from "@tiptap/extension-table-cell";
import TableHeader from "@tiptap/extension-table-header";
import TableRow from "@tiptap/extension-table-row";
// 列表
import ListItem from "@tiptap/extension-list-item";
import OrderedList from "@tiptap/extension-ordered-list";
import BulletList from "@tiptap/extension-bullet-list";

import { TextAlign } from "@tiptap/extension-text-align";
// 媒体
import Image from "@tiptap/extension-image";
// code
import css from "highlight.js/lib/languages/css";
import js from "highlight.js/lib/languages/javascript";
import ts from "highlight.js/lib/languages/typescript";
import html from "highlight.js/lib/languages/xml";
import python from "highlight.js/lib/languages/python";
import java from "highlight.js/lib/languages/java";
import json from "highlight.js/lib/languages/json";
import c from "highlight.js/lib/languages/c";
import { createLowlight } from "lowlight";
// 字数统计
import CharacterCount from "@tiptap/extension-character-count";
import Heading from "@tiptap/extension-heading";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import TaskItem from "@tiptap/extension-task-item";
import TaskList from "@tiptap/extension-task-list";
import FontFamily from "@tiptap/extension-font-family";

import Typography from "@tiptap/extension-typography";
import Underline from "@tiptap/extension-underline";
import Subscript from "@tiptap/extension-subscript";
import Superscript from "@tiptap/extension-superscript";
import { onMounted, onUnmounted, ref } from "vue";
import EditorMenu from "@/components/editor/editorbody/EditorMenu.vue";
import { CodeBlockLowlight } from "@tiptap/extension-code-block-lowlight";
import TextStyle from "@tiptap/extension-text-style";
import FontSize from "tiptap-extension-font-size";
import CodeBlockComponent from "@/components/editor/editorbody/CodeBlockComponent.vue";
import Color from "@tiptap/extension-color";
import Highlight from "@tiptap/extension-highlight";
import Link from "@tiptap/extension-link";
import OutlineList from "@/components/editor/editorbody/OutlineList.vue";

import { useDocumentStore } from "@/store/document.ts";
import emitter from "@/hooks/mitter.js";
import { useDocument } from "@/hooks/useDocument.js";
import Swal from "sweetalert2";

const documentStore = useDocumentStore();
const userStore = useUserStore();

const { getContent } = useDocument();

const lowlight = createLowlight();
lowlight.register({ html, ts, css, js, python, java, json, c });

const headings = ref<any>([]);
const loadHeadings = () => {
  // 获取整个文档结构
  const doc = editor.value?.getJSON();
  if (!doc) return;
  headings.value = doc.content?.reduce((accumulator, node) => {
    const processNode = (n: any) => {
      if (n.type === "heading" && n.content && Array.isArray(n.content)) {
        const level = parseInt(n.attrs.level, 10);
        const text = n.content[0].text;
        console.log(text);
        accumulator.push({
          level: level,
          text: text,
        });
      }
    };
    processNode(node);
    return accumulator;
  }, []);
};

// 编辑器初始化
const editor = useEditor({
  content: ``,
  extensions: [
    StarterKit,
    TaskList,
    TaskItem,
    Placeholder.configure({
      placeholder: "开始输入文本 …",
    }),
    Table.configure({
      resizable: true,
    }),
    TableRow,
    TableHeader,
    TableCell,
    OrderedList,
    BulletList,
    ListItem,
    Image,
    Typography,
    Underline,
    Subscript,
    Superscript,
    CodeBlockLowlight.extend({
      addNodeView() {
        return VueNodeViewRenderer(CodeBlockComponent);
      },
    }).configure({ lowlight }),
    TextAlign.configure({
      types: ["heading", "paragraph"],
    }),
    FontFamily,
    TextStyle,
    FontSize,
    Color,
    Highlight.configure({ multicolor: true }),
    Link.configure({
      autolink: false,
      linkOnPaste: true,
      protocols: ["https", "http", "mailto"],
      validate: (href) => /^https?:\/\//.test(href),
    }),
    CharacterCount.configure({
      limit: 100000,
    }),
    Heading.configure({
      levels: [1, 2, 3, 4],
    }),
  ],
  injectCSS: false,
  autofocus: true,
  onUpdate({ editor }) {
    loadHeadings();
    documentStore.setDocumentContent(editor.getJSON());
  },
  onCreate({ editor }) {
    loadHeadings();
  },
});
const resultDialog = ref();
const selectBubble = ref(false);
const selectOption = ref(-1);
const promptText = ref("");
const ocrDialog = ref();
const libDialog = ref(false);
const voiceDialog = ref();
const dialogImageUrl = ref("");
const dialogVisible = ref(false);
const disabled = ref(false);
const fileList = ref<UploadFile[]>([]);
const upload_btn = ref(false);
const boxdisplay = ref(true);
const ocrText = ref("");

const isValidFileType = (filename: String) => {
  const validTypes = ["txt", "pdf", "csv", "xlsx", "xls", "docx", "doc"];
  const fileType = filename.split(".").pop()?.toLowerCase();
  return validTypes.includes(fileType);
};
const libList = ref<UploadFile[]>([]);

const handleFileChange = (file: UploadFile, fileList: UploadFile[]) => {
  if (isValidFileType(file.name)) {
    libList.value = fileList;
  } else {
    Swal.fire({
      text: "不支持的文件类型",
      icon: "warning",
      timer: 2000,
      timerProgressBar: true,
    });
  }
};

const libUpload = () => {
  libDialog.value = true;
};

const libBeforeRemove = (file: UploadFile, libList: UploadFile[]) => {
  return new Promise((resolve, reject) => {
    ElMessageBox.confirm("此操作将删除该文件, 是否继续?", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(() => {
        resolve(true);
      })
      .catch(() => {
        reject(false);
      });
  });
};

// 删除文件时的逻辑
const libHandleRemove = (file: UploadFile, fileList: UploadFile[]) => {
  const index = libList.value.findIndex((f) => f.uid === file.uid);
  if (index !== -1) {
    libList.value.splice(index, 1);
  }
};

const libHandleSuccess = (file: UploadFile, libList: UploadFile[]) => {
  ElMessage({ message: "文件上传成功", type: "success" });
};

const loading = ref(false);

const doLib = async () => {
  if (!libList.value.length) {
    await Swal.fire({
      text: "请选择文件",
      icon: "info",
      toast: true,
      position: "top",
      timer: 2000,
      timerProgressBar: true,
    });
    return;
  } // 如果没有文件，不执行上传
  const loadingInstance = ElLoading.service({
    lock: true,
    text: "上传中，请稍候...",
    background: "rgba(0, 0, 0, 0.7)",
  });
  loading.value = true;
  let formData = new FormData();
  formData.append("uid", userStore.user?.uid!);
  libList.value.map((file) => {
    formData.append("files", file.raw!);
  });
  const response = await fetch("http://localhost:5000/api/postlib", {
    method: "POST",
    body: formData,
  });

  if (response.status === 200) {
    await Swal.fire({
      text: "上传成功",
      icon: "success",
      toast: true,
      position: "top",
      timer: 2000,
      timerProgressBar: true,
    });
    loading.value = false;
    loadingInstance.close();
  } else {
    await Swal.fire({
      text: "上传失败",
      icon: "error",
      toast: true,
      position: "top",
      timer: 2000,
      timerProgressBar: true,
    });
    loading.value = false;
    loadingInstance.close();
  }
};

const handleRemove = (file: UploadFile) => {
  const index = fileList.value.findIndex((f) => f.uid === file.uid);
  if (index !== -1) {
    fileList.value.splice(index, 1);
    if (fileList.value.length === 0) {
      boxdisplay.value = true;
      upload_btn.value = false;
    }
  }
};
const beforeRemove = (file: UploadFile) => {
  return new Promise((resolve, reject) => {
    ElMessageBox.confirm("此操作将删除该图片, 是否继续?", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(() => {
        resolve(true);
      })
      .catch(() => {
        reject(false);
      });
  });
};

const handlePictureCardPreview = (file: UploadFile) => {
  dialogImageUrl.value = file.url!;
  dialogVisible.value = true;
};

const handleSuccess = () => {
  ElMessage({ message: "图片上传成功", type: "success" });
};

const handleChanges = (file: UploadFile, files: UploadFile[]) => {
  fileList.value = files;
  boxdisplay.value = false;
};

const doOCR = async () => {
  boxdisplay.value = false;
  const loadingInstance = ElLoading.service({
    lock: true,
    text: "上传中，请稍候...",
    background: "rgba(0, 0, 0, 0.7)",
  });
  loading.value = true;
  let formData = new FormData();
  formData.append("uid", userStore.user?.uid!);
  fileList.value.forEach((file) => {
    formData.append("file", file.raw!);
  });
  const response = await fetch("http://localhost:5000/api/imageOCR", {
    method: "POST",
    body: formData,
  });
  const reader = response.body!.getReader();
  loading.value = false;
  loadingInstance.close();
  while (true) {
    const { done, value } = await reader.read();
    const chunk = new TextDecoder().decode(value);
    ocrText.value += chunk;
    if (done) {
      break;
    }
  }
  reader.releaseLock();
};

const bubbleTextResult = ref();
// 调用ai部分功能
const callAi = async (e: any) => {
  let text: string | undefined = "";
  if (e === 4 || e === 6 || e === 7) {
    text = editor.value?.getHTML();
  } else {
    const { state } = editor.value!;
    const { from, to } = state.selection;
    text = state.doc.textBetween(from, to, " ");
  }
  if (e === 6 || e === 7) {
    if (text == "") {
      await Swal.fire({
        text: "请填入您的需求",
        icon: "error",
        toast: true,
        position: "top",
        timer: 2000,
        timerProgressBar: true,
      });
    }
  }
  const response = await fetch("http://localhost:5000/api/bubblechat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type: e,
      content: text,
      promptText: promptText.value,
    }),
  });
  const aiBP = document.createElement("p");
  bubbleTextResult.value.appendChild(aiBP);
  const reader = response.body!.getReader();
  let returnText = "";
  while (true) {
    const { done, value } = await reader.read();
    const chunk = new TextDecoder().decode(value);
    returnText += chunk;
    aiBP.innerHTML = <string>marked.parse(returnText);
    if (done) {
      break;
    }
  }
  reader.releaseLock();
  selectOption.value = -1;
};

function bubbleCancel() {
  selectOption.value = -1;
  selectBubble.value = false;
  promptText.value = "";
  bubbleTextResult.value.innerHTML = null;
}

function ocrCancel() {
  fileList.value = [];
  ocrDialog.value.close();
  ocrText.value = "";
}

function bubbleAI() {
  selectBubble.value = false;
  resultDialog.value.showModal();
  callAi(selectOption.value);
  promptText.value = "";
  selectOption.value = -1;
}

function clipResult() {
  navigator.clipboard.writeText(bubbleTextResult.value.innerText);
  ElMessage({
    message: "成功复制到剪切板",
    type: "success",
  });
}

const structureSort = () => {
  selectBubble.value = true;
  selectOption.value = 4;
};

const tableRecognise = () => {
  selectBubble.value = true;
  selectOption.value = 5;
};

const umlRecognise = () => {
  Swal.fire({
    text: "请事先输入您的UML类型和UML需求",
    icon: "info",
    showConfirmButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    showCancelButton: true,
  }).then((result) => {
    if (result.isConfirmed) {
      selectBubble.value = true;
      selectOption.value = 6;
    }
  });
};

const mindRecognise = () => {
  Swal.fire({
    text: "请尽量以多重无序列表的格式作为您的思维导图基础内容",
    icon: "info",
    showConfirmButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    showCancelButton: true,
  }).then((result) => {
    if (result.isConfirmed) {
      selectBubble.value = true;
      selectOption.value = 7;
    }
  });
};

const aiTalking = () => {
  openAItalk.value = true;
};

const ocrRecognise = () => {
  ocrDialog.value.showModal();
};

const voiceText = ref(""); // 内容
const isRecording = ref(false); // 是否录音
const audioChunks = ref([]); // 录音的音频数据
const recordedAudio = ref();
const uploadAudio = ref(false); // 是否允许上传
let mediaRecorder; // 媒体相关情况
let stream; // 存储媒体流

function voiceCancel() {
  // 取消的时候，实际上应该把浏览器的录音状态也关闭
  voiceText.value = "";
  voiceDialog.value.close();
  isRecording.value = false;
  uploadAudio.value = false;

  if (mediaRecorder!) {
    mediaRecorder.stop(); // 停止录音
  }

  if (stream!) {
    stream.getTracks().forEach((track) => track.stop()); // 停止媒体流
    stream = null;
  }
}

const voiceRecognise = () => {
  // 打开模态框
  voiceDialog.value.showModal();
};

const startVoice = async () => {
  isRecording.value = true;
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      audioChunks.value.push(event.data);
    }
  };
  mediaRecorder.start();
  voiceText.value = "正在录音...";
  isRecording.value = true;
};

const endVoice = () => {
  mediaRecorder!.onstop = async () => {
    const audioBlob = new Blob(audioChunks.value, { type: "audio/wav" });
    recordedAudio.value = audioBlob;
    audioChunks.value = []; // 清空audioChunks
    voiceText.value = "录音结束";
    isRecording.value = false;
    uploadAudio.value = true;

    stream!.getTracks().forEach((track) => track.stop()); // 停止媒体流
    stream = null;
  };
  mediaRecorder!.stop(); // 使用全局变量mediaRecorder
};

const uploadVoice = async () => {
  let formData = new FormData();
  formData.append("uid", userStore.user?.uid!);
  if (recordedAudio.value) {
    formData.append("audio", recordedAudio.value);
    try {
      const response = await fetch("http://localhost:5000/api/asr", {
        method: "POST",
        body: formData,
      });
      const reader = response.body!.getReader();
      voiceText.value = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        const chunk = new TextDecoder().decode(value);
        voiceText.value += chunk;
      }
      reader.releaseLock();
      uploadAudio.value = false;
    } catch (error) {
      console.error("Error during fetch:", error);
      voiceText.value = "上传失败";
    }
  } else {
    voiceText.value = "没有录音文件";
  }
};

const exportPdf = async () => {
  const bodyEditor = editor.value?.getHTML();
  const printWindow = window.open(
    "about:blank",
    "打印窗口",
    "width=1200,height=900",
  );
  printWindow.document.write(bodyEditor);
  printWindow.document.close();
  printWindow.print();
};

const openAItalk = ref(false);
const sendAiQuestion = ref("");
const chatAnswer = ref("");
const aiTalkDialog = ref();

function cancelAiMessage() {
  sendAiQuestion.value = "";
  openAItalk.value = false;
}

const sendAiMessage = async () => {
  const userMessageDiv = document.createElement("div");
  userMessageDiv.className = "flex flex-row px-4 py-8 sm:px-6";
  const userImg = document.createElement("img");
  userImg.className = "mr-2 flex h-8 w-8 rounded-full sm:mr-4";
  userImg.src = "src/assets/icons/talkuser.svg";
  const userText = document.createElement("div");
  userText.className = "flex max-w-3xl items-center";
  const userP = document.createElement("p");
  userP.className = "opposans";
  let text: string | undefined = sendAiQuestion.value;
  userP.textContent = text;
  userText.appendChild(userP);
  userMessageDiv.appendChild(userImg);
  userMessageDiv.appendChild(userText);
  aiTalkDialog.value.appendChild(userMessageDiv);
  sendAiQuestion.value = "";

  const aiMessageDiv = document.createElement("div");
  aiMessageDiv.className =
    "flex bg-slate-100 px-4 py-8 dark:bg-slate-900 sm:px-6";
  const aiImg = document.createElement("img");
  aiImg.className = "mr-2 flex h-8 w-8 rounded-full sm:mr-4";
  aiImg.src = "src/assets/icons/talkai.svg";
  const aiText = document.createElement("div");
  aiText.className =
    "flex w-full flex-col items-start lg:flex-row lg:justify-between";
  const aiP = document.createElement("p");
  aiP.className = "max-w-3xl opposans";
  aiText.appendChild(aiP);
  aiMessageDiv.appendChild(aiImg);
  aiMessageDiv.appendChild(aiText);
  aiTalkDialog.value.appendChild(aiMessageDiv);

  const response = await fetch("http://localhost:5000/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content: text,
      uid: userStore.user?.uid,
    }),
  });
  const reader = response.body!.getReader();
  let returnText = "";
  while (true) {
    const { done, value } = await reader.read();
    const chunk = new TextDecoder().decode(value);
    returnText += chunk;
    aiP.innerHTML = <string>marked.parse(returnText);
    if (done) {
      break;
    }
  }
  reader.releaseLock();
};

const updateContent = async () => {
  editor.value!.commands.setContent(
    `<h1><span style="color:#ec6a52;">正在读取文本内容...</span></h1>`,
  );
  await getContent();
  editor.value!.commands.setContent(documentStore.document?.content!);
  loadHeadings();
};

const showLoading = () => {
  ElLoading.service({
    lock: true,
    text: "导出中，请稍候...",
    background: "rgba(0, 0, 0, 0.7)",
  });
};

onMounted(() => {
  emitter.on("change-content", updateContent);
  emitter.on("refresh", updateContent);
  emitter.on("structure-sort", structureSort);
  emitter.on("ai-talking", aiTalking);
  emitter.on("ocr-recognise", ocrRecognise);
  emitter.on("lib-upload", libUpload);
  emitter.on("voice-recognise", voiceRecognise);
  emitter.on("uml-recognise", umlRecognise);
  emitter.on("mind-recognise", mindRecognise);
  emitter.on("table-recognise", tableRecognise);
  emitter.on("export-pdf", exportPdf);
});

onUnmounted(() => {
  editor.value!.destroy();
  emitter.off("change-content", updateContent);
  emitter.off("refresh", updateContent);
  emitter.off("structure-sort", structureSort);
  emitter.off("ai-talking", aiTalking);
  emitter.off("ocr-recognise", ocrRecognise);
  emitter.off("lib-upload", libUpload);
  emitter.off("voice-recognise", voiceRecognise);
  emitter.off("uml-recognise", umlRecognise);
  emitter.off("mind-recognise", mindRecognise);
  emitter.off("table-recognise", tableRecognise);
  emitter.off("export-pdf", exportPdf);
});
</script>
<template>
  <div v-show="openAItalk" class="fixed z-[999] flex h-[80%] w-[70%] flex-col">
    <div
      ref="aiTalkDialog"
      class="flex-1 overflow-y-auto bg-slate-300 text-sm leading-6 text-slate-900 shadow-md sm:text-base sm:leading-7 dark:bg-slate-800 dark:text-slate-300"
    ></div>
    <!-- Prompt message input -->
    <div
      class="flex w-full items-center rounded-b-md border-t border-slate-300 bg-slate-200 p-2 dark:border-slate-700 dark:bg-slate-900"
    >
      <label class="sr-only" for="chat">输入</label>
      <textarea
        id="chat-input"
        v-model="sendAiQuestion"
        class="mx-2 flex min-h-full w-full rounded-md border border-slate-300 bg-slate-50 p-2 text-base text-slate-900 placeholder-slate-400 focus:border-blue-600 focus:outline-none focus:ring-1 focus:ring-blue-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-50 dark:placeholder-slate-400 dark:focus:border-blue-600 dark:focus:ring-blue-600"
        placeholder="输入文本"
        rows="3"
      ></textarea>
      <div>
        <button
          class="inline-flex hover:text-blue-600 sm:p-2 dark:text-slate-200 dark:hover:text-blue-600"
          @click="sendAiMessage"
        >
          <i class="ri-send-plane-line"></i>
          <span class="sr-only">Send message</span>
        </button>
      </div>
      <div>
        <button
          class="inline-flex hover:text-blue-300 sm:p-2 dark:text-slate-200 dark:hover:text-blue-600"
          @click="cancelAiMessage"
        >
          <i class="ri-close-circle-line"></i>
        </button>
      </div>
    </div>
  </div>

  <dialog ref="voiceDialog" class="model">
    <div class="modal-box">
      <form method="dialog">
        <button
          class="btm-circle btn btn-ghost btn-sm absolute right-2 top-2"
          @click="voiceCancel"
        >
          <i class="ri-close-line text-[--daisyui-color]"></i>
        </button>
      </form>
      <h3 class="alidongfang text-lg font-bold text-[--daisyui-color]">
        语音录制
      </h3>
      <span class="text-[--daisyui-color]">{{ voiceText }}</span>
      <form class="top-2 flex justify-end">
        <button
          :disabled="isRecording"
          class="opposans btn ml-2"
          @click.prevent="startVoice"
        >
          <i class="ri-mic-line"></i>开始
        </button>
        <button
          :disabled="!isRecording"
          class="opposans btn ml-2"
          @click.prevent="endVoice"
        >
          <i class="ri-mic-off-line"></i>停止
        </button>
        <button
          :disabled="!uploadAudio"
          class="opposans btn ml-2"
          @click.prevent="uploadVoice"
        >
          <i class="ri-upload-line"></i>上传
        </button>
      </form>
    </div>
  </dialog>

  <div
    v-show="libDialog"
    class="fixed left-1/2 top-1/4 h-[450px] w-[600px] -translate-x-1/2 rounded-[8px] bg-[--panel-color]"
  >
    <div class="flex flex-row justify-between p-2">
      <h3 class="alidongfang text-[24px] font-bold">本地知识库上传</h3>
      <button
        class="btn btn-circle btn-ghost btn-sm"
        @click="libDialog = false"
      >
        <i class="ri-close-line text-[24px]"></i>
      </button>
    </div>
    <el-upload
      :auto-upload="false"
      :before-remove="libBeforeRemove"
      :file-list="libList"
      :on-change="handleFileChange"
      :on-progress="showLoading"
      :on-remove="libHandleRemove"
      :on-success="libHandleSuccess"
      accept=".xls,.xlsx,.pdf,.doc,.docx,.txt"
      action="#"
      multiple
    >
      <template #trigger>
        <button class="opposans btn btn-secondary btn-sm m-2">
          <i class="ri-add-box-line"></i>添加
        </button>
      </template>
      <button class="opposans btn btn-primary btn-sm m-2" @click="doLib">
        <i class="ri-upload-line"></i>上传
      </button>
    </el-upload>
  </div>

  <dialog ref="ocrDialog" class="modal">
    <div class="modal-box h-[500px]">
      <form method="dialog">
        <button
          class="btm-circle btn btn-ghost btn-sm absolute right-2 top-2"
          @click="ocrCancel"
        >
          <i class="ri-close-line"></i>
        </button>
      </form>
      <h3 class="alidongfang text-lg font-bold">OCR上传</h3>
      <el-upload
        :auto-upload="false"
        :before-remove="beforeRemove"
        :file-list="fileList"
        :on-change="handleChanges"
        :on-progress="showLoading"
        :on-success="handleSuccess"
        accept="image/*"
        action="#"
        limit="1"
        list-type="picture-card"
      >
        <el-icon>
          <i class="ri-image-add-line"></i>
        </el-icon>
        <template #file="{ file }">
          <div>
            <img :src="file.url" class="el-upload-list__item-thumbnail" />
            <span class="el-upload-list__item-actions">
              <span
                class="el-upload-list__item-preview"
                @click="handlePictureCardPreview(file)"
              >
                <el-icon><i class="ri-zoom-in-line"></i></el-icon>
              </span>
              <span
                v-if="!disabled"
                class="el-upload-list__item-delete"
                @click="handleRemove(file)"
              >
                <el-icon><i class="ri-delete-bin-7-line"></i></el-icon>
              </span>
            </span>
          </div>
        </template>
      </el-upload>
      <form class="top-2 flex justify-end">
        <button
          v-show="!boxdisplay"
          class="opposans btn btn-primary"
          @click.prevent="doOCR"
        >
          <i class="ri-upload-line"></i>上传
        </button>
      </form>
      {{ ocrText }}
      <el-dialog v-model="dialogVisible">
        <img :src="dialogImageUrl" alt="Preview Image" w-full />
      </el-dialog>
    </div>
  </dialog>
  <dialog id="answerDialog" ref="resultDialog" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button
          class="btm-circle btn btn-ghost btn-sm absolute right-2 top-2"
          @click="bubbleCancel"
        >
          <i class="ri-close-line"></i>
        </button>
      </form>
      <h3 class="alidongfang text-lg font-bold">AI回答</h3>
      <div ref="bubbleTextResult" class="opposans py-4"></div>
      <form class="top-2 flex justify-end">
        <button class="opposans btn" @click.prevent="clipResult">
          <i class="ri-clipboard-line"></i>复制
        </button>
      </form>
    </div>
  </dialog>

  <div
    v-show="selectBubble"
    class="fixed right-1/2 top-1/4 z-20 w-96 max-w-5xl translate-x-1/2 rounded-lg bg-slate-200 dark:bg-slate-900"
  >
    <div
      class="rounded-lg rounded-b-none border border-slate-300 bg-slate-50 px-2 py-2 dark:border-slate-700 dark:bg-slate-800"
    >
      <label class="opposans sr-only" for="prompt-input">输入Prompt</label>
      <textarea
        id="prompt-input"
        v-model="promptText"
        class="opposans w-full border-0 bg-slate-50 px-0 text-base text-slate-900 focus:outline-none dark:bg-slate-800 dark:text-slate-200 dark:placeholder-slate-400"
        placeholder="输入 Prompt"
        required
        rows="6"
      ></textarea>
    </div>
    <div class="ml-2 flex items-center justify-end py-2 pr-2">
      <div>
        <button
          class="opposans inline-flex items-center gap-x-2 rounded-lg bg-blue-600 px-4 py-2.5 text-center text-base font-medium text-slate-50 hover:bg-blue-800 focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900"
          @click="bubbleAI"
        >
          发送
          <i class="ri-send-plane-line"></i>
        </button>
        <button
          class="opposans ml-2 inline-flex items-center gap-x-2 rounded-lg bg-slate-700 px-4 py-2.5 text-center text-base font-medium text-slate-50 hover:bg-blue-600 focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900"
          type="button"
          @click="bubbleCancel"
        >
          取消
          <i class="ri-close-line"></i>
        </button>
      </div>
    </div>
  </div>
  <div class="h-[90%]">
    <div
      class="h-[8%] w-full border-b-[1px] border-solid border-b-[--border-color]"
    >
      <EditorMenu :editor="editor" />
    </div>
    <div class="flex h-[92%] w-full flex-row">
      <EditorContent
        :editor="editor"
        class="prose prose-base min-w-[80%] overflow-y-auto p-2 focus:outline-none"
      />
      <BubbleMenu
        v-if="editor"
        :editor="editor"
        :tippy-options="{ placement: 'bottom' }"
      >
        <ButtonGroup>
          <Button
            icon="ri-bubble-chart-line"
            label="摘要"
            severity="secondary"
            size="small"
            @click="
              selectOption = 0;
              selectBubble = true;
            "
          />
          <Button
            icon="ri-magic-line"
            label="美化"
            severity="secondary"
            size="small"
            @click="
              selectOption = 1;
              selectBubble = true;
            "
          />
          <Button
            icon="ri-expand-diagonal-line"
            label="续写"
            severity="secondary"
            size="small"
            @click="
              selectOption = 2;
              selectBubble = true;
            "
          />
          <Button
            icon="ri-translate"
            label="翻译"
            severity="secondary"
            size="small"
            @click="
              selectOption = 3;
              selectBubble = true;
            "
          />
        </ButtonGroup>
      </BubbleMenu>
      <div
        class="relative h-full w-full overflow-y-hidden border-l-[1px] border-solid border-l-[--border-color] bg-[--small-doc] pb-10 pt-10"
      >
        <h1
          class="misans absolute top-2 w-full border-b-[2px] border-solid border-b-[--border-color] text-3xl font-bold text-[--small-text]"
        >
          内容大纲
        </h1>
        <div class="m-2 h-full overflow-y-scroll">
          <OutlineList :headings="headings"></OutlineList>
        </div>
        <h1
          class="misans absolute bottom-1 w-full border-t-[2px] border-solid border-t-[--border-color] bg-[--panel-color] text-xl font-bold"
        >
          字符
          {{ editor?.storage.characterCount.characters() }}
        </h1>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
b {
  font-weight: bold;
}

.ProseMirror {
  overflow-y: scroll;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.ProseMirror p {
  margin: 0;
}

.ProseMirror:focus {
  outline: none;
}

.tiptap p.is-editor-empty:first-child::before {
  color: #adb5bd;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}

.tiptap {
  > * + * {
    margin-top: 0.1em;
  }

  table {
    border-collapse: collapse;
    table-layout: fixed;
    width: 100%;
    margin: 0;
    overflow: hidden;

    td,
    th {
      min-width: 1em;
      border: 2px solid #ced4da;
      padding: 3px 5px;
      vertical-align: top;
      box-sizing: border-box;
      position: relative;

      > * {
        margin-bottom: 0;
      }
    }

    th {
      font-weight: bold;
      text-align: left;
      background-color: #f1f3f5;
    }

    .selectedCell:after {
      z-index: 2;
      position: absolute;
      content: "";
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      background: rgba(200, 200, 255, 0.4);
      pointer-events: none;
    }

    .column-resize-handle {
      position: absolute;
      right: -2px;
      top: 0;
      bottom: -2px;
      width: 4px;
      background-color: #adf;
      pointer-events: none;
    }

    p {
      margin: 0;
    }
  }

  pre {
    background: #0d0d0d;
    color: #fff;
    font-family: "JetBrainsMono", monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }

    .hljs-comment,
    .hljs-quote {
      color: #616161;
    }

    .hljs-variable,
    .hljs-template-variable,
    .hljs-attribute,
    .hljs-tag,
    .hljs-name,
    .hljs-regexp,
    .hljs-link,
    .hljs-name,
    .hljs-selector-id,
    .hljs-selector-class {
      color: #f98181;
    }

    .hljs-number,
    .hljs-meta,
    .hljs-built_in,
    .hljs-builtin-name,
    .hljs-literal,
    .hljs-type,
    .hljs-params {
      color: #fbbc88;
    }

    .hljs-string,
    .hljs-symbol,
    .hljs-bullet {
      color: #b9f18d;
    }

    .hljs-title,
    .hljs-section {
      color: #faf594;
    }

    .hljs-keyword,
    .hljs-selector-tag {
      color: #70cff8;
    }

    .hljs-emphasis {
      font-style: italic;
    }

    .hljs-strong {
      font-weight: 700;
    }
  }
}

.tableWrapper {
  overflow-x: auto;
}

.resize-cursor {
  cursor: ew-resize;
}
</style>
