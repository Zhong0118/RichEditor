<template>
  <node-view-wrapper class="code-block">
    <select class="select select-bordered min-h-[30px] h-[30px]" v-model="selectedLanguage" contenteditable="false">
      <option :value="null">auto</option>
      <option disabled>—</option>
      <option
        v-for="(language, index) in languages"
        :key="index"
        :value="language"
      >
        {{ language }}
      </option>
    </select>
    <pre><code><node-view-content /></code></pre>
  </node-view-wrapper>
</template>

<script lang="ts">
import { NodeViewContent, nodeViewProps, NodeViewWrapper } from "@tiptap/vue-3";

export default {
  components: {
    NodeViewWrapper,
    NodeViewContent,
  },

  props: nodeViewProps,

  data() {
    return {
      languages: this.extension.options.lowlight.listLanguages(),
    };
  },

  computed: {
    selectedLanguage: {
      get() {
        return this.node.attrs.language;
      },
      set(language: any) {
        this.updateAttributes({ language });
      },
    },
  },
};
</script>

<style lang="scss">
.tiptap {
  .code-block {
    position: relative;

    select {
      position: absolute;
      background-color: var(--white);
      right: 0.5rem;
      top: 0.5rem;
    }
  }
}
</style>
