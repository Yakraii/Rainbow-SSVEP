<template>
    <div>

        <el-dialog v-model="dialogVisible" title="导入本地数据" width="50%" :before-close="handleClose" top="5vh">
            <div class="form_area">
                <el-form :model="form" label-width="auto" style="max-width: 90%" :rules="rules">
                    <el-form-item label="检测项目名称" prop="name">
                        <el-select v-model="form.name" placeholder="请选择所检测项目的名称">
                            <el-option label="颜色感知检测" value="颜色感知检测" />
                            <el-option label="视力检测" value="视力检测" />
                            <el-option label="视觉灵敏度检测" value="视觉灵敏度检测" />
                            <el-option label="青光眼检测" value="青光眼检测" />
                            <el-option label="白内障检测" value="白内障检测" />
                            <el-option label="黄斑病检测" value="黄斑病检测" />
                        </el-select>
                    </el-form-item>

                    <el-form-item label="检测的日期" prop="date">
                        <el-date-picker v-model="form.date" type="datetime" placeholder="请选择数据提取的日期和时间"
                            style="width: 100%" />
                    </el-form-item>

                    <el-form-item label="数据文件">
                        <el-upload class="upload-demo" drag
                            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" multiple
                            style="width: 100%">
                            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                            <div class="el-upload__text">
                                Drop file here or <em>click to upload</em>
                            </div>
                        </el-upload>
                    </el-form-item>

                    <el-form-item label="通道数" prop="count">
                        <el-radio-group v-model="form.count">
                            <el-radio value="8CH">8 CH</el-radio>
                            <el-radio value="16CH">16 CH</el-radio>
                            <el-radio value="32CH">32 CH</el-radio>
                            <el-radio value="64CH">64 CH</el-radio>
                        </el-radio-group>
                    </el-form-item>

                    <el-form-item label="数据处理方法" prop="type">
                        <el-checkbox-group v-model="form.type">
                            <el-checkbox value="基线校正" name="type">
                                基线校正
                            </el-checkbox>
                            <el-checkbox value="重参考" name="type">
                                重参考
                            </el-checkbox>
                            <el-checkbox value="降采样" name="type">
                                降采样
                            </el-checkbox>
                            <el-checkbox value="差值坏导" name="type">
                                差值坏导
                            </el-checkbox>
                            <el-checkbox value="带通滤波" name="type">
                                带通滤波
                            </el-checkbox>
                            <el-checkbox value="低频漂移" name="type">
                                低频漂移
                            </el-checkbox>
                            <el-checkbox value="高频噪声" name="type">
                                高频噪声
                            </el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>

                    <el-form-item label="评估的分数">
                        <el-input-number v-model="num" :min="0" :max="100" />
                    </el-form-item>

                </el-form>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="dialogVisible = false">
                        确定
                    </el-button>
                </div>
            </template>
        </el-dialog>

        <div class="button_area">
            <el-button type="primary" plain @click="dialogVisible = true"> + 导入 </el-button>
            <div class="search">
                <el-input v-model="input" style="width: 200px" placeholder="请输入关键词" clearable />
                <el-button type="primary" plain>搜索</el-button>
            </div>
        </div>

        <div class="table_area">
            <el-table :data="tableData" height="450" style="width: 100%" stripe>
                <el-table-column prop="id" label="序号" width="70" align="center"/>
                <el-table-column prop="name" label="项目名称" width="120" align="center" />
                <el-table-column prop="date" label="检测时间" width="320" align="center">
                    <template #default="scope">
                        <div style="display: flex; align-items: center; justify-content: center">
                            <el-icon>
                                <timer />
                            </el-icon>
                            <span style="margin-left: 10px">{{ scope.row.date }}</span>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="count" label="通道数" width="120" align="center" />
                <el-table-column prop="methods" label="数据处理方法" align="center" />
                <el-table-column prop="score" label="评估分数" width="80" align="center" />
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
                        <el-button link type="primary" size="small" @click="handleEdit(scope.row)">修改</el-button>
                        <el-button link type="info" size="small" @click="download">下载</el-button>
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
import { reactive } from 'vue'
import tableDataJson from '@/assets/data/localdata_table.json'
const input = ref('')

const dialogVisible = ref(false)
const num = ref(0)
const tableData = ref(tableDataJson)

const download = () => {
    window.location.href = '../../数据文件.csv'
}

const form = reactive({
    name: '',
    date: '',
    count: '',
    type: [],
    score: num,
})

const rules = reactive({
    name: [
        { required: true, message: '请选择检测项目的名称', trigger: 'blur' },
    ],
    date: [
        {
            type: 'date',
            required: true,
            message: '请选择检测的日期和时间',
            trigger: 'change',
        },
    ],
    count: [
        { required: true, message: '请选择检测的通道数', trigger: 'blur' }
    ],
    type: [
        {
            type: 'array',
            required: true,
            message: '请选择至少一个选项',
            trigger: 'change',
        },
    ],
})

const handleDelete = (index) => {
  tableData.value.splice(index, 1);
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
</style>