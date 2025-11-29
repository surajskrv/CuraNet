<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow">
      <div class="container">
        <!-- Brand with Logo -->
        <router-link class="navbar-brand d-flex align-items-center gap-2" to="/admin/dashboard">
          <div class="bg-white rounded-circle p-1 d-flex align-items-center justify-content-center" style="width: 32px; height: 32px;">
            <img src="/img.png" alt="Logo" width="24" height="24">
          </div>
          <span class="fw-bold tracking-tight">CuraNet Admin</span>
        </router-link>

        <!-- Mobile Toggle -->
        <button 
          class="navbar-toggler border-0" 
          type="button" 
          @click="toggleNavbar"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Collapsible Content -->
        <div class="collapse navbar-collapse" :class="{ show: navbarOpen }">
          
          <!-- Main Links -->
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-3">
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/admin/dashboard" active-class="active">
                <i class="bi bi-speedometer2 me-2"></i>Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/admin/doctors" active-class="active">
                <i class="bi bi-person-badge me-2"></i>Doctors
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/admin/patients" active-class="active">
                <i class="bi bi-people me-2"></i>Patients
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/admin/appointments" active-class="active">
                <i class="bi bi-calendar-check me-2"></i>Appointments
              </router-link>
            </li>
          </ul>

          <!-- User Menu -->
          <ul class="navbar-nav align-items-lg-center gap-2">
            <li class="nav-item d-none d-lg-block">
              <div class="vr h-100 text-white opacity-50 mx-2"></div>
            </li>
            <li class="nav-item text-center text-lg-start">
              <span class="navbar-text text-white opacity-75 small d-block d-lg-inline">Logged in as</span>
              <span class="navbar-text text-white fw-bold ms-1">Admin</span>
            </li>
            <li class="nav-item ms-lg-2">
              <button 
                class="btn btn-light text-primary fw-semibold w-100 w-lg-auto d-flex align-items-center justify-content-center gap-2 shadow-sm" 
                @click="handleLogout"
              >
                <i class="bi bi-box-arrow-right"></i> Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container py-4 flex-grow-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <!-- Footer -->
    <footer class="bg-white border-top py-3 mt-auto">
      <div class="container text-center">
        <small class="text-muted">
          &copy; {{ new Date().getFullYear() }} CuraNet Hospital Management System. All rights reserved.
        </small>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  data() {
    return {
      navbarOpen: false
    }
  },
  watch: {
    // Automatically close mobile menu when route changes
    $route() {
      this.navbarOpen = false;
    }
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen
    },
    async handleLogout() {
      if(!confirm("Are you sure you want to logout?")) return;

      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_role');

      try {
        await fetch('/api/logout', { method: 'POST' }); 
      } catch (error) {
        console.warn("Backend logout failed, but frontend session cleared.");
      }

      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
/* Navigation Link Styling */
.nav-link {
  transition: all 0.2s ease;
  font-weight: 500;
  opacity: 0.9;
}

.nav-link:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  color: white !important;
  opacity: 1;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Page Transition Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>