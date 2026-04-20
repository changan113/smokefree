<template>
  <div style="padding:16px; max-width:900px; margin:0 auto;">
    <h2>风险报告与可视化</h2>
    <ReportCard :report="report" />
    <div style="display:flex; gap:16px; flex-wrap:wrap; margin-top:12px;">
      <div ref="gauge" style="width:300px;height:240px;border:1px solid #eee;"></div>
      <div ref="radar" style="width:480px;height:300px;border:1px solid #eee;"></div>
    </div>
    <div style="margin-top:16px;">
      <h3>留言墙</h3>
      <CommentBoard />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import ReportCard from '../components/ReportCard.vue'
import CommentBoard from '../components/CommentBoard.vue'

const report = ref(null)
onMounted(()=>{
  const stored = localStorage.getItem('latest_report')
  if(stored){
    report.value = JSON.parse(stored)
    renderCharts(report.value)
  }
})

function renderCharts(data){
  const gaugeDom = document.querySelector('[ref="gauge"]') || document.querySelector('div[ref="gauge"]')
  const radarDom = document.querySelector('[ref="radar"]') || document.querySelector('div[ref="radar"]')
  // compatibility: refs from template via ref() would be better; fallback to querySelector
  const gaugeEl = document.querySelector('#gauge') || document.querySelector('div[ref="gauge"]')
  const g = echarts.init(document.querySelector('[ref="gauge"]') || document.querySelector('div[ref="gauge"]'))
  const r = echarts.init(document.querySelector('[ref="radar"]') || document.querySelector('div[ref="radar"]'))
  const overall = data.overall_score || 0
  g.setOption({
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      detail: { formatter: '{value}' },
      data: [{ value: overall, name: data.overall_level || '未知' }]
    }]
  })
  const scene = data.scene_scores || {family:0,work:0,social:0}
  r.setOption({
    radar: {
      indicator: [
        { name: '家庭', max: 100},
        { name: '工作', max: 100},
        { name: '社交', max: 100}
      ]
    },
    series: [{
      type: 'radar',
      data: [{ value: [scene.family, scene.work, scene.social], name: '场景风险' }]
    }]
  })
}
</script>
