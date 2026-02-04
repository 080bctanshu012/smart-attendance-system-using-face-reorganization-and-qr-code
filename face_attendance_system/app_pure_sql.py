"""
Face Recognition Attendance System - PURE SQL VERSION
Kantipur Engineering College - BCT 5th Semester

This version uses RAW SQL instead of SQLAlchemy ORM
"""

import os
import cv2
import numpy as np
import face_recognition
import qrcode
import json
import pickle
import base64
import mysql.connector
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================================
# Configuration
# ============================================================================

SSL_CERT_FILE = 'ssl/cert.pem'
SSL_KEY_FILE = 'ssl/key.pem'
ENABLE_HTTPS = os.environ.get('FLASK_ENABLE_HTTPS', 'false').lower() == 'true'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'face-attendance-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'static/images/faces'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('ssl', exist_ok=True)

# ============================================================================
# DATABASE CONNECTION (PURE SQL)
# ============================================================================

def get_db_connection():
    """Create and return a database connection"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='attendance_db'
    )
    return conn

# ============================================================================
# DATABASE SETUP (CREATE TABLES WITH SQL)
# ============================================================================

def init_database():
    """Initialize database with tables using raw SQL"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create USER table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            role VARCHAR(20) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Create SECTION table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS section (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(10) NOT NULL UNIQUE,
            description VARCHAR(255)
        )
    """)
    
    # Create SUBJECT table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject_code VARCHAR(20) NOT NULL UNIQUE,
            subject_name VARCHAR(100) NOT NULL,
            credit_hours INT DEFAULT 3,
            teacher_id INT,
            section_id INT,
            FOREIGN KEY (teacher_id) REFERENCES user(id),
            FOREIGN KEY (section_id) REFERENCES section(id)
        )
    """)
    
    # Create STUDENT table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL UNIQUE,
            student_id VARCHAR(20) NOT NULL UNIQUE,
            section_id INT NOT NULL,
            roll_number INT,
            face_encoding BLOB,
            face_image_path VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (section_id) REFERENCES section(id)
        )
    """)
    
    # Create ATTENDANCE table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            subject_id INT NOT NULL,
            class_date DATE NOT NULL,
            status VARCHAR(20) NOT NULL,
            check_in_time TIME,
            face_confidence FLOAT,
            is_manual BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (student_id) REFERENCES student(id),
            FOREIGN KEY (subject_id) REFERENCES subject(id)
        )
    """)
    
    # Create default data
    cursor.execute("SELECT COUNT(*) FROM section")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO section (name, description) VALUES ('A', 'Section A - 25 Students')")
        cursor.execute("INSERT INTO section (name, description) VALUES ('B', 'Section B - 25 Students')")
    
    cursor.execute("SELECT COUNT(*) FROM user WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO user (username, password_hash, email, first_name, last_name, role)
            VALUES ('admin', %s, 'admin@kec.edu.np', 'System', 'Admin', 'admin')
        """, (generate_password_hash('admin123'),))
        
        cursor.execute("""
            INSERT INTO user (username, password_hash, email, first_name, last_name, role)
            VALUES ('teacher1', %s, 'teacher1@kec.edu.np', 'Ram', 'Sharma', 'teacher')
        """, (generate_password_hash('admin123'),))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized with pure SQL!")

# ============================================================================
# HELPER FUNCTIONS (USING SQL)
# ============================================================================

def execute_query(query, params=None, fetch=False):
    """Execute a SQL query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    if fetch:
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    conn.close()
    return result

def execute_query_all(query, params=None):
    """Execute a SQL query and return all results"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# ============================================================================
# LOGIN MANAGER
# ============================================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID using SQL"""
    result = execute_query("SELECT * FROM user WHERE id = %s", (user_id,))
    if result:
        return User(result)
    return None

class User(UserMixin):
    """User class using dictionary data from SQL"""
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password_hash = data['password_hash']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.role = data['role']
        self.is_active = data['is_active']
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # SQL QUERY: Get user by username
        user_data = execute_query(
            "SELECT * FROM user WHERE username = %s AND is_active = TRUE",
            (username,)
        )
        
        if user_data:
            user = User(user_data)
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        # SQL QUERIES for admin dashboard
        total_students = execute_query("SELECT COUNT(*) as count FROM student")['count']
        total_teachers = execute_query("SELECT COUNT(*) as count FROM user WHERE role = 'teacher'")['count']
        total_subjects = execute_query("SELECT COUNT(*) as count FROM subject")['count']
        today = date.today()
        present_today = execute_query(
            "SELECT COUNT(*) as count FROM attendance WHERE class_date = %s AND status = 'present'",
            (today,)
        )['count']
        
        return render_template('admin/dashboard.html',
                             total_students=total_students,
                             total_teachers=total_teachers,
                             total_subjects=total_subjects,
                             total_today=total_students,
                             present_today=present_today)
    
    elif current_user.role == 'teacher':
        # SQL QUERY: Get subjects for teacher
        subjects = execute_query_all(
            "SELECT * FROM subject WHERE teacher_id = %s",
            (current_user.id,)
        )
        return render_template('teacher/dashboard.html', subjects=subjects)
    
    else:  # student
        # SQL QUERY: Get student by user_id
        student = execute_query(
            "SELECT * FROM student WHERE user_id = %s",
            (current_user.id,)
        )
        
        if not student:
            flash('Student profile not found', 'danger')
            return redirect(url_for('dashboard'))
        
        # SQL QUERY: Get all attendance for student
        attendance_records = execute_query_all(
            "SELECT * FROM attendance WHERE student_id = %s ORDER BY class_date DESC",
            (student['id'],)
        )
        
        # Calculate stats using Python
        total_classes = len(attendance_records)
        present_count = sum(1 for a in attendance_records if a['status'] == 'present')
        absent_count = sum(1 for a in attendance_records if a['status'] == 'absent')
        attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        # Get subject-wise attendance
        subject_attendance = {}
        for record in attendance_records:
            # SQL QUERY: Get subject name
            subject = execute_query("SELECT * FROM subject WHERE id = %s", (record['subject_id'],))
            if subject:
                code = subject['subject_code']
                if code not in subject_attendance:
                    subject_attendance[code] = {
                        'subject_name': subject['subject_name'],
                        'present': 0,
                        'total': 0
                    }
                subject_attendance[code]['total'] += 1
                if record['status'] == 'present':
                    subject_attendance[code]['present'] += 1
        
        return render_template('student/dashboard.html',
                             student=student,
                             total_classes=total_classes,
                             present_count=present_count,
                             absent_count=absent_count,
                             attendance_percentage=attendance_percentage,
                             subject_attendance=subject_attendance)

@app.route('/admin/students', methods=['GET', 'POST'])
@login_required
def manage_students():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        student_id = request.form.get('student_id')
        section_id = request.form.get('section_id')
        roll_number = request.form.get('roll_number')
        
        # SQL INSERT: Create user
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user (username, password_hash, email, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s, 'student')
        """, (username, hashed_password, email, first_name, last_name))
        
        user_id = cursor.lastrowid
        
        # SQL INSERT: Create student
        cursor.execute("""
            INSERT INTO student (user_id, student_id, section_id, roll_number)
            VALUES (%s, %s, %s, %s)
        """, (user_id, student_id, section_id, roll_number))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Student added successfully', 'success')
    
    # SQL QUERY: Get all students with user info
    students = execute_query_all("""
        SELECT s.*, u.username, u.email, u.first_name, u.last_name
        FROM student s
        JOIN user u ON s.user_id = u.id
    """)
    
    # SQL QUERY: Get all sections
    sections = execute_query_all("SELECT * FROM section")
    
    return render_template('admin/students.html', students=students, sections=sections)

@app.route('/admin/student/delete/<int:student_id>')
@login_required
def delete_student(student_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get student
    student = execute_query("SELECT * FROM student WHERE id = %s", (student_id,))
    
    if student:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL DELETE: Delete attendance records first
        cursor.execute("DELETE FROM attendance WHERE student_id = %s", (student_id,))
        
        # SQL DELETE: Delete student
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        
        # SQL DELETE: Delete user
        cursor.execute("DELETE FROM user WHERE id = %s", (student['user_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Student deleted successfully', 'success')
    else:
        flash('Student not found', 'danger')
    
    return redirect(url_for('manage_students'))

@app.route('/admin/teachers', methods=['GET', 'POST'])
@login_required
def manage_teachers():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user (username, password_hash, email, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s, 'teacher')
        """, (username, hashed_password, email, first_name, last_name))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Teacher added successfully', 'success')
    
    # SQL QUERY: Get all teachers
    teachers = execute_query_all("SELECT * FROM user WHERE role = 'teacher'")
    
    return render_template('admin/teachers.html', teachers=teachers)

