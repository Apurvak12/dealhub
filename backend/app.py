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
    
    # Check if URL is provided in the request body
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Fetch webpage content (scraping)
    result = fetch_webpage_content(url)
    
    # Ensure that valid data was returned
    if result:
        try:
            title, current_price, image = result  # Ensure the result contains the required data
        except ValueError:
            return jsonify({'error': 'Unexpected data format returned from fetch_webpage_content.'}), 500
        
        # Insert or update the product in the database
        insert_or_update_product(title, current_price)
        
        # Return success response
        return jsonify({
            'message': f'Updated {title} in the database.',
            'title': title,
            'current_price': current_price,
            'image': image  # Assuming image is being fetched
        }), 200
    else:
        return jsonify({'error': 'Failed to fetch product info.'}), 500


@app.route('/fetchs', methods=['POST'])
def fetchs():
    """Fetch product details by title."""
    data = request.get_json()

    # Ensure title is provided in the request body
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required."}), 400

    title = data['title']
    
    # Get product details from the database
    product_details = get_product_info(title)
    
    if product_details:
        # Construct the product details response
        return jsonify({
            "id": product_details[0],
            "title": product_details[1],
            "current_price": product_details[2],
            "original_price": product_details[3],
            "lowest_price": product_details[4],
            "highest_price": product_details[5],
            "average_price": product_details[6],
            "last_updated": product_details[7]
        }), 200
    else:
        return jsonify({"error": "Product not found."}), 404


@app.route('/products', methods=['GET'])
def get_products():
    """Get all products from the database."""
    products = get_all_products()
    
    # Return list of products
    return jsonify(products), 200


if __name__ == '__main__':
    # Ensure the database table is created
    create_table()
    
    # Start the Flask app
    app.run(debug=True)
