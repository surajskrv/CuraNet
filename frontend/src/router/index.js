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

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const isAuth = !!token && !!user.role;

  // Redirect authenticated users away from the landing page
  if (to.path === "/" && isAuth) {
    if (user.role === "admin") return next("/admin/dashboard");
    if (user.role === "doctor") return next("/doctor/dashboard");
    if (user.role === "patient") return next("/patient/dashboard");
  }

  // Public pages for unauthenticated users
  const publicPages = ["/", "/login", "/register"];

  // If user NOT authenticated → allow only public pages
  if (!isAuth && !publicPages.includes(to.path)) {
    return next("/");
  }

  // Authenticated users trying to access login/register → redirect to dashboard
  if (isAuth && (to.path === "/login" || to.path === "/register")) {
    if (user.role === "admin") return next("/admin/dashboard");
    if (user.role === "doctor") return next("/doctor/dashboard");
    if (user.role === "patient") return next("/patient/dashboard");
  }

  // Role-based route protection
  if (to.path.startsWith("/admin") && user.role !== "admin")
    return next("/");
  if (to.path.startsWith("/doctor") && user.role !== "doctor")
    return next("/");
  if (to.path.startsWith("/patient") && user.role !== "patient")
    return next("/");

  next();
});
export default router