<template>
  <div>
    <h2 class="mb-4">Patient Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <!-- Upcoming Appointments -->
      <div class="card mb-4">
        <div class="card-header">
          <h5>Upcoming Appointments</h5>
        </div>
        <div class="card-body">
          <table class="table" v-if="dashboardData.upcoming_appointments?.length > 0">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Doctor</th>
                <th>Department</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appt in dashboardData.upcoming_appointments" :key="appt.id">
                <td>{{ formatDate(appt.scheduled_date) }}</td>
                <td>{{ appt.scheduled_time }}</td>
                <td>{{ appt.doctor_name }}</td>
                <td>{{ appt.department }}</td>
                <td>
                  <button class="btn btn-sm btn-danger" @click="cancelAppointment(appt.id)">Cancel</button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else class="text-muted">No upcoming appointments</p>
        </div>
      </div>
      
      <!-- Deaprtment -->
      <div class="card mb-4">
        <div class="card-header">
          <h5>Departments</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div v-for="spec in dashboardData.deaprtment" :key="spec.id" class="col-md-4 mb-3">
              <div class="card">
                <div class="card-body">
                  <h6>{{ spec.name }}</h6>
                  <p class="text-muted small">{{ spec.description }}</p>
                  <button class="btn btn-sm btn-primary" @click="viewDoctors(spec.id)">View Doctors</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Book Appointment Modal -->
      <div class="modal" :class="{ show: showBookingModal }" :style="{ display: showBookingModal ? 'block' : 'none' }" v-if="showBookingModal" @click.self="showBookingModal = false">
        <div class="modal-dialog modal-lg" @click.stop>
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Book Appointment with {{ selectedDoctor?.full_name }}</h5>
              <button type="button" class="btn-close" @click="showBookingModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="availabilityLoading">Loading availability...</div>
              <div v-else>
                <div class="mb-3">
                  <label class="form-label">Select Date and Time</label>
                  <div class="row">
                    <div v-for="slot in availableSlots" :key="slot.id" class="col-md-6 mb-2">
                      <button
                        class="btn btn-outline-primary w-100"
                        @click="selectSlot(slot)"
                        :disabled="slot.is_available === false"
                      >
                        {{ formatDate(slot.available_date) }} - {{ slot.start_time }} to {{ slot.end_time }}
                      </button>
                    </div>
                  </div>
                </div>
                <div v-if="selectedSlot" class="mb-3">
                  <label class="form-label">Reason for Visit</label>
                  <textarea class="form-control" v-model="bookingForm.reason" rows="3"></textarea>
                </div>
                <button
                  class="btn btn-primary"
                  @click="bookAppointment"
                  :disabled="!selectedSlot"
                >
                  Book Appointment
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Doctors List Modal -->
      <div class="modal" :class="{ show: showDoctorsModal }" :style="{ display: showDoctorsModal ? 'block' : 'none' }" v-if="showDoctorsModal" @click.self="showDoctorsModal = false">
        <div class="modal-dialog modal-lg" @click.stop>
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Doctors in {{ selectedDepartment?.name }}</h5>
              <button type="button" class="btn-close" @click="showDoctorsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="doctorsLoading">Loading...</div>
              <div v-else>
                <div v-for="doctor in doctorsList" :key="doctor.id" class="card mb-3">
                  <div class="card-body">
                    <h6>Dr. {{ doctor.full_name }}</h6>
                    <p class="text-muted">{{ doctor.bio || 'No bio available' }}</p>
                    <p><strong>Experience:</strong> {{ doctor.experience_years || 0 }} years</p>
                    <button class="btn btn-sm btn-primary" @click="viewDoctorAvailability(doctor)">Check Availability</button>
                    <button class="btn btn-sm btn-info ms-2" @click="viewDoctorProfile(doctor)">View Profile</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { patientAPI } from '@/services/api'

export default {
  name: 'PatientDashboard',
  data() {
    return {
      dashboardData: {},
      loading: true,
      showBookingModal: false,
      showDoctorsModal: false,
      selectedDoctor: null,
      selectedDepartment: null,
      selectedSlot: null,
      availableSlots: [],
      availabilityLoading: false,
      doctorsList: [],
      doctorsLoading: false,
      bookingForm: {
        reason: ''
      }
    }
  },
  mounted() {
    this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      try {
        this.dashboardData = await patientAPI.getDashboard()
      } catch (error) {
        alert('Failed to load dashboard: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async viewDoctors(specId) {
      this.selectedDepartment = this.dashboardData.deaprtment.find(s => s.id === specId)
      this.showDoctorsModal = true
      this.doctorsLoading = true
      try {
        this.doctorsList = await patientAPI.getDoctorsByDepartment(specId)
      } catch (error) {
        alert('Failed to load doctors: ' + error.message)
      } finally {
        this.doctorsLoading = false
      }
    },
    async viewDoctorAvailability(doctor) {
      this.selectedDoctor = doctor
      this.showDoctorsModal = false
      this.showBookingModal = true
      this.availabilityLoading = true
      try {
        this.availableSlots = await patientAPI.getDoctorAvailability(doctor.id)
      } catch (error) {
        alert('Failed to load availability: ' + error.message)
      } finally {
        this.availabilityLoading = false
      }
    },
    viewDoctorProfile(doctor) {
      alert(`Dr. ${doctor.full_name}\n${doctor.bio || 'No bio available'}\nExperience: ${doctor.experience_years || 0} years`)
    },
    selectSlot(slot) {
      this.selectedSlot = slot
    },
    async bookAppointment() {
      if (!this.selectedSlot) return
      
      try {
        await patientAPI.bookAppointment({
          doctor_id: this.selectedDoctor.id,
          scheduled_date: this.selectedSlot.available_date,
          scheduled_time: this.selectedSlot.start_time,
          reason: this.bookingForm.reason
        })
        alert('Appointment booked successfully!')
        this.showBookingModal = false
        this.selectedSlot = null
        this.loadDashboard()
      } catch (error) {
        alert('Failed to book appointment: ' + error.message)
      }
    },
    async cancelAppointment(appointmentId) {
      if (confirm('Are you sure you want to cancel this appointment?')) {
        try {
          await patientAPI.cancelAppointment(appointmentId)
          alert('Appointment cancelled successfully!')
          this.loadDashboard()
        } catch (error) {
          alert('Failed to cancel appointment: ' + error.message)
        }
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString()
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

