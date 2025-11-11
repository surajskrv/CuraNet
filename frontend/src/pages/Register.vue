<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Register</h3>
            <p class="text-center text-muted mb-4">Patients and Doctors can register</p>
            
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <div v-if="success" class="alert alert-success" role="alert">
              {{ success }}
            </div>
            
            <form @submit.prevent="handleRegister">
              <!-- Role Selection -->
              <div class="mb-3">
                <label class="form-label">I am registering as *</label>
                <div>
                  <div class="form-check form-check-inline">
                    <input
                      class="form-check-input"
                      type="radio"
                      id="rolePatient"
                      value="patient"
                      v-model="formData.role"
                      required
                    />
                    <label class="form-check-label" for="rolePatient">Patient</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input
                      class="form-check-input"
                      type="radio"
                      id="roleDoctor"
                      value="doctor"
                      v-model="formData.role"
                      required
                    />
                    <label class="form-check-label" for="roleDoctor">Doctor</label>
                  </div>
                </div>
              </div>
              
              <!-- Common Fields -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="username" class="form-label">Username *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="username"
                    v-model="formData.username"
                    required
                  />
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email *</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="formData.email"
                    required
                  />
                </div>
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
              
              <!-- Patient-specific fields -->
              <template v-if="formData.role === 'patient'">
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
              </template>
              
              <!-- Doctor-specific fields -->
              <template v-if="formData.role === 'doctor'">
                <div class="mb-3">
                  <label for="specialization" class="form-label">Specialization/Department *</label>
                  <select
                    class="form-select"
                    id="specialization"
                    v-model.number="formData.specialization_id"
                    required
                  >
                    <option value="">Select Specialization</option>
                    <option v-for="spec in deaprtment" :key="spec.id" :value="spec.id">
                      {{ spec.name }}
                    </option>
                  </select>
                </div>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="experienceYears" class="form-label">Experience (Years)</label>
                    <input
                      type="number"
                      class="form-control"
                      id="experienceYears"
                      v-model.number="formData.experience_years"
                      min="0"
                    />
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="doctorContactNumber" class="form-label">Contact Number</label>
                    <input
                      type="tel"
                      class="form-control"
                      id="doctorContactNumber"
                      v-model="formData.contact_number"
                    />
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="qualifications" class="form-label">Qualifications</label>
                  <input
                    type="text"
                    class="form-control"
                    id="qualifications"
                    v-model="formData.qualifications"
                    placeholder="e.g., MBBS, MD, DM"
                  />
                </div>
                
                <div class="mb-3">
                  <label for="bio" class="form-label">Bio</label>
                  <textarea
                    class="form-control"
                    id="bio"
                    rows="3"
                    v-model="formData.bio"
                    placeholder="Tell us about your background and expertise"
                  ></textarea>
                </div>
              </template>
              
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
        // Patient fields
        date_of_birth: '',
        contact_number: '',
        address: '',
        // Doctor fields
        specialization_id: '',
        experience_years: null,
        qualifications: '',
        bio: ''
      },
      confirmPassword: '',
      deaprtment: [],
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
  mounted() {
    // Load deaprtment for doctor registration
    this.loadDeaprtment()
  },
  methods: {
    async loadDeaprtment() {
      try {
        // Fetch deaprtment from public endpoint
        const response = await fetch('http://localhost:5000/api/auth/deaprtment')
        if (response.ok) {
          this.deaprtment = await response.json()
        } else {
          // Fallback list if API fails
          this.deaprtment = [
            { id: 1, name: 'Cardiology' },
            { id: 2, name: 'Oncology' },
            { id: 3, name: 'General' },
            { id: 4, name: 'Pediatrics' },
            { id: 5, name: 'Orthopedics' },
            { id: 6, name: 'Neurology' }
          ]
        }
      } catch (error) {
        console.error('Failed to load deaprtment:', error)
        // Fallback list
        this.deaprtment = [
          { id: 1, name: 'Cardiology' },
          { id: 2, name: 'Oncology' },
          { id: 3, name: 'General' },
          { id: 4, name: 'Pediatrics' },
          { id: 5, name: 'Orthopedics' },
          { id: 6, name: 'Neurology' }
        ]
      }
    },
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
