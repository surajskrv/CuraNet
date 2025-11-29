<template>
  <div>
    <h2 class="mb-4">All Appointments</h2>
    
    <!-- Filters -->
    <div class="mb-3 d-flex align-items-center gap-2">
      <select class="form-select w-auto shadow-sm" v-model="filterStatus">
        <option value="">All Status</option>
        <option value="Booked">Booked</option>
        <option value="Completed">Completed</option>
        <option value="Cancelled">Cancelled</option>
      </select>
      
      <div class="form-check form-switch ms-3">
        <input class="form-check-input" type="checkbox" id="upcomingSwitch" v-model="showUpcoming">
        <label class="form-check-label" for="upcomingSwitch">Show Upcoming Only</label>
      </div>

      <button class="btn btn-outline-secondary btn-sm ms-auto" @click="loadAppointments">
        <i class="bi bi-arrow-clockwise"></i> Refresh
      </button>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading appointments...</p>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <!-- Appointments Table -->
    <div v-else>
      <div class="table-responsive shadow-sm rounded">
        <table class="table table-hover align-middle mb-0 bg-white">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Date & Time</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredAppointments.length === 0">
              <td colspan="6" class="text-center py-4 text-muted">No appointments found matching your filters.</td>
            </tr>
            <tr v-for="appt in filteredAppointments" :key="appt.id">
              <td>#{{ appt.id }}</td>
              <td>
                <div class="fw-bold">{{ appt.patient_name }}</div>
                <div class="small text-muted">{{ appt.patient_email }}</div>
              </td>
              <td>
                <div class="fw-bold">{{ appt.doctor_name }}</div>
                <div class="small text-muted">{{ appt.doctor_specialization }}</div>
              </td>
              <td>
                <div>{{ formatDate(appt.date) }}</div>
                <div class="small text-muted">{{ appt.time }}</div>
              </td>
              <td>
                <span :class="getStatusBadgeClass(appt.status)">
                  {{ appt.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-info text-white" @click="viewHistory(appt)">
                  <i class="bi bi-clock-history me-1"></i> History
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- History Modal -->
    <div v-if="showHistoryModal" class="modal-backdrop fade show"></div>
    <div class="modal fade" :class="{ 'show d-block': showHistoryModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-xl modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Medical History: <span class="text-primary">{{ selectedPatientName }}</span>
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="historyLoading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
            
            <div v-else-if="patientHistory.length === 0" class="text-center py-4 text-muted">
              No medical history found for this patient.
            </div>

            <div v-else class="table-responsive">
              <table class="table table-bordered table-sm">
                <thead class="table-light">
                  <tr>
                    <th>Date</th>
                    <th>Doctor</th>
                    <th>Reason</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Notes</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="h in patientHistory" :key="h.appointment_id">
                    <td>{{ formatDate(h.date) }} <br><small>{{ h.time }}</small></td>
                    <td>
                      {{ h.doctor_name }}<br>
                      <small class="text-muted">{{ h.doctor_specialization }}</small>
                    </td>
                    <td>{{ h.reason || '-' }}</td>
                    <td>{{ h.diagnosis || '-' }}</td>
                    <td>{{ h.prescription || '-' }}</td>
                    <td>{{ h.notes || '-' }}</td>
                    <td>
                      <span :class="getStatusBadgeClass(h.status)">{{ h.status }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminAppointments',
  data() {
    return {
      appointments: [],
      loading: false,
      error: '',
      
      // Filters
      filterStatus: '',
      showUpcoming: false,
      
      // Modal State
      showHistoryModal: false,
      historyLoading: false,
      patientHistory: [],
      selectedPatientName: ''
    }
  },
  computed: {
    filteredAppointments() {
      let filtered = this.appointments;

      // 1. Status Filter (Dropdown)
      if (this.filterStatus) {
        filtered = filtered.filter(a => a.status === this.filterStatus);
      }

      // 2. Upcoming Filter (Switch)
      if (this.showUpcoming) {
        // Create "Today" at 00:00:00 Local Time
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

        filtered = filtered.filter(a => {
          // Requirement: Show ONLY 'Booked' slots when switch is ON
          if (a.status !== 'Booked') return false;

          if (!a.date) return false;
          
          // Parse YYYY-MM-DD manually to construct Local Date object
          // This prevents UTC offset issues (e.g. "2025-11-30" appearing as "Nov 29 7pm")
          const [year, month, day] = a.date.split('-').map(Number);
          const apptDate = new Date(year, month - 1, day); // Month is 0-indexed in JS
          
          // Compare: Appointment Date must be Today or Future
          return apptDate >= today;
        });
      }

      return filtered;
    }
  },
  mounted() {
    this.loadAppointments();
  },
  methods: {
    // --- LOAD APPOINTMENTS ---
    async loadAppointments() {
      this.loading = true;
      this.error = '';
      try {
        // Fetch all appointments. We filter client-side for better responsiveness
        // unless data set is huge.
        const params = new URLSearchParams();
        if (this.filterStatus) params.append('status', this.filterStatus);
        
        const response = await fetch(`/api/admin/appointments?${params.toString()}`, {
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
          throw new Error(`Server error (${response.status})`);
        }
        
        this.appointments = await response.json();
      } catch (err) {
        console.error(err);
        this.error = err.message || 'Error loading appointments';
      } finally {
        this.loading = false;
      }
    },

    // --- VIEW HISTORY ---
    async viewHistory(appointment) {
      this.selectedPatientName = appointment.patient_name;
      this.showHistoryModal = true;
      this.historyLoading = true;
      this.patientHistory = [];
      
      try {
        const response = await fetch(`/api/admin/patient-history/${appointment.patient_id}`, {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) throw new Error("Failed to fetch history");

        const data = await response.json();
        // Backend returns object { patient: {...}, history: [...] }
        this.patientHistory = data.history || [];
        
      } catch (err) {
        alert('Failed to load history: ' + err.message);
      } finally {
        this.historyLoading = false;
      }
    },

    closeModal() {
      this.showHistoryModal = false;
      this.patientHistory = [];
    },

    // --- HELPERS ---
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      return new Date(dateStr).toLocaleDateString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric'
      });
    },
    
    getStatusBadgeClass(status) {
      const classes = {
        'Booked': 'badge bg-primary',
        'Completed': 'badge bg-success',
        'Cancelled': 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
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