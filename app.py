from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
from datetime import datetime
import json

app = Flask(__name__)
dir_path = os.path.dirname(os.path.abspath(__file__))+'/data/users/'



# Store appointments and contact messages (in a real app, you'd use a database)
appointments = []
contact_messages = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<filename>')
def serve_static(filename):
    return render_template(filename)

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