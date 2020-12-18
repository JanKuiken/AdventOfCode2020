import numpy as np
from collections import Counter

with open('input.txt') as f:
    blob = f.read()
lines = blob[:-1].split('\n')



memory = {}  # empty dictionary, key, value will be address,value
mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # dummy mask


def str_to_int(s):
    return int(s, 2)

def int_to_str(i):
    return ('0' * 36 + bin(i)[2:])[-36:]


# ff checken of dit gaat lukken, hoeveel writes hebben we
max_xs = 0
writes = 0
for line in lines:
    command, value = line.split(' = ')
    if command == 'mask':
        mask = value
        c = Counter(mask)
        print(mask, c)
        writes += 2 ** c['X']
        max_xs = max(max_xs, c['X'])
print(writes)
print(max_xs)
# oke, 17k, dat gaat lukken met ons dictionary memory
# max 2**9 = 512 adressen tegelijkertijd

# we pakken er even een 'power' tool by
from itertools import product

def masked_addresses(mask, address):
    str_address = int_to_str(address)
    # eerst even de '0' en de '1' aanpakken
    first_step = ''
    for ac, mc in zip(str_address, mask):
        if mc == '0' :
            first_step += ac
        elif mc == '1':
            first_step += '1'
        else:
            first_step += 'X'

    addresses = []
    x_positions = [ pos for pos,c in enumerate(first_step) if c=='X']
    for replacements in product(['0', '1'], repeat=len(x_positions)):
        second_step = list(first_step)
        for pos, replace in zip(x_positions, replacements):
            second_step[pos] = replace        
        addresses.append(str_to_int(''.join(second_step)))
    
    return addresses



for line in lines:
    command, value = line.split(' = ')
    if command == 'mask':
        mask = value
        
    else:
        # command must be 'mem[...]' (i've checked input file)
        command = command.replace('mem[','')
        command = command.replace(']', '')
        address = int(command)
        value   = int(value)
        
        for a in masked_addresses(mask, address):
            memory[a] = value

print('\n\n answer:', sum(memory.values()))
# 4877695371685



