# routes.py

from flask import Blueprint, request, jsonify
from models import Product, db

# Create a Blueprint for your routes
product_bp = Blueprint('products', __name__)

# Route to create or update a product
@product_bp.route('/products', methods=['POST'])
def create_or_update_product():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    try:
        product, created = Product.objects.get_or_create(url=data['url'])
        product.update(**data)  # Update product with new data
        product.save()
        return jsonify(product.to_json()), 200 if not created else 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get a product by ID
@product_bp.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.objects(id=product_id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_json()), 200

# Route to get all products
@product_bp.route('/products', methods=['GET'])
def get_all_products():
    products = Product.objects()
    return jsonify(products), 200

# Route to get similar products (for demonstration, returning the first 3)
@product_bp.route('/products/<string:product_id>/similar', methods=['GET'])
def get_similar_products(product_id):
    current_product = Product.objects(id=product_id).first()
    if not current_product:
        return jsonify({'error': 'Product not found'}), 404
    similar_products = Product.objects(id__ne=product_id).limit(3)
    return jsonify(similar_products), 200

# Route to add a user's email to a product
@product_bp.route('/products/<string:product_id>/users', methods=['POST'])
def add_user_email_to_product(product_id):
    data = request.json
    user_email = data.get('email')

    if not user_email:
        return jsonify({'error': 'Email is required'}), 400

    product = Product.objects(id=product_id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if any(user['email'] == user_email for user in product.users):
        return jsonify({'message': 'User already exists'}), 409

    product.users.append({'email': user_email})
    product.save()
    
    return jsonify({'message': 'User added successfully'}), 201
