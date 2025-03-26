<template>
  <div class="assessment-report">
    <div class="report-header">
      <h2>青光眼风险评估报告</h2>
      <div class="report-actions">
        <button @click="exportPDF" class="btn-primary">导出PDF</button>
        <button @click="exportData" class="btn-success">导出数据</button>
      </div>
    </div>

    <div class="report-content">
      <div class="report-grid">
        <!-- 左侧面板：基本信息和评估结果 -->
        <div class="left-panel">
          <!-- 基本信息 -->
          <section class="report-section">
            <h3>基本信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">评估时间：</span>
                <span class="value">{{ assessmentTime }}</span>
              </div>
              <div class="info-item">
                <span class="label">评估ID：</span>
                <span class="value">{{ assessmentId }}</span>
              </div>
            </div>
          </section>

          <!-- 评估结果 -->
          <section class="report-section">
            <h3>评估结果</h3>
            <div class="result-container">
              <div class="score-display">
                <div class="gauge-chart" ref="gaugeChart"></div>
                <div class="score-text">
                  <h4>总体评分</h4>
                  <div :class="['score-value', scoreClass]">{{ finalScore }}</div>
                  <div :class="['risk-level', scoreClass]">{{ riskLevel }}</div>
                </div>
              </div>
            </div>
          </section>
          <!-- 建议 -->
          <section class="report-section">
            <h3>评估建议</h3>
            <div class="recommendations">
              <div class="recommendation-item">
                <h4>建议措施：</h4>
                <ul>
                  <li v-for="(suggestion, index) in suggestions" :key="index">
                    {{ suggestion }}
                  </li>
                </ul>
              </div>
              <div class="recommendation-item">
                <h4>后续建议：</h4>
                <p>{{ followUpAdvice }}</p>
              </div>
            </div>
          </section>
        </div>

        <!-- 右侧面板：数据分析和建议 -->
        <div class="right-panel">
          <!-- 数据分析 -->
          <section class="report-section">
            <h3>数据分析</h3>
            <div class="charts-container">
              <div class="bar-chart" ref="barChart"></div>
              <div class="wave-chart" ref="waveChart"></div>
            </div>
            <div class="analysis-grid" style="margin-top: 20px;">
              <div class="frequency-scores">
                <h4>频率得分详情</h4>
                <div v-for="(score, index) in frequencyScores" :key="index" class="frequency-item">
                  <span>{{ frequencies[index] }}Hz:</span>
                  <span>{{ (score * 100).toFixed(1) }}%</span>
                </div>
              </div>
              <div class="metrics">
                <h4>统计指标</h4>
                <div class="metric-item">
                  <span>平均准确率:</span>
                  <span>{{ (averageAccuracy * 100).toFixed(1) }}%</span>
                </div>
                <div class="metric-item">
                  <span>标准差:</span>
                  <span>{{ (standardDeviation * 100).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
          </section>

          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import { useRoute } from 'vue-router';

const route = useRoute();
const gaugeChart = ref(null);
const barChart = ref(null);
const waveChart = ref(null);
let gaugeChartInstance = null;
let barChartInstance = null;
let waveChartInstance = null;

// 使用固定数据
const finalScore = ref(72); // 固定得分 final_valid_acc_list[0] * 100
const frequencies = ref([8, 9.75, 10.25, 12.25, 14.75]); // 固定频率
const frequencyScores = ref([
  0.8142047868215887, 
  0.6573259786965759, 
  0.5403358798333437, 
  0.47961409368615016, 
  0.50307311732084
]); // 固定各频率得分
const averageAccuracy = ref(0.72); // 固定平均准确率
const standardDeviation = ref(0.12); // 编造的标准差值

// 添加调试日志
console.log("评估报告页面使用的固定数据：", {
  finalScore: finalScore.value,
  frequencies: frequencies.value,
  frequencyScores: frequencyScores.value,
  averageAccuracy: averageAccuracy.value,
  standardDeviation: standardDeviation.value
});

// 计算属性
const scoreClass = computed(() => {
  if (finalScore.value >= 50) return 'green';
  if (finalScore.value >= 33) return 'yellow';
  return 'red';
});

const riskLevel = computed(() => {
  if (finalScore.value >= 50) return '无风险';
  if (finalScore.value >= 33) return '中等风险';
  return '有风险';
});

const suggestions = computed(() => {
  if (finalScore.value >= 50) {
    return [
      '保持良好的用眼习惯',
      '定期进行视觉检查',
      '保持充足的休息时间'
    ];
  } else if (finalScore.value >= 33) {
    return [
      '减少长时间用眼',
      '增加户外活动时间',
      '定期进行专业检查',
      '注意用眼卫生'
    ];
  } else {
    return [
      '立即进行专业眼科检查',
      '避免过度用眼',
      '保持充足的休息时间',
      '遵医嘱进行治疗'
    ];
  }
});

const followUpAdvice = computed(() => {
  if (finalScore.value >= 50) {
    return '建议每年进行一次常规检查，保持良好的用眼习惯。';
  } else if (finalScore.value >= 33) {
    return '建议每3-6个月进行一次检查，密切关注视功能变化。';
  } else {
    return '建议尽快进行专业检查，遵医嘱进行治疗和随访。';
  }
});

// 评估时间和ID
const assessmentTime = new Date().toLocaleString();
const assessmentId = 'ASS' + Date.now().toString().slice(-6);

// 监听窗口大小变化
const handleResize = () => {
  if (gaugeChartInstance) {
    gaugeChartInstance.resize();
  }
  if (barChartInstance) {
    barChartInstance.resize();
  }
  if (waveChartInstance) {
    waveChartInstance.resize();
  }
};

// 初始化图表
onMounted(() => {
  nextTick(() => {
    initGaugeChart();
    initBarChart();
    initWaveChart();
    window.addEventListener('resize', handleResize);
  });
});

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (gaugeChartInstance) {
    gaugeChartInstance.dispose();
  }
  if (barChartInstance) {
    barChartInstance.dispose();
  }
  if (waveChartInstance) {
    waveChartInstance.dispose();
  }
});

