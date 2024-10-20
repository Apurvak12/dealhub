from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, FloatField, BooleanField, ListField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, DateTimeField, DictField

app = Flask(__name__)

# Configure the MongoDB connection
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',  # Replace with your database name
    'host': 'localhost',
    'port': 27017  # Default MongoDB port
}

db = MongoEngine(app)

class PriceHistory(EmbeddedDocument):
    price = FloatField(required=True)
    date = DateTimeField(required=True)

class User(EmbeddedDocument):
    email = StringField(required=True)

class Product(Document):
    url = StringField(required=True, unique=True)
    currency = StringField(required=True)
    image = StringField(required=True)
    title = StringField(required=True)
    currentPrice = FloatField(required=True)
    originalPrice = FloatField(required=True)
    priceHistory = ListField(EmbeddedDocumentField(PriceHistory))
    lowestPrice = FloatField()
    highestPrice = FloatField()
    averagePrice = FloatField()
    discountRate = FloatField()
    description = StringField()
    category = StringField()
    reviewsCount = FloatField()
    isOutOfStock = BooleanField(default=False)
    users = ListField(EmbeddedDocumentField(User))
    
    meta = {
        'collection': 'products',  # Name of the collection in MongoDB
        'timestamps': True          # To automatically add created_at and updated_at fields
    }

# Example usage
if __name__ == "__main__":
    app.run(debug=True)
