from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
from scrapping import scrape_amazon_product
from utils import get_average_price, get_highest_price, get_lowest_price
from nodemailer import generate_email_body, send_email

app = Flask(__name__)

# Initialize MongoDB client
client = MongoClient("your_mongodb_uri")
db = client['your_database_name']
products_collection = db['products']


def connect_to_db():
    # This function is redundant if you are using the global `db` object
    return db


def scrape_and_store_product(product_url):
    if not product_url:
        return

    try:
        scraped_product = scrape_amazon_product(product_url)

        if not scraped_product:
            return

        product = scraped_product

        existing_product = products_collection.find_one({"url": scraped_product['url']})

        if existing_product:
            updated_price_history = existing_product['priceHistory'] + [{'price': scraped_product['currentPrice']}]

            product = {
                **scraped_product,
                'priceHistory': updated_price_history,
                'lowestPrice': get_lowest_price(updated_price_history),
                'highestPrice': get_highest_price(updated_price_history),
                'averagePrice': get_average_price(updated_price_history),
            }

        new_product = products_collection.find_one_and_update(
            {"url": scraped_product['url']},
            {"$set": product},
            upsert=True,
            return_document=True
        )

        # Assuming you have a function to handle revalidation logic
        revalidate_path(f"/products/{new_product['_id']}")

    except Exception as error:
        raise Exception(f"Failed to create/update product: {str(error)}")


def get_product_by_id(product_id):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})

        if not product:
            return None

        return product

    except Exception as error:
        print(error)


def get_all_products():
    try:
        products = list(products_collection.find())
        return products

    except Exception as error:
        print(error)


def get_similar_products(product_id):
    try:
        current_product = products_collection.find_one({"_id": ObjectId(product_id)})

        if not current_product:
            return None

        similar_products = list(products_collection.find({"_id": {"$ne": ObjectId(product_id)}}).limit(3))
        return similar_products

    except Exception as error:
        print(error)


def add_user_email_to_product(product_id, user_email):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})

        if not product:
            return

        user_exists = any(user['email'] == user_email for user in product.get('users', []))

        if not user_exists:
            product['users'].append({'email': user_email})

            products_collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": {"users": product['users']}}
            )

            email_content = generate_email_body(product, "WELCOME")

            send_email(email_content, [user_email])

    except Exception as error:
        print(error)


# Example usage
if __name__ == "__main__":
    app.run(debug=True)
