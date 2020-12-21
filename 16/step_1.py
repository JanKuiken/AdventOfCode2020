import pprint
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

with open('input.txt') as f:
    blob = f.read()[:-1]

part1, part2, part3 = blob.split('\n\n')


rule = namedtuple('rule', ['name'   ,
                           'from_1' ,
                           'to_1'   ,
                           'from_2' ,
                           'to_2'     ])
rules = []
lines = part1.split('\n')
for line in lines:
    name, numbers = line.split(':')
    range_1, range_2 = numbers.split(' or ')
    from_1, to_1 = range_1.split('-')
    from_2, to_2 = range_2.split('-')
    rules.append(rule(name, 
                      int(from_1), 
                      int(to_1), 
                      int(from_2), 
                      int(to_2)))

def numbers_from_part(part):
    _, numbers = part.split(':\n')
    numbers = numbers.replace('\n', ',')
    return [int(s) for s in numbers.split(',')]
    
my_ticket      = numbers_from_part(part2)
nearby_tickets = numbers_from_part(part3)
# made a oops, nearby_tickets should be list of list of 20 items, fix it:
nearby_tickets = [[nearby_tickets.pop(0) for _ in range(20)] for __ in range(236)]

pp = pprint.PrettyPrinter(indent=4, width=200, compact=True)
pp.pprint(nearby_tickets)

# lets have a look at the rules, with a plot:
plt.close('all')
plt.figure()
for i,r in enumerate(rules):
    # using a NaN to not 'plot the gap'
    xs = [r.from_1, r.to_1, np.nan, r.from_2, r.to_2]
    ys = [i] * 5
    print(xs)
    plt.plot(xs, ys, lw=3)
plt.show()

# ok, looking at the plot, i've got a sneaking suspicion we should
# concentrate on the 'gaps'...

# and is 20! a reasonable number, don't think so...
from operator import mul
from functools import reduce
print(reduce(mul, range(1,21)))
# yup,  2432902008176640000, i thought so


# de gaten worden wel opgevuld door andere rules, blijft over waardes
# buiten bereik
# max of rules 974, min of rules 26

som = 0
for ticket in nearby_tickets:
    for number in ticket:
        if number < 26 or number > 974:
            print(number)
            som += number
print(som) 





