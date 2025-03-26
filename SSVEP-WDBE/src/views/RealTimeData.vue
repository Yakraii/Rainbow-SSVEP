<template>
    <div class="history-data-container">
        <!-- 数据概览区域 -->
        <div class="overview-section">
            <!-- 左侧概要统计 -->
            <div class="statistics-card">
                <h3>检测概览</h3>
                <div class="stat-item">
                    <span class="label">检测总次数</span>
                    <span class="value">{{ totalTests }}</span>
                </div>
                <div class="stat-item">
                    <span class="label">平均评分</span>
                    <span class="value">{{ averageScore }}</span>
                </div>
                <div class="stat-item">
                    <span class="label">风险趋势</span>
                    <el-tag :type="riskTrend.type">{{ riskTrend.text }}</el-tag>
                </div>
                <div class="stat-item">
                    <span class="label">健康状态</span>
                    <el-tag :type="healthStatus.type">{{ healthStatus.text }}</el-tag>
                </div>
            </div>
            
            <!-- 右侧趋势图 -->
            <div class="trend-chart">
                <h3>评分趋势</h3>
                <div ref="chartRef" style="height: 300px"></div>
            </div>
        </div>

        <!-- 历史记录表格区域 -->
        <div class="table-section">
            <div class="table-header">
                <h3>历史记录</h3>
                <div class="search">
                    <el-input v-model="searchKeyword" placeholder="请输入关键词" clearable />
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </div>
            </div>

            <el-table :data="filteredTableData" height="280" style="width: 100%" stripe>
                <el-table-column prop="id" label="序号" width="70" align="center" />
                <el-table-column prop="name" label="项目名称" width="160" align="center" />
                <el-table-column prop="date" label="检测时间" width="150" align="center" />
                <el-table-column prop="frequencies" label="刺激频率组合" min-width="150" align="center" show-overflow-tooltip />
                <el-table-column prop="score" label="评分结果" width="100" align="center">
                    <template #default="scope">
                        <span :class="getScoreClass(scope.row.score)">{{ scope.row.score }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="riskLevel" label="风险评级" width="100" align="center">
                    <template #default="scope">
                        <el-tag :type="getRiskType(scope.row.riskLevel)" size="small">{{ scope.row.riskLevel }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="300" align="center">
                    <template #default="scope">
                        <el-button link type="primary" size="small" @click="showDetail(scope.row)">
                            查看详情
                        </el-button>
                        <el-button link type="primary" size="small" @click="download(scope.row)">
                            下载
                        </el-button>
                        <el-popconfirm title="确认删除该记录?" confirm-button-text="确认" cancel-button-text="取消"
                            :icon="InfoFilled" icon-color="#626AEF">
                            <template #reference>
                                <el-button link type="danger" size="small" @click="handleDelete(scope.$index)">
                                    删除
                                </el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>

            <div class="pagination">
                <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next"
                    :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
            </div>
        </div>

        <!-- 详情弹窗 -->
        <el-dialog v-model="detailDialogVisible" title="检测详情" width="60%">
            <div class="detail-content">
                <div class="detail-item">
                    <span class="label">检测时间：</span>
                    <span>{{ currentDetail.date }}</span>
                </div>
                <div class="detail-item">
                    <span class="label">评分结果：</span>
                    <span :class="getScoreClass(currentDetail.score)">{{ currentDetail.score }}</span>
                </div>
                <div class="detail-item">
                    <span class="label">风险评级：</span>
                    <el-tag :type="getRiskType(currentDetail.riskLevel)">{{ currentDetail.riskLevel }}</el-tag>
                </div>
                <div class="detail-item">
                    <span class="label">系统建议：</span>
                    <span>{{ currentDetail.suggestion }}</span>
                </div>
                <div class="frequency-data">
                    <h4>频率响应数据</h4>
                    <el-table :data="currentDetail.frequencyData" style="width: 100%">
                        <el-table-column prop="frequency" label="频率(Hz)" width="120" />
                        <el-table-column prop="response" label="响应值" width="120" />
                        <el-table-column prop="status" label="状态">
                            <template #default="scope">
                                <el-tag :type="scope.row.status === '正常' ? 'success' : 'danger'">
                                    {{ scope.row.status }}
                                </el-tag>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 数据概览
const totalTests = ref(156)
const averageScore = ref(85.5)
const monthlyTests = ref(12)
const bestScore = ref(95)
const testTypes = ref(6)
const completionRate = ref(85)
const riskTrend = ref({
    type: 'success',
    text: '稳定'
})
const healthStatus = ref({
    type: 'success',
    text: '良好'
})

// 表格数据
const tableData = ref([
    {
        id: 1,
        name: '青光眼风险评估',
        date: '2024-03-20 15:30',
        frequencies: '8Hz, 9.75Hz, 10.25Hz, 12.25Hz, 14.75Hz',
        score: 92,
        riskLevel: '无风险',
        suggestion: '建议继续保持当前用眼习惯',
        frequencyData: [
            { frequency: '8Hz', response: '0.92', status: '正常' },
            { frequency: '9.75Hz', response: '0.88', status: '正常' },
            { frequency: '10.25Hz', response: '0.90', status: '正常' },
            { frequency: '12.25Hz', response: '0.95', status: '正常' },
            { frequency: '14.75Hz', response: '0.91', status: '正常' }
        ]
    },
    {
        id: 2,
        name: '青光眼风险评估',
        date: '2024-03-19 10:15',
        frequencies: '10Hz, 12Hz, 15Hz',
        score: 87,
        riskLevel: '无风险',
        suggestion: '建议减少长时间用眼，注意用眼卫生',
        frequencyData: [
            { frequency: '10Hz', response: '0.85', status: '正常' },
            { frequency: '12Hz', response: '0.87', status: '正常' },
            { frequency: '15Hz', response: '0.86', status: '正常' }
        ]
    },
    {
        id: 3,
        name: '青光眼风险评估',
        date: '2024-03-18 14:45',
        frequencies: '8.5Hz, 10.5Hz, 12.5Hz, 14.5Hz',
        score: 90,
        riskLevel: '无风险',
        suggestion: '建议定期检查，保持良好生活习惯',
        frequencyData: [
            { frequency: '8.5Hz', response: '0.91', status: '正常' },
            { frequency: '10.5Hz', response: '0.90', status: '正常' },
            { frequency: '12.5Hz', response: '0.89', status: '正常' },
            { frequency: '14.5Hz', response: '0.92', status: '正常' }
        ]
    },
    {
        id: 4,
        name: '青光眼风险评估',
        date: '2024-03-17 09:30',
        frequencies: '9Hz, 11Hz, 13Hz',
        score: 82,
        riskLevel: '无风险',
        suggestion: '建议增加护眼营养素摄入，注意用眼卫生',
        frequencyData: [
            { frequency: '9Hz', response: '0.81', status: '正常' },
            { frequency: '11Hz', response: '0.83', status: '正常' },
            { frequency: '13Hz', response: '0.79', status: '异常' }
        ]
    },
    {
        id: 5,
        name: '青光眼风险评估',
        date: '2024-03-16 16:20',
        frequencies: '7.5Hz, 9.5Hz, 11.5Hz, 13.5Hz',
        score: 88,
        riskLevel: '无风险',
        suggestion: '建议控制用眼时间，适当进行眼部按摩',
        frequencyData: [
            { frequency: '7.5Hz', response: '0.88', status: '正常' },
            { frequency: '9.5Hz', response: '0.89', status: '正常' },
            { frequency: '11.5Hz', response: '0.87', status: '正常' },
            { frequency: '13.5Hz', response: '0.90', status: '正常' }
        ]
    },
    {
        id: 6,
        name: '青光眼风险评估',
        date: '2024-03-15 11:00',
        frequencies: '8Hz, 10Hz, 12Hz, 15Hz',
        score: 85,
        riskLevel: '无风险',
        suggestion: '建议适当休息，避免长时间连续用眼',
        frequencyData: [
            { frequency: '8Hz', response: '0.84', status: '正常' },
            { frequency: '10Hz', response: '0.86', status: '正常' },
            { frequency: '12Hz', response: '0.85', status: '正常' },
            { frequency: '15Hz', response: '0.83', status: '正常' }
        ]
    }
])

// 搜索和分页
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

const filteredTableData = computed(() => {
    return tableData.value.filter(item => 
        item.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
        item.date.includes(searchKeyword.value)
    )
})

// 详情弹窗
const detailDialogVisible = ref(false)
const currentDetail = ref({})

// 图表相关
const chartRef = ref(null)
let chart = null

// 方法
const showDetail = (row) => {
    currentDetail.value = row
    detailDialogVisible.value = true
}

const handleDelete = (index) => {
    tableData.value.splice(index, 1)
}

const download = (row) => {
    // 实现下载逻辑
    console.log('下载数据:', row)
}

const handleSearch = () => {
    currentPage.value = 1
}

const handleSizeChange = (val) => {
    pageSize.value = val
    currentPage.value = 1
}

const handleCurrentChange = (val) => {
    currentPage.value = val
}

const getScoreClass = (score) => {
    if (score >= 90) return 'score-excellent'
    if (score >= 80) return 'score-good'
    if (score >= 70) return 'score-fair'
    return 'score-poor'
}

const getRiskType = (level) => {
    const types = {
        '无风险': 'success',
        '中风险': 'warning',
        '高风险': 'danger'
    }
    return types[level] || 'info'
}

const getProgressStatus = computed(() => {
    return completionRate.value >= 80 ? 'success' : 'warning'
})

// 初始化图表
onMounted(() => {
    chart = echarts.init(chartRef.value)
    const option = {
        title: {
            text: '最近6次检测评分趋势'
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                return `${params[0].name}<br/>评分：${params[0].value}分`
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['3-15', '3-16', '3-17', '3-18', '3-19', '3-20'],
            axisLabel: {
                interval: 0,
                rotate: 30
            }
        },
        yAxis: {
            type: 'value',
            min: 0,
            max: 100,
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
        },
        series: [{
            data: [85, 88, 82, 90, 87, 92],
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
                color: '#409EFF'
            },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    {
                        offset: 0,
                        color: 'rgba(64,158,255,0.3)'
                    },
                    {
                        offset: 1,
                        color: 'rgba(64,158,255,0.1)'
                    }
                ])
            }
        }]
    }
    chart.setOption(option)
})
</script>

