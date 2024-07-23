import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page you want to scrape
url = 'https://mcscertified.com/product-directory/'
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
    manufacturers = []
    
    # Debug statement to check if we can find product elements
    select_elements = soup.find_all('select', id='msw-product-launchpad-manufacturer')

    options = select_element.find_all('option')

    print(f"Found {len(options)} products on the page.")

# Main function to scrape the data and save to a CSV
def main():
    page_html = get_page_html(url)
    products = extract_product_data(page_html)
    
    # Save data to CSV
    df = pd.DataFrame(products)
   # df.to_csv('heat-pump-manufacturers.csv', index=False, sep = ';')
  #  print('Data saved to heat-pump-manufacturers.csv')
    df
 
if __name__ == '__main__':
    main()