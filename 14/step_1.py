import numpy as np

with open('input.txt') as f:
    blob = f.read()
lines = blob[:-1].split('\n')



memory = {}  # empty dictionary, key, value will be address,value
mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # dummy mask

def masked_value(value):
    str_val = ('0' * 36 + bin(value)[2:])[-36:]
    ret_val = ''
    for mc, vc in zip(mask, str_val):
        if mc == '0':
            c = '0'
        elif mc == '1':
            c = '1'
        else:
            c = vc
        ret_val += c
    return int(ret_val, 2)

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
        memory[address] = masked_value(value)

print('\n\n answer:', sum(memory.values()))




