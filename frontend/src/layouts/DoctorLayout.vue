<template>
  <div class="doctor-layout">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <router-link class="navbar-brand fw-bold" to="/doctor/dashboard">
          <i class="bi bi-heart-pulse-fill me-2"></i> CuraNet Doctor
        </router-link>
        
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" :class="{ show: navbarOpen }">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-center">
            <li class="nav-item">
              <router-link class="nav-link" to="/doctor/dashboard" active-class="active">
                <i class="bi bi-speedometer2 me-1"></i> Dashboard
              </router-link>
            </li>
            <!-- Added History Link -->
            <li class="nav-item">
              <router-link class="nav-link" to="/doctor/history" active-class="active">
                <i class="bi bi-clock-history me-1"></i> History
              </router-link>
            </li>
            <li class="nav-item border-start ms-2 ps-2 d-none d-lg-block"></li>
            <li class="nav-item">
              <button class="nav-link btn btn-link text-white" @click="handleLogout">
                <i class="bi bi-box-arrow-right me-1"></i> Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4 pb-5">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorLayout',
  data() {
    return {
      navbarOpen: false
    }
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen
    },
    async handleLogout() {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_role');
      localStorage.removeItem('user_id');

      try {
        await fetch('/api/logout', { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' } 
        });
      } catch (error) {
        console.warn("Backend logout failed", error);
      }

      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.doctor-layout {
  min-height: 100vh;
  background-color: #f8f9fa;
}
.nav-link.active {
  font-weight: bold;
  color: white !important;
  border-bottom: 2px solid white;
}
</style>