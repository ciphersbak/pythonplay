import time
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\Users\ppprakas.ORADEV\Downloads\chromedriver_win32\chromedriver.exe')
# driver.get('http://slc11sjd.us.oracle.com:8000/e92ppvinx/signon.html')  # Sign on Page URL
# driver.get('http://slc08bsb.us.oracle.com:8000/psp/e92poadjx/EMPLOYEE/ERP/c/CREATE_PROJECTS.PROJECT_GENERAL.GBL?') # xpath works with this URL
# driver.get('http://SLC08ALR.us.oracle.com:8000/psp/e92ppaetx/EMPLOYEE/ERP/c/CREATE_PROJECTS.PROJECT_GENERAL.GBL?')
driver.get('http://plef4005.us.oracle.com:8028/psp/ps/EMPLOYEE/ERP/c/CREATE_PROJECTS.PROJECT_GENERAL.GBL?')
# driver.get('http://192.168.56.101:8000/psp/ps/EMPLOYEE/ERP/c/REQUISITION_ITEMS.REQUISITIONS.GBL?')
driver.maximize_window()

try:
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys("VP1")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "pwd"))).send_keys("VP1")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, 'Submit'))).click()    
    frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
    driver.switch_to.frame(frame) # Switch iFrame
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "ICTAB_1"))).click()
    # Enter BU and Project ID on the Add Search Page    
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_GEN_ADD_BUSINESS_UNIT"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "US004")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_GEN_ADD_PROJECT_ID"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "PP9999980")
    # search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_GEN_ADD_PROJECT_ID"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, raw_input())
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, '#ICSearch'))).click() # Click Save
    # On General Information Tab
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_DESCR"))).send_keys("AUTOMATIC")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_WRK_PROJECT_STATUS"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "A")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_INTEGRATION_TMPL"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "US004")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_PC_PRJ_DEF_CALC_MT"))).send_keys("D")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_START_DT"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "01/01/2015")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_END_DT"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "31/12/2018")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_DESCR_DESCR254$0"))).send_keys("AUTOMATIC PP")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJECT_DESCR_DESCRLONG$0"))).send_keys("AUTOMATIC PP")
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click() # Click Save on Main Page
    # Click on Project Activties Link
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_ICLIENT_WRK_PROJECT_ACT_LINK"))).click()
    # On Activity Page
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PGM_HGRID_WRK_HTMLAREA$0"))).send_keys("ACTIVITY 1")    
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJ_ACTIVITY_ACTIVITY_ID$0"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "ACT1")
    time.sleep(3)
    if driver.find_element_by_id('PC_ACT_DEF_CALC_MT$0').is_enabled():
        search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_ACT_DEF_CALC_MT$0"))).send_keys("D")
    else:
        pass
    time.sleep(3)
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PROJ_ACTIVITY_END_DT$0"))).send_keys(Keys.SHIFT, Keys.HOME, Keys.BACKSPACE, Keys.SHIFT, "31/12/2018")    
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click() # Click Save on Activity Page
    time.sleep(3)
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "PC_HOME_STATE_LINK"))).click()
    time.sleep(2)

    # Prepare for Saving
    search_box = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "#ICSave"))).click() # Click Save on Main Page
    
finally:
    time.sleep(4)
    # driver.quit()
    pass