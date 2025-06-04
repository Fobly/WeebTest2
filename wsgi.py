import sys
import os

# Add the application directory to the python path
sys.path.append('/var/www/mywebsite')

# Set up virtual environment
venv_path = '/var/www/mywebsite/venv'
python_version = 'python3.10'  # Измените на вашу версию Python
site_packages = os.path.join(venv_path, 'lib', python_version, 'site-packages')
sys.path.insert(0, site_packages)

from app import app, load_data

# Load the data when the WSGI server starts
load_data()

if __name__ == "__main__":
    app.run() 