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
<img width="1470" alt="Screenshot 2025-04-20 at 12 32 17 PM" src="https://github.com/user-attachments/assets/77acd912-ad22-4f64-89d2-65fc1890122e" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 32 57 PM" src="https://github.com/user-attachments/assets/fe315fb6-7d8a-4777-b87e-c8d86707f9f4" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 33 02 PM" src="https://github.com/user-attachments/assets/4c43bd9e-37e5-49e9-b9ae-f0a6c02af73d" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 32 33 PM" src="https://github.com/user-attachments/assets/ffffab39-0271-4fcb-9cbb-3440431157de" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 32 52 PM" src="https://github.com/user-attachments/assets/0c6e4bd3-8120-418f-8fc7-5b2c352ce47b" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 33 25 PM" src="https://github.com/user-attachments/assets/a1ab7db9-4159-4f33-b03f-ccfff13dc3e7" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 33 36 PM" src="https://github.com/user-attachments/assets/e5b67230-1192-4569-9177-942d7063177b" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 33 51 PM" src="https://github.com/user-attachments/assets/17155fae-d9a7-4645-8fcd-774aae1b073e" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 33 56 PM" src="https://github.com/user-attachments/assets/eec4fb1c-6f82-4dc8-a0ed-09de70933c9a" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 34 12 PM" src="https://github.com/user-attachments/assets/149bc57c-7018-4f95-8de4-50ba137fa641" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 34 18 PM" src="https://github.com/user-attachments/assets/4b674798-a6ea-456a-b9e8-5dfe17bd9285" />

<img width="1470" alt="Screenshot 2025-04-20 at 12 34 24 PM" src="https://github.com/user-attachments/assets/0bcb9655-6ad3-4a08-9cb5-7b00d2209d10" />

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
   git clone https://github.com/nanyatrivedi/HostelManagementSystem.git
