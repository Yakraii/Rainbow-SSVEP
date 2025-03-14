<template>
    <el-scrollbar height="640px" class="Treat_scrollbar">
        <el-row :gutter="20">
            <el-col :span="16" class="l">

                <div class="treatsection">
                    <el-card style="width: 100%; height: 200%;" shadow="hover" class="animation1 animate__animated animate__bounceInDown"
                        :body-style="{ background: 'linear-gradient(to bottom, #f2eff7, #fcfcfd)' }">
                        <h1>视觉健康评估与改善建议</h1>
                        <p>欢迎来到我们的视觉健康评估与改善建议页面。我们通过先进的系统检测和评测六项重要的视觉健康指标，
                            包括颜色感知、视力、视觉灵敏度、青光眼、白内障和黄斑病变。
                            根据检测结果，我们将为您提供个性化的治理或护理建议，帮助您更好地保护和改善视觉健康。
                        </p>
                    </el-card>
                </div>

                <div class="treatsection">
                    <el-card style="max-width: 480px" shadow="hover" class="animation1 animate__animated animate__lightSpeedInLeft">
                        <h2>颜色感知改善建议</h2>
                        <p>颜色感知能力是我们日常生活中非常重要的一部分。如果检测结果显示您的颜色感知存在问题，以下是一些建议：</p>
                        <ul>
                            <li>定期进行颜色感知测试，以监测变化和及时调整护理方案。</li>
                            <li>在阅读或工作时，确保充足的自然光线或使用高显色性的灯光。</li>
                            <li>通过食用富含维生素A和C的食物，如胡萝卜和柑橘类水果，来改善眼睛健康。</li>
                            <li>使用色彩校正眼镜或滤光镜，帮助提高颜色分辨能力。</li>
                        </ul>
                    </el-card>

                    <el-card style="max-width: 480px" shadow="hover" class="animation1 animate__animated animate__bounceIn">
                        <h2>视力改善建议</h2>
                        <p>视力是影响我们生活质量的关键因素。如果检测显示您的视力下降，以下建议可能会有所帮助：</p>
                        <ul>
                            <li>定期进行视力检查，及时更换眼镜或隐形眼镜度数。</li>
                            <li>避免长时间注视电子屏幕，每隔20分钟休息一下，远眺20英尺外的物体20秒。</li>
                            <li>保持健康饮食，多摄入富含Omega-3脂肪酸的食物，如鱼类和亚麻籽。</li>
                            <li>进行适当的眼部运动，缓解眼睛疲劳。</li>
                        </ul>
                    </el-card>
                </div>

                <div class="treatsection">
                    <el-card style="max-width: 480px" shadow="hover" class="animation1 animate__animated animate__lightSpeedInLeft">
                        <h2>视觉灵敏度改善建议</h2>
                        <p>视觉灵敏度影响我们在不同光照条件下的视力表现。以下是一些提高视觉灵敏度的建议：</p>
                        <ul>
                            <li>使用光学滤镜或抗反光镜片，减少光线反射和眩光。</li>
                            <li>确保在不同环境下有适宜的照明，避免过暗或过亮。</li>
                            <li>进行户外活动，接触自然光，但避免直视强光源。</li>
                            <li>保持眼部清洁，避免眼部感染和炎症。</li>
                        </ul>
                    </el-card>

                    <el-card style="max-width: 480px" shadow="hover" class="animation1 animate__animated animate__bounceIn">
                        <h2>青光眼护理建议</h2>
                        <p>青光眼是一种严重的眼部疾病，需要早期发现和持续护理。以下是护理青光眼的建议：</p>
                        <ul>
                            <li>定期进行眼压检查，尤其是有青光眼家族史的人群。</li>
                            <li>遵医嘱使用降眼压药物，避免随意停药。</li>
                            <li>保持健康的生活方式，避免吸烟和过量饮酒。</li>
                            <li>控制血糖和血压，减少对眼睛的损害。</li>
                        </ul>
                    </el-card>
                </div>

                <div class="treatsection" style="margin-bottom: 150px">
                    <el-card style="max-width: 480px" shadow="hover" class="animation1 animate__animated animate__lightSpeedInLeft">
                        <h2>白内障护理建议</h2>
                        <p>白内障是随着年龄增长常见的眼部问题。以下是护理和延缓白内障的建议：</p>
                        <ul>
                            <li>定期眼科检查，监测白内障的发展情况。</li>
                            <li>佩戴防紫外线的太阳镜，保护眼睛免受紫外线伤害。</li>
                            <li>保持健康饮食，多摄入抗氧化剂，如维生素C和E。</li>
                            <li>避免吸烟，减少对眼睛的自由基损伤。</li>
                        </ul>
                    </el-card>

                    <el-card style="max-width: 480px" shadow="hover" class="animation1 animate__animated animate__bounceIn">
                        <h2>黄斑病变护理建议</h2>
                        <p>黄斑病变是影响中心视力的严重疾病。以下是护理黄斑病变的建议：</p>
                        <ul>
                            <li>定期进行黄斑检查，尤其是50岁以上人群。</li>
                            <li>摄入富含叶黄素和玉米黄质的食物，如深绿色蔬菜。</li>
                            <li>保持健康体重，避免肥胖带来的眼部压力。</li>
                            <li>戒烟，减少黄斑病变的风险。</li>
                        </ul>
                    </el-card>
                </div>

            </el-col>
            <el-col :span="8" class="r">
                <div class="Treat_animation animation1 animate__animated animate__bounceInDown" id="lottieId" ></div>

                <el-card shadow="hover" class="animation1 animate__animated animate__lightSpeedInRight">
                    <el-scrollbar height="400px">
                        <h2>眼科疾病检测现状</h2>
                        <p>近年来，基于脑电图（EEG）的眼科疾病检测方法取得了显著进展。以下是一些最新的研究方向和成果：</p>
                        <ul>
                            <li>
                                <strong>机器学习与深度学习算法：</strong>
                                <p>研究人员利用机器学习和深度学习模型（如卷积神经网络和循环神经网络）分析EEG数据，
                                    以检测青光眼、黄斑病变等眼科疾病。
                                    这些模型能够从大量EEG信号中提取特征，实现高精度的疾病分类和预测。
                                </p>
                            </li>
                            <li>
                                <strong>视觉诱发电位（VEP）：</strong>
                                <p>通过分析视觉刺激引起的VEP变化，研究人员可以早期检测视神经损伤和视功能障碍。
                                    VEP在检测青光眼和黄斑病变的早期症状方面表现出很高的敏感性。</p>
                            </li>
                        </ul>
                        <p style="margin-bottom: 150px">总体而言，基于EEG的眼科疾病检测正在
                            向功能性和动态检测转变，为早期诊断和个性化治疗提供了新的可能。</p>
                    </el-scrollbar>

                </el-card>


                <el-card shadow="hover" class="animation1 animate__animated animate__lightSpeedInRight">
                    <el-scrollbar height="400px">
                        <h2>基于脑电的研究前景与挑战</h2>
                        <p>尽管基于脑电图（EEG）的眼科疾病检测和治疗研究取得了许多进展，但仍存在一些挑战和未来的研究方向：</p>
                        <ul>
                            <li>
                                <strong>数据处理与分析：</strong>
                                <p>高质量的EEG数据处理和分析仍然是一个挑战。研究人员需要开发更高效、更精确的算法来提取有用的特征，并提高模型的泛化能力。</p>
                            </li>
                            <li>
                                <strong>多模态数据融合：</strong>
                                <p>如何有效融合EEG数据与其他生物信号（如眼动数据、视网膜成像数据）仍需深入研究，以提高检测和治疗的准确性和可靠性。</p>
                            </li>
                            <li>
                                <strong>个性化与实时应用：</strong>
                                <p>个性化治疗方案和实时应用是未来的重要方向。研究需要进一步探索如何根据个体的EEG特征，实时调整治疗策略。</p>
                            </li>
                            <li>
                                <strong>伦理与隐私：</strong>
                                <p>随着EEG技术的广泛应用，数据隐私和伦理问题也需引起重视。研究人员需要确保患者数据的安全性和隐私保护。</p>
                            </li>
                        </ul>
                        <p style="margin-bottom: 150px">未来，随着技术的进步和多学科的合作，基于EEG的眼科疾病检测和治疗将有望实现更大的突破，提供更加精准和高效的解决方案。</p>
                    </el-scrollbar>

                </el-card>

            </el-col>
        </el-row>
    </el-scrollbar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import lottie from 'lottie-web'

