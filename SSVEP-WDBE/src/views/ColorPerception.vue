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
                  <input type="number" v-model="box.frequency" placeholder="频率" step="0.01" />
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
                  <button type="button" @click="processData">数据处理</button>
                  <button type="button" @click="classifyData">评估</button>
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

        <div class="score-explanation">
          <h3>评分等级说明</h3>
          <p><span style="color: green; font-weight: bold;">无风险（绿色）：</span> 评分 ≥ 50，表示用户在该频率下的视功能正常。</p>
          <p><span style="color: orange; font-weight: bold;">中等风险（黄色）：</span> 33 ≤ 评分 &lt;
            50，表示用户在该频率下的视功能可能存在轻微问题，建议关注。</p>
          <p><span style="color: red; font-weight: bold;">有风险（红色）：</span> 评分 &lt; 33，表示用户在该频率下的视功能存在明显问题，建议进一步检查。</p>
        </div>

      </form>

      <!-- 评估结果展示 -->
      <div v-if="showResults" class="results-container">
        <div id="gaugeChart" class="chart"></div>
        <div id="barChart" class="chart"></div>
      </div>
    </div>

    <!-- 评分结果解释 -->
    <div v-if="finalScore !== null" class="score-explanation">
      <h3>评估结果</h3>
      <p :class="scoreClass">
        您的评分为 <strong>{{ finalScore }}</strong>，属于
        <span v-if="finalScore >= 50" class="green-text">无风险（绿色）</span>
        <span v-else-if="finalScore >= 33" class="yellow-text">中等风险（黄色）</span>
        <span v-else class="red-text">有风险（红色）</span> 等级。
      </p>
      <p>{{ scoreAdvice }}</p>
    </div>


    <!-- 刺激页面 -->
    <div class="stim-page" v-if="isRunning" @click="stopRun">
      <div class="fullscreen">
        <div class="stimulus" :style="{
          fontWeight: boldFont ? 'bold' : 'normal',
          fontSize: `${fontSize}px`,
          backgroundColor: flickerBoxes ? (currentBox?.isBlack ? 'black' : 'white') : 'black',
          color: flickerTexts ? (currentBox?.isBlack ? 'black' : 'white') : 'white',
        }">
          {{ currentBox?.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import * as echarts from 'echarts';
import axios from "axios";

const isRunning = ref(false);
const boxes = ref([]);
const intervals = ref([]);
const activeIndex = ref(-1);
const currentBox = ref(null);
const showResults = ref(false);
const finalScore = ref(null);

// 计算评分等级
const scoreClass = computed(() => {
  if (finalScore.value === null) return "";
  if (finalScore.value >= 50) return "green-text";
  if (finalScore.value >= 33) return "yellow-text";
  return "red-text";
});

// 计算建议内容
const scoreAdvice = computed(() => {
  if (finalScore.value === null) return "请完成测试以查看您的评估结果。";
  if (finalScore.value >= 50) return "您的视觉功能良好，无需担忧。";
  if (finalScore.value >= 33) return "建议适当关注，避免长时间高频视觉刺激。";
  return "建议尽快进行专业检查，以确保视功能健康。";
});

let gaugeChart = null;
let barChart = null;

// 默认设置
const presetFrequencies = [7.5, 9.75, 10.25, 12.25, 14.75];
const presetTexts = ["A", "B", "C", "D", "E"];

// 设置参数
const boldFont = ref(false);
const flickerTexts = ref(true);
const flickerBoxes = ref(false);

const fontSize = computed(() => Math.min(window.innerWidth, window.innerHeight) * 1.0);

//文件名
const fileName = ref("");

// 初始化图表
const initCharts = () => {
  if (gaugeChart) gaugeChart.dispose();
  if (barChart) barChart.dispose();

  gaugeChart = echarts.init(document.getElementById('gaugeChart'));
  barChart = echarts.init(document.getElementById('barChart'));
};

// 更新图表数据
const updateCharts = (accuracy, scores) => {
  const barOption = {
    xAxis: {
      type: 'category',
      name: '频率',
      nameLocation: 'center',
      nameGap: '30',
      data: boxes.value.map(box => box.frequency.toString()).concat(['Avg'])
    },
    yAxis: {
      type: 'value',
      name: '分数',
      nameRotate: '',
      nameLocation: 'center',
      nameGap: '25'
    },
    series: [{
      data: [
        ...scores.map(score => score * 100),
        {
          value: accuracy * 100,
          itemStyle: {
            color: '#a90000'
          }
        }
      ],
      type: 'bar'
    }]
  };
  const gaugeOption = {
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      center: ['50%', '75%'],
      radius: '90%',
      min: 0,
      max: 1,
      splitNumber: 10,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.33, '#FF6E76'],
            [0.5, '#FDDD60'],
            [1, '#7CFFB2']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'auto'
        }
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'auto',
          width: 2
        }
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'auto',
          width: 5
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 20,
        distance: -60,
        rotate: 'tangential',
        fontFamily: '新宋体',
        fontWeight: 'bold',
        formatter: function (value) {
          if (value === 0.7) {
            return '无风险';
          } else if (value === 0.4) {
            return '中等风险';
          } else if (value === 0.2) {
            return '有风险';
          }
          return '';
        }
      },
      title: {
        offsetCenter: [0, '-10%'],
        fontSize: 20,
        fontFamily: ''
      },
      detail: {
        fontSize: 90,
        offsetCenter: [0, '-35%'],
        valueAnimation: true,
        formatter: function (value) {
          return Math.round(value * 100) + '';
        },
        color: 'inherit'
      },
      data: [{
        value: accuracy,
        name: 'Grade Rating'
      }]
    }]
  };
  barChart.setOption(barOption);
  gaugeChart.setOption(gaugeOption);
};

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

