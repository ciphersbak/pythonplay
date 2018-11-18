import time
from selenium import webdriver

import requests

proxies = {
    "http": "http://www-proxy-idc.in.oracle.com:80",
    "https": "http://www-proxy-idc.in.oracle.com:80",
}

# requests.get("http://www.google.com/xhtml", proxies=proxies)
# Optional argument, if not specified will search path.
driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
# driver.get('http://www.google.com/xhtml');
driver.get(
    'http://slc10ppj.us.oracle.com:8000/psp/e92ppi14x/EMPLOYEE/ERP/c/MANAGE_ASSETS.BASIC.GBL?')  # PIA URL
time.sleep(4)  # Let the user actually see something!
# Login
search_box = driver.find_element_by_id('userid')
search_box.send_keys('VP1')
search_box = driver.find_element_by_id('pwd')
search_box.send_keys('VP1')
search_box = driver.find_element_by_name('Submit')
search_box.click()
# Change iFrame
frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
driver.switch_to.frame(frame)
# On Search Page
search_box = driver.find_element_by_name('ASSET_SRCH_PARENT_ID')
search_box.send_keys('000000000034')  # This is the parent asset
search_box = driver.find_element_by_id('#ICSearch')
search_box.click()
search_box.send_keys('Alt+1')  # Search
time.sleep(4)  # Let the user actually see something!
# This one works, it selects the first row
search_box = driver.find_element_by_id('SEARCH_RESULT1')
search_box.click()
search_box.submit()
# search_box.send_keys('ChromeDriver')
# search_box.submit()
time.sleep(4)  # Let the user actually see something!
# Choose the 3rd tab Asset Acquisition Details Tab
search_box = driver.find_element_by_id('ICTAB_3')
search_box.click()
time.sleep(4)
# Run a for loop for the rows returned
for index in range(1, 1209):
    # Check to see asset is already capitalized
    if driver.find_element_by_id('ASSET_ACQ_DET_CAPITALIZATION_SW$0').is_enabled():
        # This is the capitalize push button
        search_box = driver.find_element_by_id('ADD_WRK_CAPITALIZE_PB')
        search_box.click()
        time.sleep(4)
        search_box = driver.find_element_by_id('#ICSave')
        search_box.click()
        search_box.send_keys('Alt+1')  # Save
        time.sleep(4)
        search_box = driver.find_element_by_id(
            '#ICNextInList')  # Go to next asset
        search_box.click()
        time.sleep(4)
    else:  # Go to next asset as it is already capitalized
        search_box = driver.find_element_by_id('#ICNextInList')
        search_box.click()
        time.sleep(4)
# driver.quit()
