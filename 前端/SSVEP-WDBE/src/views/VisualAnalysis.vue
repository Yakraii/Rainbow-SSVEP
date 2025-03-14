<template>
    <el-scrollbar height="640px" id="scrollbar">
        <div class="Chartpage">
            <div class="top">
                <div id="animation1" class="wow animation1 animate__animated animate__rollIn"></div>
            </div>
            <div class="mid">
                <el-card style="width: 90%;height: 90%;" shadow="hover"
                    class="wow animate__animated animate__rotateInUpRight" >

                    <el-row>

                        <el-col :span="4">
                            <el-statistic :value="outputValue1"
                                :value-style="{ color: '#79bbff', 'font-size': '32px', 'margin-right': '10px' }">
                                <template #title>
                                    <div style="display: inline-flex; align-items: center">
                                        颜色感知评分
                                        <img src="../../public/image/icon/main/1.png" class="icon">
                                    </div>

                                </template>
                                <template #suffix>
                                    <div>分</div>
                                </template>
                            </el-statistic>
                            
                        </el-col>

                        <el-col :span="4">
                            <el-statistic :value="outputValue2"
                                :value-style="{ color: '#79bbff', 'font-size': '32px', 'margin-right': '10px' }">
                                <template #title>
                                    <div style="display: inline-flex; align-items: center">
                                        视力评分
                                        <img src="../../public/image/icon/main/2.png" class="icon">
                                    </div>

                                </template>
                                <template #suffix>
                                    <div>分</div>
                                </template>
                            </el-statistic>
                        </el-col>

                        <el-col :span="4">
                            <el-statistic :value="outputValue3"
                                :value-style="{ color: '#79bbff', 'font-size': '32px', 'margin-right': '10px' }">
                                <template #title>
                                    <div style="display: inline-flex; align-items: center">
                                        视觉灵敏度评分
                                        <img src="../../public/image/icon/main/33.png" class="icon">
                                    </div>

                                </template>
                                <template #suffix>
                                    <div>分</div>
                                </template>
                            </el-statistic>
                        </el-col>

                        <el-col :span="4">
                            <el-statistic :value="outputValue4"
                                :value-style="{ color: '#79bbff', 'font-size': '32px', 'margin-right': '10px' }">
                                <template #title>
                                    <div style="display: inline-flex; align-items: center">
                                        青光眼评分
                                        <img src="../../public/image/icon/main/44.png" class="icon">
                                    </div>

                                </template>
                                <template #suffix>
                                    <div>分</div>
                                </template>
                            </el-statistic>
                        </el-col>

                        <el-col :span="4">
                            <el-statistic :value="outputValue5"
                                :value-style="{ color: '#79bbff', 'font-size': '32px', 'margin-right': '10px' }">
                                <template #title>
                                    <div style="display: inline-flex; align-items: center">
                                        白内障评分
                                        <img src="../../public/image/icon/main/55.png" class="icon">
                                    </div>

                                </template>
                                <template #suffix>
                                    <div>分</div>
                                </template>
                            </el-statistic>
                        </el-col>

                        <el-col :span="4">
                            <el-statistic :value="outputValue6"
                                :value-style="{ color: '#79bbff', 'font-size': '32px', 'margin-right': '10px' }">
                                <template #title>
                                    <div style="display: inline-flex; align-items: center">
                                        黄斑病评分
                                        <img src="../../public/image/icon/main/6.png" class="icon">
                                    </div>

                                </template>
                                <template #suffix>
                                    <div>分</div>
                                </template>
                            </el-statistic>
                        </el-col>

                    </el-row>

                </el-card>
            </div>
            <div class="bot">
                <div class="wow animation2 animate__animated animate__rotateInUpLeft" id="animation2"></div>
            </div>
        </div>

        <div class="Chartpage">
            <div class="sec1">
                <p class="t animate__animated animate__fadeInTopLeft">生理信号分析</p>
            </div>
            <div class="sec2">
                <el-card style="width: 45%; height: 100%; margin-left: 2.5%; margin-right: 2.5%;" shadow="hover"
                    class="animate__animated animate__fadeInTopLeft" >
                    <el-empty description="description" />
                </el-card>

                <el-card style="width: 45%;height: 100%; margin-left: 2.5%; margin-right: 2.5%;" shadow="hover"
                    class="animate__animated animate__fadeInTopRight">
                    <el-empty description="description" />
                </el-card>
            </div>
            <div class="sec3">
                <el-card style="width: 45%; height: 100%; margin-left: 2.5%; margin-right: 2.5%;" shadow="hover"
                    class="animate__animated animate__fadeInBottomLeft">
                    <el-empty description="description" />
                </el-card>

                <div style="width: 45%;height: 100%; margin-left: 2.5%; margin-right: 2.5%;"
                    class="animation3 animate__animated animate__fadeInBottomRight" id="animation3">
                </div>
            </div>
        </div>

        <div class="Chartpage" style="margin-bottom: 50px;">
            <div class="sec1">
                <p class="t animate__animated animate__fadeInTopLeft">实验适应性分析</p>
            </div>
            <div class="sec2">
                <el-card style="width: 45%; height: 100%; margin-left: 2.5%; margin-right: 2.5%;" shadow="hover"
                    class="animate__animated animate__fadeInTopLeft">
                    <el-empty description="description" />
                </el-card>

                <el-card style="width: 45%;height: 100%; margin-left: 2.5%; margin-right: 2.5%;" shadow="hover"
                    class="animate__animated animate__fadeInTopRight">
                    <el-empty description="description" />
                </el-card>
            </div>
            <div class="sec3">

                <div style="width: 45%;height: 100%; margin-left: 2.5%; margin-right: 2.5%;"
                    class="animation4 animate__animated animate__fadeInBottomLeft" id="animation4">
                </div>

                <el-card style="width: 45%; height: 100%; margin-left: 2.5%; margin-right: 2.5%;" shadow="hover"
                    class="animate__animated animate__fadeInBottomRight">
                    <el-empty description="description" />
                </el-card>

            </div>
        </div>
    </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useTransition } from '@vueuse/core'
