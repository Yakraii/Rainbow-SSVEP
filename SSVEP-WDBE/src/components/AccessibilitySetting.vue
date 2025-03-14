<template>
    <el-scrollbar height="590px">
        <div class="access">
            <p class="item_t1">键盘快捷键</p>
            <p class="item_t2">常规</p>
            <el-checkbox v-model="checked">
                <p class="item_t3">字符键</p>
            </el-checkbox>
            <p class="item_t4" style="margin-left: 22px;">
                启用在激活时不使用修饰键的快捷方式。例如，用于导航通知的快捷方式，了解有关字符键快捷方式的详细信息请移步帮助文档。
            </p>
            <br>
            <p class="item_t2">命令面板</p>
            <p class="item_t4">
                修改快捷方式以触发默认搜索模式和命令模式的命令面板。
            </p>

            <el-form :model="form" label-width="auto" style="max-width: 700px; margin-top: 30px;" inline
                label-position="top">
                <el-form-item label="搜索模式">
                    <el-select v-model="value1" placeholder="Select" style="width: 340px;">
                        <el-option v-for="item in options1" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="命令模式">
                    <el-select v-model="value2" placeholder="Select" style="width: 240px">
                        <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>

                <el-button type="info">存储键盘快捷键首选项</el-button>
            </el-form>
        </div>

        <div class="access">
            <p class="item_t1">动画</p>
            <p class="item_t2">自动播放动画图像</p>
            <p class="item_t4">
                选择动画图像是否应自动播放。
            </p>
            <br>
            <div class="motion_section">
                <el-radio-group v-model="radio1" class="ml-4">
                    <el-radio value="1">
                        <p class="item_t3">与系统同步</p>
                    </el-radio>
                    <p class="item_t4" style="margin-left: 25px;">
                        采用您的系统偏好以减少操作
                    </p>
                    <el-radio value="2">
                        <p class="item_t3">启用</p>
                    </el-radio>
                    <p class="item_t4" style="margin-left: 25px;">
                        自动播放动画图像
                    </p>
                    <el-radio value="3">
                        <p class="item_t3">禁用</p>
                    </el-radio>
                    <p class="item_t4" style="margin-left: 25px;">
                        阻止动画图像自动播放
                    </p>
                </el-radio-group>
                <el-button type="info" style="width: 200px;">存储动画偏好设置</el-button>
            </div>

        </div>

        <div class="access">
            <p class="item_t1">内容</p>
            <p class="item_t2">链接下划线</p>
            <p class="item_t4">
                在与文本相邻的链接上切换下划线的可见性。
            </p>
            <br>
            <div class="motion_section">
                <el-radio-group v-model="radio2" class="ml-4">
                    <el-radio value="1">
                        <p class="item_t3">隐藏链接下划线</p>
                    </el-radio>
                    <el-radio value="2">
                        <p class="item_t3">显示链接下划线</p>
                    </el-radio>
                </el-radio-group>
                <el-button type="info" style="width: 100px;">保存</el-button>
            </div>
        </div>

        <div class="access" style="margin-bottom: 250px;">
            <p class="item_t1">编辑器设置</p>
            <p class="item_t2">URL 粘贴行为</p>
            <p class="item_t4">
                选择是否应在粘贴时设置 URL 格式。您可以使用控制换档和 VCtrl ⇧ V 以相反的方式粘贴链接。
            </p>
            <br>
            <div class="motion_section">
                <el-radio-group v-model="radio3" class="ml-4">
                    <el-radio value="1">
                        <p class="item_t3">格式化链接</p>
                    </el-radio>
                    <p class="item_t4" style="margin-left: 25px;">
                        在选择文本的同时粘贴 URL 会将格式化为 Markdown 链接
                    </p>
                    <el-radio value="2">
                        <p class="item_t3">纯文本</p>
                    </el-radio>
                    <p class="item_t4" style="margin-left: 25px;">
                        在选择文本的同时粘贴 URL 将替换文本
                    </p>
                </el-radio-group>
                <el-button type="info" style="width: 200px;">保存编辑器设置</el-button>
            </div>
        </div>
    </el-scrollbar>
</template>

<script setup>
import { ref } from 'vue'

const checked = ref('1')
const value1 = ref('Control + K 或 Control + Alt + K (默认)')
const value2 = ref('Control + Shift + K (默认)')
const radio1 = ref('1')
const radio2 = ref('1')
const radio3 = ref('1')

const options1 = [
    {
        value: 'Control + K 或 Control + Alt + K (默认)',
        label: 'Control + K 或 Control + Alt + K (默认)',
    },
    {
        value: '控制 + K',
        label: '控制 + K ',
    },
    {
        value: '控制 + Alt + K',
        label: '控制 + Alt + K ',
    },
    {
        value: '控制 + Shift + K',
        label: '控制 + Shift + K',
    },
    {
        value: '禁用',
        label: '禁用',
    },
]

const options2 = [
    {
        value: 'Control + Shift + K (默认)',
        label: 'Control + Shift + K (默认)',
    },
    {
        value: '控制 + K',
        label: '控制 + K',
    },
    {
        value: '控制 + Alt + K',
        label: '控制 + Alt + K',
    },
    {
        value: '控制 + p',
        label: '控制 + p',
    },
    {
        value: '禁用',
        label: '禁用',
    },
]

</script>

<style lang="less" scoped>
.access {
    width: 98%;
    margin-left: 16px;
    display: flex;
    flex-direction: column;
    padding: 20px;
    margin-bottom: 0px;
    .item_t1 {
        font-size: 22px;
        margin-bottom: 8px;
        font-weight: 300;
    }

    .item_t2 {
        font-size: 18px;
        margin-bottom: 8px;
        font-weight: 100;
    }

    .item_t3 {
        font-size: 14px;
        font-weight: bold;
        color: #343434;
    }

    .item_t4 {
        font-size: 11px;
        margin-bottom: 8px;
        color: #949494;
    }

    .select_area {
        display: flex;
        flex-direction: row;
    }

    .motion_section {
        display: flex;
        flex-direction: column;
        
        .el-radio-group {
            display: flex;
            flex-direction: column;
            align-items: start;
        }
    }

    .el-button{
        margin-top: 20px;
    }
}
</style>