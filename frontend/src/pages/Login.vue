<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Hospital Management System</h3>
            <h5 class="text-center mb-4">Login</h5>
            
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="username"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  required
                />
              </div>
              
              <button type="submit" class="btn btn-primary w-100 mb-3" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>
            
            <div class="text-center">
              <p class="mb-0">Don't have an account? <router-link to="/register">Register</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI, setAuthToken } from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      this.loading = true
      
      try {
        const response = await authAPI.login(this.username, this.password)
        
        // Store token and user
        setAuthToken(response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        // Redirect based on role
        if (response.user.role === 'admin') {
          this.router.push('/admin/dashboard')
        } else if (response.user.role === 'doctor') {
          this.router.push('/doctor/dashboard')
        } else if (response.user.role === 'patient') {
          this.router.push('/patient/dashboard')
        }
      } catch (error) {
        this.error = error.message || 'Login failed. Please check your credentials.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}
</style>

