<template>
    <div class="TourArea">
        <el-space>
            <el-card ref="ref1" shadow="hover">
                <img src="../../public/image/detect/1.png" class="ima">
                <p>佩戴脑电帽</p>
            </el-card>
            <el-card ref="ref2" shadow="hover">
                <img src="../../public/image/detect/2.png" class="ima">
                <p>注入导电膏</p>
            </el-card>
            <el-card ref="ref3" shadow="hover">
                <img src="../../public/image/detect/3.png" class="ima">
                <p>检查脑电提取率</p>
            </el-card>
            <el-card ref="ref4" shadow="hover">
                <img src="../../public/image/detect/4.png" class="ima">
                <p>一切准备就绪</p>
            </el-card>
        </el-space>

        <el-tour v-model="store.open" @finish="onTourFinish">
            <el-tour-step :target="ref1?.$el" title="佩戴脑电帽">
                <div class="tour_t">确保脑电帽佩戴牢固且舒适，不要过紧或过松，调整好电极的位置，以获得最佳的信号接收。</div>
            </el-tour-step>
            <el-tour-step :target="ref2?.$el" title="注入导电膏">
                <div class="tour_t">均匀涂抹导电膏，不要过量，以避免浪费，同时确保每个电极都覆盖到位，避免干燥和硬化。</div>
            </el-tour-step>
            <el-tour-step :target="ref3?.$el" title="检查脑电提取率">
                <div class="tour_t">查看提取率数据，如果有任何异常或低于标准，请重新调整脑电帽或导电膏的位置，确保信号质量达标。</div>
            </el-tour-step>
            <el-tour-step :target="ref4?.$el" title="一切准备就绪">
                <div class="tour_t">再次确认周围环境安静，以免干扰脑电波信号的采集。同时放松心情，深呼吸，准备好迎接一次轻松愉快的检测。</div>
            </el-tour-step>
        </el-tour>
    </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCounterStore } from '../stores/counter.js'
const store = useCounterStore()

const ref1 = ref()
const ref2 = ref()
const ref3 = ref()
const ref4 = ref()

const onTourFinish = () => {
    store.tour_end = true
    console.log('导览已完成')
}

</script>


<style lang="less" scoped>
.TourArea {


    .el-space {
        display: flex;
        flex-direction: row;
        align-items: center;
        padding-left: 20px;
        padding-right: 20px;
        justify-content: center;
        margin-top: 60px;

        .el-card {
            height: 300px;
            width: 200px;
            margin-left: 25px;
            margin-right: 25px;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;

            .ima {
                height: 100px;
                width: 100px;
                margin-bottom: 20px;
            }

            p {
                font-size: 18px;
                font-weight: bold;
                color: #585858;
            }

        }

    }

}

.tour_t {
    font-size: 16px;
    font-weight: 500;
    color: #606060;
}
</style>