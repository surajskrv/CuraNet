# **CuraNet - Hospital Management System**

A comprehensive web application for managing hospital operations, streamlining interactions between **Admins**, **Doctors**, and **Patients**. Built with a modern tech stack ensuring performance, security, and ease of use.

---

## 🚀 **Tech Stack**

**Frontend:** Vue.js 3 (Options API), Vite, Vue Router  
**Styling:** Bootstrap 5, Bootstrap Icons  
**Backend:** Flask (Python 3.10+)  
**Database:** SQLite (Development), SQLAlchemy ORM  
**Authentication:** Flask-Security (Token-based Auth)  
**Caching & Tasks:** Redis & Celery (Optional for background tasks)

---

## 🌟 **Features**

### 🛡️ **Admin Module**

- **Interactive Dashboard:** Real-time statistics on doctors, patients, and appointments.  
- **Doctor Management:** Onboard doctors, assign departments, view profiles, blacklist accounts.  
- **Patient Management:** View patient records, contact details, manage access.  
- **Department Management:** Create and manage hospital departments/specializations.  
- **Appointment Oversight:** View all hospital appointments with filtering.

---

### 👨‍⚕️ **Doctor Module**

- **Physician Dashboard:** Today’s schedule, upcoming appointments, assigned patients.  
- **Appointment Management:** Complete appointments, add diagnoses, prescriptions, notes.  
- **Patient History:** Access detailed medical history of treated patients.  
- **Availability Scheduler:** Visual interface to set availability for next 7 days.

---

### 🏥 **Patient Module**

- **User Portal:** Register, login, and manage personal profile.  
- **Book Appointments:** Browse doctors by department, check availability, book slots.  
- **Medical History:** View past treatments, prescriptions, diagnoses.  
- **Export Data:** Download treatment history as CSV.  
- **Appointment Management:** View and cancel upcoming schedules.

---

## 🛠️ **Setup Instructions**

### **Prerequisites**

- Python 3.8+  
- Node.js 16+ and npm  
- Redis (Optional)

---

## **1. Backend Setup (Flask)**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize DB & Create Admin
python run.py
```

## **2. Frontend Setup (Flask)**

```bash
 cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 📝 License
This project is open-source under the MIT License.
