<template>
  <div>
    <h2 class="mb-4">Doctor Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Today's Appointments</h5>
              <h3>{{ dashboardData.today_appointments?.length || 0 }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Week's Appointments</h5>
              <h3>{{ dashboardData.week_appointments?.length || 0 }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Assigned Patients</h5>
              <h3>{{ dashboardData.assigned_patients_count || 0 }}</h3>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">
              <h5>Today's Appointments</h5>
            </div>
            <div class="card-body">
              <div v-if="dashboardData.today_appointments?.length === 0">
                <p class="text-muted">No appointments today</p>
              </div>
              <table v-else class="table table-sm">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Patient</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="appt in dashboardData.today_appointments" :key="appt.id">
                    <td>{{ appt.scheduled_time }}</td>
                    <td>{{ appt.patient_name }}</td>
                    <td>
                      <button class="btn btn-sm btn-success" @click="completeAppointment(appt)">Complete</button>
                      <button class="btn btn-sm btn-warning" @click="viewPatientHistory(appt)">History</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">
              <h5>Set Availability</h5>
            </div>
            <div class="card-body">
              <button class="btn btn-primary" @click="showAvailabilityModal = true">Provide Availability (Next 7 Days)</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Complete Appointment Modal -->
      <div class="modal" :class="{ show: showCompleteModal }" :style="{ display: showCompleteModal ? 'block' : 'none' }" v-if="showCompleteModal" @click.self="closeCompleteModal">
        <div class="modal-dialog modal-lg" @click.stop>
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Complete Appointment</h5>
              <button type="button" class="btn-close" @click="closeCompleteModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveTreatment">
                <div class="mb-3">
                  <label class="form-label">Visit Type *</label>
                  <select class="form-select" v-model="treatmentForm.visit_type" required>
                    <option value="In-person">In-person</option>
                    <option value="Follow-up">Follow-up</option>
                    <option value="Emergency">Emergency</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label">Tests Done</label>
                  <input type="text" class="form-control" v-model="treatmentForm.tests_done" />
                </div>
                <div class="mb-3">
                  <label class="form-label">Diagnosis *</label>
                  <textarea class="form-control" v-model="treatmentForm.diagnosis" rows="3" required></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Prescription</label>
                  <textarea class="form-control" v-model="treatmentForm.prescription" rows="3"></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Medicines</label>
                  <textarea class="form-control" v-model="treatmentForm.medicines" rows="2" placeholder="e.g., Medicine 1 1-0-1"></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Notes</label>
                  <textarea class="form-control" v-model="treatmentForm.notes" rows="2"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Save Treatment</button>
                <button type="button" class="btn btn-secondary ms-2" @click="closeCompleteModal">Cancel</button>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Availability Modal -->
      <div class="modal" :class="{ show: showAvailabilityModal }" :style="{ display: showAvailabilityModal ? 'block' : 'none' }" v-if="showAvailabilityModal" @click.self="showAvailabilityModal = false">
        <div class="modal-dialog modal-lg" @click.stop>
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Set Availability (Next 7 Days)</h5>
              <button type="button" class="btn-close" @click="showAvailabilityModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-for="day in availabilityDays" :key="day.date" class="mb-3">
                <h6>{{ formatDate(day.date) }}</h6>
                <div class="row">
                  <div class="col-md-6">
                    <label>
                      <input type="checkbox" v-model="day.morning" />
                      Morning (08:00 - 12:00)
                    </label>
                  </div>
                  <div class="col-md-6">
                    <label>
                      <input type="checkbox" v-model="day.evening" />
                      Evening (16:00 - 21:00)
                    </label>
                  </div>
                </div>
              </div>
              <button class="btn btn-primary" @click="saveAvailability">Save Availability</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { doctorAPI } from '@/services/api'

export default {
  name: 'DoctorDashboard',
  data() {
    return {
      dashboardData: {},
      loading: true,
      showCompleteModal: false,
      showAvailabilityModal: false,
      currentAppointment: null,
      treatmentForm: {
        visit_type: 'In-person',
        tests_done: '',
        diagnosis: '',
        prescription: '',
        medicines: '',
        notes: ''
      },
      availabilityDays: []
    }
  },
  mounted() {
    this.loadDashboard()
    this.initAvailabilityDays()
  },
  methods: {
    async loadDashboard() {
      try {
        this.dashboardData = await doctorAPI.getDashboard()
      } catch (error) {
        alert('Failed to load dashboard: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    initAvailabilityDays() {
      const today = new Date()
      this.availabilityDays = []
      for (let i = 0; i < 7; i++) {
        const date = new Date(today)
        date.setDate(today.getDate() + i)
        this.availabilityDays.push({
          date: date.toISOString().split('T')[0],
          morning: false,
          evening: false
        })
      }
    },
    async completeAppointment(appointment) {
      this.currentAppointment = appointment
      this.showCompleteModal = true
    },
    async saveTreatment() {
      try {
        await doctorAPI.completeAppointment(this.currentAppointment.id, this.treatmentForm)
        alert('Treatment saved successfully!')
        this.closeCompleteModal()
        this.loadDashboard()
      } catch (error) {
        alert('Failed to save treatment: ' + error.message)
      }
    },
    async viewPatientHistory(appointment) {
      // Navigate or show patient history
      alert(`View history for patient: ${appointment.patient_name}`)
    },
    async saveAvailability() {
      const slots = []
      this.availabilityDays.forEach(day => {
        if (day.morning) {
          slots.push({
            date: day.date,
            start_time: '08:00',
            end_time: '12:00'
          })
        }
        if (day.evening) {
          slots.push({
            date: day.date,
            start_time: '16:00',
            end_time: '21:00'
          })
        }
      })
      
      try {
        await doctorAPI.setAvailability(slots)
        alert('Availability saved successfully!')
        this.showAvailabilityModal = false
      } catch (error) {
        alert('Failed to save availability: ' + error.message)
      }
    },
    closeCompleteModal() {
      this.showCompleteModal = false
      this.currentAppointment = null
      this.treatmentForm = {
        visit_type: 'In-person',
        tests_done: '',
        diagnosis: '',
        prescription: '',
        medicines: '',
        notes: ''
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
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