<style lang="less" scoped>
.history-data-container {
    padding: 20px;
    background-color: #f5f7fa;
    min-height: 100vh;

    .overview-section {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;

        .statistics-card {
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);

            h3 {
                margin-bottom: 20px;
                color: #303133;
                font-size: 18px;
                font-weight: 600;
            }

            .stat-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 4px;
                background-color: #f8f9fa;

                .label {
                    color: #606266;
                    font-size: 14px;
                }

                .value {
                    font-size: 18px;
                    font-weight: bold;
                    color: #303133;
                }

                .el-progress {
                    width: 120px;
                }
            }
        }

        .trend-chart {
            flex: 2;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);

            h3 {
                margin-bottom: 20px;
                color: #303133;
                font-size: 18px;
                font-weight: 600;
            }

            .chart-legend {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;

                .legend-item {
                    display: flex;
                    align-items: center;
                    font-size: 12px;
                    color: #606266;

                    .dot {
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        margin-right: 6px;

                        &.excellent {
                            background-color: #67C23A;
                        }

                        &.good {
                            background-color: #409EFF;
                        }

                        &.fair {
                            background-color: #E6A23C;
                        }

                        &.poor {
                            background-color: #F56C6C;
                        }
                    }
                }
            }
        }
    }

    .table-section {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);

        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0px;

            h3 {
                margin-left: 5px;
                color: #303133;
                font-size: 18px;
                font-weight: 600;
            }

            .search {
                display: flex;
                gap: 10px;
            }
        }

        .pagination {
            margin-top: 20px;
            display: flex;
            justify-content: flex-end;
        }
    }
}

.detail-content {
    .detail-item {
        margin-bottom: 15px;
        display: flex;
        align-items: center;

        .label {
            font-weight: bold;
            margin-right: 10px;
            color: #606266;
        }
    }

    .frequency-data {
        margin-top: 20px;

        h4 {
            margin-bottom: 15px;
            color: #303133;
        }
    }
}

.score-excellent {
    color: #67C23A;
    font-weight: bold;
}

.score-good {
    color: #409EFF;
    font-weight: bold;
}

.score-fair {
    color: #E6A23C;
    font-weight: bold;
}

.score-poor {
    color: #F56C6C;
    font-weight: bold;
}
</style>