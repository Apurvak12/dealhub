from flask import Flask
from flask_mongoengine import MongoEngine
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
db = MongoEngine()

is_connected = False  # Variable to track the connection status

def connect_to_db():
    global is_connected

    mongo_uri = os.getenv("MONGODB_URI")
    
    if not mongo_uri:
        print("MONGODB_URI is not defined")
        return

    if is_connected:
        print("=> using existing database connection")
        return

    try:
        app.config['MONGODB_SETTINGS'] = {
            'host': mongo_uri
        }
        db.init_app(app)  # Initialize MongoEngine with Flask app
        db.connection  # This line will establish the connection
        is_connected = True
        print("MongoDB Connected")
    except Exception as error:
        print("Error connecting to MongoDB:", error)

# Example usage
if __name__ == "__main__":
    connect_to_db()  # Connect to the database when running the application
    app.run(debug=True)
