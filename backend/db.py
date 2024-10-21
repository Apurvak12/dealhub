import sqlite3
from datetime import datetime

DB_NAME = 'products.db'

def create_table():
    """Create a table to store product details if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            current_price INTEGER,
            original_price INTEGER,
            lowest_price INTEGER,
            highest_price INTEGER,
            average_price INTEGER,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_or_update_product(title, current_price):
    """Insert a new product or update an existing one based on the title."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the product exists
    cursor.execute('SELECT * FROM products WHERE title = ?', (title,))
    row = cursor.fetchone()

    if row:
        # Update the existing product's prices
        product_id = row[0]
        original_price = row[3]
        lowest_price = min(row[4], current_price)
        highest_price = max(row[5], current_price)
        new_average = (lowest_price + highest_price) // 2

        cursor.execute('''
            UPDATE products
            SET current_price = ?, lowest_price = ?, highest_price = ?, average_price = ?, last_updated = ?
            WHERE id = ?
        ''', (current_price, lowest_price, highest_price, new_average, datetime.now(), product_id))
        print(f"Updated product '{title}':")
        print(f"Current Price: {current_price}")
        print(f"Lowest Price: {lowest_price}")
        print(f"Highest Price: {highest_price}")
        print(f"Average Price: {new_average}")
    else:
        # Insert a new product
        cursor.execute('''
            INSERT INTO products (title, current_price, original_price, lowest_price, highest_price, average_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, current_price, current_price, current_price, current_price, current_price))
        print(f"Inserted new product '{title}':")
        print(f"Current Price: {current_price}")
        print(f"Lowest Price: {current_price}")
        print(f"Highest Price: {current_price}")
        print(f"Average Price: {current_price}")


    conn.commit()
    conn.close()

def get_product_info(title):
    """Fetch a product's details from the database using the product title."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE title = ?', (title,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_all_products():
    """Fetch all products from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_title(title):
    """Fetch product details by title."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE title = ?', (title,))
    product = cursor.fetchone()
    conn.close()
    return product

