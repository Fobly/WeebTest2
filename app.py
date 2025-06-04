from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect, flash, session
import os
from datetime import datetime, timedelta
import json
from models import db, User, Appointment, Message, Service, Doctor
from functools import wraps
from sqlalchemy import inspect

# Create data directories if they don't exist
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_DIR = os.path.join(DATA_DIR, 'users')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(USERS_DIR, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "data", "clinic.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Initialize the database
db.init_app(app)

# Create the database tables and test user
with app.app_context():
    db.create_all()
    
    # Create default services if they don't exist
    default_services = [
        {
            'name': 'Общий осмотр',
            'description': 'Комплексный осмотр полости рта и диагностика',
            'price': 1500.0,
            'duration': 30
        },
        {
            'name': 'Профессиональная чистка',
            'description': 'Профессиональная гигиена полости рта',
            'price': 3000.0,
            'duration': 60
        },
        {
            'name': 'Косметическая стоматология',
            'description': 'Отбеливание, виниры, реставрация зубов',
            'price': 5000.0,
            'duration': 90
        },
        {
            'name': 'Ортодонтия',
            'description': 'Исправление прикуса, установка брекетов',
            'price': 4000.0,
            'duration': 60
        },
        {
            'name': 'Зубные импланты',
            'description': 'Установка зубных имплантов',
            'price': 15000.0,
            'duration': 120
        },
        {
            'name': 'Неотложная помощь',
            'description': 'Срочное лечение острой зубной боли',
            'price': 2000.0,
            'duration': 45
        }
    ]

    for service_data in default_services:
        if not Service.query.filter_by(name=service_data['name']).first():
            service = Service(**service_data)
            db.session.add(service)
            print(f'Created service: {service_data["name"]}')
    
    db.session.commit()  # Commit the service changes
    
    # Create a test user if it doesn't exist
    test_email = 'test@example.com'
    if not User.query.filter_by(email=test_email).first():
        test_user = User(
            first_name='Test',
            last_name='User',
            middle_name='',
            email=test_email,
            phone='+7 (999) 123-45-67',
            password='password123',
            birth_date=datetime.now().date(),
            medical_history=[]
        )
        db.session.add(test_user)
        db.session.commit()
        print(f'Created test user with email: {test_email} and password: password123')

    # Create an admin user if it doesn't exist
    admin_email = 'admin@example.com'
    if not User.query.filter_by(email=admin_email).first():
        admin_user = User(
            first_name='Admin',
            last_name='User',
            middle_name='',
            email=admin_email,
            phone='+7 (999) 999-99-99',
            password='admin123',
            birth_date=datetime.now().date(),
            medical_history=[],
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f'Created admin user with email: {admin_email} and password: admin123')

dir_path = os.path.dirname(os.path.abspath(__file__))+'/data/users/'

# Store appointments and contact messages (in a real app, you'd use a database)
appointments = []
contact_messages = []

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('У вас нет прав для доступа к этой странице')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor to make user data available in all templates
@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}

@app.template_filter('format_date')
def format_date(date_str):
    """Format ISO date string to dd.mm.yyyy format"""
    try:
        if isinstance(date_str, str):
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            date = date_str
        return date.strftime('%d.%m.%Y')
    except:
        return date_str

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/booking')
@login_required
def booking():
    return render_template('booking.html')

@app.route('/appointments')
@login_required
def appointments():
    user = User.query.get(session['user_id'])
    return render_template('appointments.html', appointments=user.appointments)

