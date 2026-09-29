from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from web_links import WEBSITES
import os

# Streamlit app URL from environment variable (or default)
# STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://benson-mugure-portfolio.streamlit.app/")

def main():
    options = Options()
    if os.getenv('HEADLESS', '').lower() in {'1', 'true', 'yes'}:
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for web_site in WEBSITES:
            try:
                driver.get(web_site)
                print(f"Opened {web_site}")

                wait = WebDriverWait(driver, 15)
                try:
                    button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
                    )
                except TimeoutException:
                    print("No wake-up button found. Assuming app is already awake ✅")
                    continue

                print("Wake-up button found. Clicking...")
                button.click()

                try:
                    wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
                    print("Button clicked and disappeared ✅ (app should be waking up)")
                except TimeoutException as error:
                    print("Button was clicked but did NOT disappear ❌ (possible failure)")
                    raise RuntimeError("Wake-up button remained visible after clicking.") from error

            except Exception as error:
                print(f"Unexpected error: {error}")
                raise
    finally:
        if driver is not None:
            driver.quit()
        print("Script finished.")

if __name__ == "__main__":
    main()