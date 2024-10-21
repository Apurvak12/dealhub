import re

def clean_and_convert_price(price_str):
    # Remove any non-numeric characters except for commas, periods, or negative signs
    cleaned_price = re.sub(r'[^\d.,-]', '', price_str)
    
    # Remove commas (commas are typically thousand separators)
    cleaned_price = cleaned_price.replace(',', '')
    
    # If there's a period, remove it if it's at the end, otherwise assume it's a decimal point
    if cleaned_price.endswith('.'):
        cleaned_price = cleaned_price[:-1]
    
    # Convert the cleaned string to integer (ignore decimal part if present)
    try:
        price_int = int(float(cleaned_price))  # Convert to float first, then to int to drop decimal
    except ValueError:
        raise ValueError(f"Invalid price format: {price_str}")
    
    return price_int
