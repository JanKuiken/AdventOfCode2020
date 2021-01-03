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
from copy import copy
from textwrap import wrap

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
    elif len(l) == 1:
        # exception case for rule 67
        return possibilities_of_normal_rule(l[0])
    elif len(l) == 0:
        return []
        
# looks cool, but does it work...
# maxlen = 0
# for k in rules.keys():
#     possibilities = possibilities_of_rule_number(k)
#     for poss in possibilities:
#         print(poss)
#         maxlen = max((maxlen, len(poss)))
# print(maxlen)

# nweeh 24, did i something wrong, or did i not read the question right?
# question: "How many messages completely match rule 0?"

# from question 19 step 2
#    completely replace rules 8: 42 and 11: 42 31 with the following:
#    8: 42 | 42 8
#    11: 42 31 | 42 11 31

# rules[8]   = [ (42,) , (42,8) ]
# rules[11]  = [ (42, 31) , (42, 11, 31) ]

# Note they were:
# rules[8]   = (42,) 
# rules[11]  = (42, 31) 

# rules[8]   = [ ]
# rules[11]  = [ ]

# some more close reading:
#    Fortunately, many of the rules are unaffected by this change; it might 
#    help to start by looking at which rules always match the same set 
#    of values and how those rules (especially rules 42 and 31) are used 
#    by the new versions of rules 8 and 11.

# possibilities_of_rule_number(42)  gives unique 128 messages of length 8
# possibilities_of_rule_number(31)  gives unique 128 messages of length 8
# samen hebben ze 256 unieke waardes

rule_0 = possibilities_of_rule_number(0)
print(Counter([len(r) for r in rule_0]))
# all are length 24

# with original rules 8 and 11, we had 2097152 items in rule_0
# with emty rules 8 and 11 we have zero items in rule_0

# i.e. all items used rule 8 or 11
# dus als een oplossing eidigd op <42> kan het ook eindigend op <42><42> of <42><42><42> enz
# dus als een oplossing eidigd op <42><31> kan het ook eindigend op <42><42><31> of <42><42><42><31> enz
#                                            maar ook op <42><42><42><31><31> etc...

# even de juiste antwoorden verzamelen met orginele rules 8 en 11:
rule_0 = possibilities_of_rule_number(0)
#answers = []
#for msg in messages:
#    if msg in rule_0:
#        answers.append(msg)
#print(len(answers))

# even knoeien
long_messages = [m for m in messages if len(m) > 24]

rule_42 = possibilities_of_rule_number(42)   # <42>
rule_31 = possibilities_of_rule_number(31)   # <31>

long_messages_42 = [msg for msg in long_messages if msg[-8:] in rule_42]
long_messages_31 = [msg for msg in long_messages if msg[-8:] in rule_31]


# filter messages which comply to <??><??><42>..<42>
filtered_42 = []
for msg in long_messages_42:
    bytes = wrap(msg, 8) # cool, googled it, i did not know this function before AdventOfCode2020
    bytes_42_valids = [b in rule_42 for b in bytes[2:]]
    print(bytes_42_valids)
    if all(bytes_42_valids):
        filtered_42.append(bytes[0] + bytes[1] )

print('===================================')


def false_and_then_true(bools):
    """
    We do not want a true followed by a false
    """
    if bools[0] == True:
        return False
    for i in range(len(bools)-1):
        if bools[i] and not bools[i+1]:
            return False
    return True


# filter messages which comply to <??><42>..<31>
filtered_31 = []
for msg in long_messages_31:
    bytes = wrap(msg, 8) # cool, googled it, i did not know this function before AdventOfCode2020
    bytes_31_valids = [b in rule_31 for b in bytes[1:]]
    print(bytes_31_valids)
    if false_and_then_true(bytes_31_valids):
        filtered_31.append(bytes[0] )



rule_0_1byte = set([r[:8] for r in rule_0])
rule_0_2byte = set([r[:16] for r in rule_0])

extra = 0
for f31 in filtered_31:
    if f31 in rule_0_1byte:
        extra += 1
print(extra)
for f42 in filtered_42:
    if f31 in rule_0_1byte:
        extra += 1
print(extra)
print(160 + extra)



def true_and_then_false(bools):
    if bools[0] == False:
        return False
    if bools[-1] == True:
        return False
    for i in range(len(bools)-1):
        if bools[i] == False and bools[i+1] == True:
            return False
    return True

bah = 0
for msg in messages:
    bytes = wrap(msg, 8) # cool, googled it, i did not know this function before AdventOfCode2020
    bytes_valids = [b in rule_42 for b in bytes]
    if true_and_then_false(bytes_valids):
        bah += 1
print('deze dan : ', bah)


