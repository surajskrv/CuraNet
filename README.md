# CuraNet - Hospital Management System

CuraNet is a comprehensive web application designed to streamline hospital operations. It facilitates interaction between **Administrators**, **Doctors**, and **Patients**, providing a unified platform for appointment booking, medical record management, and hospital administration.

## 🚀 Tech Stack

### Frontend
- **Framework:** Vue.js 3
- **Build Tool:** Vite
- **Routing:** Vue Router
- **Styling:** Bootstrap 5 & Bootstrap Icons
- **HTTP Client:** Fetch API

### Backend
- **Framework:** Flask (Python)
- **Database:** SQLite (Development), SQLAlchemy ORM
- **Authentication:** Flask-Security (Token-based Auth & Hashing)
- **API:** RESTful endpoints

---

## 🌟 Key Features

### 🛡️ Admin Module
- **Dashboard:** Real-time statistics on doctors, patients, and appointment status.
- **Doctor Management:** Onboard new doctors, assign departments, and manage profiles.
- **Patient Management:** View registered patients and manage access.
- **Department Management:** Create and organize hospital departments (e.g., Cardiology, Neurology).
- **Appointment Oversight:** View all hospital appointments with filtering capabilities.

### 👨‍⚕️ Doctor Module
- **Dashboard:** View daily/weekly schedules and upcoming appointments.
- **Availability Management:** Set specific working hours (Morning/Evening slots) for the next 7 days.
- **Consultation:** Complete appointments by adding diagnoses, prescriptions, and notes.
- **Patient History:** Access the medical history of treated patients.

### 🏥 Patient Module
- **Online Booking:** Search doctors by department or name and book available time slots.
- **Medical Profile:** Manage personal details and emergency contacts.
- **Treatment History:** View past diagnoses and prescriptions.
- **Appointment Management:** Reschedule or cancel upcoming bookings.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ & npm

### 1. Backend Setup (Flask)

1.  Navigate to the root directory.
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    cd backend
    
    pip install -r backend/requirements.txt

    # Linux
    pip3 install -r backend/requirements.txt --break-system-packages
    ```
4.  Run the application (this will automatically seed the database with default data):
    ```bash
    python -m backend.app
    ```
    *The backend runs at `http://127.0.0.1:5000`*

### 2. Frontend Setup (Vue.js)

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    *The frontend runs at `http://localhost:5173`*

---

## Default Credentials

The application initializes with the following default accounts for testing:

| Role      | Email              | Password      |
| :-------- | :----------------- | :------------ |
| **Admin** | `admin@gmail.com`  | `helloadmin`  |

---

## 📂 Project Structure

```bash
CuraNet/
├── backend/
│   ├── routes/             # API endpoints (admin, auth, doctor, patient)
│   ├── models.py           # Database models
│   ├── createData.py       # Data seeding script
│   └── app.py              # Flask app factory
├── frontend/
│   ├── src/
│   │   ├── pages/          # Vue views (Admin, Doctor, Patient)
│   │   ├── layouts/        # Page layouts
│   │   └── services/       # API integration
│   └── vite.config.js      # Vite config
├── instance/               # SQLite database

└── run.py                  # Entry point
