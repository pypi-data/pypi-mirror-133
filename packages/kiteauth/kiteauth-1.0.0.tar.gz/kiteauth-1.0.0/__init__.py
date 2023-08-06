from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from kiteconnect import KiteConnect
import time

def get_access_token(api_key, api_secret, username, password, mfa_key):
    
    kite = KiteConnect(api_key=api_key)
    login_url = kite.login_url()

    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--verbose")
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        options=options, 
    )

    print("Starting session...")

    driver.get(login_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#userid"))
    ).send_keys(username)

    driver.find_element(By.CSS_SELECTOR, '#password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#container > div > div > div.login-form > form > div.actions > button').click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#pin"))
    ).send_keys(mfa_key)

    driver.find_element(By.CSS_SELECTOR, '#container > div > div > div.login-form > form > div.actions > button').click()

    time.sleep(5)

    request_token = driver.current_url.split('request_token=')[1]

    session = kite.generate_session(request_token=request_token, api_secret=api_secret)
    return session["access_token"]

