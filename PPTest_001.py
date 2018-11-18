# PP Testing 
import urllib

u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
f = open('rt22.xml', 'wb')
f.write(data)
f.close()

from xml.etree.ElementTree import parse
doc = parse('rt22.xml')
for bus in doc.findall('bus'):
    d = bus.findtext('d')
    lat = float(bus.findtext('lat'))
    busid = bus.findtext('id')
print busid, lat