import urllib
import time
import os

uri = "https://tpswrites.wordpress.com/"  #url where result will be declared
source = urllib.urlopen(uri).read()
nw_source=source 
cntr=0
flg=True
while nw_source==source:
    if flg:
      time.sleep(2)  #refresh every 2 seconds
    try:
      nw_source = urllib.urlopen(uri).read()
    except IOError:
      print "Error in reading url"
      flg=False
      continue 
    cntr+=1
    print cntr," times refreshed"
  
    flg=True
while True:
  pass