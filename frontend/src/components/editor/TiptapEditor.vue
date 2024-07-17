<script lang="ts" setup>
import ButtonGroup from "primevue/buttongroup";
import { marked } from 'marked';
import Button from "primevue/button";
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
import http from "@/utils/requests.ts";
import { ElMessage } from "element-plus";

const documentStore = useDocumentStore();

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

const bubbleTextResult = ref();
// 调用ai部分功能
const callAi = async (e: any) => {
  let text: string | undefined = "";
  if (e !== 4) {
    const { state } = editor.value!;
    const { from, to } = state.selection;
    text = state.doc.textBetween(from, to, " ");
  } else {
    text = editor.value?.getHTML();
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
    const reader = response.body!.getReader();
    let returnText = "";
    while (true) {
      const { done, value } = await reader.read();
      const chunk = new TextDecoder().decode(value);
      returnText += chunk;
      bubbleTextResult.value.innerHTML = marked.parse(returnText);
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

const updateContent = async () => {
  editor.value!.commands.setContent(
    `<h1><span style="color:#ec6a52;">正在读取文本内容...</span></h1>`,
  );
  await getContent();
  editor.value!.commands.setContent(documentStore.document?.content!);
  loadHeadings();
};

onMounted(() => {
  emitter.on("change-content", updateContent);
  emitter.on("structure-sort", structureSort);
});

onUnmounted(() => {
  editor.value!.destroy();
  emitter.off("change-content", updateContent);
  emitter.off("structure-sort", structureSort);
});
</script>
<template>
  <dialog id="answerDialog" ref="resultDialog" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button class="btm-circle btn btn-ghost btn-sm absolute right-2 top-2" @click="bubbleCancel">
          <i class="ri-close-line"></i>
        </button>
      </form>
      <h3 class="alidongfang text-lg font-bold">AI回答</h3>
      <span class="opposans py-4" ref="bubbleTextResult"></span>
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
