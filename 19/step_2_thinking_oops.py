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
global_str = ''
max_depth = 200
pos = set()
def visit_rule_number(number, depth):
    """
    """
    global global_str
    
    rule = rules[number]
    print('depth :', depth, rule)

    #if depth > 100:
    #    return
    #    #print('Het kan te gek')

    if type(rule) == str:
        # character rule
        #if depth <= max_depth:
        if len(global_str) <= 88 or depth >= max_depth:

            global_str += rule
            #print('added : ', global_str)
            return rule

    elif type(rule) == tuple:
        #normal rule
        #if depth <= max_depth:
        #if len(global_str) <= 88:
        if len(global_str) <= 88 or depth >= max_depth:
        
            backup_str = global_str
            test_str = ''
            for number in rule:
                global_str = ''
                visit_rule_number(number, depth + 1)
                test_str += global_str
            # nice place to check
            #print('check : ', test_str, ' - ', len(test_str))
            print('check : ', len(test_str), test_str)
            pos.add(test_str)
            global_str = backup_str
        
    elif type(rule) == list:
        # options rule, input list of tuple of rules, add posibilties
        #if depth <= max_depth:

        for t in rule:
            for number in t:
            
                if len(global_str) <= 88 or depth >= max_depth:

                    visit_rule_number(number, depth + 1)


    else:
         raise ValueError('Unexpected type in visit_rule_number')

        
# ... (some code removed from  step_1.py)

# most likely i did too much work, hopefully it is useful for step 2...

# from question 19 step 2
#    completely replace rules 8: 42 and 11: 42 31 with the following:
#    8: 42 | 42 8
#    11: 42 31 | 42 11 31

# rules[8]   = [ (42,) , (42,8) ]
# rules[11]  = [ (42, 31) , (42, 11, 31) ]


# mijn test gevalletjes
rules[200] = ((48,41))                                                                                                                   
rules[201] = ((41,48))                                                                                                                   
rules[202] = [(200,201),(201,200)]   

visit_rule_number(0, depth=0)




