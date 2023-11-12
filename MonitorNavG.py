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

prefs = {
    "download.default_directory": r"C:\temp\seldl",
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
str_net_start_time = datetime.datetime.utcnow()
date_stamp = str(datetime.datetime.now()).split('.')[0]
date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
parent_directory = 'C:\\temp\seldl\\screenshots\\'
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
        #Azure AD
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(pwd)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        
    time.sleep(10)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    # Still need to figure out how to handle MFA
    time.sleep(3)
        # default landing page is the Dashboard
        # navigate to Payment factory
    try:  
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-PaymentFactory"))).click()
        # Payment release
        # search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PaymentRelease"))).click()
        # time.sleep(3)
        # Sending
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PaymentRelease-PAY_ENV_REL_SENDING"))).click()
        time.sleep(5)
        # Exception handling
        # search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PREL-ExceptionHandling"))).click()
        # time.sleep(2)
        # Payment release > Exception handling > Invalid
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PREL-ExceptionHandling-PAY_ENV_REL_INVALID"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        # print(x)
        relinvalidfilename = 'x_' + str(x) + '_REL_INVALID_' + date_stamp + '.png'
        savescreenshot(relinvalidfilename)
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + relinvalidfilename)
        # time.sleep(3)
        # Payment release > Exception handling > Removed from flow
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PREL-ExceptionHandling-PAY_ENV_REL_REJECTED"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        relrejectfilename = 'x_' + str(x) + '_REL_REMOVED_FROM_FLOW_' + date_stamp + '.png'
        savescreenshot(relrejectfilename)
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + relrejectfilename)
        # time.sleep(3)
        # Payment release > Exception handling > Sending failed
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PREL-ExceptionHandling-PAY_ENV_REL_FAILED"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[2]/div[3]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        relfailedfilename = 'x_' + str(x) + '_REL_SENDING_FAILED_' + date_stamp + '.png'
        savescreenshot(relfailedfilename)
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + relfailedfilename)
        # time.sleep(3)
        # Status feedback
        # search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PAY-StatusFeedback"))).click()
        # Envelopes Rejected
        # search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PAY-Envelope"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PAY-Envelope-PAY_ENV_SF_REJECTED"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        envrejectedfilename = 'x_' + str(x) + '_ENV_REJECTED_' + date_stamp + '.png'
        savescreenshot(envrejectedfilename)
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + envrejectedfilename)
        # time.sleep(3)
        # Payments Rejected
        # search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PAY-Payment"))).click()
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-PAY-Payment-PAY_PMT_SF_REJECTED"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        paymentsrejectedfilename = 'x_' + str(x) + '_PMT_REJECTED_' + date_stamp + '.png'
        savescreenshot(paymentsrejectedfilename)
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + paymentsrejectedfilename)
        # time.sleep(3)
        # Navigate to Messages Tab
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-Message"))).click()
        # Inbound Messages > Sent
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-ME-IN-Workflow-ME_IN_SENT"))).click()
        time.sleep(5)
        # PSR > Partially reconciled
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-SF-ExceptionHandling-SF_PARTIALLY_RECONCILED"))).click()
        time.sleep(5)
        # navigate to Monitoring
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-MonitoringAndAudit"))).click()
        time.sleep(3)        
        # Check Communications > Failed Incoming
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_IN_EXCEPTION"))).click()
        time.sleep(1)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_IN_EXCEPTION"))).click()
        time.sleep(5)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[8]/div/div[3]/div[2]/div[4]/div[2]/div[1]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        failedincomingfilename = 'x_' + str(x) + '_COMMS_FAILED_INCOMING_' + date_stamp + '.png'
        savescreenshot(failedincomingfilename)
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + failedincomingfilename)
        # time.sleep(3)
        # Check Communications > Failed Outgoing
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_OUT_EXCEPTION"))).click()
        time.sleep(1)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-FA_COMMUNICATION_EXCEPTION-FA_COMMUNICATION_OUT_EXCEPTION"))).click()
        time.sleep(5)
        # Change Data Owner to UNDP before navigating to Transmission
        changedo()
        time.sleep(2)
        # Check Transmission > Failed Incoming
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-FA_TRANSMISSION_EXCEPTION-FA_TRANSMISSION_IN_EXCEPTION"))).click()
        time.sleep(5)
        # Check Tranmission > Failed Outgoing
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-FA_TRANSMISSION_EXCEPTION-FA_TRANSMISSION_OUT_EXCEPTION"))).click()
        time.sleep(5)
        # Navigate to Statements
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tab-AccountReporting"))).click()
        time.sleep(3)
        # Partial Statements
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-AS-Workflow-Reception-AS_PARTIAL"))).click()
        time.sleep(7)        
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + statementspartialfilename)
        # time.sleep(3)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-AS-Workflow-Reception-AS_PARTIAL"))).click()
        time.sleep(2)
        # Sort Creation Date
        # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div[contains(@class, 'colCreationdate') and starts-with(., 'Creation date')]"))).click()
        actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div[contains(@class, 'colCreationdate') and starts-with(., 'Creation date')]")))).perform()
        time.sleep(7)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[4]/div/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        statementspartialfilename = 'x_' + str(x) + '_AS_940_PARTIAL_' + date_stamp + '.png'
        savescreenshot(statementspartialfilename)
        # Inconsistent Statements
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "nav-tree-AS-ExceptionHandling-Reception-AS_INCONSISTENT"))).click()
        time.sleep(7)        
        # driver.save_screenshot('C:\\temp\\seldl\\screenshots\\' + statementsinconsistentfilename)
        # time.sleep(3)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "grid-AS-ExceptionHandling-Reception-AS_INCONSISTENT"))).click()
        time.sleep(2)
        # Sort Creation Date
        # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div[contains(@class, 'colCreationdate') and starts-with(., 'Creation date')]"))).click()
        actions.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div[contains(@class, 'colCreationdate') and starts-with(., 'Creation date')]")))).perform()
        time.sleep(7)
        x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div[2]/div[3]/div[1]/table/tbody/tr/td[7][contains(@class, 'my-tree-right')]"))).text
        statementsinconsistentfilename = 'x_' + str(x) + '_AS_940_INCONSISTENT_' + date_stamp + '.png'
        savescreenshot(statementsinconsistentfilename)

        # Log out
        time.sleep(2)
        logout()

    except Exception as e:
        print(e)

    finally:
        time.sleep(2)
        pass

if __name__ == "__main__":
    main()
