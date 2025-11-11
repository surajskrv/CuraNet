<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Manage Doctors</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">Add New Doctor</button>
    </div>
    
    <div class="mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search doctors by name, username, or specialization..."
        v-model="searchQuery"
        @input="searchDoctors"
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
            <th>Specialization</th>
            <th>Experience</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doctor in doctors" :key="doctor.id">
            <td>{{ doctor.id }}</td>
            <td>{{ doctor.full_name }}</td>
            <td>{{ doctor.username }}</td>
            <td>{{ doctor.email }}</td>
            <td>{{ doctor.specialization || 'N/A' }}</td>
            <td>{{ doctor.experience_years || 0 }} years</td>
            <td>
              <span :class="doctor.is_active ? 'badge bg-success' : 'badge bg-danger'">
                {{ doctor.is_active ? 'Active' : 'Blacklisted' }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-warning me-1" @click="editDoctor(doctor)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteDoctor(doctor.id)">Blacklist</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Create/Edit Modal -->
    <div class="modal" :class="{ show: showCreateModal || showEditModal }" :style="{ display: (showCreateModal || showEditModal) ? 'block' : 'none' }" v-if="showCreateModal || showEditModal" @click.self="closeModal">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ showEditModal ? 'Edit Doctor' : 'Add New Doctor' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveDoctor">
              <div class="mb-3">
                <label class="form-label">Username *</label>
                <input type="text" class="form-control" v-model="doctorForm.username" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Email *</label>
                <input type="email" class="form-control" v-model="doctorForm.email" required />
              </div>
              <div v-if="!showEditModal" class="mb-3">
                <label class="form-label">Password *</label>
                <input type="password" class="form-control" v-model="doctorForm.password" required />
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">First Name *</label>
                  <input type="text" class="form-control" v-model="doctorForm.first_name" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Last Name *</label>
                  <input type="text" class="form-control" v-model="doctorForm.last_name" required />
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Specialization *</label>
                <select class="form-select" v-model="doctorForm.specialization_id" required>
                  <option value="">Select Specialization</option>
                  <option v-for="spec in deaprtment" :key="spec.id" :value="spec.id">
                    {{ spec.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Experience (Years)</label>
                <input type="number" class="form-control" v-model.number="doctorForm.experience_years" />
              </div>
              <div class="mb-3">
                <label class="form-label">Qualifications</label>
                <textarea class="form-control" v-model="doctorForm.qualifications" rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Bio</label>
                <textarea class="form-control" v-model="doctorForm.bio" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Contact Number</label>
                <input type="tel" class="form-control" v-model="doctorForm.contact_number" />
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
  name: 'AdminDoctors',
  data() {
    return {
      doctors: [],
      deaprtment: [],
      loading: false,
      searchQuery: '',
      showCreateModal: false,
      showEditModal: false,
      doctorForm: {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        specialization_id: '',
        experience_years: null,
        qualifications: '',
        bio: '',
        contact_number: ''
      }
    }
  },
  mounted() {
    this.loadDoctors()
    this.loadDeaprtment()
  },
  methods: {
    async loadDoctors() {
      this.loading = true
      try {
        this.doctors = await adminAPI.getDoctors(this.searchQuery)
      } catch (error) {
        alert('Failed to load doctors: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async loadDeaprtment() {
      try {
        this.deaprtment = await adminAPI.getDeaprtment()
      } catch (error) {
        console.error('Failed to load deaprtment:', error)
      }
    },
    searchDoctors() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.loadDoctors()
      }, 300)
    },
    editDoctor(doctor) {
      this.doctorForm = {
        username: doctor.username,
        email: doctor.email,
        first_name: doctor.first_name,
        last_name: doctor.last_name,
        specialization_id: doctor.specialization_id,
        experience_years: doctor.experience_years,
        qualifications: doctor.qualifications || '',
        bio: doctor.bio || '',
        contact_number: doctor.contact_number || ''
      }
      this.showEditModal = true
      this.editingDoctorId = doctor.id
    },
    async saveDoctor() {
      try {
        if (this.showEditModal) {
          await adminAPI.updateDoctor(this.editingDoctorId, this.doctorForm)
          alert('Doctor updated successfully!')
        } else {
          await adminAPI.createDoctor(this.doctorForm)
          alert('Doctor created successfully!')
        }
        this.closeModal()
        this.loadDoctors()
      } catch (error) {
        alert('Failed to save doctor: ' + error.message)
      }
    },
    async deleteDoctor(id) {
      if (confirm('Are you sure you want to blacklist this doctor?')) {
        try {
          await adminAPI.deleteDoctor(id)
          alert('Doctor blacklisted successfully!')
          this.loadDoctors()
        } catch (error) {
          alert('Failed to blacklist doctor: ' + error.message)
        }
      }
    },
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingDoctorId = null
      this.doctorForm = {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        specialization_id: '',
        experience_years: null,
        qualifications: '',
        bio: '',
        contact_number: ''
      }
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

