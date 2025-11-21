<template>
  <div>
    <h2 class="mb-4">Doctor Dashboard</h2>
    
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
      <!-- Statistics Cards -->
      <div class="row mb-4">
        <div class="col-md-4 mb-3">
          <div class="card text-white bg-primary shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title opacity-75">Today's Appointments</h5>
              <h2 class="fw-bold">{{ dashboardData.today_appointments || 0 }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card text-white bg-info shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title opacity-75">Week's Appointments</h5>
              <h2 class="fw-bold">{{ dashboardData.week_appointments || 0 }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card text-white bg-success shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title opacity-75">Assigned Patients</h5>
              <h2 class="fw-bold">{{ dashboardData.assigned_patients?.length || 0 }}</h2>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <!-- Upcoming Appointments List (Left Column) -->
        <div class="col-lg-8 mb-4">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h5 class="mb-0 text-primary">Upcoming Schedule</h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light">
                    <tr>
                      <th class="ps-3">Date & Time</th>
                      <th>Patient</th>
                      <th>Reason</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="dashboardData.upcoming_appointments?.length === 0">
                      <td colspan="4" class="text-center py-4 text-muted">No upcoming appointments.</td>
                    </tr>
                    <tr v-for="appt in dashboardData.upcoming_appointments" :key="appt.id">
                      <td class="ps-3">
                        <div class="fw-bold">{{ formatDate(appt.date) }}</div>
                        <div class="small text-muted">{{ appt.time }}</div>
                      </td>
                      <td>
                        <div class="fw-bold">{{ appt.patient_name }}</div>
                        <div class="small text-muted">{{ appt.patient_phone }}</div>
                      </td>
                      <td class="small text-muted">{{ appt.reason || '-' }}</td>
                      <td>
                        <button class="btn btn-sm btn-success me-1" @click="completeAppointment(appt)" title="Complete Treatment">
                          <i class="bi bi-check-lg"></i>
                        </button>
                        <button class="btn btn-sm btn-info text-white" @click="viewPatientHistory(appt)" title="View History">
                          <i class="bi bi-clock-history"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column: My Schedule & Quick Actions -->
        <div class="col-lg-4 mb-4">
          
          <!-- NEW: My Availability Schedule -->
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">My Active Slots</h5>
              <span class="badge bg-light text-dark border">Next 7 Days</span>
            </div>
            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <div v-if="Object.keys(mySchedule).length === 0" class="p-3 text-center text-muted small">
                  No availability set for the coming week.
                </div>
                <div v-for="(slots, date) in mySchedule" :key="date" class="list-group-item">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="fw-bold small">{{ formatDate(date) }}</span>
                    <div class="text-end">
                      <span v-for="slot in slots" :key="slot.start_time" 
                            class="badge me-1" 
                            :class="slot.is_booked ? 'bg-danger' : 'bg-success'">
                        {{ slot.start_time }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body">
              <p class="text-muted small">Manage your working hours for the upcoming week.</p>
              <button class="btn btn-outline-primary w-100 mb-3" @click="openAvailabilityModal">
                <i class="bi bi-calendar-range me-2"></i> Set Availability
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Complete Appointment Modal -->
      <div v-if="showCompleteModal" class="modal-backdrop fade show"></div>
      <div class="modal fade" :class="{ 'show d-block': showCompleteModal }" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Complete Appointment: <span class="text-primary">{{ currentAppointment?.patient_name }}</span></h5>
              <button type="button" class="btn-close" @click="closeCompleteModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveTreatment">
                <div class="mb-3">
                  <label class="form-label">Diagnosis *</label>
                  <textarea class="form-control" v-model="treatmentForm.diagnosis" rows="2" required placeholder="Primary diagnosis..."></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Prescription</label>
                  <textarea class="form-control" v-model="treatmentForm.prescription" rows="3" placeholder="Rx..."></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Additional Notes</label>
                  <textarea class="form-control" v-model="treatmentForm.notes" rows="2" placeholder="Advice, follow-up notes..."></textarea>
                </div>
                <div class="d-flex justify-content-end gap-2">
                  <button type="button" class="btn btn-secondary" @click="closeCompleteModal">Cancel</button>
                  <button type="submit" class="btn btn-primary" :disabled="submitting">
                    <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                    Save & Complete
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Availability Modal -->
      <div v-if="showAvailabilityModal" class="modal-backdrop fade show"></div>
      <div class="modal fade" :class="{ 'show d-block': showAvailabilityModal }" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Set Availability</h5>
              <button type="button" class="btn-close" @click="showAvailabilityModal = false"></button>
            </div>
            <div class="modal-body">
              <p class="alert alert-info small">
                <i class="bi bi-info-circle me-2"></i>
                Checking a box marks you as <strong>available</strong> for that slot.
              </p>
              <div v-for="day in availabilityDays" :key="day.date" class="card mb-2 border-light bg-light">
                <div class="card-body py-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <strong style="min-width: 120px;">{{ formatDate(day.date) }}</strong>
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" :id="'m-'+day.date" v-model="day.morning">
                      <label class="form-check-label" :for="'m-'+day.date">Morning (08:00 - 12:00)</label>
                    </div>
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" :id="'e-'+day.date" v-model="day.evening">
                      <label class="form-check-label" :for="'e-'+day.date">Evening (16:00 - 21:00)</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showAvailabilityModal = false">Cancel</button>
              <button class="btn btn-primary" @click="saveAvailability" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                Save Schedule
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Patient History Modal -->
      <div v-if="showHistoryModal" class="modal-backdrop fade show" style="z-index: 1060;"></div>
      <div class="modal fade" :class="{ 'show d-block': showHistoryModal }" tabindex="-1" style="z-index: 1070;">
        <div class="modal-dialog modal-xl modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Medical History: <span class="text-primary">{{ historyPatientName }}</span></h5>
              <button type="button" class="btn-close" @click="showHistoryModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="historyLoading" class="text-center py-4">
                <div class="spinner-border text-primary"></div>
              </div>
              <div v-else-if="patientHistory.length === 0" class="text-center py-4 text-muted">
                No previous medical history found.
              </div>
              <div v-else class="table-responsive">
                <table class="table table-bordered table-striped">
                  <thead class="table-light">
                    <tr>
                      <th>Date</th>
                      <th>Diagnosis</th>
                      <th>Prescription</th>
                      <th>Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="record in patientHistory" :key="record.appointment_id">
                      <td style="min-width: 100px;">{{ formatDate(record.date) }}</td>
                      <td>{{ record.diagnosis || '-' }}</td>
                      <td>{{ record.prescription || '-' }}</td>
                      <td>{{ record.notes || '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showHistoryModal = false">Close</button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorDashboard',
  data() {
    return {
      dashboardData: {
        today_appointments: 0,
        week_appointments: 0,
        upcoming_appointments: [],
        assigned_patients: []
      },
      mySchedule: {}, // New: Stores availability data for display
      loading: true,
      error: '',
      submitting: false,
      
      // Complete Modal
      showCompleteModal: false,
      currentAppointment: null,
      treatmentForm: {
        diagnosis: '',
        prescription: '',
        notes: ''
      },
      
      // Availability Modal
      showAvailabilityModal: false,
      availabilityDays: [],

      // History Modal
      showHistoryModal: false,
      historyLoading: false,
      patientHistory: [],
      historyPatientName: ''
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    // --- INIT ---
    async initData() {
        this.loading = true;
        await Promise.all([this.loadDashboard(), this.loadMySchedule()]);
        this.loading = false;
    },
    // --- LOAD DASHBOARD ---
    async loadDashboard() {
      try {
        const response = await fetch('/api/doctor/dashboard', {
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
        this.error = err.message || 'Failed to load dashboard';
      }
    },

    // --- LOAD MY SCHEDULE (Availability) ---
    async loadMySchedule() {
      try {
        const response = await fetch('/api/doctor/availability?days=7', {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });
        
        if (response.ok) {
          this.mySchedule = await response.json();
        }
      } catch (err) {
        console.error("Failed to load schedule", err);
      }
    },

    // --- COMPLETE APPOINTMENT ---
    completeAppointment(appointment) {
      this.currentAppointment = appointment;
      this.treatmentForm = { diagnosis: '', prescription: '', notes: '' };
      this.showCompleteModal = true;
    },

    async saveTreatment() {
      this.submitting = true;
      try {
        const payload = {
          appointment_id: this.currentAppointment.id,
          ...this.treatmentForm
        };

        const response = await fetch('/api/doctor/treatment', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || "Failed to save treatment");
        }

        alert('Treatment saved successfully! Appointment marked as completed.');
        this.closeCompleteModal();
        this.initData(); // Refresh lists
        
      } catch (err) {
        alert(err.message);
      } finally {
        this.submitting = false;
      }
    },

    closeCompleteModal() {
      this.showCompleteModal = false;
      this.currentAppointment = null;
    },

    // --- VIEW HISTORY ---
    async viewPatientHistory(appointment) {
      this.historyPatientName = appointment.patient_name;
      this.showHistoryModal = true;
      this.historyLoading = true;
      this.patientHistory = [];

      try {
        const response = await fetch(`/api/doctor/patient-history/${appointment.patient_id}`, {
          method: 'GET',
          headers: this.getHeaders()
        });

        if (!response.ok) throw new Error("Failed to load history");

        const data = await response.json();
        this.patientHistory = data.history || [];
      } catch (err) {
        alert(err.message);
      } finally {
        this.historyLoading = false;
      }
    },

    // --- AVAILABILITY LOGIC ---
    openAvailabilityModal() {
      this.initAvailabilityDays();
      this.showAvailabilityModal = true;
    },

    initAvailabilityDays() {
      const today = new Date();
      this.availabilityDays = [];
      // Create slots for the next 7 days
      for (let i = 1; i <= 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        this.availabilityDays.push({
          date: date.toISOString().split('T')[0], // YYYY-MM-DD
          morning: false,
          evening: false
        });
      }
    },

    async saveAvailability() {
      this.submitting = true;
      const slots = [];
      
      this.availabilityDays.forEach(day => {
        if (day.morning) {
          slots.push({ date: day.date, start_time: '08:00', end_time: '12:00' });
        }
        if (day.evening) {
          slots.push({ date: day.date, start_time: '16:00', end_time: '21:00' });
        }
      });
      
      try {
        const response = await fetch('/api/doctor/availability', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify({ availabilities: slots })
        });

        if (!response.ok) throw new Error("Failed to save availability");

        alert('Availability schedule updated successfully!');
        this.showAvailabilityModal = false;
        this.loadMySchedule(); // Refresh the display
      } catch (err) {
        alert(err.message);
      } finally {
        this.submitting = false;
      }
    },

    // --- UTILS ---
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      return new Date(dateStr).toLocaleDateString(undefined, {
        weekday: 'short', month: 'short', day: 'numeric'
      });
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  opacity: 0.5;
  background-color: #000;
}
</style>