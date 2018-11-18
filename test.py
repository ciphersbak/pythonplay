from itertools import cycle

li = [0, 1, 2, 3]

running = True
licycle = cycle(li)
# Prime the pump
nextelem = next(licycle)
while running:
    thiselem, nextelem = nextelem, next(licycle)
    print str(nextelem)