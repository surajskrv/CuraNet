# Hospital Management System (HMS) - V2

A comprehensive web application for managing hospital operations with role-based access for Admins, Doctors, and Patients.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vue.js 3 with Vite
- **Database**: SQLite
- **Caching**: Redis
- **Task Queue**: Celery with Redis
- **Authentication**: JWT (Flask-JWT-Extended)
- **Styling**: Bootstrap 4

## Features

### Admin Features
- Dashboard with statistics (total doctors, patients, appointments)
- Manage doctors (CRUD operations, blacklist)
- Manage patients (view, edit, blacklist)
- View all appointments
- Search doctors and patients
- View patient treatment history

### Doctor Features
- Dashboard with today's and week's appointments
- View assigned patients
- Complete appointments and add treatment details
- Update patient history
- Set availability for next 7 days
- View patient full treatment history

### Patient Features
- Register and login
- View departments/deaprtment
- Browse doctors by specialization
- View doctor profiles and availability
- Book appointments
- Cancel appointments
- View treatment history
- Export treatment history as CSV

### Background Jobs
- **Daily Reminders**: Sends appointment reminders via email or Google Chat Webhook
- **Monthly Reports**: Sends activity reports to doctors via email
- **CSV Export**: Async export of patient treatment history

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 20+ and npm
- Redis server
- (Optional) SMTP server for email functionality

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start Redis server:**
```bash
# Windows (if installed)
redis-server

# Linux/Mac
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis
```

3. **Set up environment variables (optional):**
Create a `.env` file or set environment variables:
```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
GOOGLE_CHAT_WEBHOOK_URL=your_webhook_url
```

4. **Run the Flask application:**
```bash
python run.py
```
Or alternatively:
```bash
python -m backend.app
```
The backend will run on `http://localhost:5000`

**Note:** If Redis is not running, the application will automatically fall back to SimpleCache (in-memory caching). Background jobs (Celery) require Redis to be running.

5. **Start Celery worker (in a separate terminal):**
```bash
celery -A backend.app.celery worker --loglevel=info
```

6. **Start Celery beat for scheduled tasks (in a separate terminal):**
```bash
celery -A backend.app.celery beat --loglevel=info
```

**Note:** If Redis is not available, Celery workers will not start. The application will continue to work normally without background jobs.

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```
The frontend will run on `http://localhost:5173`

## Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

## Database

The database (`hospital.db`) will be created automatically when you first run the application. The admin user and default deaprtment are created programmatically.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Patient registration
- `POST /api/auth/login` - Login for all roles
- `GET /api/auth/me` - Get current user

### Admin
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/doctors` - List doctors (with search)
- `POST /api/admin/doctors` - Create doctor
- `PUT /api/admin/doctors/<id>` - Update doctor
- `DELETE /api/admin/doctors/<id>` - Blacklist doctor
- `GET /api/admin/patients` - List patients (with search)
- `PUT /api/admin/patients/<id>` - Update patient
- `DELETE /api/admin/patients/<id>` - Blacklist patient
- `GET /api/admin/appointments` - List all appointments

### Doctor
- `GET /api/doctor/dashboard` - Doctor dashboard
- `GET /api/doctor/appointments` - Doctor's appointments
- `POST /api/doctor/appointments/<id>/complete` - Complete appointment
- `POST /api/doctor/appointments/<id>/cancel` - Cancel appointment
- `GET /api/doctor/patients/<id>/history` - Patient history
- `POST /api/doctor/availability` - Set availability
- `GET /api/doctor/availability` - Get availability

### Patient
- `GET /api/patient/dashboard` - Patient dashboard
- `GET /api/patient/deaprtment` - List deaprtment
- `GET /api/patient/deaprtment/<id>/doctors` - Doctors by specialization
- `GET /api/patient/doctors/<id>/availability` - Doctor availability
- `POST /api/patient/appointments` - Book appointment
- `POST /api/patient/appointments/<id>/cancel` - Cancel appointment
- `GET /api/patient/history` - Treatment history
- `POST /api/tasks/export-history` - Trigger CSV export

## Project Structure

```
HospitalV2/
├── run.py                 # Application entry point (runs backend.app)
├── requirements.txt       # Python dependencies
├── backend/
│   ├── app.py            # Flask application factory
│   ├── models.py         # Database models
│   ├── config.py         # Configuration
│   ├── extensions.py     # Flask extensions
│   ├── utils.py          # Utility functions (with safe cache wrappers)
│   ├── routes/           # API routes
│   ├── tasks.py          # Celery tasks
│   ├── celeryInit.py     # Celery initialization
│   ├── mail.py           # Email utilities
│   └── createData.py     # Database initialization
├── frontend/
│   ├── src/
│   │   ├── pages/        # Vue pages
│   │   ├── layouts/      # Layout components
│   │   ├── services/     # API services
│   │   ├── router/       # Vue Router
│   │   └── App.vue       # Main app component
│   └── package.json      # Frontend dependencies
└── hospital.db           # SQLite database (created automatically)
```

## Notes

- The application uses JWT tokens for authentication. Tokens are stored in localStorage.
- Redis is used for caching and as a message broker for Celery.
- Make sure Redis is running before starting Celery workers.
- Email functionality requires proper SMTP configuration.
- For production, update the SECRET_KEY and JWT_SECRET_KEY in config.py.
- The database is created programmatically - no manual setup required.

## Development

- Backend API runs on port 5000
- Frontend dev server runs on port 5173
- CORS is enabled for localhost:5173
- All API endpoints are prefixed with `/api`

## Troubleshooting

1. **Redis connection error**: Make sure Redis is running on port 6379
2. **Database errors**: Delete `hospital.db` and restart the application
3. **Celery tasks not running**: Ensure both Celery worker and beat are running
4. **Email not sending**: Check SMTP configuration and credentials

