# import requests
# from bs4 import BeautifulSoup
# from price_str_to_int import clean_and_convert_price

# # Specify the URL of the webpage you want to scrape
# # url = 'https://www.amazon.in/Samsung-Galaxy-Display-Expandable-Tablet/dp/B0CHZ2X647?ref=dlx_great_dg_dcl_B0CHZ2X647_dt_sl8_14&th=1'  # Replace with your actual URL

# def fetch_webpage_content(url: str):
#     if not url:
#         return None
#     # Fetch the webpage content
#     response = requests.get(url)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content
#         soup = BeautifulSoup(response.content, 'lxml')

#         # Fetch the product title (example assumes title is in <span> with id='productTitle')
#         title = soup.find('span', id='productTitle')
#         price = soup.find('span', class_='a-price-whole')  
#         product_details = soup.find('table', class_='a-normal a-spacing-micro')
        
#         table_data = {}

#         # Loop through each row in the table body
#         for row in product_details.find_all('tr'):
#             # Extract the table header (key) and the table data (value)
#             key = row.find('td', class_='a-span3').get_text(strip=True)
#             value = row.find('td', class_='a-span9').get_text(strip=True)
            
#             # Store the key-value pair in the dictionary
#             table_data[key] = value

#         # Print the extracted table data
#         for key, value in table_data.items():
#             print(f"{key}: {value}")
#         if title:
#             print("Product Title:", title.get_text(strip=True))
#         else:
#             print("Product Title not found")

#         # Print the product price
#         if price:
#             print("Product Price:", price.get_text(strip=True))
#         else:
#             print("Product Price not found")

#         if product_details:
#             print("Product Details:")
#             print(table_data)
#         else:
#             print("Product Details not found")
#     else:
#         print(f"Failed to retrieve the page. Status code: {response.status_code}")
#     return [title.get_text(strip=True), clean_and_convert_price(price.get_text(strip=True)), table_data]

# # fetch_webpage_content(url)
import requests
from bs4 import BeautifulSoup
from price_str_to_int import clean_and_convert_price

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
        product_details = soup.find('table', class_='a-normal a-spacing-micro')

        # Create an empty dictionary to store the table data
        table_data = {}

        # Check if the table with product details exists
        if product_details:
            # Loop through each row in the table body
            for row in product_details.find_all('tr'):
                # Extract the table header (key) and the table data (value)
                key = row.find('td', class_='a-span3').get_text(strip=True)
                value = row.find('td', class_='a-span9').get_text(strip=True)
                
                # Store the key-value pair in the dictionary
                table_data[key] = value
        else:
            print("Product Details table not found")

        # Print the extracted table data
        if table_data:
            print("Product Details:")
            for key, value in table_data.items():
                print(f"{key}: {value}")
        else:
            print("No product details found")

        # Print the product title
        if title:
            print("Product Title:", title.get_text(strip=True))
        else:
            print("Product Title not found")

        # Print the product price
        if price:
            print("Product Price:", price.get_text(strip=True))
        else:
            print("Product Price not found")

        return [
            title.get_text(strip=True) if title else None,
            clean_and_convert_price(price.get_text(strip=True)) if price else None,
            table_data
        ]

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
