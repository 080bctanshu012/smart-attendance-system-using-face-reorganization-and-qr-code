-- ============================================================================
-- Face Recognition Attendance System - Database Schema
-- Kantipur Engineering College - BCT 5th Semester, Section A & B
-- Database: MySQL
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS face_attendance_db;
USE face_attendance_db;

-- ============================================================================
-- Table: Users (Admin, Teacher, Student)
-- ============================================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('admin', 'teacher', 'student') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: Sections (A and B)
-- ============================================================================
CREATE TABLE sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL, -- 'A' or 'B'
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: Subjects (5th Semester Subjects)
-- ============================================================================
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    credit_hours INT DEFAULT 3,
    teacher_id INT,
    section_id INT,
    FOREIGN KEY (teacher_id) REFERENCES users(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: Students (Additional student information)
-- ============================================================================
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    student_id VARCHAR(20) UNIQUE NOT NULL, -- College ID
    section_id INT NOT NULL,
    roll_number INT,
    phone VARCHAR(15),
    parent_email VARCHAR(100),
    face_encoding LONGBLOB, -- Store face encoding data
    face_image_path VARCHAR(255), -- Path to face image
    enrollment_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: Classes (Schedule for classes)
-- ============================================================================
CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    section_id INT NOT NULL,
    teacher_id INT NOT NULL,
    day_of_week INT NOT NULL, -- 1=Monday, 2=Tuesday, etc.
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (teacher_id) REFERENCES users(id),
    UNIQUE KEY unique_class (subject_id, section_id, day_of_week, start_time)
);

-- ============================================================================
-- Table: Attendance (Attendance records)
-- ============================================================================
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    class_date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'excused') NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    marked_by INT, -- Teacher/Admin who marked
    face_recognition_confidence FLOAT, -- Confidence score from face recognition
    is_manual_override BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (marked_by) REFERENCES users(id),
    UNIQUE KEY unique_attendance (student_id, subject_id, class_date)
);

-- ============================================================================
-- Table: Attendance Sessions (For tracking live attendance)
-- ============================================================================
CREATE TABLE attendance_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    section_id INT NOT NULL,
    teacher_id INT NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME,
    is_active BOOLEAN DEFAULT TRUE,
    total_students INT DEFAULT 0,
    present_count INT DEFAULT 0,
    absent_count INT DEFAULT 0,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- ============================================================================
-- Table: Email Notifications Log
-- ============================================================================
CREATE TABLE email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT NOT NULL,
    recipient_email VARCHAR(100) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    body TEXT,
    notification_type ENUM('attendance_alert', 'low_attendance', 'daily_report', 'other') NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('sent', 'failed', 'pending') DEFAULT 'sent',
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);

-- ============================================================================
-- Table: System Settings
-- ============================================================================
CREATE TABLE system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(50) UNIQUE NOT NULL,
    setting_value VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- Insert Default Data
-- ============================================================================

-- Insert Sections
INSERT INTO sections (name, description) VALUES
('A', 'Section A - 25 Students'),
('B', 'Section B - 25 Students');

-- Insert Admin User (password: admin123 - will be hashed in application)
INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'admin@kec.edu.np', 'System', 'Admin', 'admin');

-- Insert Teachers
INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES
('teacher1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'teacher1@kec.edu.np', 'Ram', 'Sharma', 'teacher'),
('teacher2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'teacher2@kec.edu.np', 'Shyam', 'Pandey', 'teacher'),
('teacher3', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'teacher3@kec.edu.np', 'Hari', 'Bhatta', 'teacher');

-- Insert Subjects (5th Semester)
INSERT INTO subjects (subject_code, subject_name, credit_hours, teacher_id, section_id) VALUES
('BCT501', 'Database Management Systems (DBMS)', 3, 2, 1),
('BCT502', 'Computer Networks (CN)', 3, 2, 1),
('BCT503', 'Software Engineering (SE)', 3, 3, 1),
('BCT504', 'Operating Systems (OS)', 3, 4, 1),
('BCT505', 'Artificial Intelligence (AI)', 3, 3, 1),
('BCT501', 'Database Management Systems (DBMS)', 3, 2, 2),
('BCT502', 'Computer Networks (CN)', 3, 2, 2),
('BCT503', 'Software Engineering (SE)', 3, 3, 2),
('BCT504', 'Operating Systems (OS)', 3, 4, 2),
('BCT505', 'Artificial Intelligence (AI)', 3, 3, 2);

-- Insert System Settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('min_attendance_percentage', '75', 'Minimum attendance percentage required'),
('attendance_alert_threshold', '80', 'Send alert when attendance drops below this percentage'),
('college_name', 'Kantipur Engineering College', 'Name of the institution'),
('department', 'Bachelor in Computer Technology (BCT)', 'Department name'),
('semester', '5th', 'Current semester'),
('email_notifications_enabled', 'true', 'Enable email notifications'),
('face_recognition_tolerance', '0.6', 'Face recognition tolerance (lower = more strict)');

-- ============================================================================
-- Create Indexes for Performance
-- ============================================================================
CREATE INDEX idx_attendance_date ON attendance(class_date);
CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_attendance_subject ON attendance(subject_id);
CREATE INDEX idx_students_section ON students(section_id);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_sessions_date ON attendance_sessions(session_date);

-- ============================================================================
-- Create Views for Common Queries
-- ============================================================================

-- View: Student Attendance Summary
CREATE OR REPLACE VIEW v_student_attendance_summary AS
SELECT 
    s.student_id,
    CONCAT(u.first_name, ' ', u.last_name) as student_name,
    sec.name as section,
    sub.subject_code,
    sub.subject_name,
    COUNT(a.id) as total_classes,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present_count,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) as absent_count,
    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(a.id)) * 100, 2) as attendance_percentage
FROM students s
JOIN users u ON s.user_id = u.id
JOIN sections sec ON s.section_id = sec.id
JOIN attendance a ON s.id = a.student_id
JOIN subjects sub ON a.subject_id = sub.id
GROUP BY s.id, sub.id;

-- View: Daily Attendance Report
CREATE OR REPLACE VIEW v_daily_attendance AS
SELECT 
    a.class_date,
    sec.name as section,
    sub.subject_code,
    sub.subject_name,
    COUNT(DISTINCT s.id) as total_students,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present_count,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) as absent_count,
    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(DISTINCT s.id)) * 100, 2) as attendance_percentage
FROM attendance a
JOIN students s ON a.student_id = s.id
JOIN sections sec ON s.section_id = sec.id
JOIN subjects sub ON a.subject_id = sub.id
GROUP BY a.class_date, sec.id, sub.id;

-- ============================================================================
-- End of Schema
-- ============================================================================
