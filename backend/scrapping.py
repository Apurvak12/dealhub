import requests
from bs4 import BeautifulSoup
import json
import os

def extract_currency(symbol_element):
    return symbol_element.text.strip() if symbol_element else '$'

def extract_price(price_elements):
    for element in price_elements:
        if element:
            price = element.text.strip().replace(',', '').replace('$', '')
            if price.isdigit():
                return float(price)
    return None

def extract_description(soup):
    description = soup.select_one('#productDescription')
    return description.text.strip() if description else ""

def scrape_amazon_product(url):
    if not url:
        return None

    # BrightData proxy configuration (for illustration, use your actual proxy if needed)
    username = os.getenv('BRIGHT_DATA_USERNAME')
    password = os.getenv('BRIGHT_DATA_PASSWORD')
    port = 22225
    session_id = int(1000000 * random.random())

    # Proxy settings
    proxy_url = f"http://{username}-session-{session_id}:{password}@brd.superproxy.io:{port}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        # Fetch the product page
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the product title
        title = soup.select_one('#productTitle').text.strip()

        current_price = extract_price([
            soup.select_one('.priceToPay .a-price-whole'),
            soup.select_one('.a.size.base.a-color-price'),
            soup.select_one('.a-button-selected .a-color-base'),
        ])

        original_price = extract_price([
            soup.select_one('#priceblock_ourprice'),
            soup.select_one('.a-price.a-text-price span.a-offscreen'),
            soup.select_one('#listPrice'),
            soup.select_one('#priceblock_dealprice'),
            soup.select_one('.a-size-base.a-color-price'),
        ])

        out_of_stock = soup.select_one('#availability span').text.strip().lower() == 'currently unavailable'

        images = (
            soup.select_one('#imgBlkFront')['data-a-dynamic-image'] or
            soup.select_one('#landingImage')['data-a-dynamic-image'] or
            '{}'
        )

        image_urls = list(json.loads(images).keys())

        currency = extract_currency(soup.select_one('.a-price-symbol'))
        discount_rate = soup.select_one('.savingsPercentage').text.replace('-', '').replace('%', '')

        description = extract_description(soup)

        # Construct data object with scraped information
        data = {
            "url": url,
            "currency": currency or '$',
            "image": image_urls[0] if image_urls else None,
            "title": title,
            "currentPrice": current_price or original_price,
            "originalPrice": original_price or current_price,
            "priceHistory": [],
            "discountRate": float(discount_rate) if discount_rate.isdigit() else 0,
            "category": "category",
            "reviewsCount": 100,
            "stars": 4.5,
            "isOutOfStock": out_of_stock,
            "description": description,
            "lowestPrice": current_price or original_price,
            "highestPrice": original_price or current_price,
            "averagePrice": current_price or original_price,
        }

        return data
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    url = "https://www.amazon.com/example-product-url"
    product_data = scrape_amazon_product(url)
    print(product_data)

