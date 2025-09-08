import sqlite3
import json
import datetime
import os

DATABASE_NAME = 'somapopote.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Allow dictionary-like access to rows
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            name TEXT,
            grade TEXT,
            school TEXT,
            parent_phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create user_progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            lessons_completed INTEGER DEFAULT 0,
            quizzes_taken INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create quiz_results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            question TEXT NOT NULL,
            user_answer TEXT,
            correct_answer TEXT,
            is_correct BOOLEAN,
            points_earned INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create lessons table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            grade_level TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Create lesson_completions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lesson_id INTEGER,
            completion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        )
    """)
    
    # Create rewards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reward_type TEXT NOT NULL,
            amount INTEGER DEFAULT 0,
            reason TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE NOT NULL,
            status TEXT CHECK(status IN ('Present', 'Absent', 'Late')) DEFAULT 'Present',
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, date)
        )
    """)
    
    # Create teachers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            school TEXT,
            subject TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create bulk_messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulk_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER,
            message TEXT NOT NULL,
            recipient_type TEXT CHECK(recipient_type IN ('all', 'grade', 'specific')) DEFAULT 'all',
            recipients TEXT,
            status TEXT DEFAULT 'pending',
            sent_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    """)
    
    # Create voice_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voice_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_type TEXT CHECK(session_type IN ('lesson', 'quiz', 'menu')) DEFAULT 'menu',
            duration INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT FALSE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Insert sample data if tables are empty
    insert_sample_data(cursor)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def insert_sample_data(cursor):
    """Insert sample data for demonstration"""
    # Check if users table has data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Insert sample users
        sample_users = [
            ('+255714123456', 'Juma Mwinyi', 'Grade 5', 'Shule ya Msingi Mlimani', '+255714123400'),
            ('+255714123457', 'Asha Hassan', 'Grade 4', 'Shule ya Msingi Mlimani', '+255714123401'),
            ('+255714123458', 'Fatuma Omar', 'Grade 6', 'Shule ya Msingi Mlimani', '+255714123402'),
        ]
        
        cursor.executemany('''
            INSERT INTO users (phone_number, name, grade, school, parent_phone)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_users)
        
        # Insert sample teachers
        sample_teachers = [
            ('+255714123000', 'Mwalimu Anna', 'Shule ya Msingi Mlimani', 'Hisabati'),
            ('+255714123001', 'Mwalimu Bakari', 'Shule ya Msingi Mlimani', 'Sayansi'),
        ]
        
        cursor.executemany('''
            INSERT INTO teachers (phone_number, name, school, subject)
            VALUES (?, ?, ?, ?)
        ''', sample_teachers)
        
        # Insert sample lessons
        sample_lessons = [
            ('Hisabati', 'Kuongeza Namba', 'Leo utajifunza kuongeza namba. Mfano: 2 + 2 = 4', 'Grade 4', 'Mwalimu Anna'),
            ('Sayansi', 'Mazingira', 'Leo utajifunza kuhusu mazingira na umuhimu wa kupanda miti', 'Grade 4', 'Mwalimu Bakari'),
            ('Kiswahili', 'Sarufi', 'Leo utajifunza kuhusu vitenzi na matumizi yake', 'Grade 4', 'Mwalimu Anna'),
        ]
        
        cursor.executemany('''
            INSERT INTO lessons (subject, title, content, grade_level, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_lessons)
        
        # Insert sample progress
        cursor.execute("SELECT id FROM users WHERE phone_number = '+255714123456'")
        user_id = cursor.fetchone()[0]
        
        sample_progress = [
            (user_id, 'Hisabati', 45, 3, 5, 4),
            (user_id, 'Sayansi', 30, 2, 3, 2),
            (user_id, 'Kiswahili', 60, 4, 6, 5),
        ]
        
        cursor.executemany('''
            INSERT INTO user_progress (user_id, subject, points, lessons_completed, quizzes_taken, correct_answers)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_progress)
        
        # Insert sample attendance
        today = datetime.date.today().isoformat()
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        
        sample_attendance = [
            (user_id, today, 'Present', None),
            (user_id, yesterday, 'Present', None),
        ]
        
        cursor.executemany('''
            INSERT INTO attendance (user_id, date, status, notes)
            VALUES (?, ?, ?, ?)
        ''', sample_attendance)

def get_or_create_user(phone_number, name=None, grade=None, school=None, parent_phone=None):
    """Get existing user or create new one"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if user:
        # Update last active timestamp
        cursor.execute('''
            UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE phone_number = ?
        ''', (phone_number,))
        conn.commit()
        conn.close()
        return dict(user)
    else:
        # Create new user
        cursor.execute('''
            INSERT INTO users (phone_number, name, grade, school, parent_phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (phone_number, name, grade, school, parent_phone))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': user_id,
            'phone_number': phone_number,
            'name': name,
            'grade': grade,
            'school': school,
            'parent_phone': parent_phone
        }

def get_user_progress(phone_number):
    """Get user's progress across all subjects"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return None
    
    user_id = user['id']
    
    cursor.execute('''
        SELECT subject, points, lessons_completed, quizzes_taken, correct_answers
        FROM user_progress
        WHERE user_id = ?
    ''', (user_id,))
    
    progress_rows = cursor.fetchall()
    
    total_points = sum(row['points'] for row in progress_rows)
    subjects = {}
    
    for row in progress_rows:
        subjects[row['subject']] = {
            'points': row['points'],
            'lessons_completed': row['lessons_completed'],
            'quizzes_taken': row['quizzes_taken'],
            'correct_answers': row['correct_answers']
        }
    
    conn.close()
    
    return {
        'total_points': total_points,
        'subjects': subjects
    }

def update_user_progress(phone_number, subject, points):
    """Update user's progress for a specific subject"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    user_id = user['id']
    
    # Check if progress record exists for this subject
    cursor.execute('''
        SELECT id FROM user_progress WHERE user_id = ? AND subject = ?
    ''', (user_id, subject))
    
    progress = cursor.fetchone()
    
    if progress:
        # Update existing record
        cursor.execute('''
            UPDATE user_progress 
            SET points = points + ?, last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ? AND subject = ?
        ''', (points, user_id, subject))
    else:
        # Create new progress record
        cursor.execute('''
            INSERT INTO user_progress (user_id, subject, points)
            VALUES (?, ?, ?)
        ''', (user_id, subject, points))
    
    conn.commit()
    conn.close()
    return True

def save_quiz_result(phone_number, subject, is_correct, question=None, user_answer=None, correct_answer=None):
    """Save quiz result to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    user_id = user['id']
    points_earned = 10 if is_correct else 0
    
    cursor.execute('''
        INSERT INTO quiz_results (user_id, subject, question, user_answer, correct_answer, is_correct, points_earned)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, subject, question, user_answer, correct_answer, is_correct, points_earned))
    
    # Update progress
    cursor.execute('''
        UPDATE user_progress 
        SET quizzes_taken = quizzes_taken + 1,
            correct_answers = correct_answers + ?,
            points = points + ?,
            last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ? AND subject = ?
    ''', (1 if is_correct else 0, points_earned, user_id, subject))
    
    conn.commit()
    conn.close()
    return True

