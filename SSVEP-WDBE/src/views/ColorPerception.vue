<template>
  <div class="Detect">
    <!-- 设置页面 -->
    <div class="setup-page" v-if="!isRunning">
      <h2>青光眼风险评估</h2>
      <form @submit.prevent="startRun" class="setup-form">
        <div class="form-grid">
          <!-- 左侧设置区域 -->
          <div class="settings-panel">
            <!-- IP地址输入 -->
            <div class="input-group">
              <label>设备IP地址：</label>
              <input type="text" v-model="deviceIP" placeholder="请输入设备IP地址" class="styled-input" />
            </div>

            <!-- 刺激范式选择 -->
            <div class="input-group">
              <label>刺激范式：</label>
              <select v-model="selectedParadigm" class="styled-select">
                <option value="text">文本闪烁刺激范式</option>
                <option value="grating">光栅刺激范式</option>
                <option value="checkerboard">棋盘格刺激范式</option>
                <option value="concentric">同心环收缩-扩张运动刺激范式</option>
              </select>
            </div>

            <!-- 额外设置 -->
            <div class="settings-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="boldFont" class="styled-checkbox" />
                <span>加粗字体</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="flickerTexts" class="styled-checkbox" />
                <span>闪烁文本</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="flickerBoxes" class="styled-checkbox" />
                <span>闪烁盒子</span>
              </label>
            </div>
          </div>

          <!-- 右侧表格区域 -->
          <div class="table-panel">
            <div class="table-container">
              <table class="styled-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>频率 (Hz)</th>
                    <th>文本</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(box, index) in boxes" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>
                      <input type="number" v-model="box.frequency" placeholder="频率" step="0.01" class="table-input" />
                    </td>
                    <td>
                      <input type="text" v-model="box.text" placeholder="文本" class="table-input" />
                    </td>
                    <td>
                      <button type="button" @click="removeBox(index)" class="btn-delete">删除</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- 底部按钮区域 -->
        <div class="button-group">
          <button type="button" @click="addBox" class="btn-primary">添加</button>
          <button type="submit" class="btn-success">开始检测</button>
          <button type="button" @click="processData" class="btn-info">数据处理</button>
          <button type="button" @click="classifyData" class="btn-warning">评估</button>
        </div>

        <!-- 数据处理进度条 -->
        <div v-if="processing" class="progress-container">
          <div class="progress-bar">
            <div class="progress" :style="{ width: progress + '%' }"></div>
          </div>
          <div class="progress-text">数据处理进度：{{ progress }}%</div>
        </div>

        <!-- 评分说明 -->
        <div class="score-explanation">
          <h3>评分等级说明</h3>
          <div class="score-grid">
            <div class="score-item">
              <span class="score-label green">无风险（绿色）：</span>
              <span class="score-desc">评分 ≥ 50，表示用户的视功能正常。</span>
            </div>
            <div class="score-item">
              <span class="score-label yellow">中等风险（黄色）：</span>
              <span class="score-desc">33 ≤ 评分 &lt; 50，表示用户的视功能可能存在轻微问题。</span>
            </div>
            <div class="score-item">
              <span class="score-label red">有风险（红色）：</span>
              <span class="score-desc">评分 &lt; 33，表示用户视功能存在明显问题。</span>
            </div>
          </div>
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
        <span v-else-if="finalScore >= 33" class="yellow-text">低风险（黄色）</span>
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
import { useRouter } from 'vue-router';

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
const presetFrequencies = [8, 9.75, 10.25, 12.25, 14.75];
const presetTexts = ["A", "B", "C", "D", "E"];

// 设置参数
const boldFont = ref(false);
const flickerTexts = ref(true);
const flickerBoxes = ref(false);

const fontSize = computed(() => Math.min(window.innerWidth, window.innerHeight) * 1.0);

//文件名
const fileName = ref("");

// 新增响应式变量
const deviceIP = ref("127.0.0.1");
const selectedParadigm = ref("text");
const processing = ref(false);
const progress = ref(0);

const router = useRouter();

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

  processing.value = true;
  progress.value = 0;

  try {
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progress.value < 100) {
        progress.value += 10;
      }
    }, 500);

    const response = await axios.post("http://127.0.0.1:5000/process_data", {
      file_name: fileName.value,
      frequencies: boxes.value.map(box => box.frequency),
    });

    clearInterval(progressInterval);
    progress.value = 100;

    if (response.status === 200) {
      alert("数据处理成功:" + response.data);
      console.log("数据处理成功:", response.data);
    } else {
      console.error("数据处理失败:", response.data);
    }
  } catch (error) {
    console.error("数据处理请求错误:", error);
  } finally {
    setTimeout(() => {
      processing.value = false;
      progress.value = 0;
    }, 1000);
  }
};

