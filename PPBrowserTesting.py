# Web browser testing
import webbrowser as wb

# wb.open('http://finance.partneragencies.org')
# wb.open_new_tab('http://google.com')
URL = 'http://finance.partneragencies.org'
PATH = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
wb.register('chrome', None, wb.BackgroundBrowser(PATH))
chrome = wb.get('chrome')
# chrome.open_new_tab('chrome://newtab')
chrome.open_new_tab('URL')
