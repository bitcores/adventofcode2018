
codict = {}
codict[2] = []
codict[3] = []

allids = []

with open("input2.txt") as fp:
    for line in fp:
        line = line.strip()

        allids.append(line)

        two = False
        three = False
        
        for x in line:
            c = line.count(x)
            if c == 2:
                two = True
            elif c == 3:
                three = True
        
        if two:
            codict[2].append(line)
        if three:
            codict[3].append(line)

#print(codict)
chksum = len(codict[2]) * len(codict[3])
print("Checksum:> ", chksum)

match = False
mid = None
p = 0
for z in allids:
    for y in allids:
        r = False
        if z == y:
            continue
        
        for e in range(0, len(z)):
            if z[e] != y[e]:
                if r:
                    r = False
                    break
                r = not r
        if r:
            match = True
            mid = (z, y)
    if match:
        break
print("Box IDs:> ", mid)