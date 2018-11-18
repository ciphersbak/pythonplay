from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
# driver.get('http://slc11sjd.us.oracle.com:8000/e92ppvinx/signon.html')  # Sign on Page URL
driver.get('http://slc09kbb.us.oracle.com:8000/psp/e92ppvinx/EMPLOYEE/ERP/c/REQUISITION_ITEMS.REQUISITIONS.GBL?') # xpath works with this URL
# driver.get('http://192.168.56.101:8000/psp/ps/EMPLOYEE/ERP/c/REQUISITION_ITEMS.REQUISITIONS.GBL?')
driver.maximize_window()

try:
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys("VP1")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "pwd"))).send_keys("VP1")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, 'Submit'))).click()    
    frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
    driver.switch_to.frame(frame) # Switch iFrame
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, '#ICSearch'))).click() # Click Add
    # Level 0 HDR
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "REQ_HDR_REQ_NAME"))).send_keys("AUTOMATIC")
    # Level 1 Line 1
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "DESCR254_MIXED$0"))).send_keys("TEST DESCR")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 
    "REQ_LINE_QTY_REQ$0"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "10")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "REQ_LINE_UNIT_OF_MEASURE$0"))).send_keys("EA")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "ITM_CAT_WRK_CATEGORY_CD$0"))).send_keys("HARDWARE")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 
    "REQ_LINE_WRK_PRICE_REQ_C$0"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "1000")
    # Click on Schedule Icon
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, "REQ_LINE_WRK_SCHEDULE_PB$0"))).send_keys(Keys.ENTER)
    # Click on Distribution Icon
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "REQ_SCHED_WRK_DISTRIBUTE_PB$0"))).send_keys(Keys.ENTER)
    frame = driver.find_element_by_xpath('//*[@id="ptModFrame_1"]')
    driver.switch_to.frame(frame) # Switch iFrame
    # Change GL BU to US001    
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "BUSINESS_UNIT_GL$0"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "US001")
    # Default PC BU, Project and Activity
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "BUSINESS_UNIT_PC$0"))).send_keys("US001")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_ID$0"))).send_keys("000000000000168")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "ACTIVITY_ID$00"))).send_keys("100")
    # Prepare for Saving
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click() # Click OK on Distrib Page
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "REQ_PNLS_WRK_RETURN_PB"))).click() # Return to Main Page from Schedule
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click() # Click Save on Main Page
    
finally:
    # driver.quit()
    pass