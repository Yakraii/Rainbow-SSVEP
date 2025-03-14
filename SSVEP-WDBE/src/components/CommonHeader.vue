<template>
    <div class="header-container">
        <div class="l-content">
            <el-button type="primary" size="mini" @click="toggleCollapse">
                <el-icon class="el-icon--Menu">
                    <Menu />
                </el-icon>
            </el-button>
            <!-- <span class="head-text">首页</span> -->
        </div>
        <div class="r-content">
            <el-dropdown>
                <span class="el-dropdown-link" style="outline: none">
                    <img class="user-avatar" src="../../public/image/profile.png" alt="头像" />
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item>个人中心</el-dropdown-item>
                        <el-dropdown-item>退出</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup>
import { useCounterStore } from '../stores/counter.js'

const store = useCounterStore()
function toggleCollapse() {
    store.isCollapse = !store.isCollapse
}

</script>

<style lang="less" scoped>
.header-container {
    height: 60px;
    background-color: #fafafa;
    padding: 0px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.el-button {
    margin-left: 20px;
    background-color: white;
    margin-right: 15px;
    border: 1px solid #cacbd3;
}

.el-button:hover {
    background-color: #ededee;

    .el-icon svg {
        color: #5f55ec;
    }
}

.el-icon svg {
    color: #6C63FF;
}

.example-showcase .el-dropdown-link {
    cursor: pointer;
    color: var(--el-color-primary);
    display: flex;
    align-items: center;
}

.el-dropdown {
    margin-right: 20px;
}

.user-avatar {
    height: 40px;
    width: 40px;
    border-radius: 50%;
}

.head-text{
    color: #252734;
}
</style>