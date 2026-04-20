import { createRouter, createWebHistory } from 'vue-router'
import Survey from './pages/Survey.vue'
import Dashboard from './pages/Dashboard.vue'

const routes = [
  { path: '/', component: Survey },
  { path: '/dashboard', component: Dashboard }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
