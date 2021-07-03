import time
from datetime import datetime
import operator

events = []
tsevents = {}
sortedts = []
timesleep = {}
guardsmins = {}

with open("input4.txt") as fp:
    for line in fp:
        line = line.strip()
        events.append(line)

#print(events)

for e in events:
    de = e.split("] ")
    # because the dates are before 1970 we have to fub the year
    ts = int(time.mktime(datetime.strptime("1970-"+de[0][6:], "%Y-%m-%d %H:%M").timetuple()))
    
    tsevents[ts] = de[0][-2:] + " " + de[1]

sortedts = (sorted(tsevents))
ag = 0
fa = 0
for x in sortedts:
    parts = tsevents[x].split(" ")
    if "begins" in tsevents[x]:     
        ag = int(parts[2][1:])
        fa = 0
        if not ag in guardsmins:
            guardsmins[ag] = {}
    if "falls" in tsevents[x]:
        fa = int(parts[0])
    if "wakes" in tsevents[x]:
        for m in range(fa, int(parts[0])):
            if not m in guardsmins[ag]:
                guardsmins[ag][m] = 1
            else:
                guardsmins[ag][m] += 1
    #print(tsevents[x])

mmslp = 0
mg = 0
for g in guardsmins:
    s = sum(guardsmins[g].values())
    if s > mmslp:
        mmslp = s
        mg = g

mm = 0
mmt = 0
for m in guardsmins[mg]:
    if guardsmins[mg][m] > mmt:
        mmt = guardsmins[mg][m]
        mm = m

print("Part 1 result:> ", (mg * mm))

gid = 0
mmins = [0,0]
for guards in guardsmins:
    if len(guardsmins[guards]) > 0:
        m = max(guardsmins[guards].items(), key=operator.itemgetter(1))[0]
        if guardsmins[guards][m] > mmins[1]:
            mmins = [m, guardsmins[guards][m]]
            gid = guards

print("Part 2 result:> ", (gid * mmins[0]))

#print(guardsmins)
#print(sortedevents)