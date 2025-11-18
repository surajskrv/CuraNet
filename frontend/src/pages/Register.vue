<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Register</h3>
            <div class="text-right mt-3">
              <router-link to="/" class="btn btn-outline-primary px-4 py-2">
                <i class="bi bi-house-door-fill me-2"></i>
                Back to Home
              </router-link>
            </div>

            
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <div v-if="success" class="alert alert-success" role="alert">
              {{ success }}
            </div>
            
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="email" class="form-label">Email *</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="formData.email"
                  required
                />
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="password" class="form-label">Password *</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    v-model="formData.password"
                    required
                    minlength="6"
                  />
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password *</label>
                  <input
                    type="password"
                    class="form-control"
                    id="confirmPassword"
                    v-model="confirmPassword"
                    required
                  />
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="firstName" class="form-label">First Name *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="firstName"
                    v-model="formData.first_name"
                    required
                  />
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="lastName" class="form-label">Last Name *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="lastName"
                    v-model="formData.last_name"
                    required
                  />
                </div>
              </div>  
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="dateOfBirth" class="form-label">Date of Birth *</label>
                    <input
                      type="date"
                      class="form-control"
                      id="dateOfBirth"
                      v-model="formData.date_of_birth"
                      required
                    />
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="contactNumber" class="form-label">Contact Number *</label>
                    <input
                      type="tel"
                      class="form-control"
                      id="contactNumber"
                      v-model="formData.contact_number"
                      required
                    />
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="address" class="form-label">Address</label>
                  <textarea
                    class="form-control"
                    id="address"
                    rows="3"
                    v-model="formData.address"
                  ></textarea>
                </div>
              
              <button type="submit" class="btn btn-primary w-100 mb-3" :disabled="loading || !passwordsMatch">
                {{ loading ? 'Registering...' : 'Register' }}
              </button>
              
              <div v-if="!passwordsMatch" class="alert alert-warning" role="alert">
                Passwords do not match
              </div>
            </form>
            
            <div class="text-center">
              <p class="mb-0">Already have an account? <router-link to="/login">Login</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI, setAuthToken } from '@/services/api'
import { patientAPI } from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      formData: {
        role: 'patient',
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        contact_number: '',
        address: '',
      },
      confirmPassword: '',
      error: '',
      success: '',
      loading: false
    }
  },
  computed: {
    passwordsMatch() {
      return this.formData.password === this.confirmPassword || !this.formData.password
    }
  },
  methods: {
    async handleRegister() {
      if (!this.passwordsMatch) {
        this.error = 'Passwords do not match'
        return
      }
      
      this.error = ''
      this.success = ''
      this.loading = true
      
      try {
        const response = await authAPI.register(this.formData)
        this.success = 'Registration successful! Redirecting to login...'
        
        setTimeout(() => {
          this.router.push('/login')
        }, 2000)
      } catch (error) {
        this.error = error.message || 'Registration failed. Please try again.'
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
