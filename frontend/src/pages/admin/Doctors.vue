<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Manage Doctors</h2>
      <button class="btn btn-primary" @click="openCreateModal">
        <i class="bi bi-plus-lg me-1"></i> Add New Doctor
      </button>
    </div>
    
    <!-- Search Bar -->
    <div class="mb-3">
      <div class="input-group shadow-sm">
        <span class="input-group-text bg-white border-end-0"><i class="bi bi-search"></i></span>
        <input
          type="text"
          class="form-control border-start-0 ps-0"
          placeholder="Search by name or specialization..."
          v-model="searchQuery"
          @input="searchDoctors"
        />
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading doctors...</p>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <!-- Doctors Table -->
    <div v-else>
      <div class="table-responsive shadow-sm rounded">
        <table class="table table-hover align-middle mb-0 bg-white">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Specialization</th>
              <th>Department</th>
              <th>Contact</th>
              <th>Exp</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="doctors.length === 0">
              <td colspan="7" class="text-center py-4 text-muted">No doctors found.</td>
            </tr>
            <tr v-for="doctor in doctors" :key="doctor.id">
              <td>#{{ doctor.id }}</td>
              <td class="fw-bold">{{ doctor.name }}</td>
              <td>{{ doctor.specialization }}</td>
              <td>
                <span class="badge bg-soft-primary text-primary border border-primary-subtle">
                  {{ doctor.department_name || 'Unassigned' }}
                </span>
              </td>
              <td>
                <div class="small">{{ doctor.email }}</div>
                <div class="small text-muted">{{ doctor.phone }}</div>
              </td>
              <td>{{ doctor.experience || 0 }} yrs</td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="editDoctor(doctor)" title="Edit">
                  <i class="bi bi-pencil-fill"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteDoctor(doctor.id)" title="Blacklist/Delete">
                  <i class="bi bi-trash-fill"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-backdrop fade show"></div>
    <div class="modal fade" :class="{ 'show d-block': showModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Edit Doctor' : 'Add New Doctor' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveDoctor">
              
              <!-- Account Info -->
              <h6 class="mb-3 text-primary border-bottom pb-2">Account Information</h6>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Full Name *</label>
                  <input type="text" class="form-control" v-model="doctorForm.name" required placeholder="Dr. John Doe" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Email *</label>
                  <input type="email" class="form-control" v-model="doctorForm.email" required placeholder="doctor@hospital.com" />
                </div>
              </div>

              <!-- Password only shown for new users -->
              <div v-if="!isEditing" class="mb-3">
                <label class="form-label">Password *</label>
                <input type="password" class="form-control" v-model="doctorForm.password" required minlength="6" />
                <div class="form-text">Must be at least 6 characters.</div>
              </div>

              <div class="row">
                 <div class="col-md-6 mb-3">
                  <label class="form-label">Phone Number</label>
                  <input type="tel" class="form-control" v-model="doctorForm.phone" 
                  minlength="10"
                  maxlength="10"
                  pattern="[6-9]{1}[0-9]{9}"
                  placeholder="10-digit number" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Pincode</label>
                  <input type="text" class="form-control" v-model="doctorForm.pincode" 
                  minlength="6"
                  maxlength="6"
                  pattern="[0-9]{6}" />
                </div>
              </div>

              <div class="mb-3">
                  <label class="form-label">Address</label>
                  <textarea class="form-control" v-model="doctorForm.address" rows="2"></textarea>
              </div>

              <!-- Professional Info -->
              <h6 class="mb-3 text-primary border-bottom pb-2 mt-4">Professional Details</h6>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Department *</label>
                  <select class="form-select" v-model="doctorForm.department_id" required>
                    <option value="" disabled>Select Department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Specialization *</label>
                  <input type="text" class="form-control" v-model="doctorForm.specialization" required placeholder="e.g. Cardiologist" />
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Experience (Years)</label>
                  <input type="number" class="form-control" v-model="doctorForm.experience" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Qualification</label>
                  <input type="text" class="form-control" v-model="doctorForm.qualification" placeholder="e.g. MBBS, MD" />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Bio</label>
                <textarea class="form-control" v-model="doctorForm.bio" rows="3" placeholder="Short biography..."></textarea>
              </div>

              <div class="modal-footer px-0 pb-0">
                <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="submitting">
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ isEditing ? 'Update Doctor' : 'Create Doctor' }}
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
  name: 'AdminDoctors',
  data() {
    return {
      doctors: [],
      departments: [],
      loading: false,
      submitting: false,
      error: '',
      searchQuery: '',
      searchTimeout: null,
      showModal: false,
      isEditing: false,
      editingDoctorId: null,
      
      doctorForm: {
        email: '',
        password: '',
        name: '',
        phone: '',
        address: '',
        pincode: '',
        department_id: '',
        specialization: '',
        qualification: '',
        experience: '',
        bio: ''
      }
    }
  },
  mounted() {
    this.loadDoctors();
    this.loadDepartments();
  },
  methods: {
    async loadDoctors() {
      this.loading = true;
      this.error = '';
      try {
        let url = '/api/admin/doctors';
        
        if (this.searchQuery.trim()) {
          url = `/api/admin/search?type=doctor&q=${encodeURIComponent(this.searchQuery)}`;
        }

        const response = await fetch(url, {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) throw new Error(`Failed to fetch doctors (${response.status})`);
        
        this.doctors = await response.json();
      } catch (err) {
        console.error(err);
        this.error = err.message || 'Error loading doctors';
      } finally {
        this.loading = false;
      }
    },

    async loadDepartments() {
      try {
        const response = await fetch('/api/admin/departments', {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });
        if (response.ok) {
          this.departments = await response.json();
        }
      } catch (err) {
        console.error("Failed to load departments", err);
      }
    },

    // --- Search Debounce ---
    searchDoctors() {
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadDoctors();
      }, 500);
    },

    // --- Modal Logic ---
    openCreateModal() {
      this.resetForm();
      this.isEditing = false;
      this.showModal = true;
    },

    editDoctor(doctor) {
      this.isEditing = true;
      this.editingDoctorId = doctor.id;
      this.showModal = true;
      
      // Match backend keys to form keys
      this.doctorForm = {
        email: doctor.email,
        name: doctor.name, 
        phone: doctor.phone || '',
        address: doctor.address || '',
        pincode: doctor.pincode || '',
        department_id: doctor.department_id || '',
        specialization: doctor.specialization,
        qualification: doctor.qualification || '',
        experience: doctor.experience || '',
        bio: doctor.bio || '',
        password: '' 
      };
    },

    closeModal() {
      this.showModal = false;
      this.resetForm();
    },

    resetForm() {
      this.doctorForm = {
        email: '', password: '', name: '', phone: '', address: '',
        pincode: '', department_id: '', specialization: '',
        qualification: '', experience: '', bio: ''
      };
      this.editingDoctorId = null;
      this.submitting = false;
    },

    // --- CRUD Operations ---
    async saveDoctor() {
      this.submitting = true;
      try {
        const url = this.isEditing 
          ? `/api/admin/doctors/${this.editingDoctorId}`
          : '/api/admin/doctors';
          
        const method = this.isEditing ? 'PUT' : 'POST';

        const response = await fetch(url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(this.doctorForm)
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Failed to save doctor');
        }

        alert(this.isEditing ? 'Doctor updated successfully!' : 'Doctor created successfully!');
        this.closeModal();
        this.loadDoctors();
        
      } catch (err) {
        alert(err.message);
      } finally {
        this.submitting = false;
      }
    },

    async deleteDoctor(id) {
      if (!confirm('Are you sure you want to blacklist/remove this doctor?')) return;
      
      try {
        const response = await fetch(`/api/admin/doctors/${id}`, {
          method: 'DELETE',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || 'Delete failed');
        }

        this.loadDoctors(); 
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
.bg-soft-primary {
    background-color: rgba(13, 110, 253, 0.1);
    color: #0d6efd;
}
</style>