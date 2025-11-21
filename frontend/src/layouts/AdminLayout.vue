<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">CuraNet</a>
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ show: navbarOpen }">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/doctors">Doctors</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/patients">Patients</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/appointments">Appointments</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <span class="navbar-text me-3">Welcome, Admin</span>
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
  name: 'AdminLayout',
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
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_role');

      try {
        await fetch('/api/logout'); 
      } catch (error) {
        console.warn("Backend logout failed, but frontend is cleared.");
      }

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