def get_user_points(phone_number):
    """Get total points for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return 0
    
    user_id = user['id']
    
    cursor.execute('''
        SELECT COALESCE(SUM(points), 0) as total_points
        FROM user_progress
        WHERE user_id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result['total_points'] if result else 0

def update_user_points(phone_number, new_points):
    """Update user's total points"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    user_id = user['id']
    
    cursor.execute('''
        UPDATE user_progress 
        SET points = ?, last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (new_points, user_id))
    
    conn.commit()
    conn.close()
    return True

def log_reward(phone_number, reward_type, amount, reason):
    """Log a reward for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    user_id = user['id']
    
    cursor.execute('''
        INSERT INTO rewards (user_id, reward_type, amount, reason)
        VALUES (?, ?, ?, ?)
    ''', (user_id, reward_type, amount, reason))
    
    conn.commit()
    conn.close()
    return True

def get_attendance_records(phone_number, start_date=None, end_date=None):
    """Get attendance records for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return []
    
    user_id = user['id']
    
    if start_date and end_date:
        cursor.execute('''
            SELECT date, status, notes
            FROM attendance
            WHERE user_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
        ''', (user_id, start_date, end_date))
    else:
        cursor.execute('''
            SELECT date, status, notes
            FROM attendance
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT 30
        ''', (user_id,))
    
    records = cursor.fetchall()
    conn.close()
    
    return [dict(record) for record in records]

def get_all_students():
    """Get all students for teacher dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.phone_number, u.name, u.grade, u.school,
               COALESCE(SUM(up.points), 0) as total_points,
               COUNT(DISTINCT up.subject) as subjects_studied
        FROM users u
        LEFT JOIN user_progress up ON u.id = up.user_id
        GROUP BY u.id, u.phone_number, u.name, u.grade, u.school
        ORDER BY u.name
    ''')
    
    students = cursor.fetchall()
    conn.close()
    
    return [dict(student) for student in students]

