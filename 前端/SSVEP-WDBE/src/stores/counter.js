import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }
  
  //控制侧边栏是否折叠
  const isCollapse=ref(false)


  //控制漫游组件是否开始漫游
  const open = ref(false)
  const tour_end=ref(false)

  return { isCollapse,count, doubleCount, increment, open , tour_end }
})
