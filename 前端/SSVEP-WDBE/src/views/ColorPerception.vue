<template>
  <div class="Detect">
    <h1>颜色感知</h1>

    <div class="container">
      <h1>闪烁参数设置</h1>
      <div>
        <label for="frequency">频率 (Hz): </label>
        <input type="number" v-model="frequency" min="1" placeholder="输入频率 (Hz)" />
      </div>
      <div>
        <label for="count">数量: </label>
        <input type="number" v-model="count" min="1" placeholder="输入盒子数量" />
      </div>
      <button @click="startDetection" :disabled="isDetecting">开始</button>
      <button @click="stopDetection" :disabled="!isDetecting">停止</button>
    </div>

    <div class="box-container">
      <div
        v-for="(box, index) in boxes"
        :key="index"
        class="box"
        :style="{ backgroundColor: box.isBlack ? 'black' : 'white' }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 响应式数据
const frequency = ref(1); // 频率 (Hz)
const count = ref(1); // 盒子数量
const isDetecting = ref(false); // 是否正在进行检测
const boxes = ref([]); // 用来存储盒子的颜色状态
const intervals = ref([]); // 存储每个盒子的定时器引用

// 开始检测
const startDetection = () => {
  if (isDetecting.value) return; // 防止重复点击开始

  const frequencyHz = frequency.value;
  const boxCount = count.value;

  // 验证输入是否合法
  if (isNaN(frequencyHz) || isNaN(boxCount) || frequencyHz < 1 || boxCount < 1) {
    alert("请输入有效的频率和数量！");
    return;
  }

  // 清空之前生成的盒子和定时器
  boxes.value = [];
  intervals.value.forEach(interval => clearInterval(interval));
  intervals.value = [];

  // 根据用户输入生成盒子，并设置闪烁间隔
  for (let i = 0; i < boxCount; i++) {
    // 创建盒子对象，并将其添加到响应式数据中
    boxes.value.push({ isBlack: true }); // 每个盒子的初始状态

    // 设置闪烁效果
    const interval = setInterval(() => {
      boxes.value[i].isBlack = !boxes.value[i].isBlack; // 切换颜色（黑白交替）
    }, 1000 / frequencyHz);

    intervals.value.push(interval); // 存储定时器引用
  }

  isDetecting.value = true; // 标记检测开始
};

// 停止检测
const stopDetection = () => {
  intervals.value.forEach(interval => clearInterval(interval)); // 清除所有定时器
  intervals.value = [];
  isDetecting.value = false; // 标记检测停止
};
</script>

<style lang="less" scoped>
.Detect {
  h1 {
    font-size: 32px;
    font-weight: bold;
    color: rgb(53, 53, 53);
  }

  .container {
    text-align: center;
    margin-bottom: 20px;
  }

  .box-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }

  .box {
    width: 150px;
    height: 150px;
    border: 2px solid #333;
  }

  button {
    margin: 10px;
  }
}
</style>
