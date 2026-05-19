# 🎓 Faculty Appraisal System

A Django-based web application designed to manage and evaluate faculty performance efficiently. This system allows faculty members to submit their appraisal details while administrators can review, approve/reject, and generate reports.

---

## 🚀 Features

- 🔐 Authentication System (Login/Signup)
- 🧑‍🏫 Faculty Dashboard
- 🛠️ Admin Dashboard
- 📄 Appraisal Submission System
- ✅ Approval / Rejection Workflow
- 💬 Remarks & Feedback System
- 📊 PDF Report Generation
- 📱 Fully Responsive UI
- 🎨 Modern and Clean Design

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Others:** Django Templates, Static Files

---

## 📂 Project Structure
Faculty_Appraisal_System/
│
├── Faculty_Appraisal_System/ # Project settings
├── FAS/ # Main app
├── Templates/ # HTML files
├── static/ # CSS, JS, Images
├── manage.py
└── db.sqlite3

---

## ⚙️ Setup Instructions

1. Clone the repository:
  ```bash
  git clone https://github.com/tanishayadav28/faculty-appraisal-system.git
  ```
2. Go to project directory:
      cd faculty-appraisal-system
3. Install required packages:
     pip install -r requirements.txt
4. Apply migrations:
     python manage.py migrate
5. Run the server:
     python manage.py runserver

🔑 Admin Access

Create admin user:
    python manage.py createsuperuser
    
   


