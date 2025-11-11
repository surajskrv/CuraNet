const API_BASE_URL = 'http://localhost:5000/api'

// Helper function to get auth token
function getAuthToken() {
  return localStorage.getItem('token')
}

// Helper function to set auth token
function setAuthToken(token) {
  localStorage.setItem('token', token)
}

// Helper function to remove auth token
function removeAuthToken() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

// Helper function to make API requests
async function apiRequest(endpoint, options = {}) {
  const token = getAuthToken()
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.message || `Request failed with status ${response.status}`)
    }
    
    return data
  } catch (error) {
    // If it's already an Error, re-throw it
    if (error instanceof Error) {
      throw error
    }
    // Otherwise, wrap it
    throw new Error(error.message || 'Network error occurred')
  }
}

// Auth API
export const authAPI = {
  login: (username, password) => 
    apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    }),
  
  register: (userData) =>
    apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    }),
  
  getCurrentUser: () =>
    apiRequest('/auth/me')
}

// Admin API
export const adminAPI = {
  getDashboard: () =>
    apiRequest('/admin/dashboard'),
  
  getDoctors: (search = '') =>
    apiRequest(`/admin/doctors?search=${encodeURIComponent(search)}`),
  
  getDoctor: (id) =>
    apiRequest(`/admin/doctors/${id}`),
  
  createDoctor: (doctorData) =>
    apiRequest('/admin/doctors', {
      method: 'POST',
      body: JSON.stringify(doctorData)
    }),
  
  updateDoctor: (id, doctorData) =>
    apiRequest(`/admin/doctors/${id}`, {
      method: 'PUT',
      body: JSON.stringify(doctorData)
    }),
  
  deleteDoctor: (id) =>
    apiRequest(`/admin/doctors/${id}`, {
      method: 'DELETE'
    }),
  
  getPatients: (search = '') =>
    apiRequest(`/admin/patients?search=${encodeURIComponent(search)}`),
  
  getPatient: (id) =>
    apiRequest(`/admin/patients/${id}`),
  
  updatePatient: (id, patientData) =>
    apiRequest(`/admin/patients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(patientData)
    }),
  
  deletePatient: (id) =>
    apiRequest(`/admin/patients/${id}`, {
      method: 'DELETE'
    }),
  
  getAppointments: (status = '', upcoming = false) => {
    const params = new URLSearchParams()
    if (status) params.append('status', status)
    if (upcoming) params.append('upcoming', 'true')
    return apiRequest(`/admin/appointments?${params.toString()}`)
  },
  
  getPatientHistory: (appointmentId) =>
    apiRequest(`/admin/appointments/${appointmentId}/history`),
  
  getDeaprtment: () =>
    apiRequest('/admin/deaprtment')
}

// Doctor API
export const doctorAPI = {
  getDashboard: () =>
    apiRequest('/doctor/dashboard'),
  
  getAppointments: (status = '', upcoming = false) => {
    const params = new URLSearchParams()
    if (status) params.append('status', status)
    if (upcoming) params.append('upcoming', 'true')
    return apiRequest(`/doctor/appointments?${params.toString()}`)
  },
  
  getAssignedPatients: () =>
    apiRequest('/doctor/patients'),
  
  completeAppointment: (appointmentId, treatmentData) =>
    apiRequest(`/doctor/appointments/${appointmentId}/complete`, {
      method: 'POST',
      body: JSON.stringify(treatmentData)
    }),
  
  cancelAppointment: (appointmentId) =>
    apiRequest(`/doctor/appointments/${appointmentId}/cancel`, {
      method: 'POST'
    }),
  
  getPatientHistory: (patientId) =>
    apiRequest(`/doctor/patients/${patientId}/history`),
  
  updatePatientHistory: (appointmentId, treatmentData) =>
    apiRequest(`/doctor/appointments/${appointmentId}/history`, {
      method: 'PUT',
      body: JSON.stringify(treatmentData)
    }),
  
  getAvailability: (startDate = '', endDate = '') => {
    const params = new URLSearchParams()
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    return apiRequest(`/doctor/availability?${params.toString()}`)
  },
  
  setAvailability: (slots) =>
    apiRequest('/doctor/availability', {
      method: 'POST',
      body: JSON.stringify({ slots })
    })
}

// Patient API
export const patientAPI = {
  getDashboard: () =>
    apiRequest('/patient/dashboard'),
  
  getProfile: () =>
    apiRequest('/patient/profile'),
  
  updateProfile: (profileData) =>
    apiRequest('/patient/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    }),
  
  getDeaprtment: () =>
    apiRequest('/patient/deaprtment'),
  
  getDoctorsBySpecialization: (specId) =>
    apiRequest(`/patient/deaprtment/${specId}/doctors`),
  
  getDoctorDetails: (doctorId) =>
    apiRequest(`/patient/doctors/${doctorId}`),
  
  getDoctorAvailability: (doctorId) =>
    apiRequest(`/patient/doctors/${doctorId}/availability`),
  
  getAppointments: (status = '', upcoming = false, past = false) => {
    const params = new URLSearchParams()
    if (status) params.append('status', status)
    if (upcoming) params.append('upcoming', 'true')
    if (past) params.append('past', 'true')
    return apiRequest(`/patient/appointments?${params.toString()}`)
  },
  
  bookAppointment: (appointmentData) =>
    apiRequest('/patient/appointments', {
      method: 'POST',
      body: JSON.stringify(appointmentData)
    }),
  
  cancelAppointment: (appointmentId) =>
    apiRequest(`/patient/appointments/${appointmentId}/cancel`, {
      method: 'POST'
    }),
  
  getHistory: () =>
    apiRequest('/patient/history'),
  
  searchDoctors: (search) =>
    apiRequest(`/patient/doctors/search?search=${encodeURIComponent(search)}`),
  
  triggerCSVExport: () =>
    apiRequest('/tasks/export-history', {
      method: 'POST'
    }),
  
  getCSVExportStatus: (taskId) =>
    apiRequest(`/tasks/export-history/${taskId}`)
}

// Export auth functions
export { getAuthToken, setAuthToken, removeAuthToken }

