<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top py-3">
      <div class="container-xl">
        <!-- Brand -->
        <a class="navbar-brand d-flex align-items-center gap-2 me-4" href="#">
          <div class="bg-primary bg-opacity-10 rounded-circle p-1 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px">
            <img src="/img.png" alt="Logo" width="24" height="24">
          </div>
          <!-- SVG Text Logo -->
          <svg
            width="170"
            height="32"
            viewBox="0 0 250 40"
            xmlns="http://www.w3.org/2000/svg"
            
          >
            <text
              x="0"
              y="32"
              font-family="system-ui, -apple-system, sans-serif"
              font-weight="bold"
              font-size="32"
              letter-spacing="-0.5"
            >
              <tspan fill="#0d6efd">Cura</tspan>
              <tspan fill="#198754">Net</tspan>
            </text>
          </svg>
        </a>

        <!-- Mobile Toggle -->
        <button 
          class="navbar-toggler border-0 shadow-none bg-light rounded-circle p-2" 
          type="button" 
          @click="toggleNavbar"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Collapsible Content -->
        <div class="collapse navbar-collapse" :class="{ show: navbarOpen }">
          
          <!-- Navigation Links (Centered) -->
          <ul class="navbar-nav mx-auto mb-2 mb-lg-0 gap-1">
            <li class="nav-item">
              <a class="nav-link px-3 rounded-pill fw-medium" href="#services">Services</a>
            </li>
            <li class="nav-item">
              <a class="nav-link px-3 rounded-pill fw-medium" href="#departments">Departments</a>
            </li>
            <li class="nav-item">
              <a class="nav-link px-3 rounded-pill fw-medium" href="#how-it-works">How it Works</a>
            </li>
          </ul>

          <!-- Action Buttons -->
          <div class="d-flex align-items-center gap-2 mt-3 mt-lg-0">
            <router-link to="/login" class="btn btn-outline-secondary rounded-pill px-4 fw-medium border-0 btn-sm-block">
              Log In
            </router-link>
            <router-link to="/register" class="btn btn-primary rounded-pill px-4 fw-medium shadow-sm btn-sm-block">
              Book Appointment
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section d-flex align-items-center position-relative">
      <div class="container py-5 mt-3 text-center">
        <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill px-3 py-2 mb-4 fw-normal">
          <i class="bi bi-stars me-1"></i> Simplify Your Healthcare Journey
        </span>
        <h1 class="display-3 fw-bold text-dark mb-4 tracking-tight" style="letter-spacing: -1px;">
          Modern Care,<br class="d-md-none"> Accessible to All.
        </h1>
        <p class="lead text-secondary mb-5 mx-auto" style="max-width: 600px; font-weight: 400;">
          Connect with top specialists, manage appointments, and access your medical history securely—all in one place.
        </p>
        <div class="d-flex justify-content-center gap-3 flex-wrap">
          <router-link to="/register" class="btn btn-primary btn-lg rounded-pill px-5 shadow-sm py-3 fw-bold">
            Get Started
          </router-link>
          <a href="#departments" class="btn btn-light btn-lg rounded-pill px-5 py-3 fw-medium text-dark">
            Find a Doctor
          </a>
        </div>
        
        <!-- Stats Strip -->
        <div class="mt-5 pt-4 d-flex justify-content-center gap-5 text-center flex-wrap opacity-75">
          <div>
            <div class="h3 fw-bold mb-0">50+</div>
            <div class="small text-muted">Specialists</div>
          </div>
          <div class="vr"></div>
          <div>
            <div class="h3 fw-bold mb-0">24/7</div>
            <div class="small text-muted">Support</div>
          </div>
          <div class="vr"></div>
          <div>
            <div class="h3 fw-bold mb-0">10k+</div>
            <div class="small text-muted">Patients</div>
          </div>
        </div>
      </div>
    </header>

    <!-- Services -->
    <section id="services" class="py-5 bg-light-subtle">
      <div class="container py-5">
        <div class="row g-4">
          <!-- Card 1 -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm rounded-4 p-4 hover-up bg-white">
              <div class="icon-square bg-primary bg-opacity-10 text-primary mb-4 rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                <i class="bi bi-calendar-check-fill fs-4"></i>
              </div>
              <h4 class="fw-bold mb-3">Instant Booking</h4>
              <p class="text-muted mb-0">Skip the phone calls. View real-time doctor availability and book your slot in seconds.</p>
            </div>
          </div>
          <!-- Card 2 -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm rounded-4 p-4 hover-up bg-white">
              <div class="icon-square bg-success bg-opacity-10 text-success mb-4 rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                <i class="bi bi-file-earmark-medical-fill fs-4"></i>
              </div>
              <h4 class="fw-bold mb-3">Digital Records</h4>
              <p class="text-muted mb-0">Your medical history, prescriptions, and reports are stored securely and always accessible.</p>
            </div>
          </div>
          <!-- Card 3 -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm rounded-4 p-4 hover-up bg-white">
              <div class="icon-square bg-info bg-opacity-10 text-info mb-4 rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 56px; height: 56px;">
                <i class="bi bi-people-fill fs-4"></i>
              </div>
              <h4 class="fw-bold mb-3">Expert Doctors</h4>
              <p class="text-muted mb-0">Consult with verified specialists across various departments for the best care.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Departments -->
    <section id="departments" class="py-5">
      <div class="container py-5">
        <div class="text-center mb-5">
          <h2 class="fw-bold">Specialized Care</h2>
          <p class="text-muted">Comprehensive departments for every need.</p>
        </div>
        <div class="row g-3">
          <div class="col-6 col-md-3" v-for="dept in ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics']" :key="dept">
            <div class="p-4 border rounded-4 text-center hover-bg-light transition-all cursor-default">
              <div class="fw-semibold text-dark">{{ dept }}</div>
            </div>
          </div>
          <div class="col-6 col-md-3" v-for="dept in ['Dermatology', 'General Medicine', 'Gynecology', 'ENT']" :key="dept">
            <div class="p-4 border rounded-4 text-center hover-bg-light transition-all cursor-default">
              <div class="fw-semibold text-dark">{{ dept }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works (Steps) -->
    <section id="how-it-works" class="py-5 bg-primary bg-opacity-10">
      <div class="container py-5">
        <div class="row align-items-center">
          <div class="col-md-6 mb-4 mb-md-0">
            <h2 class="fw-bold mb-4">Simple steps to <br>better health.</h2>
            <div class="d-flex flex-column gap-4">
              <div class="d-flex align-items-start gap-3">
                <div class="bg-white text-primary fw-bold rounded-circle d-flex align-items-center justify-content-center shadow-sm" style="width: 40px; height: 40px; min-width: 40px;">1</div>
                <div>
                  <h6 class="fw-bold mb-1">Create Account</h6>
                  <p class="text-muted small m-0">Register in less than a minute.</p>
                </div>
              </div>
              <div class="d-flex align-items-start gap-3">
                <div class="bg-white text-primary fw-bold rounded-circle d-flex align-items-center justify-content-center shadow-sm" style="width: 40px; height: 40px; min-width: 40px;">2</div>
                <div>
                  <h6 class="fw-bold mb-1">Select Specialist</h6>
                  <p class="text-muted small m-0">Browse by department and check availability.</p>
                </div>
              </div>
              <div class="d-flex align-items-start gap-3">
                <div class="bg-white text-primary fw-bold rounded-circle d-flex align-items-center justify-content-center shadow-sm" style="width: 40px; height: 40px; min-width: 40px;">3</div>
                <div>
                  <h6 class="fw-bold mb-1">Book & Visit</h6>
                  <p class="text-muted small m-0">Confirm your slot and visit the clinic.</p>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
             <!-- Abstract Visual Placeholder -->
             <div class="bg-white rounded-4 shadow p-4 position-relative">
                <div class="d-flex align-items-center justify-content-between mb-4 border-bottom pb-3">
                   <div>
                      <div class="fw-bold">Dr. Sarah Smith</div>
                      <small class="text-success">● Available Today</small>
                   </div>
                   <button class="btn btn-sm btn-primary rounded-pill px-3">Book</button>
                </div>
                <div class="d-flex gap-2">
                   <div class="bg-light rounded p-2 flex-fill text-center"><small>09:00</small></div>
                   <div class="bg-primary text-white rounded p-2 flex-fill text-center"><small>10:00</small></div>
                   <div class="bg-light rounded p-2 flex-fill text-center"><small>11:00</small></div>
                </div>
             </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-top py-4 mt-auto">
      <div class="container d-flex flex-column flex-md-row justify-content-between align-items-center">
        <p class="text-muted mb-0 small">
          &copy; {{ new Date().getFullYear() }} <span class="fw-bold text-primary">CuraNet</span>. All rights reserved.
        </p>
        <div class="d-flex gap-3 mt-3 mt-md-0">
          <a href="#" class="text-muted text-decoration-none small">Privacy</a>
          <a href="#" class="text-muted text-decoration-none small">Terms</a>
          <a href="#" class="text-muted text-decoration-none small">Support</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "LandingPage",
  data() {
    return {
      navbarOpen: false,
    };
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen;
    },
  },
};
</script>

<style scoped>
/* Navigation Link Styling */
.nav-link {
  color: #6c757d; /* Bootstrap secondary text */
  transition: all 0.2s ease-in-out;
  font-size: 0.95rem;
}

.nav-link:hover {
  color: #0d6efd; /* Primary Blue */
  background-color: rgba(13, 110, 253, 0.08);
}

/* Card Hover Effect */
.hover-up {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.hover-up:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.075)!important;
}

/* Utilities */
.bg-light-subtle {
  background-color: #f9fbfd;
}
.transition-all {
  transition: all 0.2s;
}
.hover-bg-light:hover {
  background-color: #f8f9fa;
  transform: scale(1.02);
}
.cursor-default {
  cursor: default;
}
.btn-sm-block {
  white-space: nowrap;
}
</style>
