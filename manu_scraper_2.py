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

# Function to extract manufacturer data from the page
def extract_manufacturer_data(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    manufacturers = []
    
    # Find the select element by its id
    select_element = soup.find('select', id='msw-product-launchpad-manufacturer')
    
    if select_element:
        # Extract the values of the option elements
        options = select_element.find_all('option')
        
        for option in options:
            value = option.get('value')
            if value and value != 'Please select':  # Skip the 'Please select' option
                manufacturers.append(value)
    
    return manufacturers

# Main function to scrape the data and save to a CSV
def main():
    page_html = get_page_html(url)
    manufacturers = extract_manufacturer_data(page_html)
    
    # Save data to CSV
    df = pd.DataFrame(manufacturers, columns=['Manufacturer'])
    df.to_csv('heat_pump_manufacturers.csv', index=False, sep=';')
    print('Data saved to heat_pump_manufacturers.csv')

if __name__ == '__main__':
    main()
