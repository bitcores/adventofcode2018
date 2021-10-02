import time
st = time.time()

inputfile = "input14.txt"

def readinput():
    L = []
    with open(inputfile) as fp:
        for line in fp:
            line = line.strip()

            L.append(line)
            
    return L

def splitinput():
    L = [i.split("\n") for i in open(inputfile).read().split("\n\n")]

    return L

## Parse input
inp = readinput()
#inp = splitinput()

## Solve problem

for i in inp:
    goal = int(i)

    elves = [0, 1]
    recipies = [3, 7]

    while len(recipies) <= goal + 10:
        newrec = str(sum([recipies[e] for e in elves]))
        for r in newrec:
            recipies.append(int(r))

        for e in range(len(elves)):
            elves[e] += 1 + recipies[elves[e]]
            while elves[e] >= len(recipies):
                elves[e] -= len(recipies)
        
        #print(recipies)
        #rint(elves)
        #input()
    score = ""
    for x in range(goal, goal+10):
        score += str(recipies[x])
    print("Part 1 score:> ", score)

for i in inp:
    goal = i
    sublen = len(goal)

    elves = [0, 1]
    recipies = [3, 7]
    end = True
    while end:
        newrec = str(sum([recipies[e] for e in elves]))
        for r in newrec:
            recipies.append(int(r))
            last = recipies[-(sublen):]
            sub = ""
            for x in last:
                sub += str(x)

            if sub == goal:
                end = False
                break

        for e in range(len(elves)):
            elves[e] += 1 + recipies[elves[e]]
            while elves[e] >= len(recipies):
                elves[e] -= len(recipies)

    print("No. of recipies before input seq:> ", len(recipies[:-(sublen)]))

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)