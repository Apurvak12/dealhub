# app.py

from flask import Flask
from dotenv import load_dotenv
from routes import product_bp
from your_db_connection_file import connect_to_db

app = Flask(__name__)

# Connect to the database
connect_to_db()

# Register the product blueprint
app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run(debug=True)

