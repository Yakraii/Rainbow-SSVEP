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
                <td>
                  <input
                    type="number"
                    v-model="box.frequency"
                    placeholder="频率"
                    step="0.01"
                  />
                </td>
                <td>
                  <input type="text" v-model="box.text" placeholder="文本" />
                </td>
                <td>
                  <button type="button" @click="removeBox(index)">删除</button>
                </td>
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
          <label>
            <input type="checkbox" v-model="boldFont" /> 加粗字体
          </label>
          <label>
            <input type="checkbox" v-model="flickerTexts" /> 闪烁文本
          </label>
          <label>
            <input type="checkbox" v-model="flickerBoxes" /> 闪烁盒子
          </label>
        </div>
      </form>
    </div>

    <!-- 刺激页面 -->
    <div class="stim-page" v-if="isRunning" @click="stopRun">
      <div class="fullscreen">
        <div
          class="stimulus"
          :style="{
            fontWeight: boldFont ? 'bold' : 'normal',
            fontSize: `${fontSize}px`,
            backgroundColor: flickerBoxes ? (currentBox?.isBlack ? 'black' : 'white') : 'black',
            color: flickerTexts ? (currentBox?.isBlack ? 'black' : 'white') : 'white',
          }"
        >
          {{ currentBox?.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const isRunning = ref(false);
const boxes = ref([]);
const intervals = ref([]);
const activeIndex = ref(-1);
const currentBox = ref(null);

// 默认设置
const presetFrequencies = [7.5, 9.25, 10.25, 12.25, 14.75];
const presetTexts = ["A", "B", "C", "D", "E"];

// 设置参数
const boldFont = ref(false);
const flickerTexts = ref(true);
const flickerBoxes = ref(false);

const fontSize = computed(() => Math.min(window.innerWidth, window.innerHeight) * 1.0);

// 初始化默认参数
onMounted(() => {
  presetFrequencies.forEach((freq, index) => {
    boxes.value.push({
      frequency: freq,
      text: presetTexts[index],
      isBlack: true,
    });
  });
});

// 添加盒子
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
const startRun = () => {
  if (boxes.value.length === 0) return;
  isRunning.value = true;
  activeIndex.value = 0;
  startStimulus(activeIndex.value);
};

// 启动单个刺激
const startStimulus = (index) => {
  currentBox.value = boxes.value[index];

  // 清除之前的定时器
  intervals.value.forEach((interval) => clearInterval(interval));
  intervals.value = [];

  // 设置闪烁定时器
  if (flickerTexts.value || flickerBoxes.value) {
    const interval = setInterval(() => {
      currentBox.value.isBlack = !currentBox.value.isBlack;
    }, 1000 / (currentBox.value.frequency * 2));
    intervals.value.push(interval);
  }

  // 设置切换定时器
  const switchTimer = setTimeout(() => {
    if (activeIndex.value < boxes.value.length - 1) {
      activeIndex.value++;
      startStimulus(activeIndex.value);
    } else {
      stopRun();
    }
  }, 25000);
  intervals.value.push(switchTimer);
};

// 停止刺激
const stopRun = () => {
  intervals.value.forEach((interval) => clearInterval(interval));
  intervals.value = [];
  isRunning.value = false;
  activeIndex.value = -1;
  currentBox.value = null;
};

// 窗口大小变化处理
onMounted(() => {
  window.addEventListener("resize", () => {
    if (isRunning.value) {
      fontSize.value = Math.min(window.innerWidth, window.innerHeight) * 0.3;
    }
  });
});
</script>

<style scoped>
.Detect {
  text-align: center;
}

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

th,
td {
  border: 1px solid #ccc;
  padding: 10px;
}

.settings {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stimulus {
  transition: all linear;
  user-select: none;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>