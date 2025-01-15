from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract
import time
import os

# Path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path as per your system

# Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service("path/to/chromedriver")  # Replace with the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Solve CAPTCHA using Tesseract OCR
def solve_captcha(image_path):
    captcha_text = pytesseract.image_to_string(Image.open(image_path), config="--psm 8")
    return captcha_text.strip()

# Scraper with CAPTCHA solver
def scrape_with_captcha():
    driver = initialize_driver()

    try:
        # Open target website
        driver.get("https://example.com/captcha-page")  # Replace with your target URL

        # Wait for CAPTCHA image to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha_image"))  # Update the element ID as per the target website
        )

        # Screenshot CAPTCHA image
        captcha_element = driver.find_element(By.ID, "captcha_image")  # Update the element ID
        captcha_path = "captcha.png"
        captcha_element.screenshot(captcha_path)

        # Solve CAPTCHA
        captcha_text = solve_captcha(captcha_path)
        print(f"Solved CAPTCHA: {captcha_text}")

        # Enter CAPTCHA text
        captcha_input = driver.find_element(By.ID, "captcha_input")  # Update the element ID
        captcha_input.send_keys(captcha_text)

        # Submit form
        submit_button = driver.find_element(By.ID, "submit_button")  # Update the element ID
        submit_button.click()

        # Wait for the page to load
        time.sleep(5)

        # Scrape data
        scraped_data = driver.find_element(By.ID, "data_container").text  # 
Update the element ID
        print(f"Scraped Data: {scraped_data}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Cleanup
        driver.quit()
        if os.path.exists("captcha.png"):
            os.remove("captcha.png")

# Run the scraper
if __name__ == "__main__":
    scrape_with_captcha()