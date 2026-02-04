"""
Face Recognition Attendance System - PURE SQL VERSION
Kantipur Engineering College - BCT 5th Semester

This version uses RAW SQL instead of SQLAlchemy ORM
"""

import sqlite3
import os
import cv2
import numpy as np
import face_recognition
import qrcode
import json
import pickle
import base64
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
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'instance', 'attendance.db')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('ssl', exist_ok=True)
os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

# ============================================================================
# DATABASE CONNECTION (SQLite)
# ============================================================================

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================================
# DATABASE SETUP (CREATE TABLES WITH SQL)
# ============================================================================

def init_database():
    """Initialize database with tables using SQLite"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create USER table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            role VARCHAR(20) NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    # Create SECTION table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS section (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(10) NOT NULL UNIQUE,
            description VARCHAR(255)
        )
    """)
    
    # Create SUBJECT table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code VARCHAR(20) NOT NULL UNIQUE,
            subject_name VARCHAR(100) NOT NULL,
            credit_hours INTEGER DEFAULT 3,
            teacher_id INTEGER,
            section_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES user(id),
            FOREIGN KEY (section_id) REFERENCES section(id)
        )
    """)
    
    # Create STUDENT table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            student_id VARCHAR(20) NOT NULL UNIQUE,
            section_id INTEGER NOT NULL,
            roll_number INTEGER,
            face_encoding BLOB,
            face_image_path VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (section_id) REFERENCES section(id)
        )
    """)
    
    # Create ATTENDANCE table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            class_date TEXT NOT NULL,
            status VARCHAR(20) NOT NULL,
            check_in_time TEXT,
            face_confidence FLOAT,
            is_manual INTEGER DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES student(id),
            FOREIGN KEY (subject_id) REFERENCES subject(id)
        )
    """)
    
    # Create ALERTS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            subject_id INTEGER,
            section_id INTEGER,
            message TEXT NOT NULL,
            alert_type VARCHAR(20) DEFAULT 'general',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES user(id),
            FOREIGN KEY (subject_id) REFERENCES subject(id),
            FOREIGN KEY (section_id) REFERENCES section(id)
        )
    """)
    
    conn.commit()
    
    # Create default data
    cursor.execute("SELECT COUNT(*) FROM section")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO section (name, description) VALUES ('A', 'Section A - 25 Students')")
        cursor.execute("INSERT INTO section (name, description) VALUES ('B', 'Section B - 25 Students')")
    
    # Migration: Set is_active = 1 for all users (fix NULL values)
    cursor.execute("UPDATE user SET is_active = 1 WHERE is_active IS NULL")
    
    cursor.execute("SELECT COUNT(*) FROM user WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO user (username, password_hash, email, first_name, last_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, ('admin', generate_password_hash('admin123'), 'admin@kec.edu.np', 'System', 'Admin', 'admin'))
        
        cursor.execute("""
            INSERT INTO user (username, password_hash, email, first_name, last_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, ('teacher1', generate_password_hash('admin123'), 'teacher1@kec.edu.np', 'Ram', 'Sharma', 'teacher'))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized with SQLite!")

# ============================================================================
# HELPER FUNCTIONS (USING SQL)
# ============================================================================

def execute_query(query, params=None, fetch=False):
    """Execute a SQL query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    cursor = conn.cursor()
    
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
    result = execute_query("SELECT * FROM user WHERE id = ?", (user_id,))
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
        # is_active is handled by UserMixin (defaults to True)
    
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
            "SELECT * FROM user WHERE username = ? AND is_active = 1",
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

@app.route('/student/my-qr')
@login_required
def my_qr():
    if current_user.role != 'student':
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get student by user_id
    student = execute_query(
        "SELECT s.*, u.username, u.email, u.first_name, u.last_name, sec.name as section_name "
        "FROM student s "
        "JOIN user u ON s.user_id = u.id "
        "JOIN section sec ON s.section_id = sec.id "
        "WHERE s.user_id = ?",
        (current_user.id,)
    )
    
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # Generate QR code path
    qr_path = f"static/qr/student_{student['id']}.png"
    qr_full_path = os.path.join(os.path.dirname(__file__), qr_path)
    
    # Generate QR code if it doesn't exist
    if not os.path.exists(qr_full_path):
        os.makedirs(os.path.dirname(qr_full_path), exist_ok=True)
        qr_data = json.dumps({
            'student_id': student['id'],
            'student_user_id': current_user.id,
            'student_code': student['student_id'],
            'name': f"{student['first_name']} {student['last_name']}"
        })
        qr = qrcode.make(qr_data)
        qr.save(qr_full_path)
    
    return render_template('student/my_qr.html', student=student, qr_path=qr_path)

@app.route('/student/qr-attendance')
@login_required
def qr_attendance():
    if current_user.role != 'student':
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get student ID
    student = execute_query(
        "SELECT id, student_id FROM student WHERE user_id = ?",
        (current_user.id,)
    )
    
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # KEC Campus location (Dhapakhel, Lalitpur)
    campus_lat = 27.6635
    campus_lng = 85.3161
    
    return render_template('student/qr_attendance.html',
                         student_id=student['id'],
                         student_code=student['student_id'],
                         campus_lat=campus_lat,
                         campus_lng=campus_lng,
                         allowed_radius=200)

@app.route('/teacher/generate-qr')
@login_required
def generate_qr():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    subjects = execute_query_all(
        "SELECT * FROM subject WHERE teacher_id = ?",
        (current_user.id,)
    )
    sections = execute_query_all("SELECT * FROM section")
    
    return render_template('teacher/generate_qr.html', subjects=subjects, sections=sections)

@app.route('/teacher/show-qr')
@login_required
def show_qr_code():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    subject_id = request.args.get('subject_id')
    section_id = request.args.get('section_id')
    expiry_minutes = int(request.args.get('expiry', 30))
    
    if not subject_id or not section_id:
        flash('Please select subject and section', 'warning')
        return redirect(url_for('generate_qr'))
    
    # Get subject and section info
    subject = execute_query("SELECT * FROM subject WHERE id = ?", (subject_id,))
    section = execute_query("SELECT * FROM section WHERE id = ?", (section_id,))
    
    if not subject or not section:
        flash('Invalid subject or section', 'danger')
        return redirect(url_for('generate_qr'))
    
    # Generate random session code
    import secrets
    session_code = secrets.token_hex(16)
    
    # Store session in database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete any existing active sessions for this subject/section today
    cursor.execute("""
        DELETE FROM qr_sessions 
        WHERE subject_id = ? AND section_id = ? 
        AND expires_at > datetime('now')
    """, (subject_id, section_id))
    
    # Insert new session
    from datetime import datetime, timedelta
    expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
    
    cursor.execute("""
        INSERT INTO qr_sessions (session_code, subject_id, section_id, teacher_id, created_at, expires_at)
        VALUES (?, ?, ?, ?, datetime('now'), ?)
    """, (session_code, subject_id, section_id, current_user.id, expires_at.strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    
    # Create QR data with session code
    qr_data = json.dumps({
        'type': 'attendance_session',
        'session_code': session_code,
        'subject_id': subject_id,
        'section_id': section_id,
        'subject_name': subject['subject_name'],
        'expires_at': expires_at.isoformat()
    })
    
    # Generate QR code
    qr = qrcode.make(qr_data)
    import io
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()
    
    return render_template('teacher/qr_display.html',
                         qr_image=f"data:image/png;base64,{qr_b64}",
                         subject=subject,
                         section=section,
                         expires_at=expires_at,
                         expiry_minutes=expiry_minutes)

@app.route('/student/mark-qr-attendance', methods=['POST'])
@login_required
def mark_qr_attendance():
    if current_user.role != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    student_id = request.form.get('student_id')
    session_code = request.form.get('session_code')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    # Verify the student owns this request
    student = execute_query(
        "SELECT s.id, s.section_id FROM student s WHERE s.user_id = ? AND s.id = ?",
        (current_user.id, student_id)
    )
    
    if not student:
        return jsonify({'success': False, 'message': 'Invalid student'})
    
    # Validate session code
    session = execute_query(
        """SELECT * FROM qr_sessions 
           WHERE session_code = ? AND is_active = 1 
           AND expires_at > datetime('now')""",
        (session_code,)
    )
    
    if not session:
        return jsonify({'success': False, 'message': 'Invalid or expired QR code. Please ask teacher for a new QR code.'})
    
    subject_id = session['subject_id']
    section_id = session['section_id']
    
    # Verify student belongs to this section
    if student['section_id'] != section_id:
        return jsonify({'success': False, 'message': 'You are not enrolled in this section.'})
    
    # Verify location is within campus (KEC: 27.6635, 85.3161)
    campus_lat = 27.6635
    campus_lng = 85.3161
    allowed_radius = 200  # meters
    
    from math import radians, sin, cos, sqrt, atan2
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth's radius in meters
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    try:
        user_lat = float(latitude)
        user_lng = float(longitude)
        distance = haversine(user_lat, user_lng, campus_lat, campus_lng)
        
        if distance > allowed_radius:
            return jsonify({
                'success': False, 
                'message': f"❌ You're out of location! You are {int(distance)}m away from campus (max: {allowed_radius}m). Please move closer to KEC campus."
            })
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid location data'})
    
    today = date.today()
    current_time = datetime.now().time()
    
    # Check existing attendance
    existing = execute_query(
        "SELECT id FROM attendance WHERE student_id = ? AND subject_id = ? AND class_date = ?",
        (student_id, subject_id, today)
    )
    
    if existing:
        return jsonify({'success': False, 'message': 'Attendance already marked for today'})
    
    # Get subject name
    subject = execute_query("SELECT subject_name FROM subject WHERE id = ?", (subject_id,))
    
    # Insert attendance
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time, is_manual, latitude, longitude)
        VALUES (?, ?, ?, 'present', ?, 0, ?, ?)
    """, (student_id, subject_id, today, current_time, latitude, longitude))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True, 
        'message': '✅ Attendance marked successfully for ' + (subject['subject_name'] if subject else 'Unknown'),
        'subject_name': subject['subject_name'] if subject else 'Unknown'
    })

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
            "SELECT COUNT(*) as count FROM attendance WHERE class_date = ? AND status = 'present'",
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
            "SELECT * FROM subject WHERE teacher_id = ?",
            (current_user.id,)
        )
        return render_template('teacher/dashboard.html', subjects=subjects)
    
    else:  # student
        # SQL QUERY: Get student by user_id
        student = execute_query(
            "SELECT * FROM student WHERE user_id = ?",
            (current_user.id,)
        )
        
        if not student:
            flash('Student profile not found', 'danger')
            return redirect(url_for('dashboard'))
        
        # SQL QUERY: Get all attendance for student
        attendance_records = execute_query_all(
            "SELECT * FROM attendance WHERE student_id = ? ORDER BY class_date DESC",
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
            subject = execute_query("SELECT * FROM subject WHERE id = ?", (record['subject_id'],))
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
        
        # Get alerts count for student
        alerts_count = execute_query("SELECT COUNT(*) as count FROM alerts")['count']
        
        return render_template('student/dashboard.html',
                             student=student,
                             total_classes=total_classes,
                             present_count=present_count,
                             absent_count=absent_count,
                             attendance_percentage=attendance_percentage,
                             subject_attendance=subject_attendance,
                             alerts_count=alerts_count)

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
            INSERT INTO user (username, password_hash, email, first_name, last_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, 'student', 1)
        """, (username, hashed_password, email, first_name, last_name))
        
        user_id = cursor.lastrowid
        
        # SQL INSERT: Create student
        cursor.execute("""
            INSERT INTO student (user_id, student_id, section_id, roll_number)
            VALUES (?, ?, ?, ?)
        """, (user_id, student_id, section_id, roll_number))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Student added successfully', 'success')
    
    # SQL QUERY: Get all students with user info
    students = execute_query_all("""
        SELECT s.*, u.username, u.email, u.first_name, u.last_name, sec.name as section_name
        FROM student s
        JOIN user u ON s.user_id = u.id
        LEFT JOIN section sec ON s.section_id = sec.id
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
    student = execute_query("SELECT * FROM student WHERE id = ?", (student_id,))
    
    if student:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL DELETE: Delete attendance records first
        cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
        
        # SQL DELETE: Delete student
        cursor.execute("DELETE FROM student WHERE id = ?", (student_id,))
        
        # SQL DELETE: Delete user
        cursor.execute("DELETE FROM user WHERE id = ?", (student['user_id'],))
        
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
            INSERT INTO user (username, password_hash, email, first_name, last_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, 'teacher', 1)
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
    subjects = execute_query_all("SELECT * FROM subject WHERE teacher_id = ?", (current_user.id,))
    sections = execute_query_all("SELECT * FROM section")
    
    subject_id = request.args.get('subject_id') or request.form.get('subject_id')
    section_id = request.args.get('section_id') or request.form.get('section_id')
    
    if subject_id and section_id:
        # SQL QUERIES: Get subject and section
        subject = execute_query("SELECT * FROM subject WHERE id = ?", (subject_id,))
        section = execute_query("SELECT * FROM section WHERE id = ?", (section_id,))
        
        if subject and section:
            # SQL QUERY: Get students in section
            students = execute_query_all(
                "SELECT * FROM student WHERE section_id = ?",
                (section_id,)
            )
            
            # Get today's attendance
            today = date.today()
            attendance_dict = {}
            
            for student in students:
                # SQL QUERY: Check if student has attendance
                attendance = execute_query("""
                    SELECT * FROM attendance 
                    WHERE student_id = ? AND subject_id = ? AND class_date = ?
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
        WHERE student_id = ? AND subject_id = ? AND class_date = ?
    """, (student_id, subject_id, today))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if existing:
        # SQL UPDATE: Update existing attendance
        cursor.execute("""
            UPDATE attendance 
            SET status = ?, is_manual = 1
            WHERE id = ?
        """, (status, existing['id']))
    else:
        # SQL INSERT: Create new attendance
        cursor.execute("""
            INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time, is_manual)
            VALUES (?, ?, ?, ?, ?, 1)
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
        "SELECT * FROM student WHERE user_id = ?",
        (current_user.id,)
    )
    
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get attendance records
    attendance = execute_query_all("""
        SELECT * FROM attendance 
        WHERE student_id = ? 
        ORDER BY class_date DESC
    """, (student['id'],))
    
    return render_template('student/attendance.html', attendance=attendance)

@app.route('/capture-face/<int:student_id>', methods=['GET', 'POST'])
@login_required
def capture_face(student_id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('dashboard'))
    
    # SQL QUERY: Get student
    student = execute_query("SELECT * FROM student WHERE id = ?", (student_id,))
    
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
                        SET face_encoding = ?, face_image_path = ?
                        WHERE id = ?
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
        try:
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
        finally:
            camera.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/teacher/face-attendance', methods=['GET', 'POST'])
@login_required
def face_attendance():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    subjects = execute_query_all("SELECT * FROM subject WHERE teacher_id = ?", (current_user.id,))
    sections = execute_query_all("SELECT * FROM section")
    
    subject_id = request.args.get('subject_id') or request.form.get('subject_id')
    section_id = request.args.get('section_id') or request.form.get('section_id')
    
    if subject_id and section_id:
        subject = execute_query("SELECT * FROM subject WHERE id = ?", (subject_id,))
        section = execute_query("SELECT * FROM section WHERE id = ?", (section_id,))
        
        if subject and section:
            # Get students with face encodings
            students = execute_query_all("""
                SELECT s.*, u.username, u.email, u.first_name, u.last_name
                FROM student s
                JOIN user u ON s.user_id = u.id
                WHERE s.section_id = ? AND s.face_encoding IS NOT NULL AND s.face_encoding != ''
            """, (section_id,))
            
            return render_template('teacher/face_attendance.html',
                                subject=subject, section=section,
                                students=students)
    
    return render_template('teacher/select_attendance.html', subjects=subjects, sections=sections)

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
            VALUES (?, ?, ?, ?, ?)
        """, (subject_code, subject_name, credit_hours, teacher_id, section_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Subject added successfully', 'success')
    
    # SQL QUERIES
    subjects = execute_query_all("""
        SELECT sub.*, u.first_name as teacher_first_name, u.last_name as teacher_last_name, sec.name as section_name
        FROM subject sub
        LEFT JOIN user u ON sub.teacher_id = u.id
        LEFT JOIN section sec ON sub.section_id = sec.id
    """)
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



@app.route('/teacher/add-class', methods=['GET', 'POST'])
@login_required
def add_class():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        class_date = request.form.get('class_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        # TODO: Add class/time to database
        flash('Class scheduled successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    subjects = execute_query_all("SELECT * FROM subject WHERE teacher_id = ?", (current_user.id,))
    return render_template('teacher/add_class.html', subjects=subjects)

@app.route('/teacher/reports')
@login_required
def teacher_reports():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    # Get teacher's subjects
    subjects = execute_query_all("SELECT * FROM subject WHERE teacher_id = ?", (current_user.id,))
    
    return render_template('teacher/reports.html', subjects=subjects)

@app.route('/teacher/send-alerts', methods=['GET', 'POST'])
@login_required
def send_alerts():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        section_id = request.form.get('section_id')
        message = request.form.get('message')
        alert_type = request.form.get('alert_type')
        
        # Save alert to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (teacher_id, subject_id, section_id, message, alert_type)
            VALUES (?, ?, ?, ?, ?)
        """, (current_user.id, subject_id, section_id, message, alert_type))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Alert sent successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    subjects = execute_query_all("SELECT * FROM subject WHERE teacher_id = ?", (current_user.id,))
    sections = execute_query_all("SELECT * FROM section")
    return render_template('teacher/send_alerts.html', subjects=subjects, sections=sections)



@app.route('/student/alerts')
@login_required
def student_alerts():
    if current_user.role != 'student':
        return redirect(url_for('dashboard'))
    
    # Get student's section
    student = execute_query("SELECT * FROM student WHERE user_id = ?", (current_user.id,))
    
    if student:
        # Get all alerts (show alerts from all sections)
        alerts = execute_query_all("""
            SELECT a.*, u.first_name as teacher_name, u.last_name as teacher_last_name
            FROM alerts a
            JOIN user u ON a.teacher_id = u.id
            ORDER BY a.created_at DESC
            LIMIT 50
        """)
    else:
        alerts = []
    
    return render_template('student/alerts.html', alerts=alerts)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
