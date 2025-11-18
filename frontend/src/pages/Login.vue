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

                <!-- Password (Fixed eye icon position) -->
                <div class="mb-3 position-relative">
                  <label for="password" class="form-label">Password</label>

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
                    class="btn btn-sm position-absolute top-50 end-0 translate-middle-y border-0 bg-transparent"
                    @click="togglePass"
                  >
                    <i
                      :class="showPassword ? 'bi bi-eye-fill text-primary' : 'bi bi-eye-slash-fill text-secondary'"
                      style="font-size: 20px"
                    ></i>
                  </button>
                </div>

                <!-- Buttons -->
                <div class="d-flex flex-column flex-sm-row justify-content-between gap-2 mt-4">
                  <router-link to="/register" class="btn btn-outline-primary flex-grow-1">
                    Register
                  </router-link>
                  <button type="submit" class="btn btn-outline-success flex-grow-1">Login</button>
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
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.formData)
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.message);

        localStorage.setItem("auth_token", data.auth_token);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("user_role", data.user_role);

        switch (data.user_role) {
          case "admin": this.$router.push("/adminHome"); break;
          case "user": this.$router.push("/userHome"); break;
          default: this.$router.push("/notFound");
        }

      } catch (error) {
        this.emessage = error.message;
      }
    },

    togglePass() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>