@app.route('/medical-history')
@login_required
def medical_history():
    user = User.query.get(session['user_id'])
    return render_template('medical_history.html', history=user.medical_history)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)

        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            if remember:
                session.permanent = True
            return jsonify({'status': 'success', 'redirect': url_for('home')})
        
        return jsonify({'status': 'error', 'message': 'Неверный email или пароль'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы успешно вышли из системы')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            middle_name = data.get('middle_name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            birth_date = data.get('birth_date')

            # Validate required fields
            if not all([first_name, last_name, email, phone, password, birth_date]):
                return jsonify({
                    'status': 'error',
                    'message': 'Пожалуйста, заполните все обязательные поля'
                }), 400

            if User.query.filter_by(email=email).first():
                return jsonify({
                    'status': 'error',
                    'message': 'Email уже зарегистрирован'
                }), 400

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                email=email,
                phone=phone,
                password=password,
                birth_date=datetime.strptime(birth_date, '%Y-%m-%d').date(),
                medical_history=[]
            )
            
            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'redirect': url_for('login')
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

# Protected routes example
@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/api/book-appointment', methods=['POST'])
@login_required
def book_appointment():
    try:
        # Check if user is in session
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'Please log in to book an appointment'
            }), 401
        
        data = request.get_json()
        user = User.query.get(session['user_id'])
        
        # Verify user exists
        if not user:
            session.pop('user_id', None)  # Clear invalid session
            return jsonify({
                'status': 'error',
                'message': 'User not found. Please log in again.'
            }), 401
        
        # Validate required fields
        if not all(data.get(field) for field in ['service', 'preferred-date', 'preferred-time']):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        # Service name mapping
        service_names = {
            'general-checkup': 'Общий осмотр',
            'cleaning': 'Профессиональная чистка',
            'cosmetic': 'Косметическая стоматология',
            'orthodontics': 'Ортодонтия',
            'implants': 'Зубные импланты',
            'emergency': 'Неотложная помощь'
        }

        # Get human-readable service name
        service_input_key = data.get('service') # e.g., 'general-checkup'
        service_name = service_names.get(service_input_key) # e.g., 'Общий осмотр'
        
        if not service_name:
            return jsonify({
                'status': 'error',
                'message': 'Invalid service selected'
            }), 400

        # Fetch the Service object from the database
        service_object = Service.query.filter_by(name=service_name).first()
        if not service_object:
            # This case might happen if service_names map doesn't align with DB Service names
            return jsonify({
                'status': 'error',
                'message': f'Service "{service_name}" not found in database.'
            }), 400

        # Convert time period to actual time
        time_mapping = {
            'morning': '09:00',
            'afternoon': '13:00',
            'evening': '16:00'
        }
        
        appointment_time = time_mapping.get(data.get('preferred-time'))
        if not appointment_time:
            return jsonify({
                'status': 'error',
                'message': 'Invalid time period selected'
            }), 400

        # Combine date and time
        appointment_datetime = datetime.strptime(f"{data.get('preferred-date')} {appointment_time}", '%Y-%m-%d %H:%M')
        
        # Create new appointment
        new_appointment = Appointment(
            user_id=user.id,
            service_id=service_object.id,  # Use service_object.id
            date=appointment_datetime,
            notes=data.get('notes', ''),
            status='scheduled',
            created_at=datetime.now()
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment scheduled successfully'
        }), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Invalid date format'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        
        # Add timestamp to message
        data['timestamp'] = datetime.now().isoformat()
        contact_messages.append(data)
        
        # Save messages to a JSON file
        with open(dir_path+'contact_messages.json', 'w') as f:
            json.dump(contact_messages, f, indent=2)
        
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Load existing data if available
def load_data():
    global appointments, contact_messages
    
    try:
        if os.path.exists(dir_path+'appointments.json'):
            with open(dir_path+'appointments.json', 'r') as f:
                appointments = json.load(f)
    except:
        appointments = []
    
    try:
        if os.path.exists(dir_path+'contact_messages.json'):
            with open(dir_path+'contact_messages.json', 'r') as f:
                contact_messages = json.load(f)
    except:
        contact_messages = []

@app.route('/chat')
@login_required
def chat():
    user = User.query.get(session['user_id'])
    # Mark all admin messages as read
    unread_messages = Message.query.filter_by(
        user_id=user.id,
        is_from_admin=True,
        is_read=False
    ).all()
    for message in unread_messages:
        message.is_read = True
    db.session.commit()
    return render_template('chat.html', messages=user.chat_history)

