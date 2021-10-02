import time
from copy import deepcopy
st = time.time()

inputfile = "input15.txt"

def readinput():
    L = []
    with open(inputfile) as fp:
        for line in fp:
            line = line.rstrip()

            L.append(line)
            
    return L

def splitinput():
    L = [i.split("\n") for i in open(inputfile).read().split("\n\n")]

    return L

## Parse input
inp = readinput()
#inp = splitinput()

def turnorder():
    order = []
    for u in units:
        if units[u].hp <= 0:
            continue
        p = None
        for cid in order:
            if units[u].pos[0] < units[cid].pos[0] or \
                (units[u].pos[0] == units[cid].pos[0] and units[u].pos[1] < units[cid].pos[1]):
                p = order.index(cid)
                break
        if not p == None:
            order.insert(p, u)
        else:
            order.append(u)
    return deepcopy(order)

def printfield():
    for y in field:
        line = ""
        last = 0
        for x in field[y]:
            for _ in range(last, x):
                line += " "

            isunit = None
            for u in units:
                if units[u].pos == (y,x):
                    isunit = units[u].race
                    break

            if not isunit == None:
                line += isunit
            else:
                line += field[y][x]
            last = x+1
        print(line)

def IsOccupy(y, x, uid):
    for u in units:
        # unit does not block itself
        if u == uid:
            continue
        if units[u].pos == (y, x):
            return True
    return False

def IsEnemy(y, x, race):
    for u in units:
        if units[u].pos == (y, x) and not units[u].race == race:
            return u
    return None

def GetTarget(pos):
    for u in units:
        if units[u].pos == pos:
            return u
    return None

## Solve problem
class unit:
    def __init__(self, race, pos, atk=3):
        self.race = race
        self.pos = pos
        self.hp = 200
        self.atk = atk

#printfield()

elveswin = False
first = True
eatk = 3
while not elveswin:
    elfcount = 0
    field = {}
    units = {}
    y = 0
    uid = 0
    for l in inp:
        field[y] = {}
        for k in range(len(l)):
            if l[k] == "G" or l[k] == "E":
                field[y][k] = "."
                if l[k] == "G":
                    units[uid] = unit(l[k], (y,k))
                else:
                    units[uid] = unit(l[k], (y,k), eatk)
                    elfcount += 1
                uid += 1
            else:
                field[y][k] = l[k]
        y += 1
    turn = 0
    order = turnorder()
    combatend = False

    while not combatend:

        for uid in order:
            # if the unit is dead, skip
            if not uid in units:
                continue

            targets = []
            points = []
            pos = units[uid].pos
            loc = [[0,1], [1,0], [0,-1], [-1,0]]

            # find targets
            for u in units:
                if u == uid or units[u].race == units[uid].race:
                    continue
                targets.append(u)
            
            if len(targets) == 0:
                # no targets, end combat
                combatend = True
                break
                
            for t in targets:
                if t == uid or units[t].race == units[uid].race:
                    continue 
                y, x = units[t].pos[0], units[t].pos[1]    
                for e in loc:
                    ey, ex = y+e[0], x+e[1]
                    #print(ey,ex)
                    if field[ey][ex] == "." and not IsOccupy(ey, ex, uid):
                        points.append((ey, ex))
            
            # if unit is already in a target point, auto select
            if pos in points:
                selected = pos
                moveto = pos
            else:
                selected = None
                moveto = None

            # find the nearest reachable point
            grower = [pos]
            planted = set()
            while selected == None:
                newgrowth = set()
                potential = set()

                for g in grower:
                    planted.add(g)
                    y, x = g[0], g[1]
                    for o in loc:
                        oy, ox = y+o[0], x+o[1]
                        if (oy, ox) in points:
                            potential.add((oy, ox))
                        elif field[oy][ox] == "." and not IsOccupy(oy, ox, uid) and not (oy, ox) in planted:
                            newgrowth.add((oy, ox))
                
                if len(potential) > 0:
                    # select the target from the potential list
                    selected = (99999,99999)
                    for p in potential:
                        if p[0] < selected[0] or \
                            (p[0] == selected[0] and p[1] < selected[1]):
                            selected = p

                else:
                    if len(newgrowth) == 0:
                        # there is no path to a target
                        break
                    grower.clear()
                    grower = deepcopy(newgrowth)

            if selected == None:
                # don't move
                moveto = pos

            # move target has been found
            grower = [selected]
            planted = set()
            while moveto == None:
                newgrowth = set()
                potential = set()

                for g in grower:
                    planted.add(g)
                    y, x = g[0], g[1]
                    for o in loc:
                        oy, ox = y+o[0], x+o[1]
                        if (oy, ox) == pos:
                            potential.add((y, x))
                        elif field[oy][ox] == "." and not IsOccupy(oy, ox, uid) and not (oy, ox) in planted:
                            newgrowth.add((oy, ox))
                
                if len(potential) > 0:
                    # select the target from the potential list
                    moveto = (99999,99999)
                    for p in potential:
                        if p[0] < moveto[0] or \
                            (p[0] == moveto[0] and p[1] < moveto[1]):
                            moveto = p

                else:
                    grower.clear()
                    grower = deepcopy(newgrowth)
            
            # move unit
            units[uid].pos = moveto
            pos = units[uid].pos
            # check for opponents in range
            inrange = None
            irhp = 999
            for i in loc:
                iy, ix = pos[0]+i[0], pos[1]+i[1]
                ir = IsEnemy(iy, ix, units[uid].race)
                if not ir == None:
                    if inrange == None or units[ir].hp < irhp:
                        inrange = (iy, ix)
                        irhp = units[ir].hp
                    elif units[ir].hp == irhp and (iy < inrange[0] or \
                            (iy == inrange[0] and ix < inrange[1])):
                        inrange = (iy, ix)
            
            if not inrange == None:
                enemy = GetTarget(inrange)
                if enemy == None:
                    print("wtf")
                    input()
                units[enemy].hp -= units[uid].atk
                if units[enemy].hp <= 0:
                    units.pop(enemy)

            #printfield()
            #input()

        if combatend == True:
            break

        order = turnorder()
        turn += 1
        
    if first:
        first = False
        score = 0
        for u in units:
            score += units[u].hp

        #printfield()
        #print(turn)
        #print(score)
        print("Part 1:> ", score*turn)
    else:
        uids = list(units.keys())

        if units[uids[0]].race == "E" and len(units) == elfcount:
            elveswin = True
            break
    eatk += 1

score = 0
for u in units:
    score += units[u].hp

#printfield()
#print(turn)
#print(score)
print("Part 2:> ", score*turn)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)