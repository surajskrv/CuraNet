<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Treatment History</h2>
      <button class="btn btn-success" @click="exportCSV">Export as CSV</button>
    </div>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Visit No.</th>
            <th>Date</th>
            <th>Doctor</th>
            <th>Department</th>
            <th>Visit Type</th>
            <th>Tests Done</th>
            <th>Diagnosis</th>
            <th>Prescription</th>
            <th>Medicines</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, idx) in history" :key="record.id">
            <td>{{ idx + 1 }}</td>
            <td>{{ formatDate(record.scheduled_date) }}</td>
            <td>{{ record.doctor_name }}</td>
            <td>{{ record.department }}</td>
            <td>{{ record.treatment?.visit_type || 'N/A' }}</td>
            <td>{{ record.treatment?.tests_done || 'N/A' }}</td>
            <td>{{ record.treatment?.diagnosis || 'N/A' }}</td>
            <td>{{ record.treatment?.prescription || 'N/A' }}</td>
            <td>{{ record.treatment?.medicines || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="history.length === 0" class="text-center text-muted">
        <p>No treatment history available</p>
      </div>
    </div>
  </div>
</template>

<script>
import { patientAPI } from '@/services/api'

export default {
  name: 'PatientHistory',
  data() {
    return {
      history: [],
      loading: true,
      exportTaskId: null,
      checkingExport: false
    }
  },
  mounted() {
    this.loadHistory()
  },
  methods: {
    async loadHistory() {
      try {
        this.history = await patientAPI.getHistory()
      } catch (error) {
        alert('Failed to load history: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async exportCSV() {
      try {
        const response = await patientAPI.triggerCSVExport()
        this.exportTaskId = response.task_id
        
        // Poll for completion
        this.checkExportStatus()
      } catch (error) {
        alert('Failed to start CSV export: ' + error.message)
      }
    },
    async checkExportStatus() {
      if (!this.exportTaskId) return
      
      this.checkingExport = true
      const maxAttempts = 10
      let attempts = 0
      
      const poll = setInterval(async () => {
        attempts++
        try {
          const response = await patientAPI.getCSVExportStatus(this.exportTaskId)
          
          if (response.state === 'SUCCESS') {
            clearInterval(poll)
            this.checkingExport = false
            // The response should be a file download
            alert('CSV export completed! File should download automatically.')
          } else if (response.state === 'FAILURE' || attempts >= maxAttempts) {
            clearInterval(poll)
            this.checkingExport = false
            alert('CSV export failed or timed out')
          }
        } catch (error) {
          clearInterval(poll)
          this.checkingExport = false
          alert('Failed to check export status: ' + error.message)
        }
      }, 2000)
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString()
    }
  }
}
</script>

