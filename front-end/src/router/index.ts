import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Employee from '../views/Employee.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Employeee',
    component: Employee
  },
  {
    path: '/manager',
    name: 'Manager',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Manager.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
