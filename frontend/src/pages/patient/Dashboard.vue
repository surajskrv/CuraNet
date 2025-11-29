<template>
  <div>
    <h2 class="mb-4">Patient Dashboard</h2>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading dashboard...</p>
    </div>

    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <div v-else>
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
                  <td>{{ getDepartmentName(appt.doctor_specialization) }}</td>
                  <td>
                    <span class="badge bg-primary">{{ appt.status }}</span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-outline-primary me-1" @click="initiateReschedule(appt)">
                      <i class="bi bi-calendar-event"></i> Reschedule
                    </button>
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
      
      <div class="card mb-4 shadow-sm">
        <div class="card-header bg-white">
          <h5 class="mb-0 text-success">Book an Appointment</h5>
          <small class="text-muted">Select a department to find a doctor</small>
        </div>
        <div class="card-body">
          <div class="row">
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
                      <button class="btn btn-primary" @click="initiateBooking(doctor)">
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

      <div v-if="showBookingModal" class="modal-backdrop fade show" style="z-index: 1055;"></div>
      <div class="modal fade" :class="{ 'show d-block': showBookingModal }" tabindex="-1" style="z-index: 1060;">
        <div class="modal-dialog modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                {{ isRescheduling ? 'Reschedule Appointment' : 'Book Appointment' }}
              </h5>
              <button type="button" class="btn-close" @click="closeBookingModal"></button>
            </div>
            <div class="modal-body">
              <p class="text-muted mb-3">
                Doctor: <strong>{{ selectedDoctor?.name }}</strong>
              </p>

              <h6 class="text-primary mb-2">Select a Slot</h6>
              <div v-if="availableSlots.length === 0" class="alert alert-warning small">
                No available slots found for the next 7 days.
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

              <form ref="bookingFormRef" class="needs-validation" novalidate @submit.prevent>
                <div class="mb-3">
                  <label class="form-label">Reason for Visit <span class="text-danger">*</span></label>
                  <textarea 
                    class="form-control" 
                    :class="{'is-invalid': formErrors.reason}"
                    v-model="bookingForm.reason" 
                    rows="3"
                    placeholder="Briefly describe your symptoms..."
                    required
                    minlength="3"
                  ></textarea>
                  <div class="invalid-feedback">
                    {{ formErrors.reason || 'Please provide a reason (min 3 chars).' }}
                  </div>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeBookingModal">Cancel</button>
              
              <button 
                class="btn" 
                :class="isRescheduling ? 'btn-warning' : 'btn-success'"
                @click="confirmAction" 
                :disabled="!selectedSlot || submitting"
              >
                <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                {{ isRescheduling ? 'Confirm Reschedule' : 'Confirm Booking' }}
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

      // Booking / Reschedule Logic
      showBookingModal: false,
      selectedDoctor: null,
      availableSlots: [], 
      selectedSlot: null,
      
      isRescheduling: false, // Flag to toggle mode
      rescheduleApptId: null, // ID of appointment being rescheduled

      bookingForm: {
        reason: ''
      },
      formErrors: {}
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

    // --- SETUP BOOKING (NEW) ---
    initiateBooking(doctor) {
      this.isRescheduling = false;
      this.rescheduleApptId = null;
      this.bookingForm.reason = ''; // Clear reason
      this.prepareModal(doctor);
    },

    // --- SETUP RESCHEDULE (EXISTING) ---
    async initiateReschedule(appt) {
      this.isRescheduling = true;
      this.rescheduleApptId = appt.id;
      this.bookingForm.reason = appt.reason || ''; // Pre-fill reason
      
      // Need to fetch doctor details/availability to show in modal
      // We can construct a temp doctor object or fetch it. 
      // For simplicity, we'll fetch the doctor list for this specialization logic or 
      // just hit the specific doctor endpoint if available. 
      // Since we don't have a single doctor fetch endpoint in the list, 
      // we can try searching or assume we have to re-fetch availability.
      
      // Quick fix: Fetch specific doctor by ID to get availability
      // Assuming GET /api/patient/doctors returns list, we filter? 
      // Better: Backend `search_doctors` returns availability. 
      // Let's call search with name to narrow it down.
      
      this.submitting = true; // Show loading briefly
      try {
        const response = await fetch(`/api/patient/doctors?name=${encodeURIComponent(appt.doctor_name)}`, {
           headers: { "Auth-Token": localStorage.getItem("auth_token") }
        });
        const docs = await response.json();
        const doctor = docs.find(d => d.id === appt.doctor_id);
        
        if (doctor) {
          this.prepareModal(doctor);
        } else {
          alert("Doctor details not found.");
        }
      } catch(e) {
        alert("Error loading doctor schedule");
      } finally {
        this.submitting = false;
      }
    },

    prepareModal(doctor) {
      this.selectedDoctor = doctor;
      this.showDoctorsModal = false;
      this.showBookingModal = true;
      this.selectedSlot = null;
      this.formErrors = {};

      // Flatten availability
      this.availableSlots = [];
      if (doctor.availability) {
        for (const [dateStr, slots] of Object.entries(doctor.availability)) {
          slots.forEach(slot => {
            this.availableSlots.push({
              date: dateStr,
              time: slot.start_time
            });
          });
        }
      }
      this.availableSlots.sort((a, b) => new Date(a.date + 'T' + a.time) - new Date(b.date + 'T' + b.time));
    },

    selectSlot(slot) {
      this.selectedSlot = slot;
    },
    
    isSlotSelected(slot) {
      return this.selectedSlot && this.selectedSlot.date === slot.date && this.selectedSlot.time === slot.time;
    },

    closeBookingModal() {
      this.showBookingModal = false;
      this.bookingForm.reason = '';
      this.formErrors = {};
    },

    // --- CONFIRM ACTION (BOOK or RESCHEDULE) ---
    async confirmAction() {
      // Frontend Validation
      this.formErrors = {};
      if (!this.bookingForm.reason || this.bookingForm.reason.length < 3) {
        this.formErrors.reason = "Reason is required (min 3 chars).";
        return;
      }
      if (!this.selectedSlot) {
        alert("Please select a time slot.");
        return;
      }

      this.submitting = true;
      try {
        let url, method, payload;

        if (this.isRescheduling) {
          // UPDATE (PUT)
          url = `/api/patient/appointments/${this.rescheduleApptId}`;
          method = 'PUT';
          payload = {
            date: this.selectedSlot.date,
            time: this.selectedSlot.time
            // Note: Current backend PUT mainly updates time/date. 
            // If you want to update reason too, update backend `update_cancel_appointment` logic.
          };
        } else {
          // CREATE (POST)
          url = '/api/patient/appointments';
          method = 'POST';
          payload = {
            doctor_id: this.selectedDoctor.id,
            date: this.selectedSlot.date,
            time: this.selectedSlot.time,
            reason: this.bookingForm.reason
          };
        }

        const response = await fetch(url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.message || "Action failed");

        alert(this.isRescheduling ? "Appointment rescheduled!" : "Appointment booked successfully!");
        this.closeBookingModal();
        this.loadDashboard();
        
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