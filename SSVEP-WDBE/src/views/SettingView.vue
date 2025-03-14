<template>
    <el-tabs v-model="activeName" class="demo-tabs">
        <el-tab-pane label="个人档案" name="first">
                <PublicProfile />
        </el-tab-pane>
        <el-tab-pane label="邮箱" name="second">
                <EmailSetting />
        </el-tab-pane>
        <el-tab-pane label="辅助功能" name="third">
                <AccessibilitySetting />
        </el-tab-pane>
    </el-tabs>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import PublicProfile from '../components/PublicProfile.vue'
import EmailSetting from '../components/EmailSetting.vue'
import AccessibilitySetting from '../components/AccessibilitySetting.vue'

const activeName = ref('first')

</script>

<style>
.el-tabs {
    margin-left: 10px;
}

</style>