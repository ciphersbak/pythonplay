# This script will extend DB time intervals on DEP
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests

proxies = {
    "http": "http://www-proxy-idc.in.oracle.com:80",
    "https": "http://www-proxy-idc.in.oracle.com:80",
}
driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
wait = WebDriverWait(driver, 10)
driver.get('https://dsiweb01.us.oracle.com/dep/login.asp?WHO=')  # DEP URL
# time.sleep(4)  # Let the user actually see something!
# Login
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.NAME, 'WHO')))
SEARCH_BOX.send_keys('VP1')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.NAME, 'sPassword')))
SEARCH_BOX.send_keys('VP1')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.NAME, 'Submit')))
SEARCH_BOX.click()