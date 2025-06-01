from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect, flash, session
import os
from datetime import datetime, timedelta
import json
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Appointment
from functools import wraps

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
    
    # Create a test user if it doesn't exist
    test_email = 'test@example.com'
    if not User.query.filter_by(email=test_email).first():
        test_user = User(
            name='Test User',
            email=test_email,
            password=generate_password_hash('password123'),
            birth_date=datetime.now().date(),
            chat_history=[],
            medical_history=[]
        )
        db.session.add(test_user)
        db.session.commit()
        print(f'Created test user with email: {test_email} and password: password123')

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

# Context processor to make user data available in all templates
@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}

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

        if user and check_password_hash(user.password, password):
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
            
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            birth_date = data.get('birth_date')

            if User.query.filter_by(email=email).first():
                return jsonify({'status': 'error', 'message': 'Email уже зарегистрирован'}), 400

            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password),
                birth_date=datetime.strptime(birth_date, '%Y-%m-%d').date(),
                chat_history=[],
                medical_history=[]
            )
            
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'status': 'success', 'redirect': url_for('login')})

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

# Protected routes example
@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.get_json()
        
        # Add timestamp to appointment
        data['timestamp'] = datetime.now().isoformat()
        appointments.append(data)
        
        # Save appointments to a JSON file
        with open(dir_path+'appointments.json', 'w') as f:
            json.dump(appointments, f, indent=2)
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment scheduled successfully'
        }), 200
    except Exception as e:
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

if __name__ == '__main__':
    # Load existing data
    load_data()
    print('dir_path', dir_path)
    # Run the application
    app.run(host='0.0.0.0', port=8000, debug=True) 