@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_message():
    try:
        data = request.get_json()
        message_content = data.get('message')
        
        if not message_content:
            return jsonify({
                'status': 'error',
                'message': 'Message content is required'
            }), 400

        user = User.query.get(session['user_id'])
        
        # Create new message
        new_message = Message(
            content=message_content,
            is_from_admin=False,
            user_id=user.id
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/admin/chats')
@admin_required
def admin_chats():
    # Get users who have messages, ordered by latest message
    users_with_messages = db.session.query(User).join(Message).group_by(User.id).order_by(Message.created_at.desc()).all()
    return render_template('admin/chats.html', users=users_with_messages)

@app.route('/admin/chats/<int:user_id>')
@admin_required
def admin_chat(user_id):
    user = User.query.get_or_404(user_id)
    # Mark all user messages as read
    unread_messages = Message.query.filter_by(
        user_id=user.id,
        is_from_admin=False,
        is_read=False
    ).all()
    for message in unread_messages:
        message.is_read = True
    db.session.commit()
    return render_template('admin/chat.html', user=user, messages=user.chat_history)

@app.route('/api/admin/chat/<int:user_id>/send', methods=['POST'])
@admin_required
def admin_send_message(user_id):
    try:
        data = request.get_json()
        message_content = data.get('message')
        
        if not message_content:
            return jsonify({
                'status': 'error',
                'message': 'Message content is required'
            }), 400

        user = User.query.get_or_404(user_id)
        
        # Create new message
        new_message = Message(
            content=message_content,
            is_from_admin=True,
            user_id=user.id
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    # Get statistics
    stats = {
        'total_users': User.query.count(),
        'appointments_today': Appointment.query.filter(
            Appointment.date >= datetime.now().date(),
            Appointment.date < datetime.now().date() + timedelta(days=1)
        ).count(),
        'unread_messages': Message.query.filter_by(is_read=False, is_from_admin=False).count()
    }

    # Get recent appointments
    recent_appointments = Appointment.query.order_by(Appointment.date.desc()).limit(5).all()

    # Get unread messages with their users
    unread_messages = (
        Message.query
        .filter_by(is_read=False, is_from_admin=False)
        .join(User)
        .order_by(Message.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_appointments=recent_appointments,
                         unread_messages=unread_messages)

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/appointments')
@admin_required
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/admin/appointments/<int:appointment_id>')
@admin_required
def view_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('admin/appointment_details.html', appointment=appointment)

@app.route('/admin/appointments/<int:appointment_id>/status', methods=['POST'])
@admin_required
def update_appointment_status(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Status is required'
            }), 400
            
        appointment.status = data['status']
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment status updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/admin/appointments/<int:appointment_id>/notes', methods=['POST'])
@admin_required
def update_appointment_notes(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        
        if 'notes' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Notes are required'
            }), 400
            
        appointment.notes = data['notes']
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment notes updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/admin/medical-records')
@admin_required
def admin_medical_records():
    users = User.query.filter(User.medical_history != None).all()
    return render_template('admin/medical_records.html', users=users)

@app.route('/admin/users/<int:user_id>/medical-history', methods=['GET', 'POST'])
@admin_required
def admin_medical_history(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)  # Debug log
            
            # Validate required fields
            if not data.get('diagnosis'):
                return jsonify({
                    'status': 'error',
                    'message': 'Diagnosis is required'
                }), 400
            
            # Create new medical record
            new_record = {
                'diagnosis': data.get('diagnosis'),
                'symptoms': data.get('symptoms'),
                'treatment': data.get('treatment'),
                'prescriptions': data.get('prescriptions', []),
                'notes': data.get('notes'),
                'created_at': datetime.now().isoformat(),
                'created_by': {
                    'id': session['user_id'],
                    'first_name': User.query.get(session['user_id']).first_name,
                    'last_name': User.query.get(session['user_id']).last_name
                }
            }
            print("New record:", new_record)  # Debug log
            
            # Initialize medical_history if None
            current_history = user.medical_history or []
            
            # Create a new list and extend it
            new_history = []
            new_history.extend(current_history)
            new_history.append(new_record)
            
            # Update the field
            user.medical_history = new_history
            
            print("Updated medical history:", user.medical_history)  # Debug log
            
            # Force the session to detect the change
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            
            print("Changes committed to database")  # Debug log
            
            return jsonify({
                'status': 'success',
                'message': 'Medical record added successfully'
            })
            
        except Exception as e:
            print("Error:", str(e))  # Debug log
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    return render_template('admin/medical_history.html', user=user)

@app.route('/api/chat/mark-read', methods=['POST'])
@login_required
def mark_messages_read():
    try:
        user = User.query.get(session['user_id'])
        # Mark all admin messages as read
        Message.query.filter_by(
            user_id=user.id,
            is_from_admin=True,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/admin/chat/<int:user_id>/mark-read', methods=['POST'])
@admin_required
def admin_mark_messages_read(user_id):
    try:
        # Mark all user messages as read
        Message.query.filter_by(
            user_id=user_id,
            is_from_admin=False,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Load existing data
    load_data()
    print('dir_path', dir_path)
    # Run the application
    app.run(host='0.0.0.0', port=8080, debug=True) 