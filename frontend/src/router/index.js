import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "../views/HomeView.vue"
import ControlView from "../views/ControlView.vue"
import TimerView from "../views/TimerView.vue"
import NotFound from "../views/NotFound.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/control',
      name: 'control',
      component: ControlView,
    },
    {
      path: '/timers',
      name: 'timers',
      component: TimerView,
    },
    { path: '/404', component: NotFound },  
    { path: "/:catchAll(.*)", redirect: '/404' },  
  ],
})

export default router
