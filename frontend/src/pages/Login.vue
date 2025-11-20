<template>
  <div class="container-fluid min-vh-100 bg-light d-flex flex-column">

    <main class="flex-grow-1 d-flex align-items-center py-5 mt-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-md-8 col-lg-6 col-xl-5">

            <div class="card border-primary shadow-lg p-3 p-md-4 bg-white rounded">

              <!-- Back to home -->
              <div class="text-center mb-3">
                <router-link to="/" class="text-decoration-none">
                  <i class="bi bi-house-door-fill me-1"></i>
                  Back to Home
                </router-link>
              </div>

              <form @submit.prevent="loginUser">

                <h3 class="text-center mb-4">Login</h3>

                <div v-if="emessage" class="alert alert-danger">
                  {{ emessage }}
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label for="email" class="form-label">Email (Username)</label>
                  <input
                    id="email"
                    name="email"
                    class="form-control"
                    placeholder="example@gmail.com"
                    type="email"
                    required
                    autofocus
                    v-model="formData.email"
                  />
                </div>
                <!-- Password -->
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  
                  <div class="position-relative">
                    <input
                      id="password"
                      name="password"
                      class="form-control pe-5"
                      placeholder="password"
                      :type="showPassword ? 'text' : 'password'"
                      required
                      v-model="formData.password"
                    />

                    <button
                      type="button"
                      class="btn position-absolute top-50 end-0 translate-middle-y border-0 bg-transparent me-1"
                      @click="togglePass"
                      style="z-index: 5;"
                    >
                      <i
                        :class="showPassword ? 'bi bi-eye-fill text-danger' : 'bi bi-eye-slash-fill text-secondary'"
                        style="font-size: 1.5rem;"
                      ></i>
                    </button>
                  </div>
                </div>

                <div class="d-flex flex-column flex-sm-row justify-content-between gap-2 mt-4">
                  <button type="submit" class="btn btn-outline-success flex-grow-1 mb-3">Login</button>
                </div>
                <div class="text-center">
                  <p class="mb-0">Don't have an account? <router-link to="/register">Register</router-link></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
<script>
export default {
  data() {
    return {
      formData: {
        email: "",
        password: ""
      },
      showPassword: false,
      emessage: ""
    };
  },

  methods: {
    async loginUser() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            "Content-Type": 'application/json'
          },
          body: JSON.stringify(this.formData)
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Login failed. Please try again.');
        }
        
        localStorage.setItem("auth_token", data.auth_token);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("user_role", data.user_role);


        this.$emit('login');

        switch(data.user_role) {
          case 'admin':
            this.$router.push('/admin/dashboard');
            break;
          case 'patient':
            this.$router.push('/patient/dashboard');
            break;
          case 'doctor':
            this.$router.push('/doctor/dashboard');
            break;
          default:
            this.$router.push('/login');
            break;
        }

      } catch (error) {
        console.error("Login error:", error);
        this.emessage = error.message;
      }
    },
    togglePass() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>
