<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-health-gradient shadow-sm">
      <div class="container">
        <!-- Brand -->
        <router-link class="navbar-brand d-flex align-items-center gap-2 fw-bold" to="/patient/dashboard">
          <div class="bg-white rounded-circle p-1 d-flex align-items-center justify-content-center logo-container">
            <img src="/img.png" alt="Logo" width="24" height="24">
          </div>
          <span class="tracking-tight">CuraNet Patient</span>
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
          
          <!-- Navigation Links -->
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4">
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/patient/dashboard" active-class="active">
                <i class="bi bi-grid-fill me-2"></i>Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/patient/history" active-class="active">
                <i class="bi bi-clock-history me-2"></i>History
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill" to="/patient/profile" active-class="active">
                <i class="bi bi-person-circle me-2"></i>Profile
              </router-link>
            </li>
          </ul>

          <!-- User Menu -->
          <ul class="navbar-nav align-items-lg-center gap-2">
            <!-- Divider on Desktop -->
            <li class="nav-item d-none d-lg-block">
              <div class="vr h-100 text-white opacity-50 mx-2"></div>
            </li>
            
            <!-- User Greeting -->
            <li class="nav-item text-white">
              <div class="d-flex align-items-center gap-2">
                <div class="text-end d-none d-lg-block">
                  <div class="small opacity-75" style="line-height: 1;">Welcome,</div>
                  <div class="fw-bold" style="line-height: 1.2;">{{ userName || 'Patient' }}</div>
                </div>
                <!-- Mobile Only Greeting -->
                <span class="d-lg-none mb-2">Welcome, <strong>{{ userName || 'Patient' }}</strong></span>
              </div>
            </li>

            <!-- Logout Button -->
            <li class="nav-item ms-lg-3">
              <button 
                class="btn btn-white text-teal fw-bold shadow-sm w-100 w-lg-auto d-flex align-items-center justify-content-center" 
                @click="handleLogout"
              >
                <i class="bi bi-box-arrow-right me-2"></i> Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content Area with Transition -->
    <div class="container py-4 flex-grow-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <!-- Footer -->
    <footer class="bg-white border-top py-3 mt-auto">
      <div class="container text-center text-muted">
        <small>
          &copy; {{ new Date().getFullYear() }} <strong>CuraNet</strong>. Your Health, Our Priority.
        </small>
      </div>
    </footer>
  </div>
</template>

<script>
import { patientAPI } from '@/services/api';

export default {
  name: 'PatientLayout',
  data() {
    return {
      navbarOpen: false,
      userName: ''
    }
  },
  watch: {
    $route() {
      this.navbarOpen = false; // Close menu on route change
    }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen
    },
    
    async fetchUserProfile() {
      try {
        const data = await patientAPI.getProfile();
        this.userName = data.name;
      } catch (error) {
        console.warn("Could not fetch user name for header");
      }
    },

    async handleLogout() {
      if(!confirm("Are you sure you want to logout?")) return;

      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_role');

      try {
        await fetch('/api/logout', { method: 'POST' }); 
      } catch (error) {
        console.warn("Backend logout failed, but frontend cleared.");
      }

      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
/* Custom Gradient for Healthcare feel */
.bg-health-gradient {
  background: linear-gradient(135deg, #20c997 0%, #0d6efd 100%);
}

.logo-container {
  width: 32px; 
  height: 32px;
}

/* Nav Link Styling */
.nav-link {
  color: rgba(255, 255, 255, 0.9) !important;
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff !important;
  transform: translateY(-1px);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.25);
  color: #fff !important;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Custom Button */
.btn-white {
  background-color: #fff;
  color: #0d6efd; /* Fallback */
  color: var(--bs-primary);
  border: none;
  transition: transform 0.2s;
}
.btn-white:hover {
  transform: translateY(-1px);
  background-color: #f8f9fa;
}
.text-teal {
  color: #20c997; /* Matches gradient start */
}

/* Page Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>