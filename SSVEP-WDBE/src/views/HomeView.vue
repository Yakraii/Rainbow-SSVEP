<template>
    <el-row :gutter="10">
        <el-col :span="8" class="left-area">
            <el-card style="max-width: 480px" shadow="hover">
                <div class="user">
                    <img src="../../public/image/profile.png" class="user-avatar">
                    <div class="userinfo">
                        <p class="name">CHIYO</p>
                        <p class="access">前端工程师</p>
                    </div>
                </div>
                <template #footer>
                    <div class="login-info">
                        <p>上次登录的时间： <span>2024-05-25</span> </p>
                        <p>上次登录的地点： <span>广东</span> </p>
                    </div>
                </template>
            </el-card>

            <el-card style="max-width: 480px" shadow="hover">
                <el-table :data="tableData" stripe style="width: 100%" height="290">
                    <el-table-column prop="Project" label="项目" width="180" align="center" />
                    <el-table-column prop="Date" label="日期" width="180" align="center" />
                </el-table>
            </el-card>
        </el-col>
        <el-col :span="16" class="right-area">
            <div class="num">
                <el-card shadow="hover" v-for="item in countDate" :key="item.name" class="num-card"
                    :body-style="{ display: 'flex' }" @click="triggerAnimation($event)">
                    <div class="icon-bg" :style="{ 'background-color': item.color }">
                        <img :src="item.icon">
                    </div>
                    <div class="content">
                        <p class="times">{{ item.value }} 次</p>
                        <p class="name">{{ item.name }}</p>
                    </div>
                </el-card>
            </div>

            <el-card shadow="hover" class="graph1">
                <div ref="echarts1" style="width: 100%; height: 200px;"></div>
            </el-card>

            <div class="graph-group">
                <el-card shadow="hover" class="graph2">
                    <div ref="echarts2" style="width: 100%; height: 200px;"></div>
                </el-card>

                <el-card shadow="hover" class="graph2">
                    <div ref="echarts3" style="width: 100%; height: 200px;"></div>
                </el-card>
            </div>

        </el-col>
    </el-row>
</template>

<script setup>
import { onMounted, ref, inject } from "vue";

//通过inject使用echarts
const echarts = inject("echarts");

//通过ref获取html元素
const echarts1 = ref();
const echarts2 = ref();
const echarts3 = ref();


const tableData = [
    {
        Project: '视力检测',
        Date: '2024-06-21',
    },
    {
        Project: '黄斑病检测',
        Date: '2024-06-20',
    },
    {
        Project: '敏感度检测',
        Date: '2024-06-12',
    },
    {
        Project: '白内障检测',
        Date: '2024-06-04',
    },
    {
        Project: '颜色感知检测',
        Date: '2024-05-28',
    }, {
        Project: '青光眼检测',
        Date: '2024-05-28',
    },
    {
        Project: '黄斑病检测',
        Date: '2024-05-22',
    },
    {
        Project: '敏感度检测',
        Date: '2024-05-19',
    },
    {
        Project: '白内障检测',
        Date: '2024-05-11',
    },
]

const countDate = [
    {
        name: "颜色感知检测次数",
        value: 10,
        icon: "../../public/image/icon/main/1.png",
        color: "#359ed5",
    },
    {
        name: "视力检测次数",
        value: 12,
        icon: "../../public/image/icon/main/2.png",
        color: "#2ec3ee",
    },
    {
        name: "敏感度检测次数",
        value: 8,
        icon: "../../public/image/icon/main/3.png",
        color: "#9beabd",
    },
    {
        name: "青光眼检测次数",
        value: 4,
        icon: "../../public/image/icon/main/4.png",
        color: "#ffd960",
    },
    {
        name: "白内障检测次数",
        value: 5,
        icon: "../../public/image/icon/main/5.png",
        color: "#ff9d86",
    },
    {
        name: "黄斑病检测次数",
        value: 1,
        icon: "../../public/image/icon/main/6.png",
        color: "#f67795",
    },
]

