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
# driver.get('http://www.google.com/xhtml');
driver.get('http://slc09kas.us.oracle.com:8000/e92ppestx/signon.html')  # PIA URL
wait = WebDriverWait(driver, 10)
# driver.get('http://slc07kzj.us.oracle.com:8000/e92ppvinx/signon.html')  # PIA URL
# time.sleep(4)  # Let the user actually see something!
# Login
#SEARCH_BOX = driver.find_element_by_id('userid')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.ID, 'userid')))
SEARCH_BOX.send_keys('VP1')
#SEARCH_BOX = driver.find_element_by_id('pwd')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.ID, 'pwd')))
SEARCH_BOX.send_keys('VP1')
#SEARCH_BOX = driver.find_element_by_name('Submit')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.NAME, 'Submit')))
SEARCH_BOX.click()