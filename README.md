# Hostel Management System

A web-based Hostel Management System for managing student information, mess allocation, fee status, and complaints with admin oversight.

## 🚀 Features

- Student registration and login
- Admin login and dashboard
- Complaint registration and resolution tracking
- Mess information view for students
- Fee status view and admin update
- Admin dashboard with custom SQL query runner
- Password reset functionality

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python (Flask)
- **Database**: Oracle SQL
- **Tools**: cx_Oracle, Jinja2 template engine

## 📸 Screenshots

(Add screenshots here if you want. Just drag & drop images after pushing.)

## 🧠 How It Works

- Flask handles routing, templating, and session management.
- Oracle SQL is used to manage all backend data (students, mess, fees, complaints).
- Admin dashboard shows all student data, unpaid fees, and unresolved complaints.
- Only SELECT queries are allowed in the custom SQL interface to prevent data corruption.

## 🔐 Security

- Passwords validated on frontend and backend.
- Admin-only access for sensitive actions.
- `.env` file used to hide credentials (in local version).

## 📁 Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/HostelManagementSystem.git
