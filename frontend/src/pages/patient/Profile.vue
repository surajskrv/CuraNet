<template>
  <div>
    <h2 class="mb-4">My Profile</h2>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading profile...</p>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <div v-else class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <form @submit.prevent="updateProfile">
              
              <h5 class="mb-3 text-primary">Personal Information</h5>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Full Name</label>
                  <input type="text" class="form-control" v-model="profile.name" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Email Address</label>
                  <input type="email" class="form-control" v-model="profile.email" required />
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Phone Number</label>
                  <input type="tel" class="form-control" v-model="profile.phone" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Date of Birth</label>
                  <input type="date" class="form-control" v-model="profile.date_of_birth" />
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Gender</label>
                  <select class="form-select" v-model="profile.gender">
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Blood Group</label>
                  <select class="form-select" v-model="profile.blood_group">
                    <option value="">Select Group</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                  </select>
                </div>
              </div>
              
              <h5 class="mb-3 mt-4 text-primary">Contact Details</h5>
              <div class="row">
                <div class="col-md-8 mb-3">
                  <label class="form-label">Address</label>
                  <textarea class="form-control" v-model="profile.address" rows="2"></textarea>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Pincode</label>
                  <input type="text" class="form-control" v-model="profile.pincode" />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Emergency Contact</label>
                <input type="text" class="form-control" v-model="profile.emergency_contact" placeholder="Name & Phone Number" />
              </div>

              <h5 class="mb-3 mt-4 text-primary">Medical Overview</h5>
              <div class="mb-4">
                <label class="form-label">Existing Medical History / Allergies</label>
                <textarea class="form-control" v-model="profile.medical_history" rows="3" placeholder="List any known conditions or allergies..."></textarea>
              </div>
              
              <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary px-4" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  {{ saving ? 'Saving Changes...' : 'Update Profile' }}
                </button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientProfile',
  data() {
    return {
      profile: {
        name: '',
        email: '',
        phone: '',
        date_of_birth: '',
        address: '',
        pincode: '',
        gender: '',
        blood_group: '',
        medical_history: '',
        emergency_contact: ''
      },
      loading: true,
      saving: false,
      error: ''
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    // --- LOAD PROFILE ---
    async loadProfile() {
      this.loading = true;
      this.error = '';
      try {
        const response = await fetch('/api/patient/profile', {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            this.$router.push('/login');
            throw new Error("Session expired");
          }
          throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        this.profile = { ...this.profile, ...data }; // Merge defaults with fetched data
        
      } catch (err) {
        console.error(err);
        this.error = err.message || "Failed to load profile";
      } finally {
        this.loading = false;
      }
    },

    // --- UPDATE PROFILE ---
    async updateProfile() {
      this.saving = true;
      this.error = '';
      try {
        const response = await fetch('/api/patient/profile', {
          method: 'PUT',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(this.profile)
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Update failed");
        }

        alert('Profile updated successfully!');
        
      } catch (err) {
        console.error(err);
        this.error = err.message || "Failed to update profile";
        window.scrollTo(0, 0); // Scroll to top to see error
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
}
</style>