const userId = "user_123"; // 这里可以动态获取用户ID
const getCurrentTime = () => {
  const now = new Date();
  const pad = (num) => String(num).padStart(2, '0');
  const year = now.getFullYear();
  const month = pad(now.getMonth() + 1);
  const day = pad(now.getDate());
  const hours = pad(now.getHours());
  const minutes = pad(now.getMinutes());
  const safeTimeString = `${year}-${month}-${day}_${hours}-${minutes}`;
  return safeTimeString;
};

const startRun = async () => {
  if (boxes.value.length === 0) return;

  fileName.value = `${userId}_${getCurrentTime()}`;
  alert("保存文件名: " + fileName.value);

  try {
    const response = await axios.post("http://127.0.0.1:5000/record_data", { file_name: fileName.value });

    if (response.status === 200) {
      isRunning.value = true;
      activeIndex.value = 0;
      startStimulus(activeIndex.value);
    } else {
      console.error("后端返回错误状态:", response.status);
    }
  } catch (error) {
    console.error("请求失败:", error);
  }
};

const processData = async () => {
  if (!fileName.value) {
    console.error("文件名为空，无法处理数据");
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:5000/process_data", {
      file_name: fileName.value,
      frequencies: boxes.value.map(box => box.frequency),
    });

    if (response.status === 200) {
      alert("数据处理成功:" + response.data);
      console.log("数据处理成功:", response.data);
    } else {
      console.error("数据处理失败:", response.data);
    }
  } catch (error) {
    console.error("数据处理请求错误:", error);
  }
};

// const classifyData = async () => {
//   fileName.value = 'All';
//   if (!fileName.value) {
//     console.error("文件名为空，无法评估");
//     return;
//   }

//   try {
//     const response = await axios.post("http://127.0.0.1:5000/classify", {
//       file_name: fileName.value,
//     });

//     if (response.status === 200) {
//       const result = response.data;
//       console.log("评估成功:", result);

//       // 初始化并显示图表
//       showResults.value = true;
//       await nextTick();
//       initCharts();

//       // 从结果中提取数据
//       const accuracy = result.final_valid_acc_list[0]; // 取第一个受试者的准确率
//       const scores = result.average_scores; // 直接使用average_scores，已经是百分比形式

//       updateCharts(accuracy, scores);
//     } else {
//       console.error("评估失败:", response.data);
//     }
//   } catch (error) {
//     console.error("评估请求错误:", error);
//   }
// };
const classifyData = async () => {
  fileName.value = 'All';
  if (!fileName.value) {
    console.error("文件名为空，无法评估");
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:5000/classify", {
      file_name: fileName.value,
    });

    if (response.status === 200) {
      const result = response.data;
      console.log("评估成功:", result);

      // 提取评分数据（假设后端返回 `final_valid_acc_list` 作为评分）
      finalScore.value = result.final_valid_acc_list[0] * 100; // 乘100转换为百分制
      console.log("最终得分:", finalScore.value);

      // 初始化并显示图表
      showResults.value = true;
      await nextTick();
      initCharts();

      // 从结果中提取数据
      const accuracy = result.final_valid_acc_list[0]; // 取第一个受试者的准确率
      const scores = result.average_scores; // 直接使用average_scores，已经是百分比形式

      updateCharts(accuracy, scores);
    } else {
      console.error("评估失败:", response.data);
    }
  } catch (error) {
    console.error("评估请求错误:", error);
  }
};

// 启动单个刺激
const startStimulus = (index) => {
  currentBox.value = boxes.value[index];

  intervals.value.forEach((interval) => clearInterval(interval));
  intervals.value = [];

  if (flickerTexts.value || flickerBoxes.value) {
    const interval = setInterval(() => {
      currentBox.value.isBlack = !currentBox.value.isBlack;
    }, 1000 / (currentBox.value.frequency * 2));
    intervals.value.push(interval);
  }

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
    if (showResults.value) {
      gaugeChart?.resize();
      barChart?.resize();
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

.results-container {
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 40px;
}

.chart {
  width: 500px;
  height: 400px;
}

.score-explanation {
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 左右居中 */
  text-align: center;
  font-size: 18px;
  font-family: "Arial", sans-serif;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px 30px;
  border-radius: 10px;
  border: 2px solid #007bff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto 0;
  /* 上方间距 20px，自动水平居中 */
}

.score-explanation h3 {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 12px;
  color: #333;
}

.score-explanation p {
  margin: 10px 0;
  font-weight: 500;
  line-height: 1.5;
}

.green-text {
  color: #008000;
  font-weight: bold;
  font-size: 20px;
}

.yellow-text {
  color: #FFA500;
  font-weight: bold;
  font-size: 20px;
}

.red-text {
  color: #FF0000;
  font-weight: bold;
  font-size: 20px;
}

.score-explanation {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  font-size: 18px;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px 30px;
  border-radius: 10px;
  border: 2px solid #007bff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto 0;
}

</style>
