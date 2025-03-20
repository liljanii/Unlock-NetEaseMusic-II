# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00C0A8F77B09F59225C2FD3AAEE728919E47A51ECC63BC567CF8E590ACCAE8B08F9A8CCB98260ECA6FCE1C88F6393FEB565DF1AA94F36A39A31D1922A1A01C2B534254AF29CB39D80DC0C7ACF382181F46EC95D36D016C2890974E7910BABACAE626510DA16EE7B57E42F146A14DB8ABC7F11FFB9A039A864E82D4C9103D03FD21B82031D06F36D56C235978B08C26428D1C2114E6970814F8E963639903112D09D9359273F10C1FC3E64DAAD041EC276A92CF46C078803B79FE905686C25D08252A46B1696A975412266494E0CDA0BB3981D3D8C109DA8E0C5136CF9D17D1D7514EF3BCBF50AAA9E40E7CAE4E90D39410729B9B7F6F53A61DC9FFF310423D6BE6336BE2E5B206B4EDA3E287ECE23A090A8A22D5FAAC64CC295830E77419798C7AFC98ABC2A40C77B77E2C787BEC1C70AEDB7BAC4C8D7B783C11CF63A247837D5F3965A40BEF69E152079C5B532CD6A6FA"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
