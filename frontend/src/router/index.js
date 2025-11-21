import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // --- PUBLIC ROUTES ---
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/LandingPage.vue')
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

  // --- ADMIN ROUTES ---
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

  // --- DOCTOR ROUTES ---
  {
    path: '/doctor',
    component: () => import('@/layouts/DoctorLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'DoctorDashboard',
        component: () => import('@/pages/doctor/Dashboard.vue')
      },
      {
        path: 'history', 
        name: 'DoctorHistory',
        component: () => import('@/pages/doctor/History.vue')
      }
    ]
  },

  // --- PATIENT ROUTES ---
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

// --- NAVIGATION GUARD ---
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("auth_token");
  const role = localStorage.getItem("user_role");
  const isAuthenticated = !!token;

  const publicPages = ["/", "/login", "/register"];
  const authRequired = !publicPages.includes(to.path);

  // 1. If trying to access a protected page without login -> Go to Login
  if (authRequired && !isAuthenticated) {
    return next('/login');
  }

  // 2. If Logged in and trying to access Public Pages -> Redirect to Dashboard
  if (isAuthenticated && publicPages.includes(to.path)) {
     if (role === 'admin') return next('/admin/dashboard');
     if (role === 'doctor') return next('/doctor/dashboard');
     if (role === 'patient') return next('/patient/dashboard');
  }

  // 3. Role-Based Access Control (RBAC)
  if (isAuthenticated) {
    if (to.path.startsWith("/admin") && role !== "admin") {
      // Redirect unauthorized access to their own dashboard
      if (role === 'doctor') return next('/doctor/dashboard');
      if (role === 'patient') return next('/patient/dashboard');
      return next('/'); 
    }
    
    if (to.path.startsWith("/doctor") && role !== "doctor") {
      if (role === 'admin') return next('/admin/dashboard');
      if (role === 'patient') return next('/patient/dashboard');
      return next('/');
    }

    if (to.path.startsWith("/patient") && role !== "patient") {
       if (role === 'admin') return next('/admin/dashboard');
       if (role === 'doctor') return next('/doctor/dashboard');
       return next('/');
    }
  }

  next();
});

export default router;