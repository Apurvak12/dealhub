from __future__ import annotations
import random

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

    # Define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the title safely
        title_element = soup.select_one('#productTitle')
        title = title_element.text.strip() if title_element else "Unknown Title"

        # Get the current price safely
        current_price_elements = [
            soup.select_one('.a-price .a-price-whole'),
            soup.select_one('#priceblock_ourprice'),
            soup.select_one('#priceblock_dealprice'),
        ]
        current_price = extract_price([elem for elem in current_price_elements if elem is not None])

        # Get the original price safely
        original_price_elements = [
            soup.select_one('.a-price .a-price-symbol'),
            soup.select_one('.a-price.a-text-price span.a-offscreen'),
            soup.select_one('.a-size-base.a-color-price'),
        ]
        original_price = extract_price([elem for elem in original_price_elements if elem is not None])

        # Check if it's out of stock
        out_of_stock_element = soup.select_one('#availability span')
        out_of_stock = out_of_stock_element and out_of_stock_element.text.strip().lower() == 'currently unavailable'

        # Handle images
        img_blk_front = soup.select_one('#imgBlkFront')
        landing_image = soup.select_one('#landingImage')
        images = (
            img_blk_front['src'] if img_blk_front else
            landing_image['src'] if landing_image else
            None
        )
        image_urls = [images] if images else []

        # Extract currency and discount rate safely
        currency = extract_currency(soup.select_one('.a-price-symbol'))
        discount_rate_element = soup.select_one('.savingsPercentage')
        discount_rate = discount_rate_element.text.replace('-', '').replace('%', '') if discount_rate_element else "0"

        # Description extraction
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



 #Example usage:
if __name__ == "__main__":
    url = "https://www.amazon.com/dp/B07FZ8S74R"
    product_data = scrape_amazon_product(url)
    print(product_data)