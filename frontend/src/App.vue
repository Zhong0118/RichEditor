<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { reactive, ref } from 'vue';
const data1 = ref(123);
const data2 = ref(123123);
const data3 = ref(
  { name: 'John', age: 30 },

);
const data4 = reactive({age: 1});
const data5 = ref(123);
const data6 = ref(123);
const show1 = false;
const show2 = true;
function add() { 
  data1.value += 1;
  data3.value.age += 1;
  data4.age += 1;
}
</script>

<template>
  <div class="m-4 gap-4 flex">
    <h1 class="text-2xl">{{ data1 }}</h1>
    <h1 class="text-2xl">{{ data2 }}</h1>
    <h1 class="text-2xl">{{ data3.age }}</h1>
    <h1 class="text-2xl">{{ data4.age }}</h1>
    <h1 class="text-2xl">{{ data5 }}</h1>
    <h1 class="text-2xl">{{ data5 }}</h1>
    <h1 class="text-2xl">{{ data5 }}</h1>
    <button class="btn" @click="add" >click</button>
    <button class="btn bg-primary">click2</button>
  </div>
</template>
