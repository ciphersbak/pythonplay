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
import polling2
from polling2 import TimeoutException
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains

date_stamp = str(datetime.datetime.now()).split('.')[0]
date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")

def logout():
    # Log out
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user-exit"))).click()

def reset_to_classic_report():
    # Click Cancel on Report Screen
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/div[2]/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Cancel')]"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Cancel')]"))).click()
    time.sleep(3)

def run_report(report_name):
    
    # Pass the report name
    print("Running report " + str(report_name))
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., 'PA_Statements_DAILY')]"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., '" + str(report_name) + "')]"))).click()    
    # actions.double_click().perform()
    # actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., 'PA_Statements_DAILY')]")))).perform()
    actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., '" + str(report_name) + "')]")))).perform()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//td/em//button[contains(@class, 'x-btn-text') and starts-with(., 'Next')]"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//td/em//button[contains(@class, 'x-btn-text') and starts-with(., 'Next')]"))).click()
    # Wait for the result set to show up
    if report_name == "PA_PaymentsToReview_APBT":
        time.sleep(59)
    elif report_name == "PA_Statements_FreeMessageDetails_CREDIT":
        time.sleep(89)
    else:
        time.sleep(9)
    # search_box = wait.until(EC.element_to_be_clickable((By.ID, "0.customized-System-Report.preview"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.ID, "preview_AccountStatement-AccountStatement-17360354_2"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//td/em//button//i[contains(@class, 'fa fa-file-excel-o')]"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/div[1]/div/div/div/div/div[3]/div[1]/div/div/div[2]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/em/button/i[contains(@class, 'fa fa-file-excel-o')]"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button/i[contains(@class, 'fa fa-file-excel-o')]"))).click()
    # Wait for the XLS to be downloaded
    time.sleep(59)

def rename_report_op(report_name):
    # Pass the report name
    
    if report_name == 'PA_Payments_Tracker_SENT':
        try:
            file_handle = polling2.poll(lambda: open('C:\\temp\\seldl\\classic\Payment.xls'), ignore_exceptions=(IOError,), timeout=3, step=0.1)
            # Polling will return the value of your polling function, so you can now interact with it
            # print(file_handle)
            file_handle.close()
            print("Renaming report output for report " + str(report_name))
            os.rename('C:\\temp\\seldl\\classic\Payment.xls', 'C:\\temp\\seldl\\classic\\'+ report_name + '_' + date_stamp +'.xls')
            time.sleep(2)
        except TimeoutException as tee:
            print ("Could NOT rename Payment.xls: " + str(tee))

    elif report_name == 'PA_Payments_Tracker_TVAL':
        try:
            file_handle = polling2.poll(lambda: open('C:\\temp\\seldl\\classic\Payment (1).xls'), ignore_exceptions=(IOError,), timeout=3, step=0.1)
            # Polling will return the value of your polling function, so you can now interact with it
            # print(file_handle)
            file_handle.close()
            print("Renaming report output for report " + str(report_name))
            os.rename('C:\\temp\\seldl\\classic\Payment (1).xls', 'C:\\temp\\seldl\\classic\\'+ report_name + '_' + date_stamp +'.xls')
            time.sleep(2)
        except TimeoutException as tee1:
            print ("Could NOT rename Payment (1).xls: " + str(tee1))

    else:
        print("Report name not yet defined")

def main():
    """The main function from where the processing starts."""

# chrome_options = Options()  
# chrome_options.add_argument("--headless")  
# chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
# create a new Chrome session
# driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)

# driver = webdriver.Chrome(r'C:\Users\\prashant.atman\\Downloads\\chromedriver-win64\\chromedriver.exe')
downloadPath = "C:\\temp\seldl\\classic\\"
prefs = {
    # "download.default_directory": r"C:\temp\seldl",
    "download.default_directory": downloadPath,
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
    "profile.default_content_setting_values.automatic_downloads": 1
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

try:
    # manage SSO ADFS
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "signInName"))).send_keys(user)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
    #ADFS
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "passwordInput"))).send_keys(pwd)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "submitButton"))).click()
    
except Exception as timeout:
    #Azure AD
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(pwd)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

    time.sleep(10)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    # Still need to figure out how to handle MFA
    time.sleep(3)
    # Still need to figure out how to handle MFA
    # no need to switch to iframe
    # frame = driver.find_element_by_xpath('//*[@id="webgui"]')
    # driver.switch_to.frame(frame)
    # create action chain object
    actions = ActionChains(driver)
    time.sleep(3)
    # default landing page is the Dashboard
    # navigate to Monitoring
try:
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-MonitoringAndAudit"))).click()
    time.sleep(3)
    # Check Communications > Failed Incoming
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_IN_EXCEPTION"))).click()
    time.sleep(3)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_IN_EXCEPTION"))).click()
    time.sleep(5)
    # Check Communications > Failed Outgoing
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_OUT_EXCEPTION"))).click()
    time.sleep(3)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_OUT_EXCEPTION"))).click()
    time.sleep(5)
    # navigate to Reports > Classic Reporting
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-ReportsSearchArchive"))).click()
    time.sleep(3)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-Reporting"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-Reporting-SA_System-Report"))).click()
    
    #### Navigate to and download Classic Report Outputs ####
    #### PA_Statements_DAILY ####
    # Classic Report PA Statements Daily
    run_report('PA_Statements_DAILY')
    reset_to_classic_report()
    #### PA_Comms_OUT_UNDP_ORACLE_MT940 ####
    run_report('PA_Comms_OUT_UNDP_ORACLE_MT940')
    reset_to_classic_report()
    #### PA_PaymentsToReview_APBT ####
    run_report('PA_PaymentsToReview_APBT')
    reset_to_classic_report()
    #### PA_Statements_FreeMessageDetails_CREDIT ####
    run_report('PA_Statements_FreeMessageDetails_CREDIT')
    reset_to_classic_report()
    #### PA_Payments_Tracker_SENT ####
    run_report('PA_Payments_Tracker_SENT')
    reset_to_classic_report()
    #### PA_Payments_Tracker_TVAL ####
    run_report('PA_Payments_Tracker_TVAL')
    reset_to_classic_report()
    
    # 2 Classic Report Outputs need to be renamed to avoid confusion
    rename_report_op('PA_Payments_Tracker_SENT')
    rename_report_op('PA_Payments_Tracker_TVAL')
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., 'PA_Statements_DAILY')]"))).click()    
    # # actions.double_click().perform()
    # actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., 'PA_Statements_DAILY')]")))).perform()
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//td/em//button[contains(@class, 'x-btn-text') and starts-with(., 'Next')]"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//td/em//button[contains(@class, 'x-btn-text') and starts-with(., 'Next')]"))).click()
    # time.sleep(10)
    # # search_box = wait.until(EC.element_to_be_clickable((By.ID, "0.customized-System-Report.preview"))).click()
    # # search_box = wait.until(EC.element_to_be_clickable((By.ID, "preview_AccountStatement-AccountStatement-17360354_2"))).click()
    # # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//td/em//button//i[contains(@class, 'fa fa-file-excel-o')]"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/div[1]/div/div/div/div/div[3]/div[1]/div/div/div[2]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/em/button/i[contains(@class, 'fa fa-file-excel-o')]"))).click()
    # time.sleep(30)
        
    # Log out
    time.sleep(5)
    logout()
    # search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user"))).click()
    # search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user-exit"))).click()
finally:
    time.sleep(4)
    pass

if __name__ == "__main__":
    main()
