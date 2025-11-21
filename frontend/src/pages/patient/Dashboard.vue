<template>
  <div>
    <h2 class="mb-4">Patient Dashboard</h2>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading dashboard...</p>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <div v-else>
      <!-- Upcoming Appointments -->
      <div class="card mb-4 shadow-sm">
        <div class="card-header bg-white">
          <h5 class="mb-0 text-primary">Upcoming Appointments</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover align-middle" v-if="dashboardData.upcoming_appointments?.length > 0">
              <thead class="table-light">
                <tr>
                  <th>Date & Time</th>
                  <th>Doctor</th>
                  <th>Department</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="appt in dashboardData.upcoming_appointments" :key="appt.id">
                  <td>
                    <div class="fw-bold">{{ formatDate(appt.date) }}</div>
                    <div class="small text-muted">{{ appt.time }}</div>
                  </td>
                  <td>
                    <div class="fw-bold">{{ appt.doctor_name }}</div>
                    <div class="small text-muted">{{ appt.doctor_specialization }}</div>
                  </td>
                  <td>{{ getDepartmentName(appt.doctor_specialization) }}</td> <!-- Helper if needed, or just doctor_specialization -->
                  <td>
                    <span class="badge bg-primary">{{ appt.status }}</span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-outline-danger" @click="cancelAppointment(appt.id)">
                      <i class="bi bi-x-circle"></i> Cancel
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <p v-else class="text-center text-muted py-3">No upcoming appointments scheduled.</p>
          </div>
        </div>
      </div>
      
      <!-- Departments Grid -->
      <div class="card mb-4 shadow-sm">
        <div class="card-header bg-white">
          <h5 class="mb-0 text-success">Book an Appointment</h5>
          <small class="text-muted">Select a department to find a doctor</small>
        </div>
        <div class="card-body">
          <div class="row">
            <!-- Backend returns 'departments' key -->
            <div v-for="dept in dashboardData.departments" :key="dept.id" class="col-md-4 mb-3">
              <div class="card h-100 hover-card">
                <div class="card-body text-center">
                  <h5 class="card-title">{{ dept.name }}</h5>
                  <p class="text-muted small">{{ dept.description || 'No description available' }}</p>
                  <button class="btn btn-outline-primary stretched-link" @click="viewDoctors(dept)">
                    View Doctors
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Doctors List Modal -->
      <div v-if="showDoctorsModal" class="modal-backdrop fade show"></div>
      <div class="modal fade" :class="{ 'show d-block': showDoctorsModal }" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Doctors in {{ selectedDepartment?.name }}</h5>
              <button type="button" class="btn-close" @click="showDoctorsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="doctorsLoading" class="text-center py-4">
                <div class="spinner-border text-primary"></div>
              </div>
              <div v-else-if="doctorsList.length === 0" class="text-center py-4 text-muted">
                No doctors found in this department.
              </div>
              <div v-else>
                <div v-for="doctor in doctorsList" :key="doctor.id" class="card mb-3 border-0 shadow-sm">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                      <div>
                        <h5 class="mb-1">{{ doctor.name }}</h5>
                        <p class="text-muted mb-1 small">{{ doctor.qualification }} - {{ doctor.specialization }}</p>
                        <p class="mb-2 small">{{ doctor.bio || 'No bio available' }}</p>
                        <div class="badge bg-light text-dark border">Experience: {{ doctor.experience || 0 }} years</div>
                      </div>
                      <button class="btn btn-primary" @click="viewDoctorAvailability(doctor)">
                        Book Visit
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Booking Slot Modal -->
      <div v-if="showBookingModal" class="modal-backdrop fade show" style="z-index: 1055;"></div>
      <div class="modal fade" :class="{ 'show d-block': showBookingModal }" tabindex="-1" style="z-index: 1060;">
        <div class="modal-dialog modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Book with {{ selectedDoctor?.name }}</h5>
              <button type="button" class="btn-close" @click="showBookingModal = false"></button>
            </div>
            <div class="modal-body">
              <h6 class="text-muted mb-3">Available Slots (Next 7 Days)</h6>
              
              <div v-if="availableSlots.length === 0" class="alert alert-warning">
                No available slots found for this doctor.
              </div>

              <div class="row g-2 mb-4">
                <div v-for="(slot, index) in availableSlots" :key="index" class="col-6">
                  <button
                    class="btn w-100"
                    :class="isSlotSelected(slot) ? 'btn-primary' : 'btn-outline-secondary'"
                    @click="selectSlot(slot)"
                  >
                    <div class="small fw-bold">{{ formatDate(slot.date) }}</div>
                    <div>{{ slot.time }}</div>
                  </button>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Reason for Visit</label>
                <textarea 
                  class="form-control" 
                  v-model="bookingForm.reason" 
                  rows="3"
                  placeholder="Briefly describe your symptoms..."
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showBookingModal = false">Cancel</button>
              <button class="btn btn-success" @click="bookAppointment" :disabled="!selectedSlot || submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                Confirm Booking
              </button>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientDashboard',
  data() {
    return {
      dashboardData: {
        departments: [],
        upcoming_appointments: []
      },
      loading: true,
      error: '',
      submitting: false,
      
      // Doctors List Logic
      showDoctorsModal: false,
      doctorsLoading: false,
      doctorsList: [],
      selectedDepartment: null,

      // Booking Logic
      showBookingModal: false,
      selectedDoctor: null,
      availableSlots: [], // Flattened list of slots
      selectedSlot: null,
      bookingForm: {
        reason: ''
      }
    }
  },
  mounted() {
    this.loadDashboard()
  },
  methods: {
    // --- LOAD DASHBOARD ---
    async loadDashboard() {
      this.loading = true;
      this.error = '';
      try {
        const response = await fetch('/api/patient/dashboard', {
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

        this.dashboardData = await response.json();
      } catch (err) {
        console.error(err);
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    // --- VIEW DOCTORS ---
    async viewDoctors(department) {
      this.selectedDepartment = department;
      this.showDoctorsModal = true;
      this.doctorsLoading = true;
      this.doctorsList = [];
      
      try {
        // Backend search filters by department_id
        const response = await fetch(`/api/patient/doctors?department_id=${department.id}`, {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) throw new Error("Failed to load doctors");
        
        this.doctorsList = await response.json();
      } catch (err) {
        alert(err.message);
      } finally {
        this.doctorsLoading = false;
      }
    },

    // --- AVAILABILITY LOGIC ---
    viewDoctorAvailability(doctor) {
      this.selectedDoctor = doctor;
      this.showDoctorsModal = false; // Close list modal
      this.showBookingModal = true; // Open booking modal
      this.bookingForm.reason = '';
      this.selectedSlot = null;
      
      // Backend returns availability as a Dict: { '2023-10-10': [{start_time: '10:00', ...}] }
      // We need to flatten this into a simple array for the UI
      this.availableSlots = [];
      
      if (doctor.availability) {
        for (const [dateStr, slots] of Object.entries(doctor.availability)) {
          slots.forEach(slot => {
            this.availableSlots.push({
              date: dateStr,
              time: slot.start_time // Using start_time as the slot identifier
            });
          });
        }
      }
      // Sort slots by date/time
      this.availableSlots.sort((a, b) => new Date(a.date + 'T' + a.time) - new Date(b.date + 'T' + b.time));
    },

    selectSlot(slot) {
      this.selectedSlot = slot;
    },
    
    isSlotSelected(slot) {
      return this.selectedSlot && this.selectedSlot.date === slot.date && this.selectedSlot.time === slot.time;
    },

    // --- BOOK APPOINTMENT ---
    async bookAppointment() {
      if (!this.selectedSlot) return;
      
      this.submitting = true;
      try {
        const payload = {
          doctor_id: this.selectedDoctor.id,
          date: this.selectedSlot.date, // Backend expects 'date'
          time: this.selectedSlot.time, // Backend expects 'time'
          reason: this.bookingForm.reason
        };

        const response = await fetch('/api/patient/appointments', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.message || "Booking failed");

        alert("Appointment booked successfully!");
        this.showBookingModal = false;
        this.loadDashboard(); // Refresh upcoming appointments
        
      } catch (err) {
        alert(err.message);
      } finally {
        this.submitting = false;
      }
    },

    // --- CANCEL APPOINTMENT ---
    async cancelAppointment(appointmentId) {
      if (!confirm('Are you sure you want to cancel this appointment?')) return;

      try {
        const response = await fetch(`/api/patient/appointments/${appointmentId}`, {
          method: 'DELETE',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });
        
        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || "Cancellation failed");
        }

        alert("Appointment cancelled.");
        this.loadDashboard();
      } catch (err) {
        alert(err.message);
      }
    },

    // --- HELPERS ---
    formatDate(dateStr) {
      if (!dateStr) return '';
      const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },
    
    getDepartmentName(specialization) {
        // This is just a fallback if department name isn't directly on the appointment object
        return specialization || 'General'; 
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  opacity: 0.5;
  background-color: #000;
}
.hover-card {
  transition: transform 0.2s;
}
.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
}
</style>