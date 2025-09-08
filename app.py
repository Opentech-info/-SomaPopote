from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from services.ussd import ussd_menu
from services.sms import send_sms
from services.voice import voice_lesson
from services.gamification import award_airtime
from database import init_db, get_user_progress, update_user_progress, get_all_students, get_leaderboard_data, create_lesson as db_create_lesson, get_or_create_user, get_user_points, get_recent_quiz_results, get_attendance_records, get_db_connection
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize database
init_db()

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Teacher/parent dashboard"""
    if not session.get('logged_in') or session.get('user_type') != 'teacher':
        return redirect(url_for('login'))
    
    # Get sample data for dashboard
    students = get_all_students()
    leaderboard = get_leaderboard_data(5)
    
    # Calculate statistics
    total_students = len(students)
    active_students = sum(1 for s in students if s.get('total_points', 0) > 0)
    total_points = sum(s.get('total_points', 0) for s in students)
    avg_progress = int(sum(s.get('total_points', 0) for s in students) / len(students)) if students else 0
    
    return render_template('dashboard.html', 
                         students=students,
                         leaderboard=leaderboard,
                         stats={
                             'total_students': total_students,
                             'active_students': active_students,
                             'total_points': total_points,
                             'avg_progress': avg_progress
                         })

@app.route('/student_dashboard')
def student_dashboard():
    """Student dashboard showing personal progress and USSD activity"""
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect(url_for('login'))
    
    phone_number = session.get('phone_number')
    
    # Get user progress
    progress_data = get_user_progress(phone_number)
    if not progress_data:
        progress_data = {'total_points': 0, 'subjects': {}}
    
    # Calculate total lessons and quizzes
    total_lessons = sum(subject.get('lessons_completed', 0) for subject in progress_data['subjects'].values())
    total_quizzes = sum(subject.get('quizzes_taken', 0) for subject in progress_data['subjects'].values())
    
    # Get recent quiz results
    recent_quizzes = get_recent_quiz_results(phone_number, 10)
    
    # Sample data for dashboard
    user_data = {
        'name': session.get('user_name', 'Student'),
        'phone_number': phone_number,
        'grade': 'Grade 5',  # This should come from database
        'school': 'Shule ya Msingi Mlimani'  # This should come from database
    }
    
    progress = {
        'total_points': progress_data['total_points'],
        'total_lessons': total_lessons,
        'total_quizzes': total_quizzes,
        'streak_days': 7,  # This should be calculated from database
        'accuracy_rate': 85,  # This should be calculated from database
        'improvement_rate': 12,  # This should be calculated from database
        'subjects': progress_data['subjects']
    }
    
    recent_activities = [
        {'activity': 'alisoma somo la Hisabati', 'subject': 'Hisabati', 'time': '2 saa iliyopita', 'points': 5},
        {'activity': 'alijibu swali la Sayansi', 'subject': 'Sayansi', 'time': '5 saa iliyopita', 'points': 10},
        {'activity': 'alimaliza somo la Kiswahili', 'subject': 'Kiswahili', 'time': '1 siku iliyopita', 'points': 5},
    ]
    
    ussd_sessions = [
        {'session_type': 'Somo la Hisabati', 'duration': 15, 'completed': True, 'timestamp': '2024-01-15 14:30'},
        {'session_type': 'Jaribu la Sayansi', 'duration': 10, 'completed': True, 'timestamp': '2024-01-15 10:15'},
        {'session_type': 'Somo la Kiswahili', 'duration': 20, 'completed': False, 'timestamp': '2024-01-14 16:45'},
    ]
    
    ussd_stats = {
        'total_sessions': len(ussd_sessions),
        'total_minutes': sum(session['duration'] for session in ussd_sessions)
    }
    
    achievements = {
        'total_badges': 5,
        'badges': [
            {'name': 'Mwanafunzi Bora', 'icon': 'fa-star', 'description': 'Alipata pointi zaidi ya 100'},
            {'name': 'Mfanyakazi Bora', 'icon': 'fa-fire', 'description': 'Alisoma kwa mfululizo kwa siku 7'},
            {'name': 'Mtaalamu wa Hisabati', 'icon': 'fa-calculator', 'description': 'Alimaliza masomo 5 ya Hisabati'},
        ]
    }
    
    rewards = [
        {'reason': 'Kumaliza somo la Hisabati', 'reward_type': 'Airtime', 'amount': 100, 'timestamp': '2024-01-15'},
        {'reason': 'Kujibu swali sahihi', 'reward_type': 'Airtime', 'amount': 50, 'timestamp': '2024-01-14'},
    ]
    
    next_goals = [
        {'title': 'Fikia pointi 200', 'description': 'Endelea kujifunza kupata pointi zaidi', 'progress': 65},
        {'title': 'Maliza masomo 10', 'description': 'Maliza masomo yote kwa wiki hii', 'progress': 40},
    ]
    
    leaderboard_position = 3
    leaderboard_total = 25
    
    return render_template('student_dashboard.html', 
                         user=user_data,
                         progress=progress,
                         recent_activities=recent_activities,
                         recent_quizzes=recent_quizzes,
                         ussd_sessions=ussd_sessions,
                         ussd_stats=ussd_stats,
                         achievements=achievements,
                         rewards=rewards,
                         next_goals=next_goals,
                         leaderboard_position=leaderboard_position,
                         leaderboard_total=leaderboard_total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page for students and teachers"""
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'student')
        
        # Get user from database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if user_type == 'student':
            cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
            user = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM teachers WHERE phone_number = ?", (phone_number,))
            user = cursor.fetchone()
        
        conn.close()
        
        if user and password == '1234':  # Simple password check (in production, use proper hashing)
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['phone_number'] = user['phone_number']
            session['user_type'] = user_type
            session['user_name'] = user['name']
            
            if user_type == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Namba ya simu au neno la siri si sahihi')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        user_type = request.form.get('user_type', 'student')
        phone_number = request.form.get('phone_number')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        email = request.form.get('email')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if user_type == 'student':
                school = request.form.get('school')
                grade = request.form.get('grade')
                parent_phone = request.form.get('parent_phone')
                
                # Check if user already exists
                cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    return render_template('register.html', error='Namba ya simu tayari imesajiliwa')
                
                # Insert new student
                cursor.execute('''
                    INSERT INTO users (phone_number, name, grade, school, parent_phone, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (phone_number, full_name, grade, school, parent_phone, email))
                
            else:  # teacher
                teacher_school = request.form.get('teacher_school')
                subject = request.form.get('subject')
                experience = request.form.get('experience')
                
                # Check if teacher already exists
                cursor.execute("SELECT * FROM teachers WHERE phone_number = ?", (phone_number,))
                existing_teacher = cursor.fetchone()
                
                if existing_teacher:
                    return render_template('register.html', error='Namba ya simu tayari imesajiliwa')
                
                # Insert new teacher
                cursor.execute('''
                    INSERT INTO teachers (phone_number, name, school, subject)
                    VALUES (?, ?, ?, ?)
                ''', (phone_number, full_name, teacher_school, subject))
            
            conn.commit()
            conn.close()
            
            return render_template('login.html', success='Usajili umefanikiwa! Tafadhali ingia kwenye akaunti yako.')
            
        except Exception as e:
            conn.close()
            return render_template('register.html', error='Kuna tatizo lililotokea wakati wa usajili. Tafadhali jaribu tena.')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        
        # Here you would implement the password reset logic
        # For now, just show a success message
        return render_template('forgot_password.html', 
                             success='Tumekutumia neno la siri jipya kupitia SMS. Tafadhali angalia simu yako.')
    
    return render_template('forgot_password.html')

@app.route('/ussd', methods=['POST', 'GET'])
def ussd_handler():
    """Handle USSD requests from Africa's Talking"""
    if request.method == 'POST':
        response = ussd_menu()
        return response, 200, {'Content-Type': 'text/plain'}
    return "USSD Endpoint", 200

@app.route('/sms', methods=['POST'])
def sms_handler():
    """Handle incoming SMS and send notifications"""
    data = request.form
    phone_number = data.get('from')
    message = data.get('text')
    
    # Process SMS commands
    if message.lower().startswith('quiz'):
        # Send quiz via SMS
        quiz_response = "Swali: 2 + 2 = ?\nJibu: A.3 B.4 C.5\nTuma jibu lako kama: JIBU B"
        send_sms(phone_number, quiz_response)
    elif message.lower().startswith('jibu'):
        # Process quiz answer
        answer = message.split()[1] if len(message.split()) > 1 else ''
        if answer.upper() == 'B':
            award_airtime(phone_number, 100)  # Award 100 TZS
            response = "Sahihi! Umepokea Tsh 100 ya airtime. Endelea kujifunza!"
        else:
            response = "Jaribu tena! Jibu sahihi ni B."
        send_sms(phone_number, response)
    
    return "SMS Processed", 200

@app.route('/voice', methods=['POST'])
def voice_handler():
    """Handle voice calls for IVR lessons"""
    response = voice_lesson()
    return response, 200, {'Content-Type': 'text/xml'}

@app.route('/api/progress/<phone_number>')
def get_progress(phone_number):
    """API endpoint to get user progress"""
    progress = get_user_progress(phone_number)
    return jsonify(progress)

@app.route('/api/lesson', methods=['POST'])
def create_lesson():
    """API endpoint for teachers to create lessons"""
    if not session.get('logged_in') or session.get('user_type') != 'teacher':
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.json
    subject = data.get('subject')
    title = data.get('title')
    content = data.get('content')
    grade_level = data.get('grade_level')
    created_by = session.get('user_name', 'Unknown')
    
    if not all([subject, title, content, grade_level]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # Store lesson in database
    lesson_id = db_create_lesson(subject, title, content, grade_level, created_by)
    
    return jsonify({
        "status": "success", 
        "message": "Lesson created successfully",
        "lesson_id": lesson_id
    })

@app.route('/api/send_bulk_sms', methods=['POST'])
def send_bulk_sms():
    """API endpoint for teachers to send bulk SMS to parents"""
    if not session.get('logged_in') or session.get('user_type') != 'teacher':
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.json
    phone_numbers = data.get('phone_numbers', [])
    message = data.get('message', '')
    
    if not phone_numbers or not message:
        return jsonify({"status": "error", "message": "Missing phone numbers or message"}), 400
    
    success_count = 0
    for phone in phone_numbers:
        if send_sms(phone, message):
            success_count += 1
    
    return jsonify({
        "status": "success",
        "message": f"SMS sent to {success_count} recipients",
        "success_count": success_count,
        "total_recipients": len(phone_numbers)
    })

@app.route('/api/analytics')
def get_analytics():
    """Get analytics data for dashboard"""
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    # Sample analytics data
    analytics = {
        'daily_active_users': [45, 52, 48, 61, 55, 67, 73],
        'subject_distribution': {
            'Hisabati': 35,
            'Sayansi': 25,
            'Kiswahili': 25,
            'English': 15
        },
        'weekly_progress': [65, 72, 78, 85],
        'engagement_rate': 78
    }
    
    return jsonify(analytics)

@app.route('/api/student/<phone_number>')
def get_student_details(phone_number):
    """Get detailed student information"""
    if not session.get('logged_in') or session.get('user_type') != 'teacher':
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    # Get student details from database
    student_data = {
        'phone_number': phone_number,
        'name': 'Juma Mwinyi',
        'grade': 'Grade 5',
        'school': 'Shule ya Msingi Mlimani',
        'total_points': 135,
        'subjects': {
            'Hisabati': {'points': 45, 'lessons_completed': 3},
            'Sayansi': {'points': 30, 'lessons_completed': 2},
            'Kiswahili': {'points': 60, 'lessons_completed': 4}
        },
        'recent_activity': [
            {'date': '2024-01-15', 'activity': 'Completed Math quiz', 'points': 10},
            {'date': '2024-01-14', 'activity': 'Read Science lesson', 'points': 5}
        ]
    }
    
    return jsonify(student_data)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
