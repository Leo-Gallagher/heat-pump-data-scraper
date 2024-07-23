from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page you want to scrape
url = 'https://mcscertified.com/product-directory/'

# Path to the ChromeDriver
chromedriver_path = 'chromedriver-mac-arm64/chromedriver'  # Update this path to your actual chromedriver path

# Initialize the WebDriver
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

# Function to get the HTML of a page
def get_page_html(url):
    driver.get(url)

    # Handle the cookies pop-up
    try:
        # Update the selector for the cookies accept button
        accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
        accept_button.click()
    except Exception as e:
        print("No cookies pop-up found or could not click it:", e)

     # Click the Manufacturer tab
    try:
        manufacturer_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="msw-launchpad"]/div[1]/div[3]')))
        # Scroll into view if necessary
        actions = ActionChains(driver)
        actions.move_to_element(manufacturer_tab).perform()
        manufacturer_tab.click()
    except Exception as e:
        print("Manufacturer tab not found or could not click it:", e)

    # Wait until the select element is present
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'msw-product-launchpad-manufacturer')))
    # Wait for the options to be loaded
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#msw-product-launchpad-manufacturer option')))
    return driver.page_source

    # Wait until the select element is present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'msw-product-launchpad-manufacturer')))
    # Wait for the options to be loaded
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#msw-product-launchpad-manufacturer option')))
    return driver.page_source

# Function to extract manufacturer data from the page
def extract_manufacturer_data(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    manufacturers = []
    
    # Find the select element by its id
    select_element = soup.find('select', id='msw-product-launchpad-manufacturer')
    
    # Debug statement to check if select element is found
    if select_element:
        print("Select element found")
    else:
        print("Select element not found")
    
    if select_element:
        # Extract the values of the option elements
        options = select_element.find_all('option')
        
        # Debug statement to check if options are found
        print(f"Found {len(options)} options")
        
        for option in options:
            value = option.get('value')
            if value and value != 'Please select':  # Skip the 'Please select' option
                manufacturers.append(value)
    
    return manufacturers

# Main function to scrape the data and save to a CSV
def main():
    page_html = get_page_html(url)
    manufacturers = extract_manufacturer_data(page_html)
    
    # Debug statement to print manufacturers list
    print("Manufacturers:", manufacturers)
    
    # Save data to CSV
    if manufacturers:
        df = pd.DataFrame(manufacturers, columns=['Manufacturer'])
        df.to_csv('heat_pump_manufacturers.csv', index=False, sep=';')
        print('Data saved to heat_pump_manufacturers.csv')
    else:
        print('No manufacturers found to save.')

if __name__ == '__main__':
    main()
    # Close the WebDriver
    driver.quit()