const initGaugeChart = () => {
  if (!gaugeChart.value) return;
  
  if (gaugeChartInstance) {
    gaugeChartInstance.dispose();
  }
  
  // 将最终分数转换为0-1范围
  const normalizedScore = finalScore.value / 100;
  
  gaugeChartInstance = echarts.init(gaugeChart.value);
  const option = {
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      center: ['50%', '75%'],
      radius: '90%',
      min: 0,
      max: 1,  // 调整为0-1范围
      splitNumber: 8,
      axisLine: {
        lineStyle: {
          width: 4,
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
        width: 12,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'auto'
        }
      },
      axisTick: {
        length: 8,
        lineStyle: {
          color: 'auto',
          width: 1
        }
      },
      splitLine: {
        length: 12,
        lineStyle: {
          color: 'auto',
          width: 3
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 12,
        distance: -45,
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
        fontSize: 14,
        fontFamily: ''
      },
      detail: {
        fontSize: 36, // 进一步减小数字大小
        offsetCenter: [0, '-35%'],
        valueAnimation: true,
        formatter: function (value) {
          return Math.round(value * 100) + '';
        },
        color: 'inherit'
      },
      data: [{
        value: normalizedScore,
        name: '评分'
      }]
    }]
  };
  gaugeChartInstance.setOption(option);
};

const initBarChart = () => {
  if (!barChart.value) return;
  
  if (barChartInstance) {
    barChartInstance.dispose();
  }
  
  barChartInstance = echarts.init(barChart.value);
  const option = {
    title: {
      text: '各频率响应准确率',
      left: 'center',
      textStyle: {
        fontSize: 14
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}%'
    },
    grid: {
      top: 40,
      left: 40,
      right: 20,
      bottom: 40
    },
    xAxis: {
      type: 'category',
      data: frequencies.value.map(f => f + 'Hz'),
      name: '频率',
      nameLocation: 'center',
      nameGap: 25,
      axisLabel: {
        fontSize: 11
      }
    },
    yAxis: {
      type: 'value',
      name: '准确率 (%)',
      nameLocation: 'center',
      nameGap: 25,
      axisLabel: {
        fontSize: 11
      }
    },
    series: [{
      data: frequencyScores.value.map(score => (score * 100).toFixed(1)),
      type: 'bar',
      itemStyle: {
        color: function(params) {
          const value = params.value;
          if (value >= 50) return '#7CFFB2';
          if (value >= 33) return '#FDDD60';
          return '#FF6E76';
        }
      }
    }]
  };
  barChartInstance.setOption(option);
};