def get_lessons_by_subject(subject, grade_level=None):
    """Get lessons by subject, optionally filtered by grade level"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if grade_level:
        cursor.execute('''
            SELECT id, subject, title, content, grade_level, created_by
            FROM lessons
            WHERE subject = ? AND grade_level = ? AND is_active = TRUE
            ORDER BY created_at DESC
        ''', (subject, grade_level))
    else:
        cursor.execute('''
            SELECT id, subject, title, content, grade_level, created_by
            FROM lessons
            WHERE subject = ? AND is_active = TRUE
            ORDER BY created_at DESC
        ''', (subject,))
    
    lessons = cursor.fetchall()
    conn.close()
    
    return [dict(lesson) for lesson in lessons]

def create_lesson(subject, title, content, grade_level, created_by):
    """Create a new lesson"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO lessons (subject, title, content, grade_level, created_by)
        VALUES (?, ?, ?, ?, ?)
    ''', (subject, title, content, grade_level, created_by))
    
    lesson_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return lesson_id

def mark_lesson_completed(phone_number, lesson_id):
    """Mark a lesson as completed for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    user_id = user['id']
    
    # Check if already completed
    cursor.execute('''
        SELECT id FROM lesson_completions 
        WHERE user_id = ? AND lesson_id = ?
    ''', (user_id, lesson_id))
    
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        return True  # Already completed
    
    # Mark as completed
    cursor.execute('''
        INSERT INTO lesson_completions (user_id, lesson_id)
        VALUES (?, ?)
    ''', (user_id, lesson_id))
    
    # Update progress
    cursor.execute('''
        SELECT subject FROM lessons WHERE id = ?
    ''', (lesson_id,))
    
    lesson = cursor.fetchone()
    if lesson:
        subject = lesson['subject']
        cursor.execute('''
            UPDATE user_progress 
            SET lessons_completed = lessons_completed + 1,
                points = points + 5,
                last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ? AND subject = ?
        ''', (user_id, subject))
    
    conn.commit()
    conn.close()
    return True

def get_leaderboard_data(limit=10):
    """Get leaderboard data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.phone_number, u.name, u.grade,
               COALESCE(SUM(up.points), 0) as total_points,
               COUNT(DISTINCT CASE WHEN up.quizzes_taken > 0 THEN up.subject END) as subjects_with_quizzes
        FROM users u
        LEFT JOIN user_progress up ON u.id = up.user_id
        GROUP BY u.id, u.phone_number, u.name, u.grade
        ORDER BY total_points DESC
        LIMIT ?
    ''', (limit,))
    
    leaderboard = cursor.fetchall()
    conn.close()
    
    return [dict(entry) for entry in leaderboard]

def get_recent_quiz_results(phone_number, limit=10):
    """Get recent quiz results for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return []
    
    user_id = user['id']
    
    cursor.execute('''
        SELECT subject, question, user_answer, correct_answer, is_correct, points_earned, timestamp
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(result) for result in results]
