import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ChartData from '@/views/ChartData.vue'
import DataBase from '@/views/DataBase.vue'
import EyeHealth from '@/views/EyeHealth.vue'
import HistoricalAssessments from '@/views/HistoricalAssessments.vue'
import SettingView from '@/views/SettingView.vue'
import TreatmentRecommended from '@/views/TreatmentRecommended.vue'
import VisualAnalysis from '@/views/VisualAnalysis.vue'
import VisualDetection from '@/views/VisualDetection.vue'
import RealTimeData from '@/views/RealTimeData.vue'
import LocalData from '@/views/LocalData.vue'
import ColorPerception from '@/views/ColorPerception.vue'
import VisualAcuityTesting from '@/views/VisualAcuityTesting.vue'
import SensitivityTesting from '@/views/SensitivityTesting.vue'
import GlaucomaTest from '@/views/GlaucomaTest.vue'
import CataractDetection from '@/views/CataractDetection.vue'
import MacularTest from '@/views/MacularTest.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/HomeView' // 将根路径重定向到默认的路由路径
    },
    {
      path: '/HomeView',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/ChartData',
      name: 'ChartData',
      component: ChartData,
    },
    {
      path: '/DataBase',
      name: 'DataBase',
      component: DataBase,
      children: [
        {
          path: 'RealTimeData',
          name: 'RealTimeData',
          component: RealTimeData
        },
        {
          path: 'LocalData',
          name: 'LocalData',
          component: LocalData
        },
      ]
    },
    {
      path: '/EyeHealth',
      name: 'EyeHealth',
      component: EyeHealth,
      children: [
        {
          path: 'GlaucomaTest',
          name: 'GlaucomaTest',
          component: GlaucomaTest,
        },
        {
          path: 'CataractDetection',
          name: 'CataractDetection',
          component: CataractDetection,
        },
        {
          path: 'MacularTest',
          name: 'MacularTest',
          component: MacularTest,
        },
      ]
    },
    {
      path: '/HistoricalAssessments',
      name: 'HistoricalAssessments',
      component: HistoricalAssessments
    },
    {
      path: '/SettingView',
      name: 'SettingView',
      component: SettingView
    },
    {
      path: '/TreatmentRecommended',
      name: 'TreatmentRecommended',
      component: TreatmentRecommended
    },
    {
      path: '/VisualAnalysis',
      name: 'VisualAnalysis',
      component: VisualAnalysis
    },
    {
      path: '/VisualDetection',
      name: 'VisualDetection',
      component: VisualDetection,
      children: [
        {
          path: 'ColorPerception',
          name: 'ColorPerception',
          component: ColorPerception,
        },
        {
          path: 'VisualAcuityTesting',
          name: 'VisualAcuityTesting',
          component: VisualAcuityTesting,
        },
        {
          path: 'SensitivityTesting',
          name: 'SensitivityTesting',
          component: SensitivityTesting,
        },
      ]
    },
  ]
})

export default router
