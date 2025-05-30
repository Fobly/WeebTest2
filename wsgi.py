from app import app, load_data

# Load the data when the WSGI server starts
load_data()

if __name__ == "__main__":
    app.run() 