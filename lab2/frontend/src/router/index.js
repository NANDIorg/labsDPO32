import { createRouter, createWebHistory } from 'vue-router'
import ProductsView from '../views/ProductsView.vue'
import CategoriesView from '../views/CategoriesView.vue'

const routes = [
  {
    path: '/',
    name: 'products',
    component: ProductsView
  },
  {
    path: '/categories',
    name: 'categories',
    component: CategoriesView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