import lottie from 'lottie-web'
// import WOW from 'wow.js/dist/wow.min.js'
import WOW from "wow.js";

const source1 = ref(0)
const outputValue1 = useTransition(source1, {
    duration: 2000,
})
source1.value = 83

const source2 = ref(0)
const outputValue2 = useTransition(source2, {
    duration: 2000,
})
source2.value = 92

const source3 = ref(0)
const outputValue3 = useTransition(source3, {
    duration: 2000,
})
source3.value = 75

const source4 = ref(0)
const outputValue4 = useTransition(source4, {
    duration: 2000,
})
source4.value = 69

const source5 = ref(0)
const outputValue5 = useTransition(source5, {
    duration: 2000,
})
source5.value = 88

const source6 = ref(0)
const outputValue6 = useTransition(source6, {
    duration: 2000,
})
source6.value = 96



const lottie1 = ref(null)
const lottie2 = ref(null)
const lottie3 = ref(null)
const lottie4 = ref(null)

const init = () => {
    // 读取动画容器
    const lottieContainer1 = document.getElementById('animation1')
    const lottieContainer2 = document.getElementById('animation2')
    const lottieContainer3 = document.getElementById('animation3')
    const lottieContainer4 = document.getElementById('animation4')

    if (!lottieContainer1) return;
    if (!lottieContainer2) return;
    if (!lottieContainer3) return;
    if (!lottieContainer4) return;
    // 实例化
    lottie1.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/lucky.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer1,  // 用于渲染的容器
    });

    lottie2.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/analyse.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer2,  // 用于渲染的容器
    });

    lottie3.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/analyse2.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer3,  // 用于渲染的容器
    });

    lottie4.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/discuss.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer4,  // 用于渲染的容器
    });

    lottie1.value.setSpeed(1.0);
    lottie2.value.setSpeed(0.7);
    lottie3.value.setSpeed(1.0);
    lottie4.value.setSpeed(0.4);

    // 设置容器透明度
    lottieContainer1.style.opacity = "0.7";
    lottieContainer2.style.opacity = "0.8";
    lottieContainer3.style.opacity = "0.6";
    lottieContainer4.style.opacity = "0.5";
}


const onStart = () => {
    lottie1.value?.play();
    lottie2.value?.play();
    lottie3.value?.play();
    lottie4.value?.play();
}

const wow = ref(null);
const initWOW = () => {
    wow.value = new WOW();
    wow.value.init();
}



onMounted(() => {
    init()
    onStart()
    initWOW()
})

</script>

<style lang="less" scoped>
.el-scrollbar {
    display: flex;
    flex-direction: column;
    padding-bottom: 0px;

    .el-col {
        text-align: center;
    }

    .Chartpage {
        height: 620px;
        margin-top: 20px;

        .top {
            height: 33%;
            display: flex;
            justify-content: right;
            align-items: center;

            .animation1 {
                height: 100%;
                width: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
        }

        .mid {
            height: 34%;
            display: flex;
            justify-content: center;
            align-items: center;

            .el-card {
                align-content: center;

                .el-row {
                    width: 100%;
                    height: 100%;
                    text-align: center;

                    span {
                        font-size: 32px;
                    }

                    div {
                        font-size: 18px;
                        font-weight: bold;
                    }

                    .icon {
                        height: 20px;
                        width: 20px;
                        margin-left: 10px;
                    }
                }
            }
        }

        .bot {
            height: 33%;
            display: flex;
            justify-content: left;
            align-items: center;

            .animation2 {
                height: 100%;
                width: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
        }

        .sec1 {
            height: 6%;
            display: flex;
            flex-direction: row;
            align-items: center;

            .t {
                font-size: 18px;
                margin-left: 20px;
                font-weight: bold;
                color: rgb(46, 45, 45);
            }
        }

        .sec2 {
            height: 47%;
            display: flex;
            flex-direction: row;
            align-items: center;
            padding: 20px;
            padding-top: 5px;
            padding-bottom: 5px;
        }

        .sec3 {
            height: 47%;
            display: flex;
            flex-direction: row;
            align-items: center;
            padding: 20px;
            padding-top: 5px;
            padding-bottom: 5px;

            .animation3 {
                height: 100%;
                width: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .animation4 {
                height: 100%;
                width: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
        }
    }
}
</style>