@app.route('/teacher/attendance', methods=['GET', 'POST'])
@login_required
def take_attendance():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    # SQL QUERIES
    subjects = execute_query_all("SELECT * FROM subject WHERE teacher_id = %s", (current_user.id,))
    sections = execute_query_all("SELECT * FROM section")
    
    subject_id = request.args.get('subject_id') or request.form.get('subject_id')
    section_id = request.args.get('section_id') or request.form.get('section_id')
    
    if subject_id and section_id:
        # SQL QUERIES: Get subject and section
        subject = execute_query("SELECT * FROM subject WHERE id = %s", (subject_id,))
        section = execute_query("SELECT * FROM section WHERE id = %s", (section_id,))
        
        if subject and section:
            # SQL QUERY: Get students in section
            students = execute_query_all(
                "SELECT * FROM student WHERE section_id = %s",
                (section_id,)
            )
            
            # Get today's attendance
            today = date.today()
            attendance_dict = {}
            
            for student in students:
                # SQL QUERY: Check if student has attendance
                attendance = execute_query("""
                    SELECT * FROM attendance 
                    WHERE student_id = %s AND subject_id = %s AND class_date = %s
                """, (student['id'], subject_id, today))
                
                if attendance:
                    attendance_dict[student['id']] = attendance
            
            return render_template('teacher/take_attendance.html',
                                 subject=subject, section=section,
                                 students=students, attendance_dict=attendance_dict)
    
    return render_template('teacher/select_attendance.html', subjects=subjects, sections=sections)

