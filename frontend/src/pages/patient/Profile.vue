<template>
  <div>
    <h2 class="mb-4">My Profile</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else class="row">
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="updateProfile">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Username</label>
                  <input type="text" class="form-control" v-model="profile.username" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-control" v-model="profile.email" required />
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">First Name</label>
                  <input type="text" class="form-control" v-model="profile.first_name" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Last Name</label>
                  <input type="text" class="form-control" v-model="profile.last_name" required />
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Date of Birth</label>
                  <input type="date" class="form-control" v-model="profile.date_of_birth" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Contact Number</label>
                  <input type="tel" class="form-control" v-model="profile.contact_number" required />
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Address</label>
                <textarea class="form-control" v-model="profile.address" rows="3"></textarea>
              </div>
              
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { patientAPI } from '@/services/api'

export default {
  name: 'PatientProfile',
  data() {
    return {
      profile: {},
      loading: true,
      saving: false
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    async loadProfile() {
      try {
        this.profile = await patientAPI.getProfile()
      } catch (error) {
        alert('Failed to load profile: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async updateProfile() {
      this.saving = true
      try {
        await patientAPI.updateProfile(this.profile)
        alert('Profile updated successfully!')
        // Update local storage
        localStorage.setItem('user', JSON.stringify(this.profile))
      } catch (error) {
        alert('Failed to update profile: ' + error.message)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

