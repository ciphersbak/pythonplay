import time
from datetime import date, datetime, timedelta
import os
import json
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import TimeoutException
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
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
# creating the date object of today's date 
todays_date = date.today()
Current_year = todays_date.year
Current_month = todays_date.month 

def get_first_date_of_current_month(year, month):
    """Return the first date of the month.

    Args:
        year (int): Year
        month (int): Month

    Returns:
        date (datetime): First date of the current month
    """
    first_date = datetime(year, month, 1)
    # return first_date.strftime("%Y-%m-%d")
    return first_date.strftime("%d/%m/%Y")

def get_last_date_of_month(year, month):
    """Return the last date of the month.
    
    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """
    
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
    
    # return last_date.strftime("%Y-%m-%d")
    return last_date.strftime("%d/%m/%Y")

def get_quarter_dates(year, month):
    """Return the first and last dates for a quarter.
    
    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        dates (datetime): First and Last date of the current quarter
    """
    curr_q = round((month - 1) / 3 + 1)
    quarter_first_date = datetime(year, 3 * curr_q - 2, 1)
    if curr_q == 4:
        quarter_last_date = datetime(year, 12, 31)
    else:
        quarter_last_date = datetime(year, 3 * curr_q + 1, 1) + timedelta(days=1)
    
    return quarter_first_date.strftime("%d/%m/%Y"), quarter_last_date.strftime("%d/%m/%Y")

def logout():
    # Log out
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user"))).click()
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "menu-user-exit"))).click()


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
        #Azure AD
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(pwd)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

    time.sleep(10)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    # Still need to figure out how to handle MFA
    time.sleep(3)
    # default landing page is the Dashboard
    # navigate to Reports > Manual reporting > Manually created
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-ReportsSearchArchive"))).click()
        time.sleep(2)
        # search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-Manual"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-Manual-REP_Reporting-ManualReportReadyToExecute"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-Manual-REP_Reporting-ManualReportReadyToExecute"))).click()
        # Click New From Template to trigger a manual report
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[8]/table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'New from template')]"))).click()
        # Select the report and enter input parameters
        # Report UN MT940 Account Statement XLSX
        actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[4]/td[1]/div[contains(@class, 'cellTemplate') and starts-with(., 'UNDP_MT940_Account_Statement')]")))).perform()
        time.sleep(2)
        
        # Parameters
        # CB From Date
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "1.UNMT940AccountStatement.ClosingBalanceDateFrom"))).click()
        # Clear and send CB From Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')][@type='text']"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[3]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')][@type='text']"))).send_keys(get_quarter_dates(Current_year, Current_month)[0])
        time.sleep(2)
        # CB To Date
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "1.UNMT940AccountStatement.ClosingBalanceDateTo"))).click()
        # Clear and send CB To Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')][@type='text']"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[4]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_quarter_dates(Current_year, Current_month)[1])
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'OK')]"))).click()
        time.sleep(2)
        # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[3]/div/div/table/tbody/tr[2][contains(@class, ' fetchGrid-selected')]"))).click()
        
        # Click New From Template to trigger a manual report
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'New from template')]"))).click()
        # Report UN Inbound Message XLSX
        actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[3]/td[1]/div[contains(@class, 'cellTemplate') and starts-with(., 'UNDP_Inbound_Message')]")))).perform()
        time.sleep(2)
        
        # Parameters
        # Clear and send Start Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[1]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[1]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_first_date_of_current_month(Current_year, 1))
        time.sleep(2)
        # End Date
        # Clear and send End Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_last_date_of_month(Current_year, 12))
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'OK')]"))).click()
        time.sleep(2)

        # Click New From Template to trigger a manual report
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'New from template')]"))).click()
        # Report UNDP_Statements_FreeMessageDetails XLSX
        actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[8]/td[1]/div[contains(@class, 'cellTemplate') and starts-with(., 'UNDP_Statements_FreeMessageDetails')]")))).perform()
        time.sleep(2)
        
        # Parameters UNDP_Statements_FreeMessageDetails XLSX
        # Clear and send Start Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[1]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[1]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_first_date_of_current_month(Current_year, Current_month))
        time.sleep(2)
        # Clear and send End Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_last_date_of_month(Current_year, Current_month))
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'OK')]"))).click()
        time.sleep(2)

        # Click New From Template to trigger a manual report
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'New from template')]"))).click()
        # Report UNDP_Statements_FreeMessageDetails XLSX
        actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[6]/td[1]/div[contains(@class, 'cellTemplate') and starts-with(., 'UNDP_Payment_Tracker')]")))).perform()
        time.sleep(2)

        # Parameters UNDP_Payment_Tracker XLSX
        # Clear and send Start Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[1]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[1]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_first_date_of_current_month(Current_year, Current_month))
        time.sleep(2)
        # Clear and send End Date
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).clear()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/div[1]/div/input[contains(@class, ' x-form-field x-form-text ')]"))).send_keys(get_last_date_of_month(Current_year, Current_month))
        time.sleep(2)
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'OK')]"))).click()
        time.sleep(2)
        
        # Get ready to run the reports
        # Set focus on the grid
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[2]/td[1]/div[contains(@class, 'cellCreationdate')]"))).click()
        # Select all and Execute report
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Select all')]"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/em/button[contains(@class, 'x-btn-text') and starts-with(., 'Execute report')]"))).click()
        # actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//tr/td//div[contains(@class, 'cellName') and starts-with(., 'PA_Statements_DAILY')]")))).perform()
        # actions.context_click(on_element=search_box).perform()
        
        # Log out
        time.sleep(2)
        logout()

    finally:
        time.sleep(2)
        pass

if __name__ == "__main__":
    main()
