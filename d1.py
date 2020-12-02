
freq = [0]
eone = -99999
frst = -99999

while True:
    with open("input1.txt") as fp:
        for line in fp:
            line = int(line.strip())
            nfreq = freq[-1] + line
            if nfreq in freq and frst == -99999:
                frst = nfreq
                break
            freq.append(nfreq)
    if eone == -99999:
        eone = freq[-1]
    if frst != -99999:
        break

print("Frequency change:> ", eone)
print("First repeat:> ", frst)