<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Treatment History</h2>
      <button 
        class="btn btn-success" 
        @click="exportCSV" 
        :disabled="history.length === 0"
      >
        <i class="bi bi-file-earmark-spreadsheet me-2"></i> Export as CSV
      </button>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading records...</p>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <div v-else>
      <div class="table-responsive shadow-sm rounded">
        <table class="table table-hover align-middle mb-0 bg-white">
          <thead class="table-light">
            <tr>
              <th>Date</th>
              <th>Doctor</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="history.length === 0">
              <td colspan="5" class="text-center py-4 text-muted">No treatment history found.</td>
            </tr>
            <tr v-for="record in history" :key="record.appointment_id">
              <td>
                <div class="fw-bold">{{ formatDate(record.date) }}</div>
                <div class="small text-muted">{{ record.time }}</div>
              </td>
              <td>
                <div class="fw-bold">{{ record.doctor_name }}</div>
                <div class="small text-muted">{{ record.doctor_specialization }}</div>
              </td>
              <td>{{ record.diagnosis || '-' }}</td>
              <td>{{ record.prescription || '-' }}</td>
              <td>
                <small class="text-muted">{{ record.notes || '-' }}</small>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientHistory',
  data() {
    return {
      history: [],
      loading: true,
      error: ''
    }
  },
  mounted() {
    this.loadHistory()
  },
  methods: {
    // --- FETCH HISTORY ---
    async loadHistory() {
      this.loading = true;
      this.error = '';
      try {
        const response = await fetch('/api/patient/treatment-history', {
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
          throw new Error(`Server error: ${response.status}`);
        }

        this.history = await response.json();
        
      } catch (err) {
        console.error(err);
        this.error = err.message || "Failed to load history";
      } finally {
        this.loading = false;
      }
    },

    // --- CLIENT-SIDE CSV EXPORT ---
    exportCSV() {
      if (this.history.length === 0) return;

      try {
        // 1. Define CSV Headers
        const headers = ['Date', 'Time', 'Doctor Name', 'Specialization', 'Diagnosis', 'Prescription', 'Notes'];
        
        // 2. Map Data to CSV Rows
        const rows = this.history.map(record => [
          record.date,
          record.time,
          `"${record.doctor_name}"`, // Quote strings to handle commas
          record.doctor_specialization,
          `"${record.diagnosis || ''}"`,
          `"${record.prescription || ''}"`,
          `"${record.notes || ''}"`
        ]);

        // 3. Combine into CSV String
        const csvContent = [
          headers.join(','),
          ...rows.map(row => row.join(','))
        ].join('\n');

        // 4. Create Download Link
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `treatment_history_${new Date().toISOString().slice(0,10)}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

      } catch (err) {
        alert("Failed to export CSV: " + err.message);
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return '-';
      return new Date(dateStr).toLocaleDateString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric'
      });
    }
  }
}
</script>

<style scoped>
/* Optional: Highlight row on hover */
tr:hover {
  background-color: #f8f9fa;
}
</style>