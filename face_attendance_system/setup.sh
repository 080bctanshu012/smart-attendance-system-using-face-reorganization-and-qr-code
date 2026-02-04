#!/bin/bash

echo "=========================================="
echo "Face Recognition Attendance System Setup"
echo "=========================================="

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Please install it first:"
    echo "  sudo apt update"
    echo "  sudo apt install mysql-server"
    exit 1
fi

echo ""
echo "Step 1: Starting MySQL..."
sudo service mysql start

echo ""
echo "Step 2: Creating database..."
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS face_attendance_db;
USE face_attendance_db;

-- Create Sections
CREATE TABLE IF NOT EXISTS sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Users
CREATE TABLE IF NOT EXISTS users (
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

-- Create Subjects
CREATE TABLE IF NOT EXISTS subjects (
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

-- Create Students
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    section_id INT NOT NULL,
    roll_number INT,
    phone VARCHAR(15),
    parent_email VARCHAR(100),
    face_encoding BLOB,
    face_image_path VARCHAR(255),
    enrollment_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Attendance
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    class_date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'excused') NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    marked_by INT,
    face_recognition_confidence FLOAT,
    is_manual_override BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (marked_by) REFERENCES users(id),
    UNIQUE KEY unique_attendance (student_id, subject_id, class_date)
);

-- Insert Sections
INSERT INTO sections (name, description) VALUES 
('A', 'Section A - 25 Students'),
('B', 'Section B - 25 Students');

-- Insert Admin (password: admin123)
INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES 
('admin', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'admin@kec.edu.np', 'System', 'Admin', 'admin');

-- Insert Teachers
INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES 
('teacher1', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'teacher1@kec.edu.np', 'Ram', 'Sharma', 'teacher'),
('teacher2', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'teacher2@kec.edu.np', 'Shyam', 'Pandey', 'teacher');

-- Insert Sample Students (Section A)
INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES
('studentA01', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA01@kec.edu.np', 'Aarav', 'Shrestha', 'student'),
('studentA02', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA02@kec.edu.np', 'Aayush', 'Pandey', 'student'),
('studentA03', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA03@kec.edu.np', 'Abhishek', 'Maharjan', 'student');

-- Create Student Records
INSERT INTO students (user_id, student_id, section_id, roll_number) VALUES
(3, '020BCT001', 1, 1),
(4, '020BCT002', 1, 2),
(5, '020BCT003', 1, 3);

-- Insert Subjects
INSERT INTO subjects (subject_code, subject_name, credit_hours, teacher_id, section_id) VALUES
('BCT501', 'Database Management Systems (DBMS)', 3, 2, 1),
('BCT502', 'Computer Networks (CN)', 3, 2, 1),
('BCT503', 'Software Engineering (SE)', 3, 3, 1);

SELECT 'Setup completed successfully!' AS status;
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Login Credentials:"
echo "  Admin:   admin / admin123"
echo "  Teacher: teacher1 / admin123"
echo "  Student: studentA01 / admin123"
echo ""
echo "Camera Access Requirements:"
echo "  Camera access requires a secure context (HTTPS or localhost)."
echo ""
echo "Option 1 - Use localhost (recommended for development):"
echo "  python app.py"
echo "  Then open: http://localhost:5000"
echo ""
echo "Option 2 - Enable HTTPS (for network access):"
echo "  FLASK_ENABLE_HTTPS=true python app.py"
echo "  Then open: https://localhost:5000"
echo "  (Use https://YOUR_IP:5000 for network access)"
echo ""
echo "Note: For HTTPS mode, you'll need to accept the self-signed certificate warning in your browser."
