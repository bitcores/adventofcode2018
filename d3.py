
claims = {}
claimareas = {}
uniquesquares = set()
overlapsquares = set()

with open("input3.txt") as fp:
    for line in fp:
        line = line.strip()
        parts = line.split(" @ ")
        claims[parts[0][1:]] = parts[1]

#print(claims)
uniqueclaim = 0
for x in claims:
    e = claims[x].split(": ")
    p = e[0].split(",")
    s = e[1].split("x")

    arealist = []
    for y in range(int(p[1]), int(p[1])+int(s[1])):
        for z in range(int(p[0]), int(p[0])+int(s[0])):
            #print((y*1000)+x)
            pos = (y*1000)+z
            arealist.append(pos)
            if pos in uniquesquares:
                overlapsquares.add(pos)
            uniquesquares.add(pos)

    claimareas[x] = arealist

for x in claimareas:
    overlaps = 0

    for y in claimareas[x]:
        if y in overlapsquares:
            overlaps += 1
    
    if overlaps == 0:
        uniqueclaim = x

#print(claimareas)
print("Number of overlapping squares:> ", len(overlapsquares))
print("ID of non-overlapping claim:> ", uniqueclaim)
        