<template>
  <div style="margin-top:8px;">
    <div style="display:flex; gap:8px;">
      <input v-model="nick" placeholder="昵称" />
      <input v-model="content" placeholder="说点感想..." style="flex:1;" />
      <button @click="post" :disabled="posting">发表</button>
    </div>
    <div style="margin-top:12px;">
      <div v-for="c in comments" :key="c.id" style="padding:8px;border-bottom:1px solid #f0f0f0;">
        <div style="font-weight:600">{{ c.nick }} <span style="font-weight:400;color:#999;font-size:12px;">{{ c.created_at }}</span></div>
        <div>{{ c.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getComments, postComment } from '../utils/api'

const nick = ref('')
const content = ref('')
const comments = ref([])
const posting = ref(false)

async function load(){
  const res = await getComments()
  comments.value = res.data || []
}
onMounted(()=>load())

async function post(){
  if(!nick.value || !content.value) { alert('请填写昵称和内容'); return }
  posting.value = true
  try{
    await postComment({ nick: nick.value, content: content.value })
    nick.value = ''
    content.value = ''
    await load()
  }catch(e){
    console.error(e); alert('提交失败')
  }finally{ posting.value = false }
}
</script>
