<template>
    <el-dialog v-model="dialogVisible" title="上传新的头像" width="500">
        <el-upload class="avatar-uploader" action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
            :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon">
                <Plus />
            </el-icon>
        </el-upload>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="dialogVisible = false">
                    保存
                </el-button>
            </div>
        </template>
    </el-dialog>
    <el-row :gutter="20">
        <el-col :span="16">
            <el-card style="max-width: 100%;" shadow="hover">
                <el-form :model="ProfileForm" label-width="auto" style="max-width: 90%" label-position="top">

                    <el-form-item label="用户名">
                        <el-input v-model="oldname" clearable />
                    </el-form-item>

                    <el-form-item label="居住地址">
                        <el-input v-model="ProfileForm.address" type="textarea" placeholder="请填写您的居住地址" clearable />
                    </el-form-item>

                    <el-form-item label="生日">
                        <el-date-picker v-model="ProfileForm.date" type="date" placeholder="选择你的生日"
                            style="width: 100%" />
                    </el-form-item>

                    <el-form-item label="性 别">
                        <el-radio-group v-model="ProfileForm.sex">
                            <el-radio value="男">男</el-radio>
                            <el-radio value="女">女</el-radio>
                        </el-radio-group>
                    </el-form-item>

                    <el-form-item label="个人介绍">
                        <el-input v-model="ProfileForm.intro" type="textarea" placeholder="请简单介绍一下你自己" clearable />
                    </el-form-item>

                    <el-form-item label="是否允许任何人可见">
                        <el-switch v-model="ProfileForm.delivery" />
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">保存</el-button>
                        <el-button>取消</el-button>
                    </el-form-item>

                </el-form>
            </el-card>

        </el-col>


        <el-col :span="8" class="r_content">
            <span>个人资料图片</span>
            <img src="../../public/image/profile.png" class="Settingavatar" @click="dialogVisible = true">
            <div class="tips">
                点击可以更改头像
            </div>
        </el-col>
    </el-row>
</template>

<script setup>
import { reactive } from 'vue'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const oldname = ref('CHIYO')

const dialogVisible = ref(false)

const ProfileForm = reactive({
    name: oldname,
    address: '',
    date: '',
    delivery: false,
    sex: '',
    intro: '',
})

const onSubmit = () => {
    ElMessage({
    message: '恭喜你，成功保存啦！',
    type: 'success',
  })
}

</script>


<style lang="less" scoped>
.r_content {
    display: flex;
    flex-direction: column;

    .Settingavatar {
        height: 200px;
        width: 200px;
        border-radius: 50%;
        margin-top: 20px;
    }

    .tips {
        margin-left: 50px;
        margin-top: 10px;
        font-size: 12px;
        color: #7a7979;
    }
}


.avatar-uploader,.el-upload {
    border: 2px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
    display: flex;
    justify-content: center;
}

.avatar-uploader:hover {
    border-color: var(--el-color-primary);
}
.el-upload:hover {
    border-color: var(--el-color-primary);
}
.el-icon.avatar-uploader-icon {
    font-size: 48px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}

.el-card{
    height: 590px;
}
</style>