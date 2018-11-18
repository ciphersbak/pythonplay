# Web browser testing
import webbrowser as wb

# This will open in default browser
#webbrowser.open('http://oilprice.com')
#webbrowser.open_new_tab('http://google.com')
URL_1 = 'http://investing.com'
URL_2 = 'http://oilprice.com'
# Windows
# be mindful of the forward slash
CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
#webbrowser.Chrome.open(self,url=url,new=0,autoraise=True)
# I want to open multiple tabs in Chrome
wb.get(CHROME_PATH).open_new(URL_1)
wb.get(CHROME_PATH).open_new_tab(URL_2)
#wb.get(CHROME_PATH).open_new_tab('chrome://newtab')