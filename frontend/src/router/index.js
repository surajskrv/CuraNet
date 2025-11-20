import { createRouter, createWebHistory } from 'vue-router'

const routes = [
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

// --- FIXED NAVIGATION GUARD ---
router.beforeEach((to, from, next) => {
  // 1. Retrieve keys exactly as you set them in loginUser()
  const token = localStorage.getItem("auth_token");
  const role = localStorage.getItem("user_role");

  // 2. Check if user is authenticated
  const isAuthenticated = !!token && !!role;

  // 3. Define public pages (Pages anyone can see)
  const publicPages = ["/", "/login", "/register"];
  const authRequired = !publicPages.includes(to.path);

  // --- LOGIC FLOW ---

  // Case A: User is NOT logged in and tries to access a restricted page
  if (authRequired && !isAuthenticated) {
    return next('/login');
  }

  // Case B: User IS logged in but tries to access Login/Register/Landing
  if (isAuthenticated && publicPages.includes(to.path)) {
     if (role === 'admin') return next('/admin/dashboard');
     if (role === 'doctor') return next('/doctor/dashboard');
     if (role === 'patient') return next('/patient/dashboard');
  }

  // Case C: Role-Based Security (Prevent Patient from seeing Admin pages)
  if (isAuthenticated) {
    if (to.path.startsWith("/admin") && role !== "admin") {
      // Unauthorized access -> send back to their own dashboard
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

  // If none of the above block the request, proceed
  next();
});

export default router;