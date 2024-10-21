from typing import List, Union

# Notification types
class Notification:
    WELCOME = 'WELCOME'
    CHANGE_OF_STOCK = 'CHANGE_OF_STOCK'
    LOWEST_PRICE = 'LOWEST_PRICE'
    THRESHOLD_MET = 'THRESHOLD_MET'

# Data class for product information in emails
class EmailProductInfo:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

# Data class for the content of emails
class EmailContent:
    def __init__(self, subject: str, body: str):
        self.subject = subject
        self.body = body

THRESHOLD_PERCENTAGE = 40

# Extracts and returns the price from a list of possible elements.
def extract_price(*elements) -> str:
    for element in elements:
        price_text = element.text.strip()

        if price_text:
            clean_price = ''.join(filter(lambda x: x.isdigit() or x == '.', price_text))

            if clean_price:
                first_price = next((match for match in [float(clean_price)] if match is not None), None)

            return str(first_price) if first_price else clean_price
            
    return ''

# Extracts and returns the currency symbol from an element.
def extract_currency(element) -> str:
    currency_text = element.text.strip()[:1]
    return currency_text if currency_text else ""

# Extracts description from two possible elements from Amazon.
def extract_description(soup) -> str:
    selectors = [
        ".a-unordered-list .a-list-item",
        ".a-expander-content p",
        # Add more selectors here if needed
    ]

    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            text_content = '\n'.join(element.get_text(strip=True) for element in elements)
            return text_content

    # If no matching elements were found, return an empty string.
    return ""

def get_highest_price(price_list: List[dict]) -> float:
    highest_price = price_list[0]['price']

    for item in price_list:
        if item['price'] > highest_price:
            highest_price = item['price']

    return highest_price

def get_lowest_price(price_list: List[dict]) -> float:
    lowest_price = price_list[0]['price']

    for item in price_list:
        if item['price'] < lowest_price:
            lowest_price = item['price']

    return lowest_price

def get_average_price(price_list: List[dict]) -> float:
    sum_of_prices = sum(item['price'] for item in price_list)
    average_price = sum_of_prices / len(price_list) if price_list else 0

    return average_price

def get_email_notif_type(scraped_product: dict, current_product: dict) -> Union[str, None]:
    lowest_price = get_lowest_price(current_product['priceHistory'])

    if scraped_product['currentPrice'] < lowest_price:
        return Notification.LOWEST_PRICE
    if not scraped_product['isOutOfStock'] and current_product['isOutOfStock']:
        return Notification.CHANGE_OF_STOCK
    if scraped_product['discountRate'] >= THRESHOLD_PERCENTAGE:
        return Notification.THRESHOLD_MET

    return None

def format_number(num: float = 0) -> str:
    return f"{int(num):,}"
