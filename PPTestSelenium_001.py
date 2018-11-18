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

# requests.get("http://www.google.com/xhtml", proxies=proxies)
# Optional argument, if not specified will search path.
driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
# driver.get('http://www.google.com/xhtml');
wait = WebDriverWait(driver, 10)
driver.get('http://slc10pqi.us.oracle.com:8000/psp/e92ppi14x/EMPLOYEE/ERP/c/MANAGE_ASSETS.BASIC.GBL?')  # PIA URL
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
# Change iFrame
frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
driver.switch_to.frame(frame)
# On Search Page
#SEARCH_BOX = driver.find_element_by_name('ASSET_SRCH_PARENT_ID')
SEARCH_BOX = wait.until(EC.element_to_be_clickable(
    (By.NAME, 'ASSET_SRCH_PARENT_ID')))
SEARCH_BOX.send_keys('000000000034')  # This is the parent asset
# SEARCH_BOX = driver.find_element_by_id('#ICSearch')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.ID, '#ICSearch')))
SEARCH_BOX.click()
SEARCH_BOX.send_keys('Alt+1')  # Search
# time.sleep(4)  # Let the user actually see something!
# This one works, it selects the first row
#SEARCH_BOX = driver.find_element_by_id('SEARCH_RESULT1')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.ID, 'SEARCH_RESULT1')))
SEARCH_BOX.click()
SEARCH_BOX.submit()
# SEARCH_BOX.send_keys('ChromeDriver')
# SEARCH_BOX.submit()
# time.sleep(4)  # Let the user actually see something!
# Choose the 3rd tab Asset Acquisition Details Tab
#SEARCH_BOX = driver.find_element_by_id('ICTAB_3')
SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.ID, 'ICTAB_3')))
SEARCH_BOX.click()
# time.sleep(4)
# Run a for loop for the rows returned
for index in range(1, 1500):
    # Check to see asset is already capitalized
    if driver.find_element_by_id('ASSET_ACQ_DET_CAPITALIZATION_SW$0').is_enabled():
        # This is the capitalize push button
        #SEARCH_BOX = driver.find_element_by_id('ADD_WRK_CAPITALIZE_PB')
        SEARCH_BOX = wait.until(EC.element_to_be_clickable(
            (By.ID, 'ADD_WRK_CAPITALIZE_PB')))
        SEARCH_BOX.click()
        # time.sleep(4)
        # SEARCH_BOX = driver.find_element_by_id('#ICSave')
        SEARCH_BOX = wait.until(EC.element_to_be_clickable((By.ID, '#ICSave')))
        SEARCH_BOX.click()
        SEARCH_BOX.send_keys('Alt+1')  # Save
        # time.sleep(4)
        # SEARCH_BOX = driver.find_element_by_id('#ICNextInList')  # Go to next
        # asset
        SEARCH_BOX = wait.until(
            EC.element_to_be_clickable((By.ID, '#ICNextInList')))
        SEARCH_BOX.click()
        # time.sleep(4)
    else:  # Go to next asset as it is already capitalized
        SEARCH_BOX = driver.find_element_by_id('#ICNextInList')
        SEARCH_BOX = wait.until(
            EC.element_to_be_clickable((By.ID, '#ICNextInList')))
        SEARCH_BOX.click()
        # time.sleep(4)
# driver.quit()
