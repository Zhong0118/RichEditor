<template>
  <div class="flex h-full flex-wrap items-center justify-center">
    <button
      class="opposans btn btn-outline border-2 border-dashed btn-success mb-auto mr-2 mt-auto h-[32px] min-h-[32px] pl-[1px] pr-[1px] text-xs"
    >
      <span class="iconfont icon-wenku text-[--daisyui-color]">知识库</span>
    </button>
    <div class="dropdown">
      <div
        class="btn btn-outline border-2 border-dashed btn-success mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[72px] min-w-[72px] p-0"
        role="button"
        tabindex="0"
      >
        <i :class="aiIcon" class="text-[24px] text-[--basic3]"></i>
        <span class="text-[--basic4]">AI</span>
        <i class="ri-arrow-down-s-line text-[--basic3]"></i>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[100px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items10" class="">
          <EditorButton5 :key="index" :="item" />
        </li>
      </ul>
    </div>
    <el-divider
      direction="vertical"
      style="margin-left: 0; margin-right: 4px"
    />
    <EditorButton v-for="(item, index) in items3" :key="index" :="item" />
    <el-divider
      direction="vertical"
      style="margin-left: 0; margin-right: 4px"
    />
    <div class="dropdown dropdown-hover">
      <div
        class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[48px] min-w-[32px] p-0"
        role="button"
        tabindex="0"
      >
        <i :class="headIcon" class="text-[18px]"></i>
        <i class="ri-arrow-down-s-line"></i>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[34px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items4">
          <EditorButton2 :key="index" :="item" />
        </li>
      </ul>
    </div>

    <div class="dropdown dropdown-hover">
      <div
        class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[48px] min-w-[32px] p-0"
        role="button"
        tabindex="0"
      >
        <i :class="fontFamilyIcon" class="text-[18px]"></i>
        <i class="ri-arrow-down-s-line"></i>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[104px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items6">
          <EditorButton3 :key="index" :="item" />
        </li>
      </ul>
    </div>

    <div class="dropdown dropdown-hover">
      <div
        class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[48px] min-w-[32px] p-0"
        role="button"
        tabindex="0"
      >
        <i :class="fontSizeIcon" class="text-[18px]"></i>
        <i class="ri-arrow-down-s-line"></i>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[84px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items7">
          <EditorButton4 :key="index" :="item" />
        </li>
      </ul>
    </div>

    <el-divider
      direction="vertical"
      style="margin-left: 0; margin-right: 4px"
    />
    <EditorButton v-for="(item, index) in items1" :key="index" :="item" />

    <el-tooltip content="字体颜色" effect="dark" placement="top">
      <button
        class="btn btn-ghost mb-auto mr-1 mt-auto flex h-[32px] min-h-[32px] w-[64px] min-w-[64px] flex-row pl-[1px] pr-[1px]"
      >
        <i class="ri-brush-line text-[18px]"></i>
        <el-color-picker
          v-model="textColor"
          :predefine="predefineColors"
          color-format="hex"
          size="small"
          @change="props.editor?.commands.setColor(textColor)"
        />
      </button>
    </el-tooltip>

    <el-tooltip content="背景颜色" effect="dark" placement="top">
      <button
        class="btn btn-ghost mb-auto mr-1 mt-auto flex h-[32px] min-h-[32px] w-[64px] min-w-[64px] flex-row pl-[1px] pr-[1px]"
      >
        <i class="ri-palette-line text-[18px]"></i>
        <el-color-picker
          v-model="bgColor"
          :predefine="preBgColors"
          color-format="hex"
          size="small"
          @change="props.editor?.commands.setHighlight({ color: bgColor })"
        />
      </button>
    </el-tooltip>

    <el-divider
      direction="vertical"
      style="margin-left: 0; margin-right: 4px"
    />
    <EditorButton v-for="(item, index) in items2" :key="index" :="item" />
    <div class="dropdown dropdown-hover">
      <div
        class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[48px] min-w-[32px] p-0"
        role="button"
        tabindex="0"
      >
        <i :class="alignIcon" class="text-[18px]"></i>
        <i class="ri-arrow-down-s-line"></i>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[34px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items5">
          <EditorButton2 :key="index" :="item" />
        </li>
      </ul>
    </div>
    <el-divider
      direction="vertical"
      style="margin-left: 0; margin-right: 4px"
    />
    <div class="dropdown">
      <div
        class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[64px] min-w-[64px] p-0"
        role="button"
        tabindex="0"
      >
        <i class="ri-apps-2-add-line text-[18px]"></i>
        <span>插入</span>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[34px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items8">
          <EditorButton2 :key="index" :="item" />
        </li>
      </ul>
    </div>

    <div class="dropdown dropdown-hover">
      <div
        class="btn btn-ghost mb-auto mr-1 mt-auto h-[32px] min-h-[32px] w-[72px] min-w-[72px] p-0"
        role="button"
        tabindex="0"
      >
        <i class="ri-grid-line text-[18px]"></i>
        <span class="text-[10px]">表格设置</span>
      </div>
      <ul
        class="menu dropdown-content right-1/2 z-[10] w-[34px] translate-x-1/2 rounded-[8px] bg-base-100 p-[2px] shadow"
        tabindex="0"
      >
        <li v-for="(item, index) in items9">
          <EditorButton2 :key="index" :="item" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Editor } from "@tiptap/vue-3";
import EditorButton from "./EditorButton.vue";
import EditorButton2 from "./EditorButton2.vue";
import EditorButton3 from "./EditorButton3.vue";
import EditorButton4 from "./EditorButton4.vue";
import EditorButton5 from "./EditorButton5.vue";
import { ref } from "vue";
import Swal from "sweetalert2";

const props = defineProps<{ editor: Editor }>();
const headIcon = ref("ri-heading");
const fontFamilyIcon = ref("ri-font-sans-serif");
const fontSizeIcon = ref("ri-font-size-2");
const alignIcon = ref("ri-timeline-view");
const aiIcon = ref("iconfont icon-aigc-s");

const textColor = ref("#000000"); // 颜色选择器的颜色值
const predefineColors = ref([
  "#000000",
  "#333c4d",
  "#AEB7C5",
  "#ff4500",
  "#ff8c00",
  "#ffd700",
  "#90ee90",
  "#00ced1",
  "#1e90ff",
  "#c71585",
]);

const bgColor = ref("#ffffff");
const preBgColors = ref([
  "#ffffff",
  "#93aec1",
  "#9dbdba",
  "#f8b042",
  "#ec6a52",
  "#f3b7ad",
  "#f2f2f2",
  "#F0F9FF",
]);

function formatLinkAddress(linkAddress: string) {
  console.log(linkAddress);
  if (
    !linkAddress.startsWith("http://") &&
    !linkAddress.startsWith("https://")
  ) {
    linkAddress = "https://" + linkAddress;
  }
  return linkAddress;
}

function clickLinkInsert() {
  Swal.fire({
    title: "请输入链接地址",
    html: `
      <input id="link-name" class="swal2-input" placeholder="链接名称">
      <input id="link-address" class="swal2-input" placeholder="链接地址">
    `,
    showCancelButton: true,
    confirmButtonText: "确认",
    cancelButtonText: "取消",
  }).then((result) => {
    if (result.isConfirmed) {
      // 使用 Swal 获取用户输入的值
      const linkNameElement = document.getElementById(
        "link-name",
      ) as HTMLInputElement | null;
      const linkAddressElement = document.getElementById(
        "link-address",
      ) as HTMLInputElement | null;
      if (linkNameElement && linkAddressElement) {
        const linkName = linkNameElement.value;
        let linkAddress = linkAddressElement.value;
        linkAddress = formatLinkAddress(linkAddress);
        props.editor
          .chain()
          .focus()
          .setLink({ href: linkAddress, target: "_blank" })
          .run();
        props.editor
          .chain()
          .focus()
          .insertContent({ type: "text", text: linkName })
          .run();
      } else {
        Swal.fire("错误", "链接名称和地址不能为空", "error");
      }
    }
  });
}

// function resetHeadIcon() {
//   if (!props.editor) return;
//   const { selection } = props.editor.state;
//   if (selection.empty || !selection.$head.node(1).type.name.startsWith('heading')) {
//     headIcon.value = 'ri-paragraph';
//   } else {
//     const level = selection.$head.node(1).attrs.level;
//     headIcon.value = 'ri-h-' + level;
//   }
// }
//
// // 监听编辑器状态变化以重置 headIcon
// watch(() => props.editor?.state.selection, resetHeadIcon);

/**
 * AI相关内容
 */
const items10 = [
  {
    icon: "iconfont icon-pinglun",
    text: "AI对话",
    action: ""
  },
  {
    icon: "iconfont icon-OCRshibie",
    text: "OCR识别",
    action: ""
  },
  {
    icon: "iconfont icon-yuyin",
    text: "语音识别",
    action: ""
  },
  {
    icon: "iconfont icon-shipin1",
    text: "视频识别",
    action: ""
  },
  {
    icon: "iconfont icon-fuwenben",
    text: "一键排版",
    action: ""
  },
];

const items6 = [
  {
    text: "Arial",
    style: "font-family: Arial, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("Arial, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", { fontFamily: "Arial, sans-serif" }),
  },
  {
    text: "Playwrite",
    style: "font-family: Playwrite IT Moderna, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("Playwrite IT Moderna, sans-serif")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "Playwrite IT Moderna, sans-serif",
      }),
  },
  {
    text: "Inter",
    style: "font-family: Inter, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("Inter, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", { fontFamily: "Inter, sans-serif" }),
  },
  {
    text: "Comic Sans",
    style: "font-family: Comic Sans MS, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("Comic Sans MS, Comic Sans")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "Comic Sans MS, Comic Sans",
      }),
  },
  {
    text: "Monospace",
    style: "font-family: monospace, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("monospace, sans-serif")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "monospace, sans-serif",
      }),
  },
  {
    text: "Ubuntu",
    style: "font-family: Ubuntu, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("Ubuntu, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", { fontFamily: "Ubuntu, sans-serif" }),
  },
  {
    text: "Reey",
    style: "font-family: ReeyRegular, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("ReeyRegular, sans-serif")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "ReeyRegular, sans-serif",
      }),
  },

  {
    text: "宋体",
    style: "font-family: SimSun, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("SimSun, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", { fontFamily: "SimSun, sans-serif" }),
  },
  {
    text: "仿宋",
    style: "font-family: FangSong, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("FangSong, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "FangSong, sans-serif",
      }),
  },
  {
    text: "楷体",
    style: "font-family: KaiTi, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("KaiTi, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", { fontFamily: "KaiTi, sans-serif" }),
  },
  {
    text: "思源黑体",
    style: "font-family: Source Han Sans, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("Source Han Sans, sans-serif")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "Source Han Sans, sans-serif",
      }),
  },
  {
    text: "OPPO",
    style: "font-family: OPPOSans, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("OPPOSans, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "OPPOSans, sans-serif",
      }),
  },
  {
    text: "小米",
    style: "font-family: MiSans, sans-serif;",
    action: () =>
      props.editor?.chain().focus().setFontFamily("MiSans, sans-serif").run(),
    isActive: () =>
      props.editor?.isActive("textStyle", { fontFamily: "MiSans, sans-serif" }),
  },
  {
    text: "阿里刀立体",
    style: "font-family: AlimamaDaoLiTi, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("AlimamaDaoLiTi, sans-serif")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "AlimamaDaoLiTi, sans-serif",
      }),
  },
  {
    text: "阿里东方楷",
    style: "font-family: AlimamaDongFangDaKai, sans-serif;",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .setFontFamily("AlimamaDongFangDaKai, sans-serif")
        .run(),
    isActive: () =>
      props.editor?.isActive("textStyle", {
        fontFamily: "AlimamaDongFangDaKai, sans-serif",
      }),
  },
];
const items7 = [
  {
    text: "12px",
    style: "font-size: 12px;",
    action: () => props.editor?.chain().focus().setFontSize("12px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "12px" }),
  },
  {
    text: "14px",
    style: "font-size: 14px;",
    action: () => props.editor?.chain().focus().setFontSize("14px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "14px" }),
  },
  {
    text: "16px",
    style: "font-size: 16px;",
    action: () => props.editor?.chain().focus().setFontSize("16px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "16px" }),
  },
  {
    text: "20px",
    style: "font-size: 20px;",
    action: () => props.editor?.chain().focus().setFontSize("20px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "20px" }),
  },
  {
    text: "24px",
    style: "font-size: 24px;",
    action: () => props.editor?.chain().focus().setFontSize("24px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "24px" }),
  },
  {
    text: "30px",
    style: "font-size: 30px;",
    action: () => props.editor?.chain().focus().setFontSize("30px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "30px" }),
  },
  {
    text: "36px",
    style: "font-size: 36px;",
    action: () => props.editor?.chain().focus().setFontSize("36px").run(),
    isActive: () => props.editor?.isActive("textStyle", { fontSize: "36px" }),
  },
];

const items5 = [
  {
    icon: "align-left",
    title: "Ctrl+Shift+L",
    text: "段落",
    action: () => props.editor?.chain().focus().setTextAlign("left").run(),
    isActive: () => props.editor?.isActive({ textAlign: "left" }),
  },
  {
    icon: "align-center",
    title: "Ctrl+Shift+E",
    text: "标题一",
    action: () => props.editor?.chain().focus().setTextAlign("center").run(),
    isActive: () => props.editor?.isActive({ textAlign: "center" }),
  },
  {
    icon: "align-right",
    title: "Ctrl+Shift+R",
    text: "标题二",
    action: () => props.editor?.chain().focus().setTextAlign("right").run(),
    isActive: () => props.editor?.isActive({ textAlign: "right" }),
  },
  {
    icon: "align-justify",
    title: "Ctrl+Shift+J",
    text: "标题三",
    action: () => props.editor?.chain().focus().setTextAlign("justify").run(),
    isActive: () => props.editor?.isActive({ textAlign: "justify" }),
  },
];

const items4 = [
  {
    icon: "paragraph",
    title: "Ctrl+Alt+0",
    text: "段落",
    action: () => props.editor?.chain().focus().setParagraph().run(),
    isActive: () => props.editor?.isActive("paragraph"),
  },
  {
    icon: "h-1",
    title: "Ctrl+Alt+1",
    text: "标题一",
    action: () =>
      props.editor?.chain().focus().toggleHeading({ level: 1 }).run(),
    isActive: () => props.editor?.isActive("heading", { level: 1 }),
  },
  {
    icon: "h-2",
    title: "Ctrl+Alt+2",
    text: "标题二",
    action: () =>
      props.editor?.chain().focus().toggleHeading({ level: 2 }).run(),
    isActive: () => props.editor?.isActive("heading", { level: 2 }),
  },
  {
    icon: "h-3",
    title: "Ctrl+Alt+3",
    text: "标题三",
    action: () =>
      props.editor?.chain().focus().toggleHeading({ level: 3 }).run(),
    isActive: () => props.editor?.isActive("heading", { level: 3 }),
  },
  {
    icon: "h-4",
    title: "Ctrl+Alt+4",
    text: "标题四",
    action: () =>
      props.editor?.chain().focus().toggleHeading({ level: 4 }).run(),
    isActive: () => props.editor?.isActive("heading", { level: 4 }),
  },
];

const items1 = [
  {
    icon: "bold",
    title: "粗体 Ctrl+B",
    action: () => props.editor?.chain().focus().toggleBold().run(),
    isActive: () => props.editor?.isActive("bold"),
  },
  {
    icon: "italic",
    title: "斜体 Ctrl+I",
    action: () => props.editor?.chain().focus().toggleItalic().run(),
    isActive: () => props.editor?.isActive("italic"),
  },
  {
    icon: "underline",
    title: "下划线 Ctrl+U",
    action: () => props.editor?.chain().focus().toggleUnderline().run(),
    isActive: () => props.editor?.isActive("underline"),
  },
  {
    icon: "strikethrough",
    title: "删除线 Ctrl+Shift+S",
    action: () => props.editor?.chain().focus().toggleStrike().run(),
    isActive: () => props.editor?.isActive("strike"),
  },
  {
    icon: "code-line",
    title: "代码 Ctrl+E",
    action: () => props.editor?.chain().focus().toggleCode().run(),
    isActive: () => props.editor?.isActive("code"),
  },
  {
    icon: "superscript-2",
    title: "上标",
    action: () => props.editor?.chain().focus().toggleSuperscript().run(),
    isActive: () => props.editor?.isActive("superscript"),
  },
  {
    icon: "subscript-2",
    title: "下标",
    action: () => props.editor?.chain().focus().toggleSubscript().run(),
    isActive: () => props.editor?.isActive("subscript"),
  },
];

const items2 = [
  {
    icon: "list-ordered-2",
    title: "有序列表 Ctrl+Shift+7",
    action: () => props.editor?.chain().focus().toggleOrderedList().run(),
    isActive: () => props.editor?.isActive("orderedList"),
  },
  {
    icon: "list-radio",
    title: "无序列表 Ctrl+Shift+8",
    action: () => props.editor?.chain().focus().toggleBulletList().run(),
    isActive: () => props.editor?.isActive("bulletList"),
  },
  {
    icon: "list-check-3",
    title: "任务列表 Ctrl+Shift+9",
    action: () => props.editor?.chain().focus().toggleTaskList().run(),
    isActive: () => props.editor?.isActive("taskList"),
  },
];

const items3 = [
  {
    icon: "arrow-go-back-line",
    title: "撤销 Ctrl+Z",
    action: () => props.editor?.chain().focus().undo().run(),
  },
  {
    icon: "arrow-go-forward-line",
    title: "重做 Ctrl+Shift+Z",
    action: () => props.editor?.chain().focus().redo().run(),
  },
  {
    icon: "format-clear",
    title: "清除样式",
    action: () =>
      props.editor?.chain().focus().clearNodes().unsetAllMarks().run(),
  },
];

const items8 = [
  {
    icon: "double-quotes-l",
    title: "引用块",
    action: () => props.editor?.chain().focus().setBlockquote().run(),
  },
  {
    icon: "code-box-line",
    title: "代码块",
    action: () => props.editor?.chain().focus().setCodeBlock().run(),
  },
  {
    icon: "separator",
    title: "水平线",
    action: () => props.editor?.chain().focus().setHorizontalRule().run(),
  },
  {
    icon: "table-line",
    title: "表格",
    action: () =>
      props.editor
        ?.chain()
        .focus()
        .insertTable({ rows: 3, cols: 3, withHeaderRow: true })
        .run(),
  },
  {
    icon: "link",
    title: "链接",
    action: () => clickLinkInsert(),
  },
];

const items9 = [
  {
    icon: "insert-row-top",
    title: "添加行前",
    action: () => props.editor?.chain().focus().addRowBefore().run(),
  },
  {
    icon: "insert-row-bottom",
    title: "添加行后",
    action: () => props.editor?.chain().focus().addRowAfter().run(),
  },
  {
    icon: "insert-column-left",
    title: "添加列前",
    action: () => props.editor?.chain().focus().addColumnBefore().run(),
  },
  {
    icon: "insert-column-right",
    title: "添加列后",
    action: () => props.editor?.chain().focus().addColumnAfter().run(),
  },
  {
    icon: "delete-row",
    title: "删除行",
    action: () => props.editor?.chain().focus().deleteRow().run(),
  },
  {
    icon: "delete-column",
    title: "删除列",
    action: () => props.editor?.chain().focus().deleteColumn().run(),
  },
  {
    icon: "slash-commands-2",
    title: "删除表格",
    action: () => props.editor?.chain().focus().deleteTable().run(),
  },
  {
    icon: "focus-mode",
    title: "设置头",
    action: () => props.editor?.chain().focus().toggleHeaderCell().run(),
  },
  {
    icon: "merge-cells-horizontal",
    title: "合并 | 取消",
    action: () => props.editor?.chain().focus().mergeOrSplit().run(),
  },
];
</script>

<style lang="scss">
.divider {
  background-color: rgba(#fff, 0.25);
  height: 1.25rem;
  margin-left: 0.5rem;
  margin-right: 0.75rem;
  width: 1px;
  display: inline-block;
}
</style>
