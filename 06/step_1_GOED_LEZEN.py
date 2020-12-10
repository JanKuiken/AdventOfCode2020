
from string import ascii_lowercase

with open('input.txt') as f:
    alles = f.read()

groepen = alles.split('\n\n')

groepen = [s.split() for s in groepen]

teller = 0

for groep in groepen:
    for letter in ascii_lowercase:
        allemaal = True
        for persoon in groep:
            if not letter in persoon:
                allemaal = False
        if allemaal:
            teller += 1
    print(groep)
    print(teller)


