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

str_net_start_time = datetime.datetime.utcnow()
date_stamp = str(datetime.datetime.now()).split('.')[0]
date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
# downloadPath = "C:\\temp\seldl\\scheduled\\"
parent_directory = 'C:\\temp\seldl\\scheduled\\'
new_directory = date_stamp
# Path 
path = os.path.join(parent_directory, new_directory)
os.mkdir(path)
prefs = {
    "download.default_directory": path,
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
paramList = []

def logout():
    # Log out
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user-exit"))).click()

def applyfilters():
    # apply generic filters
    # filter on Requestor (Prashant Atman) - Right Click
    # actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[5]/div[contains(@class, 'colRequestor') and starts-with(., 'Requestor')]")))).perform()
    actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[5]/div[contains(@class, 'colRequestor') and starts-with(., 'Requestor')]")))).perform()
    time.sleep(2)
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).send_keys("Prashant Atman")
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).send_keys(Keys.ENTER)
    
    # filter on Creation date (Today) - Right Click
    # actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[1]/div[contains(@class, 'colCreationdate') and starts-with(., 'Creation date')]")))).perform()
    actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[1]/div[contains(@class, 'colCreationdate') and starts-with(., 'Creation date')]")))).perform()
    time.sleep(2)
    # mouse hover and click
    # hover = actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[6]/ul/li[7]")).perform()
    hover = actions.move_to_element(driver.find_element(By.XPATH, "//ul/li[7]")).perform()
    time.sleep(2)
    # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/ul/li[1]/div/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Today')]"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Today')]"))).click()
    time.sleep(2)

def resetfilter():
    # call this before downloading output for new report name
    # blank out filter on report definition
    # actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div[contains(@class, 'colReportdefinition') and starts-with(., 'Report definition')]")))).perform()
    actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/div[contains(@class, 'colReportdefinition') and starts-with(., 'Report definition')]")))).perform()
    time.sleep(2)
    # clear and send ENTER
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).clear()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).send_keys(Keys.ENTER)

def download_report_op(report_name):
    # segragate download logic by report name and report parameters
    # core logic sits here
    print("Downloading report output for report name: " + str(report_name))
    # filter on Report definition and pick the latest row
    # actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div[contains(@class, 'colReportdefinition') and starts-with(., 'Report definition')]")))).perform()
    actions.context_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/div[contains(@class, 'colReportdefinition') and starts-with(., 'Report definition')]")))).perform()
    time.sleep(2)
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).send_keys(report_name)
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-menu-list']/li[5]/descendant::input[@type='text']"))).send_keys(Keys.ENTER)
    # click on filtered grid
    # handle case for no rows
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-REP-Workflow-REP_Reporting-Report"))).click()
    time.sleep(5)
    # navigate to latest row (first row from top and double click)
    # actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'fetchGrid-container')]")))).perform()
    actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table[contains(@class, 'fetchGrid')]/tbody/tr[2]/td[2]")))).perform()
    time.sleep(2)

    xDef1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[2]/td[2]/div[contains(@class, 'cellDefinition')]"))).text
    xVal1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[2]/td[3]/div[contains(@class, 'cellValue')]"))).text
    xnewVal1 = xVal1.replace("-20", "").replace("-", "")
    xDef2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[3]/td[2]/div[contains(@class, 'cellDefinition')]"))).text
    xVal2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[3]/td[3]/div[contains(@class, 'cellValue')]"))).text
    xnewVal2 = xVal2.replace("-20", "").replace("-", "")
    time.sleep(2)
    # print("Definition: " + repr(xDef1) + " Value: " + repr(xVal1))
    # print("Definition: " + repr(xDef2) + " Value: " + repr(xVal2))
        
    if report_name == 'UN_Inbound_Message':
        # read parameters
        # EndDate, StartDate
        xUIM = xnewVal2 + "_" + xnewVal1
        paramList.append(xUIM)

    elif report_name == 'UN_MT940_Account_Statement':
        # read parameters
        # ClosingBalanceDateFrom, ClosingBalanceDateTo
        xUMAS = xnewVal1 + "_" + xnewVal2
        paramList.append(xUMAS)

    elif report_name == 'UN_Statements_FreeMessageDetails':
        # read parameters
        # End date, Start date
        xUSF = xnewVal2 + "_" + xnewVal1
        paramList.append(xUSF)

    elif report_name == 'UNDP_Payment_Tracker':
        # read parameters
        # EndDate, StartDate
        xUPT = xnewVal2 + "_" + xnewVal1
        paramList.append(xUPT)

    else:
        print("Report name not yet defined : " + download_report_op.__name__)

    # navigate to Save as and save the report
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Save as')]"))).click()
    time.sleep(2)
    # Click on cancel on Report dialog box
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Cancel')]"))).click()

