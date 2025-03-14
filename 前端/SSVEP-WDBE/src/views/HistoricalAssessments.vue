<template>
    <div class="history_content">
        <el-scrollbar height="590px" style="width: 800px;">
            <el-timeline style="max-width: 780px">
                <el-timeline-item v-for="item in timestamp_data" :key="item.index" :type="item.type" :color="item.color"
                    :hollow="item.hollow" :timestamp="item.date" placement="top">
                    <el-card shadow="hover" @click="triggerAnimation($event)">
                        <div class="con">
                            <div class="l">
                                <p class="t1">{{ item.name }}</p>
                                <p class="t2">{{ item.count }}</p>
                            </div>
                            <div class="r">
                                <el-button link :type=item.type size="large">
                                    <p class="t3">{{ item.score }}</p>
                                </el-button>
                            </div>
                        </div>
                    </el-card>
                </el-timeline-item>
            </el-timeline>
        </el-scrollbar>

        <div class="ani_box">
            <div class="history_sun" id="lottieId2"></div>

            <div class="history_animation" id="lottieId"></div>
        </div>

    </div>

</template>

<script setup>
import timestamp_data from '@/assets/data/timestamp_data.json'
import { ref, onMounted } from 'vue'
import lottie from 'lottie-web'


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


const lottieInstance = ref(null)
const lottieInstance2 = ref(null)

const init = () => {
    // 读取动画容器
    const lottieContainer = document.getElementById('lottieId')
    const lottieContainer2 = document.getElementById('lottieId2')

    if (!lottieContainer) return;
    if (!lottieContainer2) return;
    // 实例化
    lottieInstance.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/newspaper_animation.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer,  // 用于渲染的容器
    });

    lottieInstance2.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/sun.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer2,  // 用于渲染的容器
    });

    lottieInstance.value.setSpeed(1.5);
    lottieInstance2.value.setSpeed(0.8);

    // 设置容器透明度
    lottieContainer.style.opacity = "0.8";
    lottieContainer2.style.opacity = "0.4";
}


const onStart = () => {
    lottieInstance.value?.play();
    lottieInstance2.value?.play();
}

onMounted(() => {
    init()
    onStart()
})



</script>

<style lang="less" scoped>
.history_content {
    display: flex;
    flex-direction: row;

    .el-card {
        .con {
            display: flex;
            flex-direction: row;

            .l {
                width: 70%;

                .t1 {
                    font-size: 24px;
                    font-weight: bold;
                    color: #444343;
                }

                .t2 {
                    font-size: 20px;
                    font-weight: bold;
                    color: #636262;
                }
            }

            .r {
                width: 30%;
                display: flex;
                justify-content: center;
                align-items: center;

                .t3 {
                    font-size: 22px;
                    font-weight: bolder;
                }
            }
        }
    }

    .ani_box {
        display: flex;
        flex-direction: column;

        .history_sun {
            margin-top: 20px;
            margin-left: 250px;
            height: 150px;
            width: 150px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .history_animation {
            margin-top: 70px;
            height: 400px;
            width: 400px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

    }

}
</style>