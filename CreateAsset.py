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
# driver.get('http://slc11siy.us.oracle.com:8000/psp/e92ppfpcx/EMPLOYEE/ERP/c/MANAGE_ASSETS.ASSET_ENTRY.GBL')
driver.get('http://slc10ubp.us.oracle.com:8000/psp/ps/EMPLOYEE/ERP/c/MANAGE_ASSETS.ASSET_ENTRY.GBL')
driver.maximize_window()
# driver.implicitly_wait(10) # seconds
wait = WebDriverWait(driver, 10)

try:
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys("VP1")
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "pwd"))).send_keys("VP1")
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "Submit"))).click()
    frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
    driver.switch_to.frame(frame) # Switch iFrame    
    time.sleep(3)
    # Accept default values and click Add
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "#ICSearch"))).click()
    # Profile ID
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "ASSET_PROFILE_ID"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "MACHINERY")
    time.sleep(2)
    # Trans Date
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "ADD_WRK_TRANS_DT"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "01/01/2018")
    # Accounting Date
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "ADD_WRK_ACCOUNTING_DT"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "01/01/2018")
    # Specify Location
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "ASSET_LOCATION_LOCATION"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "US001")
    # Specify Asset Cost
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "COST_TXN_COST$0"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "12000")
    # Click Default Profile
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "ADD_WRK_DEFAULT_PB"))).click()
    time.sleep(3)
    # Click save    
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click()
finally:
    time.sleep(4)
    # driver.quit()
    pass