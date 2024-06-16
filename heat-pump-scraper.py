import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = 'https://theheatpumpwarehouse.co.uk'
category_url = f'{base_url}/product-category/heat-pumps/air-source-heat-pumps/'

# Define headers with a common User-Agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Create a session to persist headers across requests
session = requests.Session()
session.headers.update(headers)

# Function to get the HTML of a page
def get_page_html(url):
    response = session.get(url)
    response.raise_for_status()
    return response.text

# Function to extract product data from a product page

def extract_product_data(product_url):
    product_html = get_page_html(product_url)
    product_soup = BeautifulSoup(product_html, 'html.parser')
    
    try:
        name = product_soup.find('h1', class_='product_title').text.strip()
    except AttributeError:
        name = 'N/A'
    
    try:
        price = product_soup.find('span', class_='woocommerce-Price-amount amount').text.strip()
    except AttributeError:
        price = 'N/A'
    
    try:
        sku = product_soup.find('span', class_='sku').text.strip() if product_soup.find('span', class_='sku') else 'N/A'
    except AttributeError:
        sku = 'N/A'
    
    try:
        description = product_soup.find('div', class_='woocommerce-product-details__short-description').text.strip()
    except AttributeError:
        description = 'N/A'
    
    return {
        'Product Name': name,
        'Price': price,
        'SKU': sku,
        'Description': description,
        'URL': product_url
    }

# Function to extract product links from a category page
def extract_product_links(category_html):
    soup = BeautifulSoup(category_html, 'html.parser')
    product_links = []
    for link in soup.select('h2.woocommerce-loop-product__title a'):
        product_links.append(link['href'])
    return product_links

# Function to handle pagination and scrape all products
def scrape_category(category_url):
    products = []
    page = 1
    
    while True:
        print(f'Scraping page {page}...')
        url = f'{category_url}/page/{page}/'
        category_html = get_page_html(url)
        product_links = extract_product_links(category_html)
        
        if not product_links:
            break
        
        for product_link in product_links:
            product_data = extract_product_data(product_link)
            products.append(product_data)
            time.sleep(1)  # Sleep to be respectful of the website's server
        
        page += 1
        time.sleep(2)  # Sleep to avoid getting blocked
    
    return products

# Main function to scrape all categories and save to a CSV
def main():
    all_products = []
    category_html = get_page_html(category_url)
    soup = BeautifulSoup(category_html, 'html.parser')
    
    # Extract links to subcategories (brands)
    subcategory_links = [a['href'] for a in soup.select('ul.product-categories li.cat-item a')]
    
    for subcategory_link in subcategory_links:
        print(f'Scraping category: {subcategory_link}')
        products = scrape_category(subcategory_link)
        all_products.extend(products)
    
    # Save data to CSV
    df = pd.DataFrame(all_products)
    df.to_csv('heat_pump_products.csv', index=False)
    print('Data saved to heat_pump_products.csv')

if __name__ == '__main__':
    main()