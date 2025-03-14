<template>
    <div class="Detect">
      <h1>青光眼检测</h1>
  
      <el-dialog v-model="store.tour_end" title="检测" width="80%" top="5vh">
        <div class="vedio">
          <video src="../../public/image/stimulus.mp4" controls
              preload="auto" width="100%" height="100%"></video>
        </div>
        <template #footer>
          <div class="dialog-footer">
            <el-button type="primary" @click="store.tour_end = false">
              结束检测
            </el-button>
          </div>
        </template>
      </el-dialog>
  
      <div class="tour">
        <DetectTour />
      </div>
      <div class="button_area">
        <el-button type="primary" plain @click="DetectStart">开始检测</el-button>
      </div>
  
    </div>
  </template>
  
  <script setup lang="ts">
  import DetectTour from '../components/DetectTour.vue'
  import { useCounterStore } from '../stores/counter.js'
  
  const store = useCounterStore()
  
  const DetectStart = () => {
    store.open = true
  }
  
  </script>
  
  
  <style lang="less" scoped>
  .Detect {
    h1 {
      font-size: 32px;
      font-weight: bold;
      color: rgb(53, 53, 53);
    }
  
    .tour {
      width: 100%;
      height: 450px;
    }
  
    .button_area {
      display: flex;
      justify-content: end;
  
      .el-button {
        margin-right: 20px;
        margin-top: 0px;
        width: 200px;
        height: 50px;
      }
    }
  
    .vedio{
      width: 90%;
      height: 500px;
    }
  
  }
  </style>