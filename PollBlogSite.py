import requests
from bs4 import BeautifulSoup
import time
import pprint

while True:
    url = "https://tpswrites.wordpress.com/"
    # set the headers like we are a browser,
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(url, headers=headers)
    print 'response : ' + str(response.status_code)
    # print 'content : ' + str(response.content)
    # parse the downloaded homepage and grab all text, then,
    # soup = BeautifulSoup(response.text, "lxml")
    soup = BeautifulSoup(response.content, 'html.parser')
    # soup
    soup.prettify()
    list(soup.children)
    # soup.find_all('article')[0].get_text()
    for index, item in enumerate(soup.find_all('article')):
    	print "--Post-- %s is %s" % (index, item)
    	links = [a.attrs.get('href') for a in soup.select('div.video-summary-data a[href^=/tpswrites.wordpress.com/]')]
    	# pprint.pprint(soup.find_all('article')[1].get_text())
    	# item += 1
	
    # if the number of times the word "Judiciary" occurs on the page is less than 1,
    if str(soup).find("Judiciary") == 1:
        # wait 1 second,
        time.sleep(1)
        print 'Found something'
        # continue with the script,
        continue
    # but if the word "Judiciary" occurs any other number of times,
    else:
        # print('In else: ' + str(soup))
        break