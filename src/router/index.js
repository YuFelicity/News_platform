import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const routes = [
  {
    path: '/login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('@/views/Home.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: 'news/:id',
        component: () => import('@/views/NewsDetail.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: 'user',
        component: () => import('@/views/UserCenter.vue'),
        meta: { requiresAuth: true },
        children: [
          {
            path: 'profile',
            component: () => import('@/views/UserProfile.vue')
          },
          {
            path: 'favorites',
            component: () => import('@/views/Favorites.vue')
          },
          {
            path: 'history',
            component: () => import('@/views/History.vue')
          }
        ]
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
