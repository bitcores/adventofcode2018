import time
from collections import defaultdict
st = time.time()

inputfile = "input9.txt"

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
# it may be worth optimizing this some time, but for now brute force it is

for l in inp:
    scores = defaultdict(int)
    pm = l.split("; ")
    p = pm[0].split(" ")
    m = pm[1].split(" ")
    players = int(p[0])
    lastmarble = int(m[-2])
    #lastmarble = int(m[-2])*100 # part 2

    circle = [0]
    pos = 0
    marble = 1
    cplayer = 1
    while marble <= lastmarble:
        if marble % 23 == 0:
            pos -= 7
            if pos < 0:
                pos += len(circle)
            scores[cplayer] += circle.pop(pos)
            scores[cplayer] += marble
        else:
            pos += 2
            while pos > len(circle):
                pos -= len(circle)
            if pos == len(circle):
                circle.append(marble)
            else:
                circle.insert(pos, marble)

        marble += 1
        cplayer += 1
        if cplayer > players:
            cplayer = 1
        #if marble % 1000 == 0:
        #    print(marble)
        # part two will take over 7,000,000 marbles and two hours
        #print(circle)
        
    #print(scores)
    #input()
    print("Max score is:> ", max(scores.values()))

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)