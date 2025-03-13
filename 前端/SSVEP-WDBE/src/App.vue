<script setup>
import Main from '@/views/MainView.vue'
import { provide } from "vue";

//引入echarts
import * as echarts from "echarts";

//通过provide提供echarts
provide("echarts", echarts);

</script>

<template>
  <div class="root">
    <Main />
  </div>
</template>

<style>
.root {
  height: 100%;
  width: 100%;
}

body {
  background-color: #fafafa;
}
</style>