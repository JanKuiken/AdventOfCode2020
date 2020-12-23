"""
Observations from input data:

- rules are not in order (nweeh, don't care)
- only 2 character rules : "a" and "b"
- every rule consists of: 1/2 subrules or an 2 options of 1/2 subrules
- there seem to be 134 rules
- we found 113 option rules (my editor found 113 '|' symbols)
- so there must be 134-2-113 = 19 'normal' rules   

Would it be feasable to work out all rules to get a collection of all
possible messages? Doubtfull with all the options rules, each doubles the
amount of possibilities.
But we don't know the depth of the rule nesting yet...
First store the rules and messages in appropriate datastructures.

"""
from collections import Counter
from itertools import product

with open('input.txt') as f:
    blob = f.read()[:-1]

part1, part2 = blob.split('\n\n')

messages = [] # list for the messages

lines = part2.split('\n')
for line in lines:
    messages.append(line)

# hmm, is there something funny going on with the length of the
# messages, lets check...
msg_len = [len(m) for m in messages]
count = Counter(msg_len)
print(count)
print(len(count))
# yup we have only 9 distinct lengths:
#    24: 181
#    32:  78 
#    40:  72
#    48:  43
#    56:  35
#    64:  19
#    72:  13
#    80:   8
#    88:   5


rules = {} # dictionary to store the rules
           # key   : rule_id 
           # value : - 'a' or 'b' for chararcter rules
           #       : tuple with subrules ints for 'normal' rules
           #       : list with tuples as above for 'option rules' 

lines = part1.split('\n')
for line in lines:
    number, content = line.split(': ')
    number = int(number)
    if content == '"a"':
        rules[number] = 'a'
    elif content == '"b"':
        rules[number] = 'b'
    elif ' | ' in content:
        options = content.split(' | ')
        rules[number] = [tuple([int(n) for n in opt.split(' ')]) for opt in options]
    else:
        rules[number] = tuple([int(n) for n in content.split(' ')])

# let's check some stuff, number of subrules, mostly 2 but...
print('=================')
for number, rule in rules.items():
    if type(rule) == tuple:
        print(number, len(rule))
print('=================')
for number, rule in rules.items():
    if type(rule) == list:
        print(number, [len(t) for t in rule])
print('=================')
# Ahaa, there is only one normal rule (8) with a single subrule and
# only one option rule (67) with single subrules...

# those two must be used often in the messages, because the otherwise the
# lengths of the message would be powers of two, the only length of a power
# of two is 64 (buggers, we still have 19 of those....)

# with the largest message lenght of 88 i estimated the rule-depth should
# nor exceed 7 'cause 2^7=128...


# attempt to brute force, recursivly find all possibilities of a rule
# (buggers rule 8 and 67 make it complicated...)
def possibilities_of_rule_number(number):
    """
    """
    rule = rules[number]
    if type(rule) == str:
        return possibilities_of_character_rule(rule)
    elif type(rule) == tuple:
        return possibilities_of_normal_rule(rule)
    elif type(rule) == list:
        return possibilities_of_options_rule(rule)
    else:
         raise ValueError('Unexpected type in possibilities_of_rule')

def possibilities_of_character_rule(s):
    # character rule simply return the character ('a' or 'b') packed in a list
    return [s]

def possibilities_of_normal_rule(t):
    # normal rule, input tuple of rules, combine posibilties
    if len(t) == 2: 
        p1 = possibilities_of_rule_number(t[0])
        p2 = possibilities_of_rule_number(t[1])
        return([s1+s2 for s1,s2 in product(p1,p2)])
    else:
        # exception case for rule 8
        return possibilities_of_rule_number(t[0])

def possibilities_of_options_rule(l):
    # options rule, input list of tuple of rules, add posibilties
    if len(l) == 2:
        p1 = possibilities_of_normal_rule(l[0])
        p2 = possibilities_of_normal_rule(l[1])
        return p1 + p2
    else:
        # exception case for rule 67
        return possibilities_of_normal_rule(l[0])
        
# looks cool, but does it work...
maxlen = 0
for k in rules.keys():
    possibilities = possibilities_of_rule_number(k)
    for poss in possibilities:
        print(poss)
        maxlen = max((maxlen, len(poss)))

print(maxlen)
# nweeh 24, did i something wrong, or did i not read the question right?
# question: "How many messages completely match rule 0?"

rule_0 = possibilities_of_rule_number(0)
total = 0
for msg in messages:
    if msg in rule_0:
        total += 1

print('\n\n answer :', total)

# most likely i did too much work, hopefully it is useful for step 2...