@app.route('/teacher/manual-attendance', methods=['POST'])
@login_required
def manual_attendance():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    student_id = request.form.get('student_id')
    subject_id = request.form.get('subject_id')
    status = request.form.get('status')
    today = date.today()
    current_time = datetime.now().time()
    
    # SQL QUERY: Check existing attendance
    existing = execute_query("""
        SELECT * FROM attendance 
        WHERE student_id = %s AND subject_id = %s AND class_date = %s
    """, (student_id, subject_id, today))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if existing:
        # SQL UPDATE: Update existing attendance
        cursor.execute("""
            UPDATE attendance 
            SET status = %s, is_manual = TRUE
            WHERE id = %s
        """, (status, existing['id']))
    else:
        # SQL INSERT: Create new attendance
        cursor.execute("""
            INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time, is_manual)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (student_id, subject_id, today, status, current_time))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Attendance marked!', 'success')
    return redirect(url_for('take_attendance', subject_id=subject_id))

@app.route('/student/attendance')
@login_required
def my_attendance():
    if current_user.role != 'student':
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get student
    student = execute_query(
        "SELECT * FROM student WHERE user_id = %s",
        (current_user.id,)
    )
    
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get attendance records
    attendance = execute_query_all("""
        SELECT * FROM attendance 
        WHERE student_id = %s 
        ORDER BY class_date DESC
    """, (student['id'],))
    
    return render_template('student/attendance.html', attendance=attendance)

@app.route('/capture-face/<int:student_id>', methods=['GET', 'POST'])
@login_required
def capture_face(student_id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get student
    student = execute_query("SELECT * FROM student WHERE id = %s", (student_id,))
    
    if request.method == 'POST':
        image_data = request.form.get('image_data')
        if image_data:
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            filename = f"student_{student_id}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            # Generate face encoding
            try:
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    # Convert encoding to binary
                    encoding_binary = pickle.dumps(encodings[0])
                    
                    # SQL UPDATE: Store face encoding
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        UPDATE student 
                        SET face_encoding = %s, face_image_path = %s
                        WHERE id = %s
                    """, (encoding_binary, filepath, student_id))
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    flash('Face captured successfully!', 'success')
                else:
                    flash('No face detected. Try again.', 'danger')
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
    
    return render_template('admin/capture_face.html', student=student)

@app.route('/video-feed')
def video_feed():
    def generate():
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                break
            frame = cv2.flip(frame, 1)
            
            # Detect faces
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        camera.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin/subjects', methods=['GET', 'POST'])
@login_required
def manage_subjects():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        subject_code = request.form.get('subject_code')
        subject_name = request.form.get('subject_name')
        credit_hours = request.form.get('credit_hours')
        teacher_id = request.form.get('teacher_id')
        section_id = request.form.get('section_id')
        
        # SQL INSERT: Create subject
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO subject (subject_code, subject_name, credit_hours, teacher_id, section_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (subject_code, subject_name, credit_hours, teacher_id, section_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Subject added successfully', 'success')
    
    # SQL QUERIES
    subjects = execute_query_all("SELECT * FROM subject")
    teachers = execute_query_all("SELECT * FROM user WHERE role = 'teacher'")
    sections = execute_query_all("SELECT * FROM section")
    
    return render_template('admin/subjects.html', subjects=subjects, teachers=teachers, sections=sections)

@app.route('/admin/reports')
@login_required
def admin_reports():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    # SQL QUERIES
    total_students = execute_query("SELECT COUNT(*) as count FROM student")['count']
    total_teachers = execute_query("SELECT COUNT(*) as count FROM user WHERE role = 'teacher'")['count']
    total_subjects = execute_query("SELECT COUNT(*) as count FROM subject")['count']
    
    # Get attendance stats
    attendance = execute_query_all("SELECT * FROM attendance")
    present_count = sum(1 for a in attendance if a['status'] == 'present')
    absent_count = sum(1 for a in attendance if a['status'] == 'absent')
    
    return render_template('admin/reports.html',
                         total_students=total_students,
                         total_teachers=total_teachers,
                         total_subjects=total_subjects,
                         present_count=present_count,
                         absent_count=absent_count)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
