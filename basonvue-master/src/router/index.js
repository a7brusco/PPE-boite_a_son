import { createRouter, createWebHistory } from 'vue-router'
import Sequencer from '@/views/Sequencer.vue'
import InitKit from '@/views/InitKit.vue'

const routes = [
  {
    path: '/',
    name: 'Sequencer',
    component: Sequencer,
  },
  {
    path: '/initKit/:id',
    name: 'InitKit',
    component: InitKit,
    props:true,
  },
  //{
    //path: '/about',
    //name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    //component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  //}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
