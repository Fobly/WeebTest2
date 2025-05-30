# Bright Smile Dental Clinic Website

A modern, responsive website for a dental clinic built with HTML, CSS, JavaScript, and Flask.

## Features

- Responsive design that works on all devices
- Interactive navigation with smooth scrolling
- Service showcase with hover effects
- Team member profiles
- Contact form with server-side storage
- Appointment booking system
- Emergency contact information
- Social media integration

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Website

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

The website will be available at the above URL.

## File Structure

- `index.html` - Main homepage
- `services.html` - Services page
- `about.html` - About us page
- `contact.html` - Contact page
- `booking.html` - Appointment booking page
- `styles.css` - All website styles
- `script.js` - Client-side JavaScript
- `app.py` - Flask server application
- `requirements.txt` - Python dependencies
- `appointments.json` - Stored appointment data
- `contact_messages.json` - Stored contact form messages

## Development

- The website uses Flask's development server with debug mode enabled
- Form submissions are stored in JSON files (in a production environment, use a proper database)
- Static files are served directly by Flask

## Production Deployment

For production deployment:

1. Disable debug mode in `app.py`
2. Use a production-grade WSGI server (e.g., Gunicorn)
3. Set up a proper database instead of JSON files
4. Configure proper security headers
5. Use HTTPS
6. Set up proper logging

## License

This project is licensed under the MIT License - see the LICENSE file for details. 