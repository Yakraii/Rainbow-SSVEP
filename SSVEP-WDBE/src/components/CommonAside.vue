<template>

    <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="store.isCollapse" @open="handleOpen"
        @close="handleClose" text-color="#9799a8" active-text-color="#46495c" background-color="#ffffff"
        :class="{ 'expanded': !store.isCollapse, 'collapsed': store.isCollapse }">


        <el-container>
            <el-header height="15%">
                <div class="title-name">
                    <div class="logo-con">
                        <img src="../../public/image/eye of horus.png" class="logo-img">
                    </div>
                    <text>Eyes of Horus</text>
                </div>
            </el-header>

            <el-scrollbar height="630px">
                <el-main>

                    <div class="con" @click="clickMenu('/HomeView')">
                        <el-menu-item index="1">
                            <el-icon>
                                <House />
                            </el-icon>
                            <template #title>
                                <span class="Aside-text">主页</span>
                            </template>
                        </el-menu-item>
                    </div>


                    <el-sub-menu index="2">
                        <template #title>
                            <el-icon>
                                <Files />
                            </el-icon>
                            <span class="Aside-text">数据仓库</span>
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="2-1" @click="clickMenu('/DataBase/RealTimeData')">实时数据</el-menu-item>
                            <el-menu-item index="2-2" @click="clickMenu('/DataBase/LocalData')">导入数据</el-menu-item>
                        </el-menu-item-group>
                    </el-sub-menu>

                    <el-sub-menu index="3">
                        <template #title>
                            <el-icon>
                                <Stopwatch />
                            </el-icon>
                            <span class="Aside-text">视功能检测</span>
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="3-1"
                                @click="clickMenu('/VisualDetection/ColorPerception')">颜色感知</el-menu-item>
                            <el-menu-item index="3-2"
                                @click="clickMenu('/VisualDetection/VisualAcuityTesting')">视力检测</el-menu-item>
                            <el-menu-item index="3-3"
                                @click="clickMenu('/VisualDetection/SensitivityTesting')">敏感度检测</el-menu-item>
                        </el-menu-item-group>
                    </el-sub-menu>

                    <el-sub-menu index="4">
                        <template #title>
                            <el-icon>
                                <View />
                            </el-icon>
                            <span class="Aside-text">眼健康检测</span>
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="4-1" @click="clickMenu('/EyeHealth/GlaucomaTest')">青光眼检测</el-menu-item>
                            <el-menu-item index="4-2"
                                @click="clickMenu('/EyeHealth/CataractDetection')">白内障检测</el-menu-item>
                            <el-menu-item index="4-3" @click="clickMenu('/EyeHealth/MacularTest')">黄斑病检测</el-menu-item>
                        </el-menu-item-group>
                    </el-sub-menu>

                    <el-menu-item index="5" @click="clickMenu('/VisualAnalysis')">
                        <el-icon>
                            <DataAnalysis />
                        </el-icon>
                        <template #title>
                            <span class="Aside-text">视功能分析</span>
                        </template>
                    </el-menu-item>

                    <el-menu-item index="6" @click="clickMenu('/ChartData')">
                        <el-icon>
                            <DataLine />
                        </el-icon>
                        <template #title>
                            <span class="Aside-text">图表数据</span>
                        </template>
                    </el-menu-item>

                    <el-menu-item index="7" @click="clickMenu('/TreatmentRecommended')">
                        <el-icon>
                            <MagicStick />
                        </el-icon>
                        <template #title>
                            <span class="Aside-text">治疗建议</span>
                        </template>
                    </el-menu-item>

                    <el-menu-item index="8" @click="clickMenu('/HistoricalAssessments')">
                        <el-icon>
                            <Calendar />
                        </el-icon>
                        <template #title>
                            <span class="Aside-text">历史评测</span>
                        </template>
                    </el-menu-item>

                    <el-menu-item index="9" @click="clickMenu('/SettingView')">
                        <el-icon>
                            <Setting />
                        </el-icon>
                        <template #title>
                            <span class="Aside-text">设置</span>
                        </template>
                    </el-menu-item>
                </el-main>
            </el-scrollbar>

        </el-container>

    </el-menu>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { useCounterStore } from '../stores/counter.js'

const store = useCounterStore()

const handleOpen = (key, keyPath) => {
    console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
    console.log(key, keyPath)
}

const router = useRouter()
const clickMenu = (path) => {
    router.push(path)
}


</script>


<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 250px;
    min-height: 100vh;
    background-color: #ffffff;
}

.el-menu-item {
    background-color: #ffffff;
    color: #9799a8;
    font-size: 14px;
    font-weight: 600;
}

.el-menu-item-group__title {
    padding: 0px;
}

.el-menu-item:hover {
    background-color: #e1e1e1;
}

.el-sub-menu__title:hover {
    background-color: #e1e1e1;
}

.el-menu-vertical-demo {
    .el-icon svg {
        color: #9799a8;
    }
}

span {
    font-size: 16px;
    font-weight: bold;
}

.title-name {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 70px;
}

text {
    font-size: 20px;
    font-weight: bolder;
    color: #6762ff;
}

.logo-con {
    background-color: #6762ff;
    width: 40px;
    height: 40px;
    margin-right: 10px;
    margin-left: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo-img {
    height: 32px;
    width: 32px;
}

.menu-item-content {
    width: 250px;
    background-color: bisque;
}

.el-header {
    padding: 0px;
}

.el-main {
    padding: 0px;
}

.el-menu {
    border-right: none;
}


.collapsed {
    width: 65px;
    height: 100vh;
    overflow: hidden;

    .Aside-text {
        display: none;
    }

    .el-sub-menu__icon-arrow {
        display: none;
    }

    text {
        display: none;
    }

    .logo-con {
        background-color: #6762ff;
        width: 40px;
        height: 40px;
        margin-right: 0px;
        margin-left: 13px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
}
</style>