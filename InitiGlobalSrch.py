import time
import os
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()  
# chrome_options.add_argument("--headless")  
# chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
# create a new Chrome session
# driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)

driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
driver.get('http://slc10prz.us.oracle.com:8000/e92ppestx/signon.html')
driver.maximize_window()
# driver.implicitly_wait(10) # seconds
wait = WebDriverWait(driver, 10)

try:
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys("VP1")
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "pwd"))).send_keys("VP1")
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "Submit"))).click()
    # get the search textbox
    time.sleep(3)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "pthdr2Search"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "pthdr2srchedit"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "WM_EMPLID2")
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "pthdrSrchHref"))).click()
    # driver.execute_script("document.body.style.zoom='80%';")        
finally:
    time.sleep(4)
    # driver.quit()
    pass