from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

profile = webdriver.FirefoxProfile()
# profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.socks', '127.0.0.1')
# profile.set_preference('network.proxy.socks_port', 9050)
browser = webdriver.Firefox(profile)
browser.get("http://yahoo.com")
# browser.save_screenshot("/Users/admin/Pictures/screenshot.png")
browser.close()