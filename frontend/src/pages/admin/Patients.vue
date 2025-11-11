<template>
  <div>
    <h2 class="mb-4">Manage Patients</h2>
    
    <div class="mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search patients by name, username, or contact..."
        v-model="searchQuery"
        @input="searchPatients"
      />
    </div>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Username</th>
            <th>Email</th>
            <th>Contact</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in patients" :key="patient.id">
            <td>{{ patient.id }}</td>
            <td>{{ patient.full_name }}</td>
            <td>{{ patient.username }}</td>
            <td>{{ patient.email }}</td>
            <td>{{ patient.contact_number }}</td>
            <td>
              <span :class="patient.is_active ? 'badge bg-success' : 'badge bg-danger'">
                {{ patient.is_active ? 'Active' : 'Blacklisted' }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-warning me-1" @click="editPatient(patient)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deletePatient(patient.id)">Blacklist</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Edit Modal -->
    <div class="modal" :class="{ show: showEditModal }" :style="{ display: showEditModal ? 'block' : 'none' }" v-if="showEditModal" @click.self="closeModal">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Patient</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="savePatient">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" class="form-control" v-model="patientForm.username" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" v-model="patientForm.email" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Contact Number</label>
                <input type="tel" class="form-control" v-model="patientForm.contact_number" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Address</label>
                <textarea class="form-control" v-model="patientForm.address" rows="3"></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Save</button>
              <button type="button" class="btn btn-secondary ms-2" @click="closeModal">Cancel</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI } from '@/services/api'

export default {
  name: 'AdminPatients',
  data() {
    return {
      patients: [],
      loading: false,
      searchQuery: '',
      showEditModal: false,
      patientForm: {},
      editingPatientId: null
    }
  },
  mounted() {
    this.loadPatients()
  },
  methods: {
    async loadPatients() {
      this.loading = true
      try {
        this.patients = await adminAPI.getPatients(this.searchQuery)
      } catch (error) {
        alert('Failed to load patients: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    searchPatients() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.loadPatients()
      }, 300)
    },
    editPatient(patient) {
      this.patientForm = { ...patient }
      this.editingPatientId = patient.id
      this.showEditModal = true
    },
    async savePatient() {
      try {
        await adminAPI.updatePatient(this.editingPatientId, this.patientForm)
        alert('Patient updated successfully!')
        this.closeModal()
        this.loadPatients()
      } catch (error) {
        alert('Failed to save patient: ' + error.message)
      }
    },
    async deletePatient(id) {
      if (confirm('Are you sure you want to blacklist this patient?')) {
        try {
          await adminAPI.deletePatient(id)
          alert('Patient blacklisted successfully!')
          this.loadPatients()
        } catch (error) {
          alert('Failed to blacklist patient: ' + error.message)
        }
      }
    },
    closeModal() {
      this.showEditModal = false
      this.patientForm = {}
      this.editingPatientId = null
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

