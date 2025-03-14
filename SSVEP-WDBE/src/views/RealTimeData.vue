<template>
    <div>

        <el-dialog v-model="dialogVisible" title="现在去检测" width="40%" :before-close="handleClose" top="5vh">
            <div class="nav">
                <el-card class="nav_item" shadow="hover" v-for="item in countDate" :key="item.name"
                    @click="clickMenu(item.path)">
                    <img :src="item.icon" class="logo">
                    <p class="text">{{ item.name }}</p>
                </el-card>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="dialogVisible = false">
                        下次一定
                    </el-button>
                </div>
            </template>
        </el-dialog>

        <div class="button_area">
            <el-button type="primary" plain @click="dialogVisible = true"> 检测 </el-button>
            <div class="search">
                <el-input v-model="input" style="width: 200px" placeholder="请输入关键词" clearable />
                <el-button type="primary" plain>搜索</el-button>
            </div>
        </div>

        <div class="table_area">
            <el-table :data="tableData" height="450" style="width: 100%" stripe>
                <el-table-column prop="id" label="序号" width="120" align="center" />
                <el-table-column prop="name" label="项目名称" width="220" align="center" />
                <el-table-column prop="date" label="检测时间" align="center">
                    <template #default="scope">
                        <div style="display: flex; align-items: center; justify-content: center">
                            <el-icon>
                                <timer />
                            </el-icon>
                            <span style="margin-left: 10px">{{ scope.row.date }}</span>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="count" label="通道数" width="220" align="center" />
                <el-table-column prop="score" label="评估分数" width="120" align="center" />
                <el-table-column fixed="right" label="操作" width="250" align="center">
                    <template #default>
                        <el-popconfirm title="你确认要删除这条数据吗?" confirm-button-text="是的" cancel-button-text="算了"
                            :icon="InfoFilled" icon-color="#626AEF">
                            <template #reference>
                                <el-button link type="danger" size="small" @click="handleDelete(scope.rowIndex)">
                                    删除
                                </el-button>
                            </template>
                        </el-popconfirm>
                        <el-button link type="primary" size="small" @click="download">下载</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <div class="demo-pagination-block">
                <el-pagination v-model:current-page="currentPage3" v-model:page-size="pageSize3" :background=false
                    layout="prev, pager, next, jumper" :total="1000" @size-change="handleSizeChange"
                    @current-change="handleCurrentChange" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import tableDataJson from '@/assets/data/localdata_table.json'
const input = ref('')

const dialogVisible = ref(false)

const tableData = ref(tableDataJson)

const download = () => {
    window.location.href = '../../数据文件.csv'
}

const countDate = [
    {
        name: "颜色感知检测",
        icon: "../../public/image/icon/main/1.png",
        path:"/VisualDetection/ColorPerception",
    },
    {
        name: "视力检测",
        icon: "../../public/image/icon/main/2.png",
        path:"/VisualDetection/VisualAcuityTesting",
    },
    {
        name: "敏感度检测",
        icon: "../../public/image/icon/main/3.png",
        path:"/VisualDetection/SensitivityTesting",
    },
    {
        name: "青光眼检测",
        icon: "../../public/image/icon/main/4.png",
        path:"/EyeHealth/GlaucomaTest",
    },
    {
        name: "白内障检测",
        icon: "../../public/image/icon/main/5.png",
        path:"/EyeHealth/CataractDetection",
    },
    {
        name: "黄斑病检测",
        icon: "../../public/image/icon/main/6.png",
        path:"/EyeHealth/MacularTest",
    },
]

const router = useRouter()
const clickMenu = (path) => {
    router.push(path)
}

</script>

<style lang="less" scoped>
.button_area {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 20px;

    .el-input {
        margin-right: 10px;
    }
}

.demo-pagination-block {
    display: flex;
    flex-direction: column;
    align-items: end;
    margin-top: 20px;
    margin-right: 20px;
}

.el-pagination {
    --el-pagination-bg-color: #fafafa;
}


.nav {
    width: 100%;
    height: 450px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;

    .nav_item {
        width: 25%;
        height: 200px;
        margin: 7px;
        background-color: #fafafa;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;

        .logo {
            width: 90px;
            height: 90px;
            margin-bottom: 20px;
        }

        .text {
            font-size: 16px;
            font-weight: bold;
            color: #3f3f3f;
        }
    }
}

</style>