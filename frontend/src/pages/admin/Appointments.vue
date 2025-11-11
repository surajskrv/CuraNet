<template>
  <div>
    <h2 class="mb-4">All Appointments</h2>
    
    <div class="mb-3">
      <select class="form-select d-inline-block" style="width: auto;" v-model="filterStatus" @change="loadAppointments">
        <option value="">All Status</option>
        <option value="Booked">Booked</option>
        <option value="Completed">Completed</option>
        <option value="Cancelled">Cancelled</option>
      </select>
      <button class="btn btn-sm btn-primary ms-2" @click="showUpcoming = !showUpcoming; loadAppointments()">
        {{ showUpcoming ? 'Show All' : 'Show Upcoming Only' }}
      </button>
    </div>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Patient Name</th>
            <th>Doctor Name</th>
            <th>Department</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appt in appointments" :key="appt.id">
            <td>{{ appt.id }}</td>
            <td>{{ appt.patient_name }}</td>
            <td>{{ appt.doctor_name }}</td>
            <td>{{ appt.specialization || 'N/A' }}</td>
            <td>{{ formatDate(appt.scheduled_date) }}</td>
            <td>{{ appt.scheduled_time }}</td>
            <td>
              <span :class="getStatusBadgeClass(appt.status)">
                {{ appt.status }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-info" @click="viewHistory(appt)">View History</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- History Modal -->
    <div class="modal" :class="{ show: showHistoryModal }" :style="{ display: showHistoryModal ? 'block' : 'none' }" v-if="showHistoryModal" @click.self="showHistoryModal = false">
      <div class="modal-dialog modal-lg" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Patient History</h5>
            <button type="button" class="btn-close" @click="showHistoryModal = false"></button>
          </div>
          <div class="modal-body">
            <div v-if="historyLoading">Loading...</div>
            <div v-else>
              <table class="table">
                <thead>
                  <tr>
                    <th>Visit No.</th>
                    <th>Date</th>
                    <th>Visit Type</th>
                    <th>Tests Done</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Medicines</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(h, idx) in patientHistory" :key="h.id">
                    <td>{{ idx + 1 }}</td>
                    <td>{{ formatDate(h.scheduled_date) }}</td>
                    <td>{{ h.treatment?.visit_type || 'N/A' }}</td>
                    <td>{{ h.treatment?.tests_done || 'N/A' }}</td>
                    <td>{{ h.treatment?.diagnosis || 'N/A' }}</td>
                    <td>{{ h.treatment?.prescription || 'N/A' }}</td>
                    <td>{{ h.treatment?.medicines || 'N/A' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI } from '@/services/api'

export default {
  name: 'AdminAppointments',
  data() {
    return {
      appointments: [],
      loading: false,
      filterStatus: '',
      showUpcoming: false,
      showHistoryModal: false,
      patientHistory: [],
      historyLoading: false
    }
  },
  mounted() {
    this.loadAppointments()
  },
  methods: {
    async loadAppointments() {
      this.loading = true
      try {
        this.appointments = await adminAPI.getAppointments(
          this.filterStatus,
          this.showUpcoming
        )
      } catch (error) {
        alert('Failed to load appointments: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async viewHistory(appointment) {
      this.showHistoryModal = true
      this.historyLoading = true
      try {
        this.patientHistory = await adminAPI.getPatientHistory(appointment.id)
      } catch (error) {
        alert('Failed to load history: ' + error.message)
      } finally {
        this.historyLoading = false
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A'
      return new Date(dateStr).toLocaleDateString()
    },
    getStatusBadgeClass(status) {
      const classes = {
        'Booked': 'badge bg-primary',
        'Completed': 'badge bg-success',
        'Cancelled': 'badge bg-danger'
      }
      return classes[status] || 'badge bg-secondary'
    }
  }
}
</script>

<style scoped>
.modal.show {
  display: block !important;
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1050;
}
.modal-dialog {
  margin: 1.75rem auto;
  position: relative;
  z-index: 1051;
}
</style>