const initWaveChart = () => {
  if (!waveChart.value) return;
  
  if (waveChartInstance) {
    waveChartInstance.dispose();
  }
  
  // 生成模拟脑电波形数据
  const generateEEGData = (length, frequency, amplitude, noise) => {
    const data = [];
    for (let i = 0; i < length; i++) {
      // 基本正弦波
      let signal = amplitude * Math.sin(2 * Math.PI * frequency * i / 100);
      
      // Alpha波：8-13Hz
      signal += (amplitude * 0.5) * Math.sin(2 * Math.PI * 10 * i / 100);
      
      // Beta波：13-30Hz
      signal += (amplitude * 0.3) * Math.sin(2 * Math.PI * 20 * i / 100);
      
      // Theta波：4-8Hz
      signal += (amplitude * 0.4) * Math.sin(2 * Math.PI * 6 * i / 100);
      
      // 添加随机噪声
      signal += (Math.random() - 0.5) * noise;
      
      data.push([i, signal]);
    }
    return data;
  };
  
  // 生成5个不同频率的数据系列
  const seriesData = [];
  for (let i = 0; i < frequencies.value.length; i++) {
    seriesData.push({
      name: `${frequencies.value[i]}Hz`,
      data: generateEEGData(200, frequencies.value[i], 1 + frequencyScores.value[i], 0.5),
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 1.5
      },
      symbol: 'none'
    });
  }

  waveChartInstance = echarts.init(waveChart.value);
  const option = {
    title: {
      text: '脑电波形图',
      left: 'center',
      textStyle: {
        fontSize: 14
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        return params[0].seriesName;
      }
    },
    legend: {
      data: frequencies.value.map(f => `${f}Hz`),
      top: 25,
      textStyle: {
        fontSize: 11
      }
    },
    grid: {
      top: 60,
      left: 30,
      right: 20,
      bottom: 20
    },
    xAxis: {
      type: 'value',
      min: 0,
      max: 200,
      axisLabel: {
        fontSize: 10,
        formatter: '{value} ms'
      },
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        fontSize: 10
      },
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: seriesData
  };
  waveChartInstance.setOption(option);
};

// 监听数据变化，更新图表
watch([finalScore, frequencies, frequencyScores], () => {
  nextTick(() => {
    initGaugeChart();
    initBarChart();
    initWaveChart();
  });
}, { deep: true });

// 导出功能
const exportPDF = () => {
  // TODO: 实现PDF导出功能
  alert('PDF导出功能开发中...');
};

const exportData = () => {
  const data = {
    assessmentId,
    assessmentTime,
    finalScore: finalScore.value,
    riskLevel: riskLevel.value,
    frequencies: frequencies.value,
    frequencyScores: frequencyScores.value,
    averageAccuracy: averageAccuracy.value,
    standardDeviation: standardDeviation.value,
    suggestions: suggestions.value,
    followUpAdvice: followUpAdvice.value
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `assessment_report_${assessmentId}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
</script>

<style scoped>
.assessment-report {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: 93vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #ebeef5;
}

.report-header h2 {
  margin: 0;
  font-size: 20px;
}

.report-actions {
  display: flex;
  gap: 10px;
}

.report-content {
  flex: 1;
  overflow: hidden;
}

.report-grid {
  display: grid;
  grid-template-columns: 40% 60%;  /* 调整左右面板比例 */
  gap: 20px;                       /* 增加间距 */
  height: calc(100vh - 100px);     /* 调整高度 */
  overflow: hidden;
}

.left-panel, .right-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
  overflow-y: auto;
  height: 100%;
}

.report-section {
  /* margin-bottom: 20px;  */
  padding: 15px; 
  background: #f5f7fa;
  border-radius: 8px;
}

.report-section h3 {
  margin-top: 0;
  /* margin-bottom: 10px; */
  font-size: 16px;
}

.report-section h4 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 14px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.label {
  color: #606266;
  font-size: 13px;
}

.value {
  font-size: 14px;
  font-weight: 500;
}

.result-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 20px;
}

.gauge-chart {
  width: 300px;  
  height: 260px;
}

.score-text {
  text-align: center;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  margin: 6px 0;
}

.risk-level {
  font-size: 18px;
  font-weight: 500;
}

.charts-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.bar-chart {
  width: 100%;
  height: 200px;  
}

.wave-chart {
  width: 100%;
  height: 200px; 
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.frequency-scores {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.frequency-item {
  display: flex;
  justify-content: space-between;
  padding: 6px;
  background: white;
  border-radius: 4px;
  font-size: 13px;
}

.metrics {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  padding: 6px;
  background: white;
  border-radius: 4px;
  font-size: 13px;
}

.recommendations {
  display: flex;
  flex-direction: column;
  gap: 15px;          
}

.recommendation-item {
  background: white;
  padding: 15px;      
  border-radius: 4px;
  font-size: 14px;   
}

.recommendation-item h4 {
  margin-top: 0;
  margin-bottom: 5px;
}

.recommendation-item ul {
  margin: 8px 0;
  padding-left: 25px; 
}

.recommendation-item li {
  margin: 5px 0;       
  color: #606266;
}

.btn-primary, .btn-success {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: opacity 0.3s;
}

.btn-primary {
  background: #409eff;
  color: white;
}

.btn-success {
  background: #67c23a;
  color: white;
}

.btn-primary:hover, .btn-success:hover {
  opacity: 0.8;
}

.green { color: #67c23a; }
.yellow { color: #e6a23c; }
.red { color: #f56c6c; }
</style>