const lottieInstance = ref(null)

const init = () => {
    // 读取动画容器
    const lottieContainer = document.getElementById('lottieId')

    if (!lottieContainer) return;
    // 实例化
    lottieInstance.value = lottie.loadAnimation({
        // UED 提供的 动画的 json 文件
        path: '../../public/doctor.json',
        // 渲染方式
        renderer: "svg",
        // 是否循环
        loop: true,
        autoplay: true, // 自动播放
        container: lottieContainer,  // 用于渲染的容器
    });

    lottieInstance.value.setSpeed(1.5);

    // 设置容器透明度
    lottieContainer.style.opacity = "0.8";
}


const onStart = () => {
    lottieInstance.value?.play();
}

onMounted(() => {
    init()
    onStart()
})

</script>

<style lang="less" scoped>
.Treat_scrollbar {
    .l {
        .treatsection {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-left: 20px;
            padding-right: 20px;

            .el-card {
                width: 48%;
                height: 350px;
            }
        }
    }


    .r {
        padding-left: 20px;
        padding-right: 10px;

        .Treat_animation {
            margin-left: 70px;
            margin-bottom: 20px;
            height: 250px;
            width: 250px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .el-card {
            height: 400px;
            margin-bottom: 20px;
            width: 95%;
        }
    }

    h1 {
        font-size: 24px;
        font-weight: bold;
        color: rgb(50, 50, 50);
        margin-bottom: 5px;
    }

    h2 {
        font-size: 20px;
        font-weight: bold;
        color: rgb(50, 50, 50);
        margin-bottom: 5px;
    }

    li,
    p {
        font-size: 15px;
        font-weight: 400;
        color: rgb(117, 116, 116)
    }

}
</style>