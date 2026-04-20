<template>
  <div style="margin-top:12px;padding:12px;border-radius:8px;background:#fff;border:1px solid #eee;">
    <h3>AI 评估报告（系统）</h3>
    <pre style="white-space:pre-wrap">{{ reportText }}</pre>
  </div>
</template>

<script setup>
import { computed, toRefs } from 'vue'
const props = defineProps({ report: Object })
const reportText = computed(()=> props.report?.ai_report ?? '暂无报告，请先提交问卷')
</script>

<style scoped>
pre { font-family: inherit; line-height:1.5; }
</style>
