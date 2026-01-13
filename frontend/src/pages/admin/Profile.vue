<template>
  <div>
    <h2 class="mb-4">Admin Profile</h2>

    <!-- Alerts -->
    <div v-if="message" class="alert alert-success alert-dismissible fade show" role="alert">
      <i class="bi bi-check-circle-fill me-2"></i>{{ message }}
      <button type="button" class="btn-close" @click="message = ''"></button>
    </div>
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow-sm">
          <div class="card-header bg-white text-center py-4">
            <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px; font-size: 2rem;">
              {{ getInitials(profile.name) }}
            </div>
            <h5 class="mb-0">{{ profile.name }}</h5>
            <small class="text-muted">Administrator</small>
          </div>
          
          <div class="card-body p-4">
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label for="email" class="form-label">Email Address</label>
                <input 
                  type="email" 
                  class="form-control bg-light" 
                  id="email" 
                  v-model="profile.email" 
                  required
                  readonly
                  title="Email cannot be changed"
                />
                <div class="form-text text-muted">Email address cannot be changed.</div>
              </div>

              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  v-model="profile.name" 
                  required 
                />
              </div>

              <div class="mb-4">
                <label for="password" class="form-label">New Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="profile.password" 
                  placeholder="Leave blank to keep current password"
                  minlength="6"
                />
              </div>

              <div class="d-grid">
                <button type="submit" class="btn btn-primary" :disabled="submitting">
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  {{ submitting ? 'Saving Changes...' : 'Update Profile' }}
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
  name: "AdminProfile",
  data() {
    return {
      profile: {
        name: "",
        email: "",
        password: ""
      },
      loading: true,
      submitting: false,
      message: "",
      error: ""
    };
  },
  mounted() {
    this.loadProfile();
  },
  methods: {

    // --- Load Profile ---
    async loadProfile() {
      this.loading = true;
      this.error = "";
      try {
        const response = await fetch("/api/admin/profile", { 
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem('auth_token'),
          },
        });

        if (!response.ok) {
           if (response.status === 401) {
             this.$router.push('/login');
             return;
           }
           throw new Error(`Failed to load profile (${response.status})`);
        }

        const data = await response.json();
        
        this.profile.name = data.name ; 
        this.profile.email = data.email ; 
        
      } catch (err) {
        console.error(err);
        this.error = "Could not load profile details.";
      } finally {
        this.loading = false;
      }
    },

    // --- Update Profile ---
    async updateProfile() {
      this.submitting = true;
      this.message = "";
      this.error = "";
      
      try {
        const payload = {
          name: this.profile.name,
          ...(this.profile.password && { password: this.profile.password })
        };

        const response = await fetch("/api/admin/profile", {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem('auth_token'),
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Failed to update profile");
        }

        this.message = "Profile updated successfully!";
        this.profile.password = ""; // Clear password field
        
      } catch (err) {
        console.error(err);
        this.error = err.message;
      } finally {
        this.submitting = false;
      }
    },
    
    getInitials(name) {
      if (!name) return 'A';
      return name.charAt(0).toUpperCase();
    }
  },
};
</script>