<script lang="ts" setup>
import { EditorContent, useEditor, VueNodeViewRenderer } from "@tiptap/vue-3";
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
import { Heading } from "@tiptap/extension-heading";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import TaskItem from "@tiptap/extension-task-item";
import TaskList from "@tiptap/extension-task-list";
import FontFamily from "@tiptap/extension-font-family";

import Typography from "@tiptap/extension-typography";
import Underline from "@tiptap/extension-underline";
import Subscript from "@tiptap/extension-subscript";
import Superscript from "@tiptap/extension-superscript";
import { onMounted, onUnmounted } from "vue";
import EditorMenu from "@/components/editor/editorbody/EditorMenu.vue";
import { CodeBlockLowlight } from "@tiptap/extension-code-block-lowlight";
import TextStyle from "@tiptap/extension-text-style";
import FontSize from "tiptap-extension-font-size";
import CodeBlockComponent from "@/components/editor/editorbody/CodeBlockComponent.vue";
import Color from "@tiptap/extension-color";
import Highlight from "@tiptap/extension-highlight";
import Link from "@tiptap/extension-link";

const lowlight = createLowlight();
lowlight.register({ html, ts, css, js, python, java, json, c });

const loadHeadings = () => {
  const headings = [] as any[];
  if (!editor.value) return;
  const transaction = editor.value.state.tr;
  if (!transaction) return;

  editor.value?.state.doc.descendants((node, pos) => {
    if (node.type.name === "heading") {
      const start = pos;
      const end = pos + node.content.size;
      const id = `heading-${headings.length + 1}`;
      if (node.attrs.id !== id) {
        transaction?.setNodeMarkup(pos, undefined, {
          ...node.attrs,
          id,
        });
      }
      headings.push({
        level: node.attrs.level,
        text: node.textContent,
        start,
        end,
        id,
      });
    }
  });
  transaction?.setMeta("addToHistory", false);
  transaction?.setMeta("preventUpdate", true);
  editor.value?.view.dispatch(transaction);
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
    Heading,
  ],
  injectCSS: false,
  autofocus: true,
  onUpdate({ editor }) {
    loadHeadings();
  },
  onCreate({ editor }) {
    loadHeadings();
  },
});

// defineExpose({
//   insert: (text) => {
//     editor.value
//       ?.chain()
//       .focus()
//       .command(({ tr }) => {
//         // 在事务中执行以下代码
//         tr.insertText(text);
//         return true;
//       })
//       .run();
//   },
// });

onMounted(() => {});

onUnmounted(() => {
  editor.value!.destroy();
});
</script>
<template>
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
      <div
        class="relative h-full w-full overflow-y-hidden border-l-[1px] border-solid border-l-[--border-color] bg-[--small-doc] pb-10 pt-10"
      >
        <h1
          class="misans absolute top-2 w-full border-b-[2px] border-solid border-b-[--border-color] text-3xl font-bold"
        >
          内容大纲
        </h1>
        <div class="m-2 h-full overflow-y-scroll">
          <ul class="menu w-full rounded-box">
            <li><a class="opposans">Item 1</a></li>
            <li>
              <a>Parent</a>
              <ul>
                <li><a>Submenu 1</a></li>
                <li><a>Submenu 2</a></li>
                <li>
                  <a>Parent</a>
                  <ul>
                    <li><a>Submenu 1</a></li>
                    <li><a>Submenu 2</a></li>
                  </ul>
                </li>
              </ul>
            </li>
            <li><a>Item 3</a></li>
          </ul>
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
