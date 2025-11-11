<template>
  <div>
    <h2 class="mb-4">Admin Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else>
      <!-- Statistics Cards -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card text-white bg-primary">
            <div class="card-body">
              <h5 class="card-title">Total Doctors</h5>
              <h2>{{ stats.total_doctors }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-success">
            <div class="card-body">
              <h5 class="card-title">Total Patients</h5>
              <h2>{{ stats.total_patients }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-info">
            <div class="card-body">
              <h5 class="card-title">Total Appointments</h5>
              <h2>{{ stats.total_appointments }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-warning">
            <div class="card-body">
              <h5 class="card-title">Upcoming Appointments</h5>
              <h2>{{ stats.upcoming_appointments }}</h2>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Quick Actions</h5>
              <router-link to="/admin/doctors" class="btn btn-primary me-2">Manage Doctors</router-link>
              <router-link to="/admin/patients" class="btn btn-success me-2">Manage Patients</router-link>
              <router-link to="/admin/appointments" class="btn btn-info">View Appointments</router-link>
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
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        total_doctors: 0,
        total_patients: 0,
        total_appointments: 0,
        upcoming_appointments: 0
      },
      loading: true,
      error: ''
    }
  },
  mounted() {
    this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      try {
        this.stats = await adminAPI.getDashboard()
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

