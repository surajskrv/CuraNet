<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-info">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Hospital Management System</a>
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ show: navbarOpen }">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/patient/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/patient/history">History</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/patient/profile">Profile</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <span class="navbar-text me-3">Welcome, {{ userData?.first_name || '' }}</span>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-light btn-sm" @click="handleLogout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container-fluid mt-3">
      <router-view />
    </div>
  </div>
</template>

<script>

export default {
  name: 'PatientLayout',
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
      // 1. Clear ALL data saved during login
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_role');

      // 2. (Optional) Notify Backend to kill the session cookie
      // This is important because your Flask backend uses login_user()
      try {
        await fetch('/api/logout'); 
      } catch (error) {
        console.warn("Backend logout failed, but frontend is cleared.");
      }

      // 3. Redirect to Login
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.nav-link.router-link-active {
  font-weight: bold;
}
</style>