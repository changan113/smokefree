import axios from 'axios'

const base = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const client = axios.create({ baseURL: base, timeout: 10000 })

export function postReport(payload){
  return client.post('/api/report', payload)
}

export function getComments(){
  return client.get('/api/comments')
}

export function postComment(payload){
  return client.post('/api/comments', payload)
}