onMounted(() => {
    // 渲染echarts的父元素
    var infoE1 = echarts1.value;
    var infoE2 = echarts2.value;
    var infoE3 = echarts3.value;

    //  light dark
    var userEc1 = echarts.init(infoE1, "light");
    var userEc2 = echarts.init(infoE2, "light");
    var userEc3 = echarts.init(infoE3, "light");

    // 指定图表的配置项和数据
    var option1 = {
        title: {
            text: '综合评分指数'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['颜色感知', '视力', '灵敏度', '青光眼', '白内障', '黄斑病']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07']
        },
        yAxis: {
            type: 'value',
            min: null,
            max: null,
            scale: false  // 关闭自动调整刻度
        },
        series: [
            {
                name: '颜色感知',
                type: 'line',
                data: [42, 78, 56, 13, 71, 48, 19]
            },
            {
                name: '视力',
                type: 'line',
                data: [76, 56, 95, 34, 47, 18, 65]
            },
            {
                name: '灵敏度',
                type: 'line',
                data: [53, 24, 46, 32, 69, 82, 97]
            },
            {
                name: '青光眼',
                type: 'line',
                data: [12, 65, 38, 81, 27, 44, 93]
            },
            {
                name: '白内障',
                type: 'line',
                data: [5, 59, 29, 88, 50, 21, 79]
            },
            {
                name: '黄斑病',
                type: 'line',
                data: [37, 63, 22, 78, 91, 58, 15]
            }
        ]
    };

    var option2 = {
        title: {
            text: '累计检测次数'
        },
        tooltip: {
            trigger: 'axis'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            data: ['颜色', '视力', '灵敏度', '青光眼', '白内障', '黄斑病'],
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: [10, 12, 8, 4, 5, 1],
                type: 'bar'
            }
        ]
    };

    var option3 = {
        title: {
            text: '检测偏好',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    { value: 10, name: '颜色感知' },
                    { value: 12, name: '视力检测' },
                    { value: 8, name: '视觉灵敏度' },
                    { value: 4, name: '青光眼' },
                    { value: 5, name: '白内障' },
                    { value: 1, name: '黄斑病' }
                ]
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    userEc1.setOption(option1);
    userEc2.setOption(option2);
    userEc3.setOption(option3);
});

const triggerAnimation = (event) => {
    const cardElement = event.currentTarget.closest('.el-card'); // 获取点击的整个卡片元素
    if (!cardElement) return;

    // 添加动画类
    cardElement.classList.add('animate__animated', 'animate__pulse');

    // 监听动画结束事件
    cardElement.addEventListener('animationend', () => {
        // 删除动画类
        cardElement.classList.remove('animate__animated', 'animate__pulse');
    }, { once: true }); // 确保事件监听器只会触发一次
}

</script>

<style lang="less" scoped>
.left-area {
    margin-bottom: 0%;

    .el-card {
        margin-left: 3%;
        margin-top: 2%;
        margin-bottom: 3%;
    }

    .user {
        display: flex;
        flex-direction: row;
        align-items: center;

        .user-avatar {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 40px;
        }

        .userinfo {
            display: flex;
            flex-direction: column;
            text-align: center;

            .name {
                font-size: 32px;
                margin-bottom: 0px;
            }

            .access {
                color: #999999;
                margin-top: 0px;
            }
        }
    }

    .login-info {
        display: flex;
        flex-direction: column;

        p {
            font-size: 14px;
            color: #3f3f3f;
        }

        span {
            font-size: 14px;
            color: #626161;
            margin-left: 50px;
        }
    }

    .el-table {
        font-size: 14px;
    }

}

.right-area {
    margin-top: 8px;
    margin-right: 0px;
    margin-bottom: 0%;
    height: 100%;
    width: 100%;
    overflow: hidden;

    .num {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        padding-left: 0px;

        .el-card {
            width: 32%;
            margin-bottom: 20px;
            margin-right: 10px;
            margin-left: 0px;

            /deep/.el-card__body {
                padding: 0;
            }

            .icon-bg {
                height: 75px;
                width: 100px;
                display: flex;
                justify-content: center;
                align-items: center;

                img {
                    height: 45px;
                    width: 45px;
                    border-radius: 50%;
                }
            }

            .content {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                width: 100%;

                .times {
                    font-size: 27px;
                    font-weight: bold;
                    color: #595959;
                }

                .name {
                    font-size: 14px;
                    color: #919191;
                }
            }

        }

    }

    .graph1 {
        width: 99%;
        height: 200px;
        margin-bottom: 20px;
    }

    .graph-group {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        padding-right: 2%;

        .graph2 {
            height: 200px;
            width: 49%;
        }
    }
}
</style>