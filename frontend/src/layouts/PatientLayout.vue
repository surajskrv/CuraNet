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
import { removeAuthToken } from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'PatientLayout',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      navbarOpen: false,
      userData: JSON.parse(localStorage.getItem('user') || '{}')
    }
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen
    },
    handleLogout() {
      removeAuthToken()
      this.router.push('/login')
    }
  }
}
</script>

<style scoped>
.nav-link.router-link-active {
  font-weight: bold;
}
</style>

