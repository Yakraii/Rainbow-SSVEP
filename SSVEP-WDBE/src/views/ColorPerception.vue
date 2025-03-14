<!-- <template>
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
</style> -->


<template>
  <div class="Detect">
    <!-- 设置页面 -->
    <div class="setup-page" v-if="!isRunning">
      <h2>颜色感知检测</h2>
      <form @submit.prevent="startRun">
        <!-- 频率输入表格 -->
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>频率 (Hz)</th>
                <th>文本</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(box, index) in boxes" :key="index">
                <td>{{ index + 1 }}</td>
                <td><input type="number" v-model="box.frequency" placeholder="频率" min="1" /></td>
                <td><input type="text" v-model="box.text" placeholder="文本" /></td>
                <td><button type="button" @click="removeBox(index)">删除</button></td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4">
                  <button type="button" @click="addBox">添加</button>
                  <button type="submit">开始</button>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>

        <!-- 额外设置 -->
        <div class="settings">
          <label><input type="checkbox" v-model="boldFont" /> 加粗字体</label>
          <label><input type="checkbox" v-model="flickerTexts" /> 闪烁文本</label>
          <label><input type="checkbox" v-model="flickerBoxes" /> 闪烁盒子</label>
          <label>持续时间 (秒): <input type="number" v-model="duration" placeholder="秒" min="1" /></label>
        </div>
      </form>
    </div>

    <!-- 刺激页面 -->
    <div class="stim-page" v-if="isRunning" @click="stopRun">
      <div class="fullscreen">
        <div
          v-for="(box, index) in boxes"
          :key="index"
          class="stimulus"
          :style="{
            width: `${100 / cols}%`,
            height: `${100 / rows}%`,
            fontWeight: boldFont ? 'bold' : 'normal',
            fontSize: `${fontSize}px`,
            backgroundColor: flickerBoxes ? (box.isBlack ? 'black' : 'white') : 'transparent',
            color: flickerTexts ? (box.isBlack ? 'black' : 'white') : 'white'
          }"
        >
          {{ box.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const isRunning = ref(false);
const boxes = ref([]);
const intervals = ref([]);

// 设置参数
const boldFont = ref(false);
const flickerTexts = ref(true);
const flickerBoxes = ref(false);
const duration = ref(null);

// 屏幕分割计算
const rows = computed(() => Math.ceil(Math.sqrt(boxes.value.length)));
const cols = computed(() => Math.ceil(boxes.value.length / rows.value));
const fontSize = computed(() => Math.min(window.innerWidth / cols.value, window.innerHeight / rows.value) * 0.6);

// 添加盒子（默认频率 7Hz，文本 A, B, C...）
const addBox = () => {
  boxes.value.push({
    frequency: 7,
    text: String.fromCharCode(65 + boxes.value.length),
    isBlack: true,
  });
};

// 删除盒子
const removeBox = (index) => {
  boxes.value.splice(index, 1);
};

// 开始刺激
// const startRun = () => {
//   if (boxes.value.length === 0) return;
//   isRunning.value = true;

//   intervals.value.forEach(clearInterval);
//   intervals.value = [];

//   if (flickerTexts.value || flickerBoxes.value) {
//     boxes.value.forEach((box) => {
//       const interval = setInterval(() => {
//         box.isBlack = !box.isBlack;
//       }, 1000 / box.frequency / 2);
//       intervals.value.push(interval);
//     });
//   }

//   if (duration.value) {
//     setTimeout(stopRun, duration.value * 1000);
//   }
// };
const startRun = () => {
  if (boxes.value.length === 0) return;
  isRunning.value = true;

  intervals.value.forEach(clearInterval);
  intervals.value = [];

  if (flickerTexts.value || flickerBoxes.value) {
    boxes.value.forEach((box) => {
      const interval = setInterval(() => {
        box.isBlack = !box.isBlack;
      }, 1000 / (box.frequency * 2));
      intervals.value.push(interval);
    });
  }

  // 修正持续时间设置，确保所有间隔清除
  if (duration.value && duration.value > 0) {
    const durationTimeout = setTimeout(() => {
      stopRun();
      clearTimeout(durationTimeout);
    }, duration.value * 1000);
  }
};

// 停止刺激
const stopRun = () => {
  intervals.value.forEach(clearInterval);
  intervals.value = [];
  isRunning.value = false;
};

// 监听窗口大小变化，确保字体大小自适应
onMounted(() => {
  window.addEventListener("resize", () => {
    isRunning.value && startRun();
  });
});
</script>

<style scoped>
.Detect {
  text-align: center;
}

/* 表格居中 */
.table-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

table {
  border-collapse: collapse;
  width: 60%;
  text-align: center;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
}

tfoot td {
  text-align: center;
}

/* 设置项居中，每行一个 */
.settings {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

/* 全屏模式 */
.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
  overflow: hidden;
  display: flex;
  flex-wrap: wrap;
}

/* 文字刺激 */
.stimulus {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  user-select: none;
}
</style>
