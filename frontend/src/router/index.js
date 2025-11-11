import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/Register.vue')
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/pages/admin/Dashboard.vue')
      },
      {
        path: 'doctors',
        name: 'AdminDoctors',
        component: () => import('@/pages/admin/Doctors.vue')
      },
      {
        path: 'patients',
        name: 'AdminPatients',
        component: () => import('@/pages/admin/Patients.vue')
      },
      {
        path: 'appointments',
        name: 'AdminAppointments',
        component: () => import('@/pages/admin/Appointments.vue')
      }
    ]
  },
  {
    path: '/doctor',
    component: () => import('@/layouts/DoctorLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'DoctorDashboard',
        component: () => import('@/pages/doctor/Dashboard.vue')
      }
    ]
  },
  {
    path: '/patient',
    component: () => import('@/layouts/PatientLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'PatientDashboard',
        component: () => import('@/pages/patient/Dashboard.vue')
      },
      {
        path: 'history',
        name: 'PatientHistory',
        component: () => import('@/pages/patient/History.vue')
      },
      {
        path: 'profile',
        name: 'PatientProfile',
        component: () => import('@/pages/patient/Profile.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  // Public routes
  if (to.path === '/login' || to.path === '/register') {
    if (token && user.role) {
      // Redirect to appropriate dashboard
      if (user.role === 'admin') next('/admin/dashboard')
      else if (user.role === 'doctor') next('/doctor/dashboard')
      else if (user.role === 'patient') next('/patient/dashboard')
      else next()
    } else {
      next()
    }
  } else {
    // Protected routes
    if (!token) {
      next('/login')
    } else if (to.path.startsWith('/admin') && user.role !== 'admin') {
      next('/login')
    } else if (to.path.startsWith('/doctor') && user.role !== 'doctor') {
      next('/login')
    } else if (to.path.startsWith('/patient') && user.role !== 'patient') {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
