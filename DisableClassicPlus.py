# Disable Classic Plus
import time
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
# driver.get('http://slc11sjd.us.oracle.com:8000/e92ppvinx/signon.html')  # Sign on Page URL
driver.get('http://slc08afv.us.oracle.com:8000/psp/e92poadkx/EMPLOYEE/ERP/c/EOCP_SETUP.EOCP_SETUP.GBL?') # xpath works with this URL
# driver.get('http://192.168.56.101:8000/psp/ps/EMPLOYEE/ERP/c/REQUISITION_ITEMS.REQUISITIONS.GBL?')
driver.maximize_window()

try:
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys("VP1")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "pwd"))).send_keys("VP1")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, 'Submit'))).click()    
    frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
    driver.switch_to.frame(frame) # Switch iFrame
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "EOCP_WRK_EOCP_BRAND_ENABLED"))).click()
    time.sleep(3)
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, "PRCSRQSTDLG_WRK_LOADPRCSRQSTDLGPB"))).click()
    time.sleep(3)
    driver.switch_to_default_content()
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click() # Click OK

finally:
    # driver.quit()
    pass