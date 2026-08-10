import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "../views/HomeView.vue"
import ControlView from "../views/ControlView.vue"
import AlarmView from "../views/AlarmView.vue"
import AlarmEdit from "../views/AlarmEdit.vue"
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
      path: '/alarms',
      name: 'alarms',
      component: AlarmView,
    },
    {
      path: '/alarms/create',
      name: 'createAlarm',
      component: AlarmEdit,
      props: {"id": null},
    },
    {
    path: '/alarms/edit/:id',
    name: 'editAlarm',
    component: AlarmEdit,
    props: true,
  },
    { path: '/404', component: NotFound },  
    { path: "/:catchAll(.*)", redirect: '/404' },  
  ],
})

export default router
