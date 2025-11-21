<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold" href="#">
          CityCare Hospital
        </a>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto align-items-lg-center">
            <li class="nav-item">
              <a class="nav-link active" href="#services">Services</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#departments">Departments</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#how-it-works">How it works</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#contact">Contact</a>
            </li>
            <li class="nav-item ms-lg-3 mt-2 mt-lg-0">
              <router-link class="btn btn-outline-primary btn-sm" to="/login">
                Login
              </router-link>
            </li>
            <li class="nav-item ms-2 mt-2 mt-lg-0">
              <router-link class="btn btn-primary btn-sm" to="/register">
                Book Appointment
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section d-flex align-items-center">
      <div class="container py-5">
        <div class="row align-items-center">
          <div class="col-md-6 mb-4 mb-md-0">
            <h1 class="display-5 fw-bold text-white mb-3">
              Your health, our priority.
            </h1>
            <p class="lead text-white-50 mb-4">
              Book appointments, consult with experienced doctors, and access your
              medical records securely from anywhere.
            </p>
            <div class="d-flex flex-wrap gap-2">
              <router-link class="btn btn-light btn-lg fw-semibold" to="/register">
                Book an Appointment
              </router-link>
              <router-link class="btn btn-outline-light btn-lg" to="/login">
                Login
              </router-link>
            </div>
            <p class="small text-white-50 mt-3 mb-0">
              24/7 support • Trusted doctors • Secure online access
            </p>
          </div>

          <div class="col-md-6">
            <div class="card shadow-lg border-0 hero-card">
              <div class="card-body">
                <h5 class="card-title mb-3">Quick Appointment Overview</h5>
                <p class="text-muted small">
                  Log in to view your upcoming visits, prescriptions, and medical history.
                </p>
                <div class="row text-center mb-3">
                  <div class="col-4">
                    <div class="fw-bold fs-5">24/7</div>
                    <div class="text-muted small">Emergency Care</div>
                  </div>
                  <div class="col-4">
                    <div class="fw-bold fs-5">50+</div>
                    <div class="text-muted small">Specialists</div>
                  </div>
                  <div class="col-4">
                    <div class="fw-bold fs-5">30k+</div>
                    <div class="text-muted small">Patients Served</div>
                  </div>
                </div>
                <div class="d-grid gap-2">
                  <router-link class="btn btn-primary" to="/register">
                    Register
                  </router-link>
                </div>
                <p class="small text-muted mt-3 mb-0">
                  Exiting User? <router-link to="/login">Login</router-link> to get started.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Services / Highlights -->
    <main class="flex-grow-1">
      <section id="services" class="py-5">
        <div class="container">
          <h2 class="text-center mb-4">Why choose CityCare Hospital?</h2>
          <p class="text-center text-muted mb-5">
            A smarter way to manage your healthcare – from booking appointments to tracking your treatments.
          </p>
          <div class="row g-4">
            <div class="col-md-4">
              <div class="card h-100 shadow-sm border-0">
                <div class="card-body">
                  <h5 class="card-title mb-3">Online Appointment Booking</h5>
                  <p class="card-text text-muted">
                    Book, reschedule or cancel your visits at your convenience, all from a single portal.
                  </p>
                  <ul class="small text-muted mb-0">
                    <li>Real-time doctor availability</li>
                    <li>Instant booking confirmation</li>
                    <li>Appointment reminders</li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card h-100 shadow-sm border-0">
                <div class="card-body">
                  <h5 class="card-title mb-3">Specialist Doctors</h5>
                  <p class="card-text text-muted">
                    Consult with experienced doctors across multiple specialties under one roof.
                  </p>
                  <ul class="small text-muted mb-0">
                    <li>Verified, qualified professionals</li>
                    <li>Dedicated patient care</li>
                    <li>Personalized treatment plans</li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card h-100 shadow-sm border-0">
                <div class="card-body">
                  <h5 class="card-title mb-3">Secure Medical Records</h5>
                  <p class="card-text text-muted">
                    Access your diagnoses, prescriptions, and visit history anytime in a secure environment.
                  </p>
                  <ul class="small text-muted mb-0">
                    <li>View past appointments</li>
                    <li>Download prescriptions</li>
                    <li>Track ongoing treatments</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Departments -->
      <section id="departments" class="py-5 bg-white">
        <div class="container">
          <h2 class="text-center mb-4">Our Departments</h2>
          <p class="text-center text-muted mb-5">
            Comprehensive care for you and your family across a wide range of specialties.
          </p>
          <div class="row g-4">
            <div class="col-6 col-md-3">
              <div class="p-3 border rounded-3 h-100 text-center">
                <div class="fw-semibold">Cardiology</div>
                <div class="small text-muted">Heart & vascular care</div>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="p-3 border rounded-3 h-100 text-center">
                <div class="fw-semibold">Orthopedics</div>
                <div class="small text-muted">Bones & joints</div>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="p-3 border rounded-3 h-100 text-center">
                <div class="fw-semibold">Pediatrics</div>
                <div class="small text-muted">Child health</div>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="p-3 border rounded-3 h-100 text-center">
                <div class="fw-semibold">General Medicine</div>
                <div class="small text-muted">Primary care</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- How it works -->
      <section id="how-it-works" class="py-5">
        <div class="container">
          <h2 class="text-center mb-4">How it works</h2>
          <div class="row justify-content-center">
            <div class="col-md-10">
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="text-center">
                    <div class="step-circle mb-3">1</div>
                    <h5>Create your account</h5>
                    <p class="text-muted small mb-0">
                      Register as a patient with your basic details and contact information.
                    </p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="text-center">
                    <div class="step-circle mb-3">2</div>
                    <h5>Choose a doctor & time</h5>
                    <p class="text-muted small mb-0">
                      Select your preferred department, doctor, and available time slot.
                    </p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="text-center">
                    <div class="step-circle mb-3">3</div>
                    <h5>Visit & view your records</h5>
                    <p class="text-muted small mb-0">
                      Meet your doctor at the scheduled time and access your treatment details later.
                    </p>
                  </div>
                </div>
              </div>
              <div class="text-center mt-4">
                <router-link class="btn btn-primary btn-lg" to="/register">
                  Get started as a patient
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Testimonials -->
      <section class="py-5 bg-white">
        <div class="container">
          <h2 class="text-center mb-4">What our patients say</h2>
          <div class="row g-4">
            <div class="col-md-4">
              <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                  <p class="text-muted">
                    “Booking an appointment is so simple now. I can see my previous prescriptions anytime.”
                  </p>
                  <div class="fw-semibold mb-0">Anita Sharma</div>
                  <div class="small text-muted">Patient</div>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                  <p class="text-muted">
                    “The system helps me manage my appointments and patient history efficiently each day.”
                  </p>
                  <div class="fw-semibold mb-0">Dr. Rohan Mehta</div>
                  <div class="small text-muted">Consultant Physician</div>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                  <p class="text-muted">
                    “No more long waiting times or confusion about timings. Everything is organized.”
                  </p>
                  <div class="fw-semibold mb-0">Vikram Singh</div>
                  <div class="small text-muted">Patient</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Contact / CTA -->
      <section id="contact" class="py-5">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-md-7 mb-4 mb-md-0">
              <h2 class="mb-3">Need help with an appointment?</h2>
              <p class="text-muted mb-2">
                Our support team is available to assist you with any queries related to bookings or your online account.
              </p>
              <p class="mb-1">
                <strong>Emergency:</strong> +91-98765-43210 (24/7)
              </p>
              <p class="mb-0">
                <strong>Email:</strong> support@citycarehospital.com
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-top py-3 mt-auto">
      <div class="container d-flex flex-column flex-md-row justify-content-between align-items-center">
        <span class="small text-muted">
          © {{ new Date().getFullYear() }} CityCare Hospital. All rights reserved.
        </span>
      </div>
    </footer>
  </div>
</template>

<script setup>
// purely presentational component, no script logic required for now
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #0d6efd, #20c997);
}

.hero-card {
  border-radius: 1.25rem;
}

.hospital-logo-circle {
  display: inline-block;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 2px solid #0d6efd;
  position: relative;
}

.hospital-logo-circle::before,
.hospital-logo-circle::after {
  content: "";
  position: absolute;
  background-color: #0d6efd;
}

.hospital-logo-circle::before {
  width: 60%;
  height: 2px;
  top: 50%;
  left: 20%;
  transform: translateY(-50%);
}

.hospital-logo-circle::after {
  width: 2px;
  height: 60%;
  left: 50%;
  top: 20%;
  transform: translateX(-50%);
}

.step-circle {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid #0d6efd;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #0d6efd;
}
</style>
