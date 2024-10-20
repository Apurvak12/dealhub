from flask import Flask
from flask_mongoengine import MongoEngine
from routes import product_bp  # Import your blueprint

app = Flask(__name__)

# Configure your MongoDB connection
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'localhost',
    'port': 27017
}

# Initialize the database
db = MongoEngine(app)

# Register the blueprint
app.register_blueprint(product_bp, url_prefix='/api')  # All product routes will start with /api

if __name__ == '__main__':
    app.run(debug=True)


