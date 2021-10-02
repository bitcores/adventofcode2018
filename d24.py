import time
from copy import deepcopy
from math import ceil
st = time.time()

inputfile = "input24.txt"

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
class iGroup:
    def __init__(self, utype, units, hp, weak, immu, atk, atkt, ini):
        self.utype = utype
        self.units = units
        self.hp = hp
        self.weak = deepcopy(weak)
        self.immu = deepcopy(immu)
        self.atk = atk
        self.atkt = atkt
        self.ini = ini
        self.target = -1
        self.targeted = -1
    
    def GetPower(self):
        return (self.units * self.atk)

    def SetTarget(self, target):
        self.target = target

    def ClearTaret(self):
        self.target = -1
    
    def SetTargeted(self, targeted):
        self.targeted = targeted

    def ClearTareted(self):
        self.targeted = -1


def TargetOrder():
    order = []
    for r in combatants:
        i = None
        for p in range(len(order)):
            if combatants[r].GetPower() > combatants[order[p]].GetPower():
                i = p
                break
            elif combatants[r].GetPower() == combatants[order[p]].GetPower():
                if combatants[r].ini > combatants[order[p]].ini:
                    i = p
                    break
        if not i == None:
            order.insert(i, r)
        else:
            order.append(r)
    
    return deepcopy(order)

def AttackOrder():
    order = []
    for r in combatants:
        i = None
        for p in range(len(order)):
            if combatants[r].ini > combatants[order[p]].ini:
                i = p
                break
        if not i == None:
            order.insert(i, r)
        else:
            order.append(r)
    
    return deepcopy(order)

def MakeTargets(utype):
    tl = []
    for x in combatants:
        if combatants[x].utype == utype:
            tl.append(x)
    return deepcopy(tl)

#input()

end = False
first = True
boost = 0
boostbase = [10000, 1000, 100, 10, 1]
high = []
low = []

while not end:
    combatants = dict()
    gid = 0
    tgle = 0

    for l in inp:
        if l == "Infection:":
            tgle = 1
        else:
            if "units" in l:
                up = l.find("units")
                units = int(l[:up-1])
                hpp = l.find("hit points", up)
                wpp = l.find("with", up)
                hp = int(l[wpp+5:hpp-1])
                dp = l.find("does", hpp)
                edp = l.find(" ", dp+5)
                atk = int(l[dp+5:edp])
                elep = l.find("damage", edp)
                atkt = l[edp+1:elep-1]
                inip = l.find("initiative", elep)
                ini = int(l[inip+11:])
                immu = []
                weak = []
                bo = l.find("(")
                if bo > 0:
                    be = l.find(")", bo)
                    ss = l[bo+1:be]
                    wi = ss.split("; ")
                    for x in wi:
                        tt = x.split(" to ")
                        if tt[0] == "immune":
                            immu = tt[1].split(", ")
                        if tt[0] == "weak":
                            weak = tt[1].split(", ")

                if tgle == 0:
                    utype = "immune"
                    #print("Immune system", units, hp, weak, immu, atk, atkt, ini)
                    combatants[gid] = iGroup(utype, units, hp, weak, immu, atk+boost, atkt, ini)
                    gid += 1
                else:
                    utype = "infection"
                    #print("Infection", units, hp, weak, immu, atk, atkt, ini)
                    combatants[gid] = iGroup(utype, units, hp, weak, immu, atk, atkt, ini)
                    gid += 1
    # groups created, begin combat loop
    loop = False
    while True:
        # target selection phase
        targetorder = TargetOrder()
        #print(targetorder)
        imTargets = MakeTargets("immune")
        inTargets = MakeTargets("infection")

        if len(imTargets) == 0 or len(inTargets) == 0:
            break

        for g in targetorder:
            targets = imTargets
            if combatants[g].utype == "immune":
                targets = inTargets

            ptarget = -1
            ptdmg = 0
            for t in targets:
                if combatants[t].targeted >= 0:
                    continue
                
                pwr = combatants[g].GetPower()
                if combatants[g].atkt in combatants[t].immu:
                    pwr = 0
                if combatants[g].atkt in combatants[t].weak:
                    pwr *= 2

                #print("Group", g, "would do", pwr, "damage to", t)
                if pwr == 0:
                    continue

                if pwr > ptdmg:
                    ptarget = t
                    ptdmg = pwr
                elif pwr == ptdmg:
                    if combatants[t].GetPower() > combatants[ptarget].GetPower():
                        ptarget = t
                        ptdmg = pwr
                    elif combatants[t].GetPower() == combatants[ptarget].GetPower():
                        if combatants[t].ini > combatants[ptarget].ini:
                            ptarget = t
                            ptdmg = pwr
                
            if ptarget > -1:
                combatants[ptarget].targeted = g
                combatants[g].target = ptarget
                #print("Group", g, "selected target", ptarget, "for", ptdmg)
        
        # attacking
        attackorder = AttackOrder()
        totalunitsremoved = 0
        for a in attackorder:
            # group was destroyed before it got its turn
            if not a in combatants:
                continue

            tg = combatants[a].target
            # should only happen on -1 (no target)
            if not tg in combatants:
                continue

            pwr = combatants[a].GetPower()
            if combatants[a].atkt in combatants[tg].immu:
                pwr = 0
            if combatants[a].atkt in combatants[tg].weak:
                pwr *= 2
            
            
            thp = combatants[tg].hp * combatants[tg].units
            thp -= pwr
            runits = ceil(thp / combatants[tg].hp)
            totalunitsremoved += combatants[tg].units - runits
            #print(combatants[a].utype, a, "does", pwr, "damage and reduces", t, "by", combatants[t].units - runits, "units")

            if runits <= 0:
                # group is dead
                e = combatants[tg].target
                combatants.pop(tg)
                if e > -1:
                    combatants[e].targeted = -1
            else:
                combatants[tg].units = runits
                combatants[tg].targeted = -1
            combatants[a].target = -1

        if totalunitsremoved == 0:
            loop = True
            break

        #input()
    winner = None
    
    if not loop:
        sumcomb = 0
        for x in combatants:
            if winner == None:
                winner = combatants[x].utype
            #print(x, combatants[x].utype, combatants[x].units)
            sumcomb += combatants[x].units
        if first:
            print("Part 1:> ", sumcomb)
        first = False
    else:
        winner = "infection"
    
    if winner == "infection":
        boost += boostbase[0]
    else:
        boost -= boostbase[0] + 1
        boostbase.pop(0)
        if len(boostbase) > 0:
            boost += boostbase[0]
        else:
            end = True
    if end:
        print("Part 2:> ", sumcomb)


## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)