def rename_report_op(report_name):
    # Pass the report name
    
    if report_name == 'UN_MT940_Account_Statement':
        try:
            file_handle = polling2.poll(lambda: open(path + '\\' + report_name + '.xlsx'), ignore_exceptions=(IOError,), timeout=3, step=0.1)
            # Polling will return the value of your polling function, so you can now interact with it
            # print(file_handle)
            file_handle.close()
            print("Renaming report output for report " + str(report_name))
            os.rename(path + '\\' + report_name + '.xlsx', path + '\\' + report_name + '_' + paramList[1] +'.xlsx')
            time.sleep(2)
        except TimeoutException as tee:
            print ("Could NOT rename Payment.xls: " + str(tee))

    elif report_name == 'UN_Statements_FreeMessageDetails':
        try:
            file_handle = polling2.poll(lambda: open(path + '\\' + report_name + '.xlsx'), ignore_exceptions=(IOError,), timeout=3, step=0.1)
            # Polling will return the value of your polling function, so you can now interact with it
            # print(file_handle)
            file_handle.close()
            print("Renaming report output for report " + str(report_name))
            os.rename(path + '\\' + report_name + '.xlsx', path + '\\' + report_name + '_' + paramList[2] +'.xlsx')
            time.sleep(2)
        except TimeoutException as tee1:
            print ("Could NOT rename Payment (1).xls: " + str(tee1))

    elif report_name == 'UNDP_Payment_Tracker':
        try:
            file_handle = polling2.poll(lambda: open(path + '\\' + report_name + '.xlsx'), ignore_exceptions=(IOError,), timeout=3, step=0.1)
            # Polling will return the value of your polling function, so you can now interact with it
            # print(file_handle)
            file_handle.close()
            print("Renaming report output for report " + str(report_name))
            os.rename(path + '\\' + report_name + '.xlsx', path + '\\' + report_name + '_' + paramList[3] +'.xlsx')
            time.sleep(2)
        except TimeoutException as tee2:
            print("Could NOT rename something: " + str(tee2))
    
    elif report_name == 'UN_Inbound_Message':
        # do nothing for now
        time.sleep(2)
    

    else:
        print("Report name not yet defined : " + rename_report_op.__name__)

def main():
    """The main function from where the processing starts."""

    # manage SSO ADFS
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "signInName"))).send_keys(user)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
    try:
        #ADFS
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "passwordInput"))).send_keys(pwd)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "submitButton"))).click()
    except Exception as timeout:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(pwd)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

    time.sleep(10)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    time.sleep(3)
    # default landing page is the Dashboard
    # manually created/run reports are currently available under Workflow > Not published 
    # navigate to Reports > Workflow > Not published
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-ReportsSearchArchive"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-REP-Workflow-REP_Reporting-Report"))).click()
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "x-auto-53"))).click()
        time.sleep(2)
        # grid is pre-sorted by Creation date desc
        # apply generic filters
        applyfilters()
        # for report UN_Inbound_Message
        download_report_op("UN_Inbound_Message")
        resetfilter()
        # for report UN_MT940_Account_Statement
        download_report_op("UN_MT940_Account_Statement")
        resetfilter()
        # for report UN_Statements_FreeMessageDetails
        download_report_op("UN_Statements_FreeMessageDetails")
        resetfilter()
        # for report UNDP_Payment_Tracker
        download_report_op("UNDP_Payment_Tracker")
        resetfilter()

        # rename repot outputs based on report parameters
        rename_report_op("UN_Inbound_Message")
        rename_report_op("UN_MT940_Account_Statement")
        rename_report_op("UN_Statements_FreeMessageDetails")
        rename_report_op("UNDP_Payment_Tracker")

        # Log out
        time.sleep(2)
        logout()


    finally:
        time.sleep(2)
        pass

if __name__ == "__main__":
    main()