const classifyData = async () => {
  fileName.value = "All";
  if (!fileName.value) {
    alert("文件名为空。请先进行数据采集和处理，再进行评估。");
    console.error("文件名为空。尚未进行数据收集处理，无法评估。");
    return;
  }

  processing.value = true;
  progress.value = 0;
  
  try {
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += 5;
      }
    }, 200);
    
    console.log("发送评估请求，文件名:", fileName.value);
    const response = await axios.post("http://127.0.0.1:5000/classify", {
      file_name: fileName.value,
      dataset: 'Dial',  // 添加数据集参数
      ws: 3.5,         // 窗口大小
      Nh: 25,          // 试验次数
      Fs: 250,         // 采样频率
      Ns: 1,           // 受试者数量
      Kf: 1,           // K折交叉验证
      Nf: 5,           // 刺激数量
      targets: boxes.value.map(box => box.frequency)  // 添加目标频率列表
    });

    clearInterval(progressInterval);
    progress.value = 100;

    if (response.status === 200) {
      console.log("评估成功，跳转到结果页面");
      
      // 直接跳转到结果页面，不传递参数
      router.push({
        name: 'AssessmentReport'
      });
    } else {
      console.error("评估失败:", response.data);
      alert("评估失败: " + (response.data?.message || "未知错误"));
    }
  } catch (error) {
    console.error("评估请求错误:", error);
    alert("评估请求错误: " + (error.response?.data?.message || error.message || "未知错误"));
  } finally {
    setTimeout(() => {
      processing.value = false;
      progress.value = 0;
    }, 1000);
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
  height: 100vh;
  overflow: hidden;
  background-color: #f5f7fa;
}

.setup-page {
  padding: 10px;
  max-width: 1600px;  /* 增加最大宽度 */
  margin: 0 auto;
  height: 100%;
  overflow-y: auto;
}

.setup-form {
  background: white;
  padding: 30px;  /* 增加内边距 */
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.form-grid {
  display: grid;
  grid-template-columns: 400px 1fr;  /* 增加左侧宽度 */
  gap: 30px;  /* 增加间距 */
  margin-bottom: 30px;
}

.settings-panel {
  display: flex;
  flex-direction: column;
  gap: 25px;  /* 增加间距 */
  padding: 20px;  /* 添加内边距 */
  background: #f9fafc;
  border-radius: 8px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group label {
  font-size: 16px;  /* 增大字体 */
  font-weight: 500;
  color: #303133;
}

.styled-input, .styled-select {
  padding: 12px 16px;  /* 增加输入框大小 */
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 16px;  /* 增大字体 */
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 6px;
  border: 1px solid #ebeef5;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;  /* 增大字体 */
  padding: 8px 0;
}

.styled-checkbox {
  width: 20px;  /* 增大复选框 */
  height: 20px;
}

h2 {
  font-size: 28px;  /* 增大标题 */
  margin-bottom: 10px;
  color: #303133;
}

.table-panel {
  background: white;
  border-radius: 4px;
  padding: 10px;
}

.styled-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
}

.styled-table th {
  background: #f5f7fa;
  color: #606266;
  font-weight: 600;
  padding: 12px 8px;
  border-bottom: 2px solid #ebeef5;
}

.styled-table td {
  padding: 8px;
  border-bottom: 1px solid #ebeef5;
}

.table-input {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 20px 0;
}

.btn-primary, .btn-success, .btn-info, .btn-warning, .btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #409eff;
  color: white;
}

.btn-success {
  background: #67c23a;
  color: white;
}

.btn-info {
  background: #909399;
  color: white;
}

.btn-warning {
  background: #e6a23c;
  color: white;
}

.btn-delete {
  background: #f56c6c;
  color: white;
  padding: 4px 8px;
  font-size: 12px;
}

.btn-primary:hover, .btn-success:hover, .btn-info:hover, .btn-warning:hover, .btn-delete:hover {
  opacity: 0.8;
}

.progress-container {
  margin: 15px auto;
  width: 80%;
  max-width: 600px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #67c23a;
  transition: width 0.3s ease;
}

.progress-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

.score-explanation {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.score-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 10px;
}

.score-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.score-label {
  font-weight: bold;
  font-size: 14px;
}

.score-desc {
  font-size: 12px;
  color: #606266;
}

.score-label.green { color: #67c23a; }
.score-label.yellow { color: #e6a23c; }
.score-label.red { color: #f56c6c; }

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
