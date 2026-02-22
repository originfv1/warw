import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/armas',
      name: 'WeaponList',
      component: () => import('../views/armament/WeaponListView.vue') 
    },
    {
      path: '/arma/:id',
      name: 'WeaponDetail',
      component: () => import('../views/armament/WeaponDetailView.vue')
    },
    {
    path: '/aviones',
    name: 'PlaneList',
    component: () => import('../views/vehicles/plane/PlaneListView.vue')
    },
    {
      path: '/helicopteros',
      name: 'HelicopterList',
      component: () => import('../views/vehicles/helicopter/HelicopterListView.vue')
    }
  ]
})

export default router
