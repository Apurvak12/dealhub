import requests
from bs4 import BeautifulSoup
import os
import json
import random
from utils import extract_currency, extract_description, extract_price

def scrape_amazon_product(url: str):
    if not url:
        return None

    # BrightData proxy configuration
    username = str(os.getenv('BRIGHT_DATA_USERNAME'))
    password = str(os.getenv('BRIGHT_DATA_PASSWORD'))
    port = 22225
    session_id = random.randint(0, 1000000)

    # Set up the proxy options
    proxies = {
        "http": f"http://{username}-session-{session_id}:{password}@brd.superproxy.io:{port}",
        "https": f"http://{username}-session-{session_id}:{password}@brd.superproxy.io:{port}",
    }

    try:
        # Fetch the product page
        response = requests.get(url, proxies=proxies, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product title
        title = soup.select_one('#productTitle').get_text(strip=True)

        current_price = extract_price(
            soup.select_one('.priceToPay span.a-price-whole'),
            soup.select_one('.a.size.base.a-color-price'),
            soup.select_one('.a-button-selected .a-color-base'),
        )

        original_price = extract_price(
            soup.select_one('#priceblock_ourprice'),
            soup.select_one('.a-price.a-text-price span.a-offscreen'),
            soup.select_one('#listPrice'),
            soup.select_one('#priceblock_dealprice'),
            soup.select_one('.a-size-base.a-color-price')
        )

        out_of_stock = soup.select_one('#availability span').get_text(strip=True).lower() == 'currently unavailable'

        images = (
            soup.select_one('#imgBlkFront')['data-a-dynamic-image'] or 
            soup.select_one('#landingImage')['data-a-dynamic-image'] or 
            '{}'
        )

        image_urls = list(json.loads(images).keys())

        currency = extract_currency(soup.select_one('.a-price-symbol'))
        discount_rate = soup.select_one('.savingsPercentage').get_text(strip=True).replace('-', '').replace('%', '')

        description = extract_description(soup)

        # Construct data object with scraped information
        data = {
            "url": url,
            "currency": currency or '$',
            "image": image_urls[0] if image_urls else None,
            "title": title,
            "currentPrice": float(current_price) if current_price else float(original_price),
            "originalPrice": float(original_price) if original_price else float(current_price),
            "priceHistory": [],
            "discountRate": float(discount_rate) if discount_rate else None,
            "category": 'category',  # Change as necessary
            "reviewsCount": 100,
            "stars": 4.5,  # You can adjust this as needed
            "isOutOfStock": out_of_stock,
            "description": description,
            "lowestPrice": float(current_price) if current_price else float(original_price),
            "highestPrice": float(original_price) if original_price else float(current_price),
            "averagePrice": float(current_price) if current_price else float(original_price),
        }

        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
