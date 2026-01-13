<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top py-3">
      <div class="container-xl">
        <!-- Brand with Logo -->
        <router-link
          class="navbar-brand d-flex align-items-center gap-2 me-4"
          to="/admin/dashboard"
        >
          <!-- Logo Icon Container -->
          <div
            class="bg-primary bg-opacity-10 rounded-3 p-1 d-flex align-items-center justify-content-center text-primary"
            style="width: 40px; height: 40px"
          >
            <img src="/img.png" alt="CuraNet Logo" style="width: 24px; height: 24px;" />
          </div>
          
          <!-- SVG Text Logo -->
          <svg
            width="170"
            height="32"
            viewBox="0 0 250 40"
            xmlns="http://www.w3.org/2000/svg"
            class="d-none d-sm-block"
          >
            <text
              x="0"
              y="32"
              font-family="system-ui, -apple-system, sans-serif"
              font-weight="bold"
              font-size="32"
              letter-spacing="-0.5"
            >
              <tspan fill="#0d6efd">Cura</tspan>
              <tspan fill="#198754">Net</tspan>
              <tspan fill="#495057" font-weight="normal" font-size="24" dx="5">Admin</tspan>
            </text>
          </svg>
        </router-link>

        <!-- Mobile Toggle -->
        <button
          class="navbar-toggler border-0 shadow-none bg-light rounded-circle p-2"
          type="button"
          @click="toggleNavbar"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Collapsible Content -->
        <div class="collapse navbar-collapse" :class="{ show: navbarOpen }">
          <!-- Main Links -->
          <ul class="navbar-nav mx-auto mb-2 mb-lg-0 gap-1">
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill fw-medium" to="/admin/dashboard">
                <i class="bi bi-grid-1x2-fill me-2"></i>Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill fw-medium" to="/admin/doctors">
                <i class="bi bi-person-badge-fill me-2"></i>Doctors
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill fw-medium" to="/admin/patients">
                <i class="bi bi-people-fill me-2"></i>Patients
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill fw-medium" to="/admin/appointments">
                <i class="bi bi-calendar-check-fill me-2"></i>Schedule
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded-pill fw-medium" to="/admin/profile">
                <i class="bi bi-person-circle me-2"></i>Profile
              </router-link>
            </li>
          </ul>

          <!-- User Menu -->
          <div class="d-flex align-items-center gap-3 mt-3 mt-lg-0 pt-3 pt-lg-0 border-top border-lg-0">
            <!-- Divider (Desktop) -->
            <div class="d-none d-lg-block border-end h-50 mx-1" style="min-height: 24px;"></div>
            
            <div class="d-flex align-items-center gap-2 rounded-pill px-2">
                <div class="fw-bold text-dark small">Administrator</div>
            </div>

            <button
              class="btn btn-outline-danger btn-sm rounded-pill px-3 d-flex align-items-center gap-2 ms-2"
              @click="handleLogout"
              title="Logout"
            >
              <i class="bi bi-box-arrow-right"></i>
              <span class="d-lg-none">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container-xl py-4 flex-grow-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-top py-4 mt-auto">
      <div class="container text-center">
        <p class="text-muted mb-0 small">
          &copy; {{ new Date().getFullYear() }} <span class="fw-bold text-primary">CuraNet</span>. Hospital Management System. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "AdminLayout",
  data() {
    return {
      navbarOpen: false,
    };
  },
  watch: {
    // Automatically close mobile menu when route changes
    $route() {
      this.navbarOpen = false;
    },
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen;
    },
    async handleLogout() {
      if(!confirm("Are you sure you want to logout?")) return;
      try {
        await fetch('/api/logout', { 
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            "Auth-Token": localStorage.getItem("auth_token")
          }
        });
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_id');
      } catch (error) {
        console.warn("Backend logout failed", error);
      }

      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
/* Navigation Link Styling */
.nav-link {
  color: #6c757d; /* Bootstrap secondary text */
  transition: all 0.2s ease-in-out;
  font-size: 0.95rem;
}

.nav-link:hover {
  color: #0d6efd; /* Primary Blue */
  background-color: rgba(13, 110, 253, 0.08);
}

/* Active State (matched by vue-router 'router-link-active') */
.nav-link.router-link-active {
  color: #0d6efd !important;
  background-color: rgba(13, 110, 253, 0.12);
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(13, 110, 253, 0.1);
}

/* Page Transition Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Utilities */
.bg-light-subtle {
  background-color: #f8f9fa; /* Slightly off-white page background */
}
</style>