from flask import Flask, request, jsonify
from db import create_table, insert_or_update_product, get_all_products, get_product_info
from scrapping import fetch_webpage_content
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/fetch', methods=['POST'])
def fetch_product():
    """Fetch product details and store them in the database."""
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    title, current_price, _ = fetch_webpage_content(url)
    
    if title and current_price:
        insert_or_update_product(title, current_price)
        return jsonify({'message': f'Updated {title} in the database.','title':title, 'current_price':current_price,'image':"image"}), 200
    else:
        return jsonify({'error': 'Failed to fetch product info.'}), 500
@app.route('/fetchs', methods=['POST'])
def fetchs():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Check if title is provided in the request
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required."}), 400

    title = data['title']
    product_details = get_product_info(title)

    if product_details:
        return jsonify({
            "id": product_details[0],
            "title": product_details[1],
            "current_price": product_details[2],
            "original_price": product_details[3],
            "lowest_price": product_details[4],
            "highest_price": product_details[5],
            "average_price": product_details[6],
            "last_updated": product_details[7]
        })
    else:
        return jsonify({"error": "Product not found."}), 404

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products."""
    products = get_all_products()
    return jsonify(products)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)