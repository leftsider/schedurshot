import csv
import time as t
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('start-fullscreen')
chrome_options.add_argument("user-data-dir=selenium")

webdriver_service = Service("chromedriver/chromedriver") ## path to where you saved chromedriver binary

# Ask for the name of the CSV file
csv_file = input("Please enter the name of the CSV file (including the .csv extension): ")

# Read URLs from the provided CSV file
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    urls_list = list(reader)

# Get the directory of the CSV file
dir_path = os.path.dirname(os.path.realpath(csv_file))

def get_screenshots_and_save(list_of_urls):
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    # Pause the script and wait for you to log in
    input("Please log in and then press Enter to continue...")
    for url in list_of_urls:
        try:
            browser.get(url[0]) # Access the first element of each row, which should be the URL
            page = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.TAG_NAME, "body")))
            t.sleep(5)
            now = datetime.now()
            date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
            sh_url = url[0].split('://')[1].split('.')[0]
            filename = f'{sh_url}_{date_time}.png'
            print(sh_url, date_time)
            browser.save_screenshot(os.path.join(dir_path, filename)) # Save a full page screenshot
            print('screenshotted ', url[0])
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            t.sleep(2)
    browser.quit()

# Call the function directly
get_screenshots_and_save(urls_list)
