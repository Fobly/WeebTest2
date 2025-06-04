from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.types import TypeDecorator, JSON
import json

db = SQLAlchemy()

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return json.dumps([])
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_from_admin = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)  # Optional
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)  # New field for admin status
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy='dynamic', order_by=Message.created_at)
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    
    # Medical history
    medical_history = db.Column(JSONEncodedDict, default=list)

    @property
    def name(self):
        """Return full name with optional middle name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def chat_history(self):
        """Return messages in format compatible with existing templates"""
        return [
            {
                'content': msg.content,
                'created_at': msg.created_at,
                'is_from_admin': msg.is_from_admin,
                'is_read': msg.is_read
            }
            for msg in self.messages
        ]

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)  # Added notes field
    
    # Relationships
    service = db.relationship('Service', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

    def format_datetime(self):
        """Format the date and time for display"""
        return {
            'date': self.date.strftime('%d.%m.%Y'),
            'datetime': self.date.strftime('%Y-%m-%d %H:%M')
        }

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200))  # URL to photo
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 