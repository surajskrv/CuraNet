<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">CuraNet</a>
        <div class="navbar-nav ms-auto">
          <span class="navbar-text me-3">Welcome, Dr. {{ userData?.first_name || '' }}</span>
          <button class="btn btn-outline-light btn-sm" @click="handleLogout">Logout</button>
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
