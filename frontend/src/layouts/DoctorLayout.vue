<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Hospital Management System</a>
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
import { removeAuthToken } from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'DoctorLayout',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      userData: JSON.parse(localStorage.getItem('user') || '{}')
    }
  },
  methods: {
    handleLogout() {
      removeAuthToken()
      this.router.push('/login')
    }
  }
}
</script>

