import time
import datetime
import os
import json
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains

str_net_start_time = datetime.datetime.utcnow()
date_stamp = str(datetime.datetime.now()).split('.')[0]
date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
downloadPath = "C:\\temp\seldl\\dashboard\\"
prefs = {
    "download.default_directory": downloadPath,
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
}

ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options = ChromeOptions)
# driver = webdriver.Chrome()
driver.get('https://unicc-trax.avantgardportal.com/trax/')
driver.maximize_window()
# driver.implicitly_wait(10) # seconds
wait = WebDriverWait(driver, 10)
# fetch creds
with open('creds.json') as data_file:
    data = json.load(data_file)

user = data['username']
pwd =  data['password']
# print(user)
# print(pwd)
# create action chain object
actions = ActionChains(driver)
parent_directory = 'C:\\temp\seldl\\invalid\\'
new_directory = date_stamp
# Path 
path = os.path.join(parent_directory, new_directory)
os.mkdir(path)

def logout():
    # Log out
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user-exit"))).click()

def changedo():
    # Change Data Owner from default to UNDP
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-do"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "gwt-uid-17"))).click()

def savescreenshot(activity_name):
    # Save screenshots to the newly created folder    
    driver.save_screenshot(path + '\\' + activity_name)
    time.sleep(3)

def main():
    """The main function from where the processing starts."""
        
    # manage SSO ADFS
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "signInName"))).send_keys(user)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
    try:
        #ADFS
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "passwordInput"))).send_keys(pwd)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "submitButton"))).click()
    except TimeoutException:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(pwd)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

    time.sleep(10)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    time.sleep(3)
    # default landing page is the Dashboard
    # navigate to Payment factory
    try:      
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-PaymentFactory"))).click()
        # Payment reception > Exception handling > Invalid
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PREC-ExceptionHandling-PAY_PMT_REC_INVALID"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        recinvalidfilename = 'x_' + str(x) + '_REC_INVALID_' + date_stamp + '.png'
        savescreenshot(recinvalidfilename)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-PREC-ExceptionHandling-PAY_PMT_REC_INVALID"))).click()
        time.sleep(3)
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/em/button/i[contains(@class, 'fa fa-file-excel-o')]"))).click()
        time.sleep(2)
        # Payment transformation > Exception handling > Invalid
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PTRA-ExceptionHandling-PAY_PMT_TRA_INVALID"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        trainvalidfilename = 'x_' + str(x) + '_TRA_INVALID_' + date_stamp + '.png'
        savescreenshot(trainvalidfilename)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-PTRA-ExceptionHandling-PAY_PMT_TRA_INVALID"))).click()
        time.sleep(3)
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/em/button/i[contains(@class, 'fa fa-file-excel-o')]"))).click()
        time.sleep(2)
        # Change Data Owner to UNDP before navigating to Transmission
        changedo()
        time.sleep(2)
        # Navigate to Dashboard > PAY issues
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-Dashboard"))).click()
        time.sleep(7)
        # Switch iframe to get to tabs of the Dashboard
        frame = wait.until(EC.element_to_be_clickable((By.ID, "url-frame")))
        driver.switch_to.frame(frame)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "rdCaption_tabPaymentFactoryIncomingFileMonitoring"))).click()
        time.sleep(7)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "rdCaption_tabPaymentFactoryIssues"))).click()
        time.sleep(7)
        # Switch iframe to get to filter criteria and download
        frame = wait.until(EC.element_to_be_clickable((By.ID, "srPaymentIssueDashboard")))
        driver.switch_to.frame(frame)
        frame = wait.until(EC.element_to_be_clickable((By.ID, "srLoadIssueAnalytics")))
        driver.switch_to.frame(frame)
        
        # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/span/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr/td[2][contains(@class, 'rdAgTabHeading')]"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "lblHeadingFilter"))).click()
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "imgChartEdit"))).click()
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "rdAfFilterColumnID_rdAgAnalysisFilter"))).click()
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "rdAfFilterColumnID_rdAgAnalysisFilter"))).send_keys('Issue severity')
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "rdAfFilterValue_rdAgAnalysisFilter"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "rdAfFilterValue_rdAgAnalysisFilter"))).send_keys('Error')
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "lblFilterAdd_rdAgAnalysisFilter"))).click()
        time.sleep(7)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "imgTableExport"))).click()
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "lblExportExcel_rdPopupOptionItem"))).click()
        time.sleep(30)
        driver.switch_to.default_content()

        # Log out
        time.sleep(2)
        logout()

    # except Exception as e:
    #     print(e)

    finally:
        time.sleep(2)
        pass

if __name__ == "__main__":
    main()
