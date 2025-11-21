<template>
  <div>
    <h2 class="mb-4">Admin Dashboard</h2>
    
    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Loading dashboard data...</p>
    </div>
    
    <div v-else>
      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="card text-white bg-primary h-100 shadow-sm">
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <h6 class="card-title opacity-75">Total Doctors</h6>
                <h2 class="fw-bold mb-0">{{ stats.total_doctors }}</h2>
              </div>
              <i class="bi bi-person-badge position-absolute end-0 bottom-0 p-3" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3 mb-3">
          <div class="card text-white bg-success h-100 shadow-sm">
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <h6 class="card-title opacity-75">Total Patients</h6>
                <h2 class="fw-bold mb-0">{{ stats.total_patients }}</h2>
              </div>
              <i class="bi bi-people-fill position-absolute end-0 bottom-0 p-3" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3 mb-3">
          <div class="card text-white bg-info h-100 shadow-sm">
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <h6 class="card-title opacity-75">Total Appointments</h6>
                <h2 class="fw-bold mb-0">{{ stats.total_appointments }}</h2>
              </div>
              <i class="bi bi-calendar-check position-absolute end-0 bottom-0 p-3" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3 mb-3">
          <div class="card text-white bg-warning h-100 shadow-sm">
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <h6 class="card-title opacity-75 text-dark">Upcoming</h6>
                <h2 class="fw-bold mb-0 text-dark">{{ stats.upcoming_appointments }}</h2>
              </div>
              <i class="bi bi-clock-history position-absolute end-0 bottom-0 p-3 text-dark" style="font-size: 3rem; opacity: 0.2;"></i>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0"><i class="bi bi-lightning-charge-fill text-warning me-2"></i>Quick Actions</h5>
            </div>
            <div class="card-body">
              <div class="d-flex gap-3 flex-wrap">
                <router-link to="/admin/doctors" class="btn btn-outline-primary">
                  <i class="bi bi-person-plus-fill me-1"></i> Manage Doctors
                </router-link>
                
                <router-link to="/admin/patients" class="btn btn-outline-success">
                  <i class="bi bi-person-rolodex me-1"></i> Manage Patients
                </router-link>
                
                <router-link to="/admin/appointments" class="btn btn-outline-info">
                  <i class="bi bi-calendar-week me-1"></i> View Appointments
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- DEPARTMENTS SECTION -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="bi bi-building me-2 text-secondary"></i>Departments</h5>
              <button class="btn btn-sm btn-primary" @click="openDeptModal">
                <i class="bi bi-plus-lg me-1"></i> Add Department
              </button>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light">
                    <tr>
                      <th class="ps-4">Name</th>
                      <th>Description</th>
                      <th class="text-center">Doctors</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="departments.length === 0">
                      <td colspan="4" class="text-center py-4 text-muted">No departments found.</td>
                    </tr>
                    <tr v-for="dept in departments" :key="dept.id">
                      <td class="ps-4 fw-bold text-primary">{{ dept.name }}</td>
                      <td>{{ dept.description || '-' }}</td>
                      <td class="text-center">
                        <span class="badge bg-secondary rounded-pill">{{ dept.doctors_registered || 0 }}</span>
                      </td>
                      <td>{{ dept.created_at || 'N/A' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Department Modal -->
    <div v-if="showDeptModal" class="modal-backdrop fade show"></div>
    <div class="modal fade" :class="{ 'show d-block': showDeptModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Department</h5>
            <button type="button" class="btn-close" @click="closeDeptModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createDepartment">
              <div class="mb-3">
                <label class="form-label">Department Name *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="deptForm.name" 
                  required 
                  placeholder="e.g. Cardiology"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea 
                  class="form-control" 
                  v-model="deptForm.description" 
                  rows="3" 
                  placeholder="Brief description..."
                ></textarea>
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-secondary" @click="closeDeptModal">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="submittingDept">
                  <span v-if="submittingDept" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  Create
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
  name: 'AdminDashboard',
  data() {
    return {
      // Stats Data
      stats: {
        total_doctors: 0,
        total_patients: 0,
        total_appointments: 0,
        upcoming_appointments: 0
      },
      loading: true,
      error: '',

      // Department Data
      departments: [],
      showDeptModal: false,
      submittingDept: false,
      deptForm: {
        name: '',
        description: ''
      }
    }
  },
  mounted() {
    // Load both dashboard stats and department list
    this.initData();
  },
  methods: {
    async initData() {
      this.loading = true;
      try {
        await Promise.all([this.loadDashboard(), this.loadDepartments()]);
      } catch (e) {
        console.error("Init Error", e);
      } finally {
        this.loading = false;
      }
    },

    // --- DASHBOARD STATS ---
    async loadDashboard() {
      try {
        const response = await fetch("/api/admin/dashboard", {
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            this.$router.push('/login');
            return;
        }
          throw new Error(`Server error: ${response.status}`);
        }
        
        this.stats = await response.json();
        
      } catch (error) {
        console.error('Dashboard Error:', error);
        this.error = "Failed to load dashboard. " + (error.message || "Server error.");
      }
    },

    // --- DEPARTMENTS LIST ---
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

    // --- CREATE DEPARTMENT ---
    async createDepartment() {
      this.submittingDept = true;
      try {
        const response = await fetch('/api/admin/departments', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify(this.deptForm)
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Failed to create department');
        }

        alert('Department created successfully!');
        this.closeDeptModal();
        this.loadDepartments(); // Refresh list to show new dept
        
      } catch (err) {
        alert(err.message);
      } finally {
        this.submittingDept = false;
      }
    },

    // --- MODAL UTILS ---
    openDeptModal() {
      this.deptForm = { name: '', description: '' };
      this.showDeptModal = true;
    },
    closeDeptModal() {
      this.showDeptModal = false;
      this.deptForm = { name: '', description: '' };
    }
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}
/* Only animate the statistics cards */
.col-md-3 .card:hover {
  transform: translateY(-3px);
}
.modal-backdrop {
  opacity: 0.5;
  background-color: #000;
}
</style>