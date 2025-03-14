<script setup>
import CommonAside from '../components/CommonAside.vue'
import CommonHeader from '../components/CommonHeader.vue'
</script>

<template>

  <div class="common-layout">
    <el-container>
      <el-aside width="auto" background-color="#6C63FF">
        <CommonAside />
      </el-aside>
      <el-container>
        <el-header>
          <CommonHeader />
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>

</template>


<style lang="less" scoped>
.el-header {
  padding: 0px;
}

.el-aside {
  padding: 0px;
}

.el-container.is-vertical {
  margin: 0px;
}
</style>
