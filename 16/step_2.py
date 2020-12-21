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
    #plt.plot(xs, ys, lw=3)
#plt.show()

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

valid_tickets = []
for ticket in nearby_tickets:
    if not(min(ticket) < 26 or max(ticket) > 974):
        valid_tickets.append(ticket)

# oke lets make a 20x20 matrix called 'could_be'  with
#   first index : the 'index' of valid ticket numbers
#   second index : the index of rules
# initially all True, then work through the valid tickets to find out
# which valid_index violates which rule_index

could_be = np.ones((20,20), dtype=bool)
for ticket in valid_tickets:
    for valid_index, number in enumerate(ticket):
        for rule_index, rule in enumerate(rules):
            if (    (number >= rule.from_1 and number <= rule.to_1) 
                 or (number >= rule.from_2 and number <= rule.to_2)) :
                pass # oke could be
            else:
                could_be[valid_index, rule_index] = False

print(could_be)
print(np.sum(could_be, axis = 1))
print(np.sum(could_be, axis = 0))

# oke, we have a row with only one 'could_be', we can set the rule_index
# of other rows to False, same for columns visa versa. 
# Repeat this action untill we end up with only one True in each row and column

while(True):
    row_sums = np.sum(could_be, axis = 1)
    col_sums = np.sum(could_be, axis = 0)
    # break if we can
    if max(row_sums) == 1 and max(col_sums) == 1:
        break
    # eliminate where row_sum = 1
    for row_index in range(20):
        if row_sums[row_index] == 1:
            # find the columns
            for col_index in range(20):
                if could_be[row_index,col_index]:
                    # set the whole column to False....
                    could_be[:,col_index] = False
                    # except of course the True we found
                    could_be[row_index,col_index] = True
    # eliminate where col_sum = 1
    for col_index in range(20):
        if col_sums[col_index] == 1:
            # find the rows
            for row_index in range(20):
                if could_be[row_index,col_index]:
                    # set the whole row to False....
                    could_be[row_index,:] = False
                    # except of course the True we found
                    could_be[row_index,col_index] = True

print(could_be)
print(np.sum(could_be, axis = 1))
print(np.sum(could_be, axis = 0))

# cool, we have a solid mapping from ticket index to rule index

answer = 1
for rule_index in range(20):
    for ticket_index in range(20):
        if could_be[ticket_index, rule_index]:
            print(rule_index, 
                  ticket_index, 
                  rules[rule_index].name,
                  my_ticket[ticket_index])
            if rules[rule_index].name.startswith('departure'):
                answer *= my_ticket[ticket_index]

print('\n\n answer:', answer)




