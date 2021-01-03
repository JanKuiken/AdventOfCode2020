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
#maxlen = 0
#for k in rules.keys():
#    possibilities = possibilities_of_rule_number(k)
#    for poss in possibilities:
#        print(poss)
#        maxlen = max((maxlen, len(poss)))
#print(maxlen)
# nweeh 24, did i something wrong, or did i not read the question right?
# question: "How many messages completely match rule 0?"

if False:   # Part One even in een if False: block
    rule_0 = possibilities_of_rule_number(0)
    total = 0
    for msg in messages:
        if msg in rule_0:
            total += 1

    print('\n\n answer part one :', total)

# most likely i did too much work, hopefully it is useful for step 2...

# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

# new rules:
# rules[8] = [(42,), (42,8)]
# rules[11] = [(42,31), (42,11,31)]


set_31 = set(possibilities_of_rule_number(31))
set_42 = set(possibilities_of_rule_number(42))

print(len(set_31))
print(len(set_42))
print(len(set_31.union(set_42)))

# 31 en 42 leveren elk alleen maar '8 bits' sub messages af, 
# elk 128 van 256 mogelijkheden

# rules[31] -> [(48, 133), (41, 127)]
# rules[42] -> [(41, 68), (48, 105)]

if False:
    #rules[8]  = "_rule_8_"
    #rules[11] = "_rule11_"
    rules[31] = "_rule31_"
    rules[42] = "_rule42_"

    rule_0 = possibilities_of_rule_number(0)
    print(rule_0)
    # aha 1 oplossing : ['_rule42__rule42__rule31_']
    raise ValueError('Stop hier maar')
# if if False block gezet

# zonder aanpassing eidigen we dus altijd met rule_11

# kunnen we de messages allemaal inkorten tot '3 bytes' ?
# byte 3 mag rule_31 of rule_42 zijn, maw alles
# we moeten eindigen op rule_31

# als de 3e byte uit rule_31 komt en alle volgende ook 
# uit 31 is het een geldige message

# als de 3e byte uit rule_34 komt en alle volgende eerst
# uit 42 en dan uit 31 komen is het een geldige message
# (minstens 1 uit 31)

# we kunnen ze geldig maken door de 3e byte te veranderen
# in eentje van 31 en dan de onverandere rules te gebruiken

# we gaan messages groter dan 3 bytes op deze manier verbouwen.

if False:
    messages_adapted = []
    for msg in messages:
        if len(msg) <= 24:
            messages_adapted.append(msg)
        elif msg[-8:] in set_42:
            # don't bother does not end with rule 31
            pass
        else:
            # even niet te moeilijk, langste message is 11 'bytes'
            # minus de eerste twee is 9
            n_bytes = len(msg) // 8
            bytes = [msg[8*i:8*(i+1)] for i in range(2,n_bytes)]
            in_rule_42 = [byte in set_42 for byte in bytes]
            #print(n_bytes, msg, bytes, in_rule_42)
            # we mogen niet van rule 31 terug naar rule 42
            from_31_to_42 = False
            for i in range(len(in_rule_42)-1):
                b_1 = in_rule_42[i]
                b_2 = in_rule_42[i+1]
                if b_1 == False and b_2 == True:
                    from_31_to_42 = True
            if from_31_to_42:
                print(n_bytes, msg, bytes, in_rule_42)
                print('Valt af')
            else:
                new_msg = msg[0:16] + 'bbbbbbbb'  # last of set_31
                print(n_bytes, msg, bytes, in_rule_42)
                print(new_msg)
                messages_adapted.append(new_msg)

good = 0
width = 8  # for example 5, else 8
for msg in messages:
    
        n_bytes = len(msg) // width
        bytes = [msg[width*i:width*(i+1)] for i in range(n_bytes)]
        in_rule_42 = [byte in set_42 for byte in bytes]
        #in_rule_31 = [byte in set_31 for byte in bytes]
        #print(n_bytes, in_rule_42)
        length = len(in_rule_42)
        len_42 = sum(in_rule_42)
        len_31 = length - len_42
        if (     all(in_rule_42[:len_42])   # 42 all in front
             and len_42 >= (len_31+1) 
             and len_31 > 0           ):
            
            print(in_rule_42)
            print(msg)
            #print(in_rule_31)
            good += 1
        
print('\n\n answer :', good)

if False:
    rule_0 = possibilities_of_rule_number(0)
    total = 0
    for msg in messages_adapted:
        if msg in rule_0:
            total += 1

    print('\n\n answer :', total)

# damn het is niet 375
# en ook niet 371
# en ook niet 266
# en ook niet 211
# en ook niet 372



