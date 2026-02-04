# Face Recognition Attendance System

## Kantipur Engineering College - BCT 5th Semester Project

A complete attendance management system using facial recognition technology for automatic attendance marking.

---

## 🚀 Features

- **Face Recognition**: Automatic student identification using webcam
- **Real-time Attendance**: Mark attendance instantly with face detection
- **Three User Roles**: Admin, Teacher, and Student with different permissions
- **Dashboard Analytics**: Visual reports and attendance statistics
- **Email Notifications**: Automated alerts for low attendance
- **Export to Excel/PDF**: Generate reports for documentation
- **Manual Override**: Teachers can manually update attendance

---

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- MySQL 8.0 or higher
- Webcam for face recognition
- 4GB RAM minimum (8GB recommended)

### Required Software
- MySQL Server
- Python pip
- Git (optional)

---

## 🛠️ Installation Steps

### 1. Clone or Download the Project
```bash
cd /home/hacker/python
git clone <repository-url>
# OR download and extract the zip file
```

### 2. Create Virtual Environment
```bash
cd face_attendance_system
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: On Windows, you may need to install `dlib` separately:
```bash
pip install cmake
pip install dlib
```

### 4. Configure Database

#### Option A: Using MySQL Command Line
```bash
mysql -u root -p
CREATE DATABASE face_attendance_db;
EXIT;
```

Then import the schema:
```bash
mysql -u root -p face_attendance_db < database_schema.sql
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Create a new connection
3. Create a new schema named `face_attendance_db`
4. Open and execute `database_schema.sql`

### 5. Configure Application Settings

Edit `app.py` and update the following configurations:

```python
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password@localhost/face_attendance_db'

# Email Configuration (for notifications)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

**Important**: For Gmail, you need to generate an App Password:
1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate App Password for "Mail"

### 6. Create Required Directories
```bash
mkdir -p static/images/faces
```

### 7. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

---

## 👤 Default Login Credentials

| Role    | Username   | Password  |
|---------|------------|-----------|
| Admin   | admin      | admin123  |
| Teacher | teacher1   | admin123  |
| Student | student1   | admin123  |

---

## 📁 Project Structure

```
face_attendance_system/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── database_schema.sql       # MySQL database schema
├── README.md                 # This file
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── login.html           # Login page
│   ├── error.html           # Error page
│   ├── admin/               # Admin templates
│   │   ├── dashboard.html
│   │   ├── students.html
│   │   ├── teachers.html
│   │   ├── subjects.html
│   │   ├── reports.html
│   │   └── capture_face.html
│   ├── teacher/             # Teacher templates
│   │   ├── dashboard.html
│   │   ├── select_attendance.html
│   │   ├── take_attendance.html
│   │   └── reports.html
│   └── student/             # Student templates
│       ├── dashboard.html
│       └── attendance.html
└── static/                  # Static files
    └── images/faces/        # Student face images
```

---

## 🎯 Usage Guide

### Admin Features
1. **Dashboard**: View overall statistics and analytics
2. **Manage Students**: Add, edit, delete students
3. **Manage Teachers**: Add faculty members
4. **Manage Subjects**: Configure subjects for each section
5. **Reports**: Generate and export attendance reports

### Teacher Features
1. **Dashboard**: View assigned subjects and today's summary
2. **Take Attendance**: Manual or face recognition-based marking
3. **Reports**: View attendance analytics
4. **Send Alerts**: Notify students with low attendance

### Student Features
1. **Dashboard**: View personal attendance statistics
2. **My Attendance**: Complete attendance history

---

## 📊 Face Recognition Setup

### Capturing Student Faces
1. Login as Admin
2. Go to Students management
3. Click the camera icon next to a student
4. Allow camera access
5. Position face in frame and click "Capture"
6. Click "Save Face" to store the encoding

### Tips for Best Results
- Ensure good lighting (avoid backlight)
- Face the camera directly
- Keep a neutral expression
- Stay within the frame
- Remove glasses or hats if possible

---

## 📧 Email Notifications

The system sends automatic email alerts when a student's attendance drops below 75%. Configure email settings in `app.py` to enable this feature.

---

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL service is running
   - Verify database credentials in `app.py`
   - Ensure database schema is imported

2. **Face Recognition Not Working**
   - Check camera permissions
   - Ensure good lighting conditions
   - Verify face encoding is saved
   - Check tolerance settings in database

3. **Module Import Errors**
   - Reinstall requirements: `pip install -r requirements.txt`
   - Install dlib separately if on Windows

4. **Port Already in Use**
   - Change port in `app.py` or kill existing process
   ```bash
   # Linux/Mac
   lsof -ti:5000 | xargs kill -9
   ```

### Getting Help
- Check the console output for error messages
- Ensure all prerequisites are installed
- Verify database schema is properly imported

---

## 📝 License

This project is developed for educational purposes as part of the BCT 5th Semester curriculum at Kantipur Engineering College.

---

## 👨‍💻 Developed By

**Kantipur Engineering College**
- Department: Bachelor in Computer Technology (BCT)
- Semester: 5th Semester
- Sections: A and B

---

## 📞 Support

For questions or issues, please contact:
- College IT Department
- Project Supervisor

---

**Happy Coding! 🎓**
