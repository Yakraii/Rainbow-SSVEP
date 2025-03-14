<template>
    <el-scrollbar height="590px">
        <div class="email_intro">
            <el-card style="width: 98%" shadow="hover">
                <p class="p1">主要电子邮件将用于与帐户相关的通知，也可用于密码重置。</p>
                <ul>
                    <li>
                        <div class="li_t">
                            <p class="p2">在电子邮件中不可见</p>
                            <p class="p3">此电子邮件不会用作问题反馈、社区交流的“发件人”地址。我们将改用 “133511913+CHIYO@users.noreply.SSVEP.com”</p>
                        </div>
                    </li>

                    <li>
                        <div class="li_t">
                            <p class="p2">接收通知</p>
                            <p class="p3">此电子邮件地址是收取我们服务通知的默认地址，即对问题的回复、健康报表等。</p>
                        </div>
                    </li>
                </ul>
            </el-card>
        </div>

        <div class="email_item">
            <p class="item_t1">添加电子邮箱地址</p>
            <div class="mt-4">
                <el-input v-model="input3" style="max-width: 400px" placeholder="电子邮箱地址" class="input-with-select">
                    <template #prepend>
                        <el-icon>
                            <Message />
                        </el-icon>
                    </template>
                    <template #append>
                        <el-select v-model="select" placeholder="选择邮箱类型" style="width: 160px">
                            <el-option label="@qq.com" value="1" />
                            <el-option label="@163.com" value="2" />
                            <el-option label="@gmail.com" value="3" />
                            <el-option label="@yahoo.com" value="4" />
                        </el-select>
                    </template>
                </el-input>
            </div>
            <el-divider />
        </div>

        <div class="email_item">
            <p class="item_t1">主要电子邮箱地址</p>
            <span class="item_t2">
                由于您启用了电子邮件隐私，因此将用于与帐户相关的通知以及密码重置。
                将用于问题反馈、社区交流等操作。<br>
                3321571675@qq.com133511913+CHIYO@users.noreply.SSVEP.com
            </span>
            <div class="input_area">
                <el-input v-model="input" style="width: 240px" value="3321571675@qq.com" />
                <el-button type="primary" plain>更改</el-button>
            </div>
            <el-divider />
        </div>

        <div class="email_item">
            <p class="item_t1">备用电子邮箱地址</p>
            <span class="item_t2">
                您的备份 GitHub 电子邮件地址将用作安全相关帐户通知的附加目标，也可用于密码重置。
            </span>
            <div class="input_area">
                <el-input v-model="input" style="width: 240px" value="3221371472@162.com" />
                <el-button type="primary" plain>更改</el-button>
            </div>
            <p class="item_t3">
                除了您的主要电子邮件外，请添加经过验证的电子邮件，以便选择备用电子邮件地址。
            </p>
            <el-divider />
        </div>

        <div class="email_item">
            <el-radio-group v-model="radio" class="ml-4">
                <el-radio value="1">
                    <p class="item_t1">将我的电子邮件地址保密</p>
                </el-radio>
                <p class="item_t3" style="margin-left: 25px;">
                    我们将删除您的公开个人资料电子邮件，并在执行问题反馈、社区交流时使用 133511913+CHIYO1@users.noreply.SSVEP.com，
                    代表您发送电子邮件。
                    <br>
                    如果希望使用您的私人电子邮件，则必须设置您的电子邮箱公开。此时，邮件与公共电子邮件关联的先前的寄件将保持公开状态。
                </p>
                <el-radio value="2">
                    <p class="item_t1">阻止暴露我的电子邮件的推送</p>
                </el-radio>
                <p class="item_t3" style="margin-left: 25px;">
                    当你寄出邮件时，我们将检查邮箱的地址。<br>
                    如果该寄件的作者电子邮件是你的帐户上的私人电子邮件，我们将阻止发送并警告你不要公开你的私人电子邮件。
                </p>
            </el-radio-group>
        </div>

        <div class="email_item" style="margin-top: 20px;">
            <p class="p1">
                电子邮件首选项
            </p>
            <p class="item_t1" style="color: #818181; font-weight: 100;">
                通过我们的各种营销平台进行订阅。每个电子邮件地址都有自己的订阅。
            </p>
            <el-divider />
            <div class="input_area" style="margin-bottom: 250px;">
                <el-input v-model="input" style="height: 40px;" value="3321571675@qq.com" />
            </div>
        </div>
    </el-scrollbar>

</template>

<script setup>
import { ref } from 'vue'
const select = ref('')
const input = ref('')
const radio = ref('1')
</script>

<style lang="less" scoped>
.email_intro {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
    .el-card {
        margin-left: 5px;
        margin-top: 5px;

        ul li::marker {
            color: #525252;
        }

        li {
            margin-top: 10px;
        }

        .p1 {
            font-size: 22px;
            font-weight: bold;
            color: #343434;
        }

        .p2 {
            font-size: 16px;
            color: #525252;
        }

        .p3 {
            font-size: 12px;
            color: #525252;
        }
    }
}

.el-divider--horizontal {
    margin-top: 20px;
    margin-bottom: 20px;
}

.email_item {
    width: 98%;
    margin-left: 16px;
    display: flex;
    flex-direction: column;
    padding: 20px;
    padding-bottom: 0px;
    padding-top: 0px;

    .item_t1 {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .item_t2 {
        font-size: 13px;
        margin-bottom: 10px;
        color: #818181;
    }

    .item_t3 {
        font-size: 11px;
        margin-bottom: 10px;
        color: #aeaeae;
    }

    .p1 {
        font-size: 22px;
        font-weight: bold;
        color: #343434;
    }

    .input_area {
        display: flex;
        flex-direction: row;

        .el-button {
            margin-left: 10px;
        }
    }

    .el-radio-group {
        display: flex;
        flex-direction: column;
        align-items: start;

        .item_t1 {
            margin-bottom: 0px;
        }
    }


}
</style>