# app.py

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from config import Config
from models import Product, mongo
from scraping import scrape_amazon_product
from utils import get_average_price, get_highest_price, get_lowest_price

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

@app.route('/scrape', methods=['POST'])
def scrape_and_store_product():
    data = request.get_json()
    product_url = data.get('url')

    if not product_url:
        return jsonify({"error": "Invalid URL"}), 400

    scraped_product = scrape_amazon_product(product_url)

    if not scraped_product:
        return jsonify({"error": "Failed to scrape product"}), 500

    existing_product = mongo.db.products.find_one({"url": scraped_product["url"]})

    if existing_product:
        updated_price_history = existing_product["price_history"] + [scraped_product["current_price"]]
        updated_product = {
            "url": scraped_product["url"],
            "current_price": scraped_product["current_price"],
            "price_history": updated_price_history,
            "lowest_price": get_lowest_price(updated_price_history),
            "highest_price": get_highest_price(updated_price_history),
            "average_price": get_average_price(updated_price_history),
            "users": existing_product["users"],
        }
        mongo.db.products.update_one({"url": scraped_product["url"]}, {"$set": updated_product})
    else:
        new_product = {
            "url": scraped_product["url"],
            "current_price": scraped_product["current_price"],
            "price_history": [scraped_product["current_price"]],
            "lowest_price": scraped_product["current_price"],
            "highest_price": scraped_product["current_price"],
            "average_price": scraped_product["current_price"],
            "users": []
        }
        mongo.db.products.insert_one(new_product)

    return jsonify(scraped_product), 200

@app.route('/products/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = mongo.db.products.find_one({"_id": product_id})

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200

@app.route('/products', methods=['GET'])
def get_all_products():
    products = list(mongo.db.products.find())
    return jsonify(products), 200

@app.route('/similar/<product_id>', methods=['GET'])
def get_similar_products(product_id):
    current_product = mongo.db.products.find_one({"_id": product_id})

    if not current_product:
        return jsonify({"error": "Product not found"}), 404

    similar_products = list(mongo.db.products.find({"_id": {"$ne": product_id}}).limit(3))
    return jsonify(similar_products), 200

@app.route('/add_user_email/<product_id>', methods=['POST'])
def add_user_email_to_product(product_id):
    data = request.get_json()
    user_email = data.get('email')

    if not user_email:
        return jsonify({"error": "Email is required"}), 400

    product = mongo.db.products.find_one({"_id": product_id})

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if user_email not in product.get("users", []):
        mongo.db.products.update_one({"_id": product_id}, {"$addToSet": {"users": user_email}})

    return jsonify({"message": "Email added successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
