import requests
from bs4 import BeautifulSoup
from price_str_to_int import clean_and_convert_price
import sqlite3
from datetime import datetime

DB_NAME = 'product.db'


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
             image_url TEXT,
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


def insert_or_update_product(title, current_price,image_url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the product exists
    cursor.execute('SELECT * FROM products WHERE title = ?', (title,))
    row = cursor.fetchone()

    if row:
        # Update the existing product's prices
        product_id = row[0]
        original_price = row[3] if row[3] else current_price  # Ensure original_price is not None
        lowest_price = min(row[4], current_price) if row[4] else current_price
        highest_price = max(row[5], current_price) if row[5] else current_price
        new_average = (lowest_price + highest_price) // 2

        cursor.execute('''
            UPDATE products
            SET current_price = ?, lowest_price = ?, highest_price = ?, average_price = ?, last_updated = ?
            WHERE id = ?
        ''', (current_price, lowest_price, highest_price, new_average, datetime.now(), product_id))
        
        # Print updated product information
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

        # Print newly inserted product information
        print(f"Inserted new product '{title}':")
        print(f"Current Price: {current_price}")
        print(f"Lowest Price: {current_price}")
        print(f"Highest Price: {current_price}")
        print(f"Average Price: {current_price}")

    conn.commit()
    conn.close()


def fetch_webpage_content(url: str):
    if not url:
        return None
    # Fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')

        # Fetch the product title (example assumes title is in <span> with id='productTitle')
        title = soup.find('span', id='productTitle')
        price = soup.find('span', class_='a-price-whole')  
        image = soup.find('img', id='landingImage')
        product_details = soup.find('table', class_='a-normal a-spacing-micro')

        # Check if title and price are found
        if title and price:
            title_text = title.get_text(strip=True)
            price_text = price.get_text(strip=True)
            current_price = clean_and_convert_price(price_text)
            image_url = image['src']

            # Print the fetched product title and price
            print("Product Title:", title_text)
            print("Product Price:", price_text)
            print("Product Image URL:", image_url)

            # Prepare to collect product details
            table_data = {}
            if product_details:
                # Loop through each row in the table body
                for row in product_details.find_all('tr'):
                    # Extract the table header (key) and the table data (value)
                    key = row.find('td', class_='a-span3')
                    value = row.find('td', class_='a-span9')
                    
                    if key and value:  # Ensure both key and value are found
                        table_data[key.get_text(strip=True)] = value.get_text(strip=True)

                # Print the extracted table data
                for key, value in table_data.items():
                    print(f"{key}: {value}")

            return [title_text, current_price, image_url,table_data]

        else:
            print("Failed to fetch title or price.")
            return None
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    create_table()
    url = 'https://www.amazon.in/HP-GeForce-Graphics-Response-15-fb0106AX/dp/B0BWS9YNCX/ref=asc_df_B0BWS9YNCX/?tag=googleshopdes-21&linkCode=df0&hvadid=709855510254&hvpos=&hvnetw=g&hvrand=5473536068874361193&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9299869&hvtargid=pla-2007836798308&psc=1&mcid=15cc96ee31fc35c8a19e6d73773f6eb2&gad_source=1'
    product_data = fetch_webpage_content(url)

    if product_data:
        title, current_price, details,image_url = product_data
        insert_or_update_product(title, current_price,image_url)
