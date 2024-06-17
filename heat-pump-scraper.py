import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page you want to scrape
url = 'https://www.theheatpumpwarehouse.co.uk/product-category/heat-pumps/air-source-heat-pumps/mitsubishi/'
# Define headers with a common User-Agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to get the HTML of a page
def get_page_html(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Function to extract product data from the page
def extract_product_data(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    products = []
    
    # Debug statement to check if we can find product elements
    product_elements = soup.find_all('div', class_='product-inner')
    print(f"Found {len(product_elements)} products on the page.")
    
    for product in product_elements:
        try:
            name = product.find('h3', class_='woocommerce-loop-product__title').text.strip()
        except AttributeError:
            name = 'N/A'
        
        try:
            price_container = product.find('div', class_="inc-vat")
            price = price_container.find('span', class_='woocommerce-Price-amount amount').text.strip()
        except AttributeError:
            price = 'N/A'
        
        print(f"Product found: {name} - {price}")  # Debug statement to verify product details
        
        products.append({
            'Product Name': name,
            'Price': price
        })
    
    return products

# Main function to scrape the data and save to a CSV
def main():
    page_html = get_page_html(url)
    products = extract_product_data(page_html)
    
    # Save data to CSV
    df = pd.DataFrame(products)
    df.to_csv('hitachi_products.csv', index=False, sep = ';')
    print('Data saved to hitachi_products.csv')

if __name__ == '__main__':
    main()