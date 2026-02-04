# Face Recognition Attendance System - DBMS Perspective

## Complete Data Flow from Python to SQL and Back

---

## Table of Contents
1. [DBMS Architecture Overview](#dbms-architecture-overview)
2. [Python to SQL Connection](#python-to-sql-connection)
3. [Two Approaches: ORM vs Pure SQL](#two-approaches-orm-vs-pure-sql)
4. [Data Flow: Python → SQL (INSERT)](#data-flow-python--sql-insert)
5. [Data Flow: SQL → Python (SELECT)](#data-flow-sql--python-select)
6. [How Face Encoding Works](#how-face-encoding-works)
7. [Complete Attendance Flow](#complete-attendance-flow)
8. [SQL Queries Explained](#sql-queries-explained)
9. [Database Relationships](#database-relationships)
10. [Pure SQL Examples](#pure-sql-examples)

---

## DBMS Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PYTHON LAYER                           │   │
│  │  - Flask routes (app.py)                                 │   │
│  │  - Face recognition logic                                │   │
│  │  - QR code generation                                    │   │
│  │  - User authentication                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               SQLALCHEMY ORM LAYER                        │   │
│  │  - Converts Python objects to SQL                        │   │
│  │  - Converts SQL results to Python objects                 │   │
│  │  - Handles database operations                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 MYSQL/SQLITE DATABASE                    │   │
│  │  - Stores all data in tables                             │   │
│  │  - Handles queries                                       │   │
│  │  - Manages relationships                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Two Approaches: ORM vs Pure SQL

### Approach 1: SQLAlchemy ORM (Original)
Uses Python objects instead of writing SQL directly:

```python
# Connect to database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Define model (automatically creates table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))

# Query (Python code, SQL is generated automatically)
user = User.query.filter_by(username='admin').first()
students = Student.query.filter_by(section_id=1).all()
```

**Advantages:**
- Write Python instead of SQL
- Database agnostic (works with MySQL, PostgreSQL, SQLite)
- Automatic table creation
- Type safety

**Disadvantages:**
- Hides SQL from you (not good for learning DBMS)
- Less control over queries
- Performance overhead

---

### Approach 2: Pure SQL (For DBMS Project) ✅ RECOMMENDED
Write SQL queries directly:

```python
# Connect to database directly
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='attendance_db'
)
cursor = conn.cursor(dictionary=True)

# Write SQL query directly
cursor.execute("SELECT * FROM user WHERE username = %s", ('admin',))
user = cursor.fetchone()

# Close connection
cursor.close()
conn.close()
```

**Advantages:**
- You learn SQL properly
- Full control over queries
- Better performance
- Understand database fundamentals

**Disadvantages:**
- More code to write
- Database-specific syntax
- Manual connection management

---

### Comparison Table

| Feature | ORM (SQLAlchemy) | Pure SQL |
|---------|------------------|----------|
| **Code Style** | Python objects | SQL queries |
| **Learning DBMS** | ❌ Poor | ✅ Good |
| **Query Control** | Limited | Full |
| **Database Portability** | ✅ Yes | ❌ No |
| **Development Speed** | ✅ Fast | ❌ Slower |
| **Performance** | Slight overhead | ✅ Optimal |

---

### Example: Login Query Comparison

```python
# ==================== ORM APPROACH ====================
# SQLAlchemy generates SQL automatically
user = User.query.filter_by(username=username, is_active=True).first()

# Generated SQL (hidden from you):
# SELECT * FROM user WHERE username = ? AND is_active = ? LIMIT 1

# ==================== PURE SQL APPROACH ====================
# You write SQL directly
cursor.execute("""
    SELECT * FROM user 
    WHERE username = %s AND is_active = TRUE 
    LIMIT 1
""", (username,))
user = cursor.fetchone()
```

---

### Example: Get All Students in Section

```python
# ==================== ORM APPROACH ====================
students = Student.query.filter_by(section_id=1).all()

# Generated SQL:
# SELECT * FROM student WHERE section_id = 1

# ==================== PURE SQL APPROACH ====================
cursor.execute(
    "SELECT * FROM student WHERE section_id = %s", 
    (1,)
)
students = cursor.fetchall()
```

---

### Example: Insert New Student

```python
# ==================== ORM APPROACH ====================
student = Student(
    user_id=5,
    student_id='075BCT001',
    section_id=1,
    roll_number=5
)
db.session.add(student)
db.session.commit()

# ==================== PURE SQL APPROACH ====================
cursor.execute("""
    INSERT INTO student (user_id, student_id, section_id, roll_number)
    VALUES (%s, %s, %s, %s)
""", (5, '075BCT001', 1, 5))
conn.commit()
```

---

### Which Approach to Use?

| Your Goal | Use This |
|-----------|----------|
| **Learn DBMS/SQL** | Pure SQL ✅ |
| **Semester Project** | Pure SQL ✅ |
| **Production App** | ORM (SQLAlchemy) |
| **Rapid Development** | ORM (SQLAlchemy) |
| **Job Interview** | Both (know both!) |

---

## Python to SQL Connection

### Step 1: Database Connection Setup

```python
# Python Code (app.py)
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/attendance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SQLAlchemy instance (this creates the connection)
db = SQLAlchemy(app)
```

**What happens here:**
1. Flask creates the web application
2. SQLAlchemy reads the database URI
3. SQLAlchemy establishes connection to MySQL
4. Connection is stored in `db` object
5. This connection is used for all database operations

### Step 2: Database URI Format

```
mysql+pymysql://username:password@host/database_name
```

| Part | Example | Meaning |
|------|---------|---------|
| `mysql` | Database type | We're using MySQL |
| `pymysql` | Driver | PyMySQL connector |
| `root` | Username | MySQL username |
| `password` | Password | MySQL password |
| `localhost` | Host | Database server address |
| `attendance_db` | Database name | Database to use |

---

## Data Flow: Python → SQL (INSERT)

### Example: Adding a New Student

```
┌──────────────────────────────────────────────────────────────────┐
│                      PYTHON CODE                                  │
│  student = Student(                                               │
│      user_id=5,                                                   │
│      student_id="075BCT001",                                      │
│      section_id=1,                                                │
│      roll_number=5                                                 │
│  )                                                                │
│  db.session.add(student)                                         │
│  db.session.commit()                                              │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    SQLALCHEMY ORM TRANSLATES                      │
│                                                                  │
│  INSERT INTO student (user_id, student_id, section_id, roll_number)
│  VALUES (5, '075BCT001', 1, 5)                                   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      MYSQL DATABASE                              │
│                                                                  │
│  student table:                                                   │
│  ┌────┬─────────┬──────────────┬─────────────┬────────────┐     │
│  │ id │ user_id │ student_id   │ section_id  │ roll_number│     │
│  ├────┼─────────┼──────────────┼─────────────┼────────────┤     │
│  │ 1  │    5    │ 075BCT001    │      1      │     5      │     │
│  └────┴─────────┴──────────────┴─────────────┴────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process:

1. **Python Object Creation**
   ```python
   # Student object is created in Python memory
   student = Student(user_id=5, student_id="075BCT001", section_id=1, roll_number=5)
   ```

2. **Add to Session**
   ```python
   # Object is added to SQLAlchemy session (not yet in database)
   db.session.add(student)
   ```

3. **ORM Translation**
   ```python
   # SQLAlchemy converts object to SQL query
   # SELECT * FROM student WHERE id = LAST_INSERT_ID()
   ```

4. **Database Execution**
   ```python
   # Query is sent to MySQL
   # INSERT INTO student VALUES (NULL, 5, '075BCT001', 1, 5, NULL, NULL)
   ```

5. **Commit**
   ```python
   # Changes are permanently saved
   db.session.commit()
   ```

---

## Data Flow: SQL → Python (SELECT)

### Example: Fetching Student Data

```
┌──────────────────────────────────────────────────────────────────┐
│                      PYTHON CODE                                  │
│                                                                  │
│  student = Student.query.filter_by(student_id="075BCT001").first()│
│  print(student.first_name)                                       │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    SQLALCHEMY ORM TRANSLATES                     │
│                                                                  │
│  SELECT * FROM student WHERE student_id = '075BCT001' LIMIT 1   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      MYSQL DATABASE                               │
│                                                                  │
│  Query executed on student table                                 │
│  Results returned to Python                                      │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    PYTHON RECEIVES DATA                          │
│                                                                  │
│  student = <Student object>                                      │
│  - student.id = 1                                               │
│  - student.user_id = 5                                           │
│  - student.student_id = "075BCT001"                             │
│  - student.face_encoding = <binary data>                        │
└──────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process:

1. **Python Query**
   ```python
   # Create query in Python
   query = Student.query.filter_by(student_id="075BCT001")
   ```

2. **ORM Translation**
   ```python
   # SQLAlchemy converts to SQL
   # SELECT * FROM student WHERE student_id = '075BCT001'
   ```

3. **Database Execution**
   ```python
   # Query sent to MySQL
   # Results returned as rows
   ```

4. **ORM Object Creation**
   ```python
   # SQLAlchemy converts row to Python object
   # student = Student(id=1, user_id=5, student_id="075BCT001", ...)
   ```

5. **Use Data**
   ```python
   # Now we can use the object in Python
   print(student.first_name)  # Output: "John"
   ```

---

## How Face Encoding Works

### Face Encoding Storage Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: CAPTURE FACE                                          │
│  ┌─────────────────┐                                           │
│  │   Camera captures │                                          │
│  │   student photo    │                                          │
│  │   (image.jpg)      │                                          │
│  └─────────────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   face_recognition library converts image to            │   │
│  │   128-dimensional numerical array (face encoding)        │   │
│  │                                                         │   │
│  │   [0.123, 0.456, 0.789, ..., 0.321]  ← 128 numbers       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: STORE IN DATABASE                                      │
│                                                                  │
│  Python Code:                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  import pickle                                           │  │
│  │                                                          │  │
│  │  # Convert array to binary (pickle)                      │  │
│  │  encoding_binary = pickle.dumps(face_encoding)          │  │
│  │                                                          │  │
│  │  # Store in database                                     │  │
│  │  student.face_encoding = encoding_binary                 │  │
│  │  db.session.commit()                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                      │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MySQL stores binary data in BLOB column:               │   │
│  │                                                          │   │
│  │  SELECT face_encoding FROM student WHERE id = 1;         │   │
│  │                                                          │   │
│  │  Returns: 0x8901AFCD... (binary data)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: RETRIEVE FOR VERIFICATION                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  # Retrieve from database                                │  │
│  │  query = "SELECT face_encoding FROM student WHERE id = 1"│  │
│  │  result = db.session.execute(query).fetchone()          │  │
│  │                                                          │  │
│  │  # Convert binary back to array (unpickle)               │  │
│  │  stored_encoding = pickle.loads(result['face_encoding']) │  │
│  │                                                          │  │
│  │  # Compare with current face                             │  │
│  │  current_encoding = face_recognition.face_encodings(     │  │
│  │      current_image)[0]                                   │  │
│  │                                                          │  │
│  │  # Compare using Euclidean distance                      │  │
│  │  match = face_recognition.compare_faces(                 │  │
│  │      [stored_encoding], current_encoding                 │  │
│  │  )                                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Database Column for Face Encoding:

```sql
-- In MySQL, face encoding is stored as BLOB (binary large object)
CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    face_encoding BLOB,  -- Stores pickled 128-dim numpy array
    ...
);

-- In SQLite (used in current project)
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    face_encoding BLOB,  -- Same concept
    ...
);
```

---

## Complete Attendance Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ATTENDANCE MARKING FLOW                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   STUDENT    │     │    FLASK     │     │    MYSQL     │
│   LOGGED IN  │────▶│   RECEIVES   │────▶│   DATABASE   │
│              │     │   REQUEST    │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                           │                       ▲
                           │                       │
                           ▼                       │
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  FACE MATCH   │     │   QUERY DB   │     │  ATTENDANCE  │
│  VERIFIED ✓   │◀────│  FOR STUDENT │◀────│   RECORDED   │
│               │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                           │
                           ▼
┌──────────────┐     ┌──────────────┐
│   SUCCESS    │     │   INSERT     │
│   MESSAGE    │◀────│   ATTENDANCE │
│   SHOWN      │     │   RECORD     │
└──────────────┘     └──────────────┘

STEP-BY-STEP:

1. STUDENT LOGS IN
   └─> SELECT * FROM user WHERE username = 'student1'

2. STUDENT CLICKS "MARK ATTENDANCE"
   └─> Browser requests /student/verify-face

3. FLASK QUERIES DATABASE FOR STUDENT INFO
   └─> SELECT * FROM student WHERE user_id = 5
   └─> SELECT * FROM user WHERE id = 5

4. FLASK RETRIEVES FACE ENCODING
   └─> SELECT face_encoding FROM student WHERE id = 3

5. STUDENT'S FACE CAPTURED AND COMPARED
   └─> Face encoding generated from camera
   └─> Compared with stored encoding
   └─> If match (distance < 0.6): proceed

6. ATTENDANCE RECORDED IN DATABASE
   └─> INSERT INTO attendance (student_id, subject_id, class_date, status)
   └─> VALUES (3, 1, '2024-01-15', 'present')

7. SUCCESS MESSAGE RETURNED TO STUDENT
   └─> {"success": true, "message": "Attendance marked!"}
```

---

## SQL Queries Explained

### Query 1: User Login

```python
# Python/ORM
user = User.query.filter_by(username='admin').first()
```

```sql
-- Generated SQL
SELECT * FROM user WHERE username = 'admin' LIMIT 1;
```

**What it does:**
1. Searches `user` table for row where username is 'admin'
2. Returns first matching row
3. SQLAlchemy converts row to User object

---

### Query 2: Get All Students in a Section

```python
# Python/ORM
students = Student.query.filter_by(section_id=1).all()
```

```sql
-- Generated SQL
SELECT * FROM student WHERE section_id = 1;
```

**What it does:**
1. Searches `student` table for all rows where section_id is 1
2. Returns all matching rows
3. SQLAlchemy converts each row to Student object

---

### Query 3: Join - Get Student with User Info

```python
# Python/ORM
students = Student.query.join(User).add_columns(
    User.username, User.email, User.first_name, User.last_name,
    Student.student_id, Student.roll_number
).all()
```

```sql
-- Generated SQL
SELECT u.username, u.email, u.first_name, u.last_name, 
       s.student_id, s.roll_number
FROM student s
JOIN user u ON s.user_id = u.id;
```

**What it does:**
1. Joins `student` table with `user` table
2. Links them on `student.user_id = user.id`
3. Returns combined data from both tables

---

### Query 4: Count Students

```python
# Python/ORM
total = Student.query.count()
```

```sql
-- Generated SQL
SELECT COUNT(*) FROM student;
```

**What it does:**
1. Counts all rows in `student` table
2. Returns single number

---

### Query 5: Check Existing Attendance

```python
# Python/ORM
today = date.today()
existing = Attendance.query.filter_by(
    student_id=3,
    subject_id=1,
    class_date=today
).first()
```

```sql
-- Generated SQL
SELECT * FROM attendance 
WHERE student_id = 3 
  AND subject_id = 1 
  AND class_date = '2024-01-15'
LIMIT 1;
```

**What it does:**
1. Searches `attendance` table for today's attendance
2. Checks if student already marked attendance for this subject
3. Returns first match or None

---

### Query 6: Insert Attendance

```python
# Python/ORM
attendance = Attendance(
    student_id=3,
    subject_id=1,
    class_date=date.today(),
    status='present',
    check_in_time=datetime.now().time()
)
db.session.add(attendance)
db.session.commit()
```

```sql
-- Generated SQL
INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time)
VALUES (3, 1, '2024-01-15', 'present', '10:30:00');
```

**What it does:**
1. Creates new row in `attendance` table
2. Records that student 3 was present for subject 1 on today's date

---

### Query 7: Update Attendance

```python
# Python/ORM
existing = Attendance.query.filter_by(...).first()
if existing:
    existing.status = 'late'
    existing.is_manual = True
    db.session.commit()
```

```sql
-- Generated SQL
UPDATE attendance 
SET status = 'late', is_manual = TRUE
WHERE id = 15;
```

**What it does:**
1. Finds attendance record with id = 15
2. Updates status to 'late'
3. Marks as manually entered

---

### Query 8: Delete Student

```python
# Python/ORM
student = Student.query.get(3)
if student:
    # Delete related attendance records first
    Attendance.query.filter_by(student_id=3).delete()
    # Delete student
    db.session.delete(student)
    db.session.commit()
```

```sql
-- Generated SQL
DELETE FROM attendance WHERE student_id = 3;
DELETE FROM student WHERE id = 3;
```

**What it does:**
1. Deletes all attendance records for student 3
2. Deletes student 3 from database
3. Preserves data integrity (no orphaned records)

---

## Database Relationships

### Entity Relationship Diagram (ERD)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    USER      │         │   SECTION   │         │   SUBJECT   │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ PK id       │         │ PK id       │         │ PK id       │
│ username    │         │ name        │         │ subject_code│
│ password    │         │ description │         │ subject_name│
│ email       │         └──────┬──────┘         │ credit_hours│
│ first_name  │                │               │ FK teacher_id│
│ last_name   │                │               │ FK section_id│
│ role        │                │               └──────┬──────┘
│ is_active   │                │                      │
└──────┬──────┘                │                      │
       │                       │                      │
       │              ┌────────▼────────┐            │
       │              │    STUDENT       │            │
       │              ├──────────────────┤            │
       │              │ PK id            │            │
       │              │ FK user_id       │◀───────────┘
       │              │ student_id       │
       │              │ FK section_id ────┼──────────┐
       │              │ roll_number       │          │
       │              │ face_encoding    │          │
       │              │ face_image_path │          │
       │              └────────┬─────────┘          │
       │                       │                    │
       │              ┌────────▼────────┐           │
       │              │  ATTENDANCE     │           │
       │              ├─────────────────┤           │
       │              │ PK id           │           │
       │              │ FK student_id ──┼───────────┘
       └─────────────▶│ FK subject_id   │
                      │ class_date      │
                      │ status          │
                      │ check_in_time    │
                      │ face_confidence │
                      │ is_manual       │
                      └─────────────────┘
```

### Relationship Types:

```
USER ─────┬──────► STUDENT (One-to-One)
          │          Each user can have one student profile
          │          FK: student.user_id → user.id
          │
          ├─────────► TEACHER (One-to-One)
          │          Each user can have teacher role
          │          FK: subject.teacher_id → user.id
          │
          └─────────► ADMIN (Same table)
                     Role column distinguishes admin/teacher/student

SECTION ──────► STUDENT (One-to-Many)
               One section has many students
               FK: student.section_id → section.id

SECTION ──────► SUBJECT (One-to-Many)
               One section has many subjects
               FK: subject.section_id → section.id

SUBJECT ─────► ATTENDANCE (One-to-Many)
               One subject has many attendance records
               FK: attendance.subject_id → subject.id

STUDENT ─────► ATTENDANCE (One-to-Many)
               One student has many attendance records
               FK: attendance.student_id → student.id
```

---

## Data Flow Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                        COMPLETE DATA FLOW                           │
└─────────────────────────────────────────────────────────────────────┘

  PYTHON APP                          DATABASE (MySQL/SQLite)
  ───────────                         ──────────────────────
       │                                    │
       │  1. User submits form              │
       │  ──────────────────────           │
       │  request.form['username']         │
       │       │                           │
       │       ▼                           │
       │  ┌─────────────┐                  │
       │  │  Validate   │                  │
       │  │  Input      │                  │
       │  └─────────────┘                  │
       │       │                            │
       │       ▼                            │
       │  ┌─────────────┐                  │
       │  │ ORM Creates │──────▶ INSERT INTO...
       │  │ Object      │                  │
       │  └─────────────┘                  │
       │       │                            │
       │       ▼                            │
       │  ┌─────────────┐                  │
       │  │ session.   │──────▶ COMMIT     │
       │  │ commit()   │                  │
       │  └─────────────┘                  │
       │                                    │
       │  2. Display data                  │
       │  ──────────────────────           │
       │       │                            │
       │       ▼                            │
       │  ┌─────────────┐                  │
       │  │ Query DB    │◀────── SELECT *  │
       │  │            │        FROM table │
       │  └─────────────┘                  │
       │       │                            │
       │       ▼                            │
       │  ┌─────────────┐                  │
       │  │ ORM Converts│                  │
       │  │ Rows to     │                  │
       │  │ Objects     │                  │
       │  └─────────────┘                  │
       │       │                            │
       │       ▼                            │
       │  ┌─────────────┐                  │
       │  │ Render HTML │                  │
       │  │ with Data   │                  │
       │  └─────────────┘                  │
       │       │                            │
       │       ▼                            │
       │  ┌─────────────┐                  │
       │  │ Send to     │                  │
       │  │ Browser     │                  │
       │  └─────────────┘                  │
       │                                    │
       ▼                                    ▼
```

---

## Key Takeaways

1. **ORM abstracts SQL**: SQLAlchemy converts Python code to SQL queries
2. **Objects ↔ Tables**: Python objects map to database table rows
3. **Session manages state**: `db.session` tracks changes and commits them
4. **Relationships connect tables**: Foreign keys link related data
5. **Binary data stored as BLOB**: Face encodings stored as pickled binary
6. **Flow is bidirectional**: Python → Database and Database → Python

---

## For DBMS Project: What to Focus On

1. **Understand the data flow**: Python → SQL → Python
2. **Know the relationships**: How tables are connected
3. **Write SQL queries**: Practice SELECT, INSERT, UPDATE, DELETE
4. **Understand indexing**: How database optimizes queries
5. **Know transactions**: How COMMIT/ROLLBACK work
6. **Understand constraints**: Foreign keys, unique constraints

---

## Practice Questions for DBMS Exam

1. What is the difference between ORM and raw SQL?
2. Draw the ER diagram for this attendance system
3. Write SQL query to get all students in Section A
4. What is a foreign key? Give example from this project
5. How is face encoding stored in database? Why BLOB?
6. Explain the data flow when a student logs in
7. What is the difference between ORM and Pure SQL approaches?
8. Write SQL query to count students present today
9. Explain one-to-many relationship with example from this project
10. What is the purpose of LIMIT in SQL?

---

## Pure SQL Examples (app_pure_sql.py)

For a DBMS project, use **[`app_pure_sql.py`](app_pure_sql.py)** instead of the ORM version.

### Database Connection

```python
import mysql.connector

def get_db_connection():
    """Create and return a database connection"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='attendance_db'
    )
    return conn
```

### Execute Query Function

```python
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
```

### Login Route (Pure SQL)

```python
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
            user = User(user_data)  # Create User object from dict
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')
```

### Add Student (Pure SQL)

```python
@app.route('/admin/students', methods=['POST'])
def manage_students():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    student_id = request.form.get('student_id')
    section_id = request.form.get('section_id')
    roll_number = request.form.get('roll_number')
    
    # Create connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL INSERT: Create user
    hashed_password = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO user (username, password_hash, email, first_name, last_name, role)
        VALUES (%s, %s, %s, %s, %s, 'student')
    """, (username, hashed_password, email, first_name, last_name))
    
    user_id = cursor.lastrowid  # Get auto-generated ID
    
    # SQL INSERT: Create student
    cursor.execute("""
        INSERT INTO student (user_id, student_id, section_id, roll_number)
        VALUES (%s, %s, %s, %s)
    """, (user_id, student_id, section_id, roll_number))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Student added successfully', 'success')
```

### Get All Students with JOIN (Pure SQL)

```python
# SQL QUERY: Get all students with user info using JOIN
students = execute_query_all("""
    SELECT s.*, u.username, u.email, u.first_name, u.last_name
    FROM student s
    JOIN user u ON s.user_id = u.id
""")
```

### Delete Student (Pure SQL)

```python
@app.route('/admin/student/delete/<int:student_id>')
def delete_student(student_id):
    # Get student first
    student = execute_query(
        "SELECT * FROM student WHERE id = %s", 
        (student_id,)
    )
    
    if student:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL DELETE: Delete attendance records first
        cursor.execute(
            "DELETE FROM attendance WHERE student_id = %s", 
            (student_id,)
        )
        
        # SQL DELETE: Delete student
        cursor.execute(
            "DELETE FROM student WHERE id = %s", 
            (student_id,)
        )
        
        # SQL DELETE: Delete user
        cursor.execute(
            "DELETE FROM user WHERE id = %s", 
            (student['user_id'],)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Student deleted successfully', 'success')
    
    return redirect(url_for('manage_students'))
```

### Mark Attendance (Pure SQL)

```python
@app.route('/teacher/manual-attendance', methods=['POST'])
def manual_attendance():
    student_id = request.form.get('student_id')
    subject_id = request.form.get('subject_id')
    status = request.form.get('status')
    today = date.today()
    current_time = datetime.now().time()
    
    # Check existing attendance
    existing = execute_query("""
        SELECT * FROM attendance 
        WHERE student_id = %s AND subject_id = %s AND class_date = %s
    """, (student_id, subject_id, today))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if existing:
        # SQL UPDATE
        cursor.execute("""
            UPDATE attendance 
            SET status = %s, is_manual = TRUE
            WHERE id = %s
        """, (status, existing['id']))
    else:
        # SQL INSERT
        cursor.execute("""
            INSERT INTO attendance (student_id, subject_id, class_date, status, check_in_time, is_manual)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (student_id, subject_id, today, status, current_time))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Attendance marked!', 'success')
    return redirect(url_for('take_attendance', subject_id=subject_id))
```

---

## File Summary

| File | Description |
|------|-------------|
| [`app.py`](app.py) | Original version using SQLAlchemy ORM |
| [`app_pure_sql.py`](app_pure_sql.py) | **RECOMMENDED** - Pure SQL version |
| [`DBMS_EXPLANATION.md`](DBMS_EXPLANATION.md) | This guide |
| [`requirements.txt`](requirements.txt) | Python dependencies |
| [`templates/`](templates/) | HTML templates |

**For DBMS Project: Use `app_pure_sql.py`**
