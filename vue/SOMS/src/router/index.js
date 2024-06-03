import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from "../stores/user.js"
import HomeView from '@/views/HomeView.vue'
import Register from '@/components/auth/Register.vue'
import Login from '@/components/auth/Login.vue'
import Dashboard from '@/components/user/Dashboard.vue'
import DashboardVideo from '@/components/user/DashboardVideo.vue'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import Profile from '@/components/user/Profile.vue'


let handlingFirstRoute = true

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'Login',
      component : Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path:'/dashboardvideo',
      name: 'DashboardVideo',
      component: DashboardVideo
    },
    {
      path: '/admin',
      name: 'AdminDashboard',
      component: AdminDashboard
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    } 
  ]
})

router.beforeEach(async (to, from, next) => {  
  const userStore = useUserStore()  
  if (handlingFirstRoute) {
    handlingFirstRoute = false
    await userStore.restoreToken()
  }
  if ((to.name == 'Login') || (to.name == 'Home') || (to.name == 'Register')) {
    next()
    return
  }
  if (!userStore.user) {
    next({ name: 'Home' })
    return
  }
  next()
})

export default router
