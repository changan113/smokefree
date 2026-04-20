<template>
  <div style="padding:16px; max-width:720px; margin:0 auto;">
    <h2>二手烟风险问卷</h2>
    <van-field v-model="age" type="number" label="年龄" placeholder="例如：30" />
    <van-field v-model="exposure_years" type="number" label="暴露年限（年）" placeholder="例如：5" />
    <van-field v-model="hours_per_day" type="number" label="每日暴露时长（小时）" placeholder="例如：2" />
    <van-radio-group v-model="main_environment" style="margin-top:8px;">
      <van-radio name="family">家庭</van-radio>
      <van-radio name="work">工作</van-radio>
      <van-radio name="social">社交</van-radio>
    </van-radio-group>

    <van-cell-group>
      <van-cell title="环境是否密闭">
        <template #right-icon>
          <van-switch v-model:checked="environment_enclosed" />
        </template>
      </van-cell>
      <van-cell title="是否与吸烟者同住">
        <template #right-icon>
          <van-switch v-model:checked="living_with_smoker" />
        </template>
      </van-cell>
    </van-cell-group>

    <van-textarea v-model="extra_notes" rows="3" placeholder="其他说明（选填）" />

    <div style="margin-top:16px;">
      <van-button type="primary" block @click="onSubmit" :loading="loading">提交并生成报告</van-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { postReport } from '../utils/api'
import { useRouter } from 'vue-router'

const age = ref(30)
const exposure_years = ref(5)
const hours_per_day = ref(2)
const main_environment = ref('family')
const environment_enclosed = ref(true)
const living_with_smoker = ref(false)
const extra_notes = ref('')
const loading = ref(false)
const router = useRouter()

function showToast(msg){
  // lightweight fallback
  alert(msg)
}

async function onSubmit(){
  loading.value = true
  try{
    const payload = {
      age: Number(age.value),
      exposure_years: Number(exposure_years.value),
      hours_per_day: Number(hours_per_day.value),
      main_environment: main_environment.value,
      environment_enclosed: Boolean(environment_enclosed.value),
      living_with_smoker: Boolean(living_with_smoker.value),
      extra_notes: extra_notes.value
    }
    const res = await postReport(payload)
    // store in localStorage and navigate
    localStorage.setItem('latest_report', JSON.stringify(res.data))
    router.push('/dashboard')
  }catch(e){
    console.error(e)
    showToast('提交失败，请稍后重试')
  }finally{
    loading.value = false
  }
}
</script>

<style scoped>
h2 { margin: 12px 0; }
</style>
