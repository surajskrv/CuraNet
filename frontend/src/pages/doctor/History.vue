<template>
  <div>
    <h2 class="mb-4">Treatment History</h2>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading history...</p>
    </div>

    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>
    
    <div v-else>
      <div class="card shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-4">Date</th>
                  <th>Patient</th>
                  <th>Contact</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="history.length === 0">
                  <td colspan="5" class="text-center py-4 text-muted">No treatment records found.</td>
                </tr>
                <tr v-for="record in history" :key="record.id">
                  <td class="ps-4 text-nowrap">
                    <div class="fw-bold">{{ formatDate(record.date) }}</div>
                    <div class="small text-muted">{{ record.time }}</div>
                  </td>
                  <td>
                    <div class="fw-bold">{{ record.patient_name }}</div>
                    <div class="small text-muted">{{ record.gender || 'N/A' }}, {{ calculateAge(record.date_of_birth) }}</div>
                  </td>
                  <td class="small">{{ record.patient_phone }}</td>
                  <td>{{ record.treatment?.diagnosis || '-' }}</td>
                  <td>
                    <div class="text-truncate" style="max-width: 200px;" :title="record.treatment?.prescription">
                      {{ record.treatment?.prescription || '-' }}
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorHistory',
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
    async loadHistory() {
      this.loading = true;
      try {
        const response = await fetch('/api/doctor/appointments?status=Completed', {
          method: 'GET',
          headers: {
            "Content-Type": "application/json",
            "Auth-Token": localStorage.getItem("auth_token")
          },
        });

        if (!response.ok) {
          if (response.status === 401) this.$router.push('/login');
          throw new Error(`Failed to load history (${response.status})`);
        }

        this.history = await response.json();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString();
    },
    calculateAge(dob) {
      if (!dob) return '';
      const birthDate = new Date(dob);
      const ageDifMs = Date.now() - birthDate.getTime();
      const ageDate = new Date(ageDifMs);
      return Math.abs(ageDate.getUTCFullYear() - 1970) + ' yrs';
    }
  }
}
</script>