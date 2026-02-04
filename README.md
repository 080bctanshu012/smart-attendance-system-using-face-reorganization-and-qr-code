# smart-attendance-system-using-face-reorganization-and-qr-code
# Face Attendance System 
# By :- Anshu Shah , Lokesh Chand , Bishal Joshi , Anubhav Zha

A web-based attendance management system for Kantipur Engineering College using face recognition and QR codes.

## What is this?

This project is made for BCT 5th Semester. It lets teachers take attendance using face scan or QR code. Students can mark their own attendance by scanning a QR code that the teacher displays.

## Features

### For Teachers
- Generate QR codes for their subjects
- Take attendance using face camera
- View attendance reports
- Send alerts to students

### For Students
- View their own QR code
- Mark attendance by scanning teacher's QR code
- View their attendance history
- See alerts from teachers

### For Admin
- Manage all users (teachers, students)
- Manage subjects and sections
- Capture face data for students

## How to Install

1. First, make sure you have Python installed (version 3.x)

2. Install the required packages:
   ```
   pip install -r face_attendance_system/requirements.txt
   ```

   This will install:
   - flask - for the web server
   - face-recognition - for face detection
   - opencv-python - for camera access
   - qrcode - for generating QR codes
   - numpy - for math operations

3. If face-recognition gives error, you may need to install cmake first:
   ```
   pip install cmake
   ```

## How to Run

1. Open terminal and go to the project folder:
   ```
   cd face_attendance_system
   ```

2. Run the app:
   ```
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Demo Accounts

Use these to test the system:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | teacher1 | admin123 |
| Student | student1 | student123 |

Note: These are just demo accounts. You can add more users through the admin panel.

## Project Structure

```
face_attendance_system/
├── app.py                    # Main Flask application
├── database_schema.sql       # Database structure
├── requirements.txt         # Python packages needed
├── setup.sh                 # Setup script for Linux/Mac
├── instance/
   └── attendance.db        # SQLite database file
├── static/
   ├── images/faces/        # Stored face images
   └── qr/                  # Generated QR codes
├── templates/
   ├── admin/               # Admin panel pages
   ├── student/             # Student pages
   ├── teacher/             # Teacher pages
   ├── base.html            # Base template
   └── login.html           # Login page
└── ssl/                     # SSL certificates for HTTPS
```

## Database Tables

The system uses SQLite with these tables:

- **user** - stores all users (admins, teachers, students)
- **student** - student details linked to user
- **subject** - subjects taught by teachers
- **section** - class sections (A, B, etc.)
- **attendance** - daily attendance records
- **qr_sessions** - active QR session codes
- **alerts** - messages from teachers to students

## Technical Details

- Built with Flask (Python web framework)
- Database: SQLite (no server needed)
- Face recognition using dlib library
- QR codes generated with session codes
- Location validation for QR attendance (KEC campus)
- HTTPS support available (set FLASK_ENABLE_HTTPS=true)

## Common Issues

**Camera not working?**
- Check if camera is connected
- Make sure no other app is using the camera
- Try running as admin/sudo

**Face recognition not accurate?**
- Good lighting is important
- Face should be clearly visible
- Try different angles

**QR code not scanning?**
- Adjust screen brightness
- Hold phone steady
- Make sure QR code is fully visible

## Credits

Made for BCT 5th Semester project at Kantipur Engineering College.
