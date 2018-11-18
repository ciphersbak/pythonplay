import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

# create a new Chrome session
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)  

# navigate to the application home page
driver.get("https://tpswrites.wordpress.com/")

# get the search textbox
articles = driver.find_elements_by_xpath('//*[@id="infinite-wrap"]/article')
for index, article in enumerate(articles):
    repeatArticles = driver.find_elements_by_xpath('//*[@id="infinite-wrap"]/article')
    articleHREF = repeatArticles[index].find_element_by_xpath('./header/h1/a')
    
    print str(index + 1) + ": " + articleHREF.get_attribute('href')
    articleHREF.click()
    rootElement = driver.find_element_by_xpath('//*[@id="masthead"]/div[1]/div/div/p/a')
    rootElement.click()

driver.quit()