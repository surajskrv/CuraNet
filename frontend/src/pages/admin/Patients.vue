<template>
  <div>
    <h2 class="mb-4">Manage Patients</h2>
    
    <!-- Search Bar -->
    <div class="mb-3">
      <div class="input-group shadow-sm">
        <span class="input-group-text bg-white border-end-0"><i class="bi bi-search"></i></span>
        <input
          type="text"
          class="form-control border-start-0 ps-0"
          placeholder="Search patients by name, email, or phone..."
          v-model="searchQuery"
          @input="searchPatients"
        />
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading patients...</p>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <!-- Patients Table -->
    <div v-else>
      <div class="table-responsive shadow-sm rounded">
        <table class="table table-hover align-middle mb-0 bg-white">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Patient Name</th>
              <th>Contact Info</th>
              <th>Gender/Blood</th>
              <th>Location</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="patients.length === 0">
              <td colspan="6" class="text-center py-4 text-muted">No patients found.</td>
            </tr>
            <tr v-for="patient in patients" :key="patient.id">
              <td>#{{ patient.id }}</td>
              <td class="fw-bold">{{ patient.name }}</td>
              <td>
                <div class="small">{{ patient.email }}</div>
                <div class="small text-muted">{{ patient.phone }}</div>
              </td>
              <td>
                <span class="badge bg-light text-dark border me-1">{{ patient.gender || 'N/A' }}</span>
                <span class="badge bg-danger bg-opacity-10 text-danger">{{ patient.blood_group || '-' }}</span>
              </td>
              <td class="small text-muted" style="max-width: 200px;">
                {{ patient.address }} <span v-if="patient.pincode">({{ patient.pincode }})</span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="editPatient(patient)" title="Edit">
                  <i class="bi bi-pencil-fill"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deletePatient(patient.id)" title="Blacklist/Delete">
                  <i class="bi bi-trash-fill"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-backdrop fade show"></div>
    <div class="modal fade" :class="{ 'show d-block': showEditModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Patient</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="savePatient">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="patientForm.name" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" v-model="patientForm.email" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Phone Number</label>
                <input type="tel" class="form-control" v-model="patientForm.phone" required />
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Gender</label>
                  <select class="form-select" v-model="patientForm.gender">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                   <label class="form-label">Blood Group</label>
                   <input type="text" class="form-control" v-model="patientForm.blood_group" />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Address</label>
                <textarea class="form-control" v-model="patientForm.address" rows="2"></textarea>
              </div>
              <div class="mb-3">
                 <label class="form-label">Pincode</label>
                 <input type="text" class="form-control" v-model="patientForm.pincode" />
              </div>

              <div class="modal-footer px-0 pb-0">
                <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="submitting">
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminPatients',
  data() {
    return {
      patients: [],
      loading: false,
      submitting: false,
      error: '',
      searchQuery: '',
      searchTimeout: null,
      showEditModal: false,
      editingPatientId: null,
      
      patientForm: {
        name: '',
        email: '',
        phone: '',
        address: '',
        pincode: '',
        gender: '',
        blood_group: ''
      }
    }
  },
  mounted() {
    this.loadPatients();
  },
  methods: {
    // --- LOAD PATIENTS ---
    async loadPatients() {
      this.loading = true;
      this.error = '';
      try {

        let url = '/api/admin/patients';
        if (this.searchQuery.trim()) {
          url = `/api/admin/search?type=patient&q=${encodeURIComponent(this.searchQuery)}`;
        }

        const response = await fetch(url, {
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
        
        this.patients = await response.json();
      } catch (err) {
        console.error(err);
        this.error = err.message || 'Error loading patients';
      } finally {
        this.loading = false;
      }
    },

    // --- SEARCH ---
    searchPatients() {
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadPatients();
      }, 500);
    },

    // --- EDIT MODAL ---
    editPatient(patient) {
      this.editingPatientId = patient.id;
      this.patientForm = {
        name: patient.name,
        email: patient.email,
        phone: patient.phone,
        address: patient.address,
        pincode: patient.pincode,
        gender: patient.gender,
        blood_group: patient.blood_group
      };
      this.showEditModal = true;
    },

    closeModal() {
      this.showEditModal = false;
      this.editingPatientId = null;
      this.patientForm = {};
    },

    // --- UPDATE PATIENT ---
    async savePatient() {
      this.submitting = true;
      try {
        const response = await fetch(`/api/admin/patients/${this.editingPatientId}`, {
          method: 'PUT',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(this.patientForm)
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || 'Update failed');
        }

        alert('Patient updated successfully!');
        this.closeModal();
        this.loadPatients();
      } catch (err) {
        alert(err.message);
      } finally {
        this.submitting = false;
      }
    },

    // --- DELETE PATIENT ---
    async deletePatient(id) {
      if (!confirm('Are you sure you want to blacklist/remove this patient?')) return;
      
      try {
        const response = await fetch(`/api/admin/patients/${id}`, {
          method: 'DELETE',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) {
          throw new Error('Delete failed');
        }

        this.loadPatients();
      } catch (err) {
        alert(err.message);
      }
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