-- ============================================================================
-- Sample Data for Face Recognition Attendance System
-- Kantipur Engineering College - BCT 5th Semester
-- ============================================================================

USE face_attendance_db;

-- ============================================================================
-- Sample Students for Section A (25 Students)
-- ============================================================================

-- Password for all students: admin123 (hashed)
-- Username format: studentA01, studentA02, etc.

INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES
('studentA01', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA01@kec.edu.np', 'Aarav', 'Shrestha', 'student'),
('studentA02', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA02@kec.edu.np', 'Aayush', 'Pandey', 'student'),
('studentA03', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA03@kec.edu.np', 'Abhishek', 'Maharjan', 'student'),
('studentA04', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA04@kec.edu.np', 'Aditya', 'Khatri', 'student'),
('studentA05', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA05@kec.edu.np', 'Amit', 'Bhattarai', 'student'),
('studentA06', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA06@kec.edu.np', 'Ankit', 'Rajbanshi', 'student'),
('studentA07', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA07@kec.edu.np', 'Anmol', 'Khadka', 'student'),
('studentA08', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA08@kec.edu.np', 'Ashish', 'Nepal', 'student'),
('studentA09', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA09@kec.edu.np', 'Bibek', 'Sharma', 'student'),
('studentA10', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA10@kec.edu.np', 'Bikash', 'Gurung', 'student'),
('studentA11', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA11@kec.edu.np', 'Bishal', 'Basnet', 'student'),
('studentA12', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA12@kec.edu.np', 'Chetan', 'Poudel', 'student'),
('studentA13', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA13@kec.edu.np', 'Deepak', 'Khanal', 'student'),
('studentA14', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA14@kec.edu.np', 'Dilip', 'Rai', 'student'),
('studentA15', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA15@kec.edu.np', 'Gaurav', 'Dhakal', 'student'),
('studentA16', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA16@kec.edu.np', 'Harsh', 'Jha', 'student'),
('studentA17', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA17@kec.edu.np', 'Kiran', 'Limbu', 'student'),
('studentA18', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA18@kec.edu.np', 'Krishna', 'Bhandari', 'student'),
('studentA19', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA19@kec.edu.np', 'Manish', 'Tamang', 'student'),
('studentA20', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA20@kec.edu.np', 'Nabin', 'Karmacharya', 'student'),
('studentA21', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA21@kec.edu.np', 'Nischal', 'Pokhrel', 'student'),
('studentA22', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA22@kec.edu.np', 'Prabin', 'Adhikari', 'student'),
('studentA23', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA23@kec.edu.np', 'Prasanna', 'Chapain', 'student'),
('studentA24', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA24@kec.edu.np', 'Rahul', 'Thapa', 'student'),
('studentA25', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentA25@kec.edu.np', 'Rajesh', 'Hamal', 'student');

-- ============================================================================
-- Sample Students for Section B (25 Students)
-- ============================================================================

INSERT INTO users (username, password_hash, email, first_name, last_name, role) VALUES
('studentB01', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB01@kec.edu.np', 'Rohan', 'Malla', 'student'),
('studentB02', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB02@kec.edu.np', 'Roshan', 'Bajracharya', 'student'),
('studentB03', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB03@kec.edu.np', 'Sagar', 'Dongol', 'student'),
('studentB04', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB04@kec.edu.np', 'Sanjay', 'Pradhan', 'student'),
('studentB05', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB05@kec.edu.np', 'Santosh', 'Oli', 'student'),
('studentB06', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB06@kec.edu.np', 'Shreejal', 'Shakya', 'student'),
('studentB07', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB07@kec.edu.np', 'Shristi', 'Kunwar', 'student'),
('studentB08', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB08@kec.edu.np', 'Siddhant', 'Bajracharya', 'student'),
('studentB09', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB09@kec.edu.np', 'Sujan', 'Shrestha', 'student'),
('studentB10', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB10@kec.edu.np', 'Sunil', 'Mahato', 'student'),
('studentB11', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB11@kec.edu.np', 'Suraj', 'Yadav', 'student'),
('studentB12', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB12@kec.edu.np', 'Suresh', 'Aryal', 'student'),
('studentB13', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB13@kec.edu.np', 'Ujjwal', 'Giri', 'student'),
('studentB14', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB14@kec.edu.np', 'Utsav', 'Poudel', 'student'),
('studentB15', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB15@kec.edu.np', 'Varun', 'Regmi', 'student'),
('studentB16', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB16@kec.edu.np', 'Vikram', 'Singh', 'student'),
('studentB17', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB17@kec.edu.np', 'Yash', 'Kumar', 'student'),
('studentB18', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB18@kec.edu.np', 'Yuvraj', 'Sinha', 'student'),
('studentB19', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB19@kec.edu.np', 'Zeeshan', 'Miya', 'student'),
('studentB20', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB20@kec.edu.np', 'Alish', 'KC', 'student'),
('studentB21', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB21@kec.edu.np', 'Anish', 'Joshi', 'student'),
('studentB22', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB22@kec.edu.np', 'Barsha', 'Rana', 'student'),
('studentB23', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB23@kec.edu.np', 'Diya', 'Khatri', 'student'),
('studentB24', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB24@kec.edu.np', 'Elina', 'Bajracharya', 'student'),
('studentB25', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi', 'studentB25@kec.edu.np', 'Gauri', 'Sharma', 'student');

-- ============================================================================
-- Create Student Records with Section A (IDs 1-25)
-- ============================================================================

INSERT INTO students (user_id, student_id, section_id, roll_number, parent_email) VALUES
(4, '020BCT001', 1, 1, 'parentA01@email.com'),
(5, '020BCT002', 1, 2, 'parentA02@email.com'),
(6, '020BCT003', 1, 3, 'parentA03@email.com'),
(7, '020BCT004', 1, 4, 'parentA04@email.com'),
(8, '020BCT005', 1, 5, 'parentA05@email.com'),
(9, '020BCT006', 1, 6, 'parentA06@email.com'),
(10, '020BCT007', 1, 7, 'parentA07@email.com'),
(11, '020BCT008', 1, 8, 'parentA08@email.com'),
(12, '020BCT009', 1, 9, 'parentA09@email.com'),
(13, '020BCT010', 1, 10, 'parentA10@email.com'),
(14, '020BCT011', 1, 11, 'parentA11@email.com'),
(15, '020BCT012', 1, 12, 'parentA12@email.com'),
(16, '020BCT013', 1, 13, 'parentA13@email.com'),
(17, '020BCT014', 1, 14, 'parentA14@email.com'),
(18, '020BCT015', 1, 15, 'parentA15@email.com'),
(19, '020BCT016', 1, 16, 'parentA16@email.com'),
(20, '020BCT017', 1, 17, 'parentA17@email.com'),
(21, '020BCT018', 1, 18, 'parentA18@email.com'),
(22, '020BCT019', 1, 19, 'parentA19@email.com'),
(23, '020BCT020', 1, 20, 'parentA20@email.com'),
(24, '020BCT021', 1, 21, 'parentA21@email.com'),
(25, '020BCT022', 1, 22, 'parentA22@email.com'),
(26, '020BCT023', 1, 23, 'parentA23@email.com'),
(27, '020BCT024', 1, 24, 'parentA24@email.com'),
(28, '020BCT025', 1, 25, 'parentA25@email.com');

-- ============================================================================
-- Create Student Records with Section B (IDs 26-50)
-- ============================================================================

INSERT INTO students (user_id, student_id, section_id, roll_number, parent_email) VALUES
(29, '020BCT026', 2, 1, 'parentB01@email.com'),
(30, '020BCT027', 2, 2, 'parentB02@email.com'),
(31, '020BCT028', 2, 3, 'parentB03@email.com'),
(32, '020BCT029', 2, 4, 'parentB04@email.com'),
(33, '020BCT030', 2, 5, 'parentB05@email.com'),
(34, '020BCT031', 2, 6, 'parentB06@email.com'),
(35, '020BCT032', 2, 7, 'parentB07@email.com'),
(36, '020BCT033', 2, 8, 'parentB08@email.com'),
(37, '020BCT034', 2, 9, 'parentB09@email.com'),
(38, '020BCT035', 2, 10, 'parentB10@email.com'),
(39, '020BCT036', 2, 11, 'parentB11@email.com'),
(40, '020BCT037', 2, 12, 'parentB12@email.com'),
(41, '020BCT038', 2, 13, 'parentB13@email.com'),
(42, '020BCT039', 2, 14, 'parentB14@email.com'),
(43, '020BCT040', 2, 15, 'parentB15@email.com'),
(44, '020BCT041', 2, 16, 'parentB16@email.com'),
(45, '020BCT042', 2, 17, 'parentB17@email.com'),
(46, '020BCT043', 2, 18, 'parentB18@email.com'),
(47, '020BCT044', 2, 19, 'parentB19@email.com'),
(48, '020BCT045', 2, 20, 'parentB20@email.com'),
(49, '020BCT046', 2, 21, 'parentB21@email.com'),
(50, '020BCT047', 2, 22, 'parentB22@email.com'),
(51, '020BCT048', 2, 23, 'parentB23@email.com'),
(52, '020BCT049', 2, 24, 'parentB24@email.com'),
(53, '020BCT050', 2, 25, 'parentB25@email.com');

-- ============================================================================
-- Sample Attendance Records (Last 10 days)
-- Subject 1 = DBMS, Section A
-- ============================================================================

-- Generate sample attendance for 10 days
-- Using a stored procedure approach or manual inserts

INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time, marked_by, is_manual_override) VALUES
-- Day 1 (10 days ago)
(1, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:05:00', 2, 0),
(2, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:02:00', 2, 0),
(3, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'absent', NULL, 2, 1),
(4, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:10:00', 2, 0),
(5, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:01:00', 2, 0),
(6, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'late', '08:25:00', 2, 1),
(7, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:03:00', 2, 0),
(8, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:04:00', 2, 0),
(9, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'absent', NULL, 2, 1),
(10, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'present', '08:06:00', 2, 0),
-- Day 2
(1, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:00:00', 2, 0),
(2, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:05:00', 2, 0),
(3, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:10:00', 2, 0),
(4, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:02:00', 2, 0),
(5, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'absent', NULL, 2, 1),
(6, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:03:00', 2, 0),
(7, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:01:00', 2, 0),
(8, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'late', '08:30:00', 2, 1),
(9, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:04:00', 2, 0),
(10, 1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'present', '08:05:00', 2, 0),
-- Continue for more students and days... (simplified for sample)

-- Day 3
(1, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:02:00', 2, 0),
(2, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:03:00', 2, 0),
(3, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:01:00', 2, 0),
(4, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'absent', NULL, 2, 1),
(5, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:04:00', 2, 0),
(6, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:02:00', 2, 0),
(7, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'late', '08:20:00', 2, 1),
(8, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:05:00', 2, 0),
(9, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:01:00', 2, 0),
(10, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'present', '08:03:00', 2, 0);

-- ============================================================================
-- Add More Sample Attendance (Last 7 days)
-- ============================================================================

-- Generate more records for demonstration
INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time, marked_by, is_manual_override) 
SELECT 
    s.id,
    1,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 7) DAY),
    ELT(FLOOR(1 + RAND() * 3), 'present', 'absent', 'late'),
    TIME_ADD('08:00:00', INTERVAL FLOOR(RAND() * 30) MINUTE),
    2,
    0
FROM students s
WHERE s.section_id = 1
LIMIT 100;

-- ============================================================================
-- Verify Data
-- ============================================================================

SELECT 'Users created:' as info, COUNT(*) as count FROM users;
SELECT 'Students created:' as info, COUNT(*) as count FROM students;
SELECT 'Attendance records:' as info, COUNT(*) as count FROM attendance;
