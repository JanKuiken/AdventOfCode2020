
from string import ascii_lowercase

with open('input.txt') as f:
    alles = f.read()

groepen = alles.split('\n\n')

groepen = [s.split() for s in groepen]

teller = 0

for groep in groepen:
    samen = ''.join(groep)
    teller += len(set(samen))

    print(groep)
    print(teller)


