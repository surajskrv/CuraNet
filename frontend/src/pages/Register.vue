<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-body">
            
            <div class="text-center mb-4">
              <h3 class="card-title">CuraNet</h3>
            </div>
            
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h4 class="mb-0">Register</h4>
              <router-link to="/" class="btn btn-outline-primary btn-sm px-3">
                <i class="bi bi-house-door-fill me-1"></i>
                Back to Home
              </router-link>
            </div>

            <div v-if="emessage" class="alert alert-danger" role="alert">
              {{ emessage }}
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
                    v-model="formData.password2"
                    required
                  />
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="fullName" class="form-label">Full Name *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="fullName"
                    v-model="formData.name"
                    required
                  />
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="gender" class="form-label">Gender *</label>
                  <select class="form-select" id="gender" v-model="formData.gender" required>
                    <option value="" disabled>Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
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
                      pattern="[0-9]{10}"
                    />
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="blood" class="form-label">Blood Group *</label>
                    <select class="form-select" id="blood" v-model="formData.blood_group" required>
                        <option value="" disabled>Select Group</option>
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
                  
                  <div class="col-md-6 mb-3">
                    <label for="pincode" class="form-label">Pincode *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="pincode"
                      v-model="formData.pincode"
                      required
                      pattern="[0-9]{6}"
                    />
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="address" class="form-label">Address *</label>
                  <textarea
                    class="form-control"
                    id="address"
                    rows="3"
                    v-model="formData.address"
                  ></textarea>
                </div>
              
              <button type="submit" class="btn btn-primary w-100 mb-3" :disabled="isLoading">
                {{ isLoading ? 'Registering...' : 'Register' }}
              </button>
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
export default {
  data() {
    return {
      formData: {
        email: "",
        password: "",
        password2: "",
        name: "",
        address: "",
        pincode: "",
        contact_number: "",
        date_of_birth: "",
        gender: "",
        blood_group: "",
      },
      emessage: "",
      isLoading: false, // Added missing state
    };
  },
  methods: {
    // RENAMED from addUser to handleRegister so the form can find it
    async handleRegister() {
      if (this.formData.password !== this.formData.password2) {
        this.emessage= "Passwords do not match";
        return;
      }

      if (this.formData.password.length < 5) {
        this.emessage = "Password must be at least 5 characters";
        return;
      }

      if (!/^\d{6}$/.test(this.formData.pincode)) {
        this.emessage = "Please enter a valid 6-digit pincode number";
        return;
      }
      if (!/^\d{10}$/.test(this.formData.contact_number)) {
        this.emessage = "Please enter a valid 10-digit phone number";
        return;
      }

      this.isLoading = true;
      this.emessage = "";

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.formData.email,
            password: this.formData.password,
            name: this.formData.name,
            address: this.formData.address,
            pincode: this.formData.pincode,
            phone: this.formData.contact_number, // Mapping contact_number to phone
            date_of_birth: this.formData.date_of_birth,
            blood_group: this.formData.blood_group,
            gender: this.formData.gender,
            role: "patient" // Explicitly telling backend this is a patient
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          // Use backend message if available
          throw new Error(data.message || "Registration failed");
        }

        alert("Registration successful! Please login.");
        this.$router.push("/login");
      } catch (error) {
        this.emessage = error.message; // Show the actual error from backend
        console.error("Registration error:", error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}
</style>