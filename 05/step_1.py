

with open('input.txt') as f:
    alles = f.read()
    
alles = alles.replace('B', '1')
alles = alles.replace('F', '0')
alles = alles.replace('R', '1')
alles = alles.replace('L', '0')

boarding_passes = alles.split()

IDs = [int(i, base=2) for i in boarding_passes]

print(max(IDs))

IDs.sort()

n = len(IDs)
for i in range(n-1):
    if (IDs[i+1] - IDs[i]) == 2:
        print(IDs[i+1], IDs[i])

