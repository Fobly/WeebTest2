import sys
import os

# Add the virtual environment site-packages to the path
activate_this = '/var/www/mywebsite/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Add the application directory to the python path
sys.path.append('/var/www/mywebsite')

from app import app, load_data

# Load the data when the WSGI server starts
load_data()

if __name__ == "__main__":
    app.run() 