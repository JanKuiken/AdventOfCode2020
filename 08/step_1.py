
from string import ascii_lowercase

with open('input.txt') as f:
    alles = f.read()

instructions   = alles.split('\n')
accumulator    = 0
visited        = set()
pc             = 0

while(True):

    # check program counter
    if pc in visited:
        print('Loop detected')
        break
    if pc < 0 or pc >= len(instructions):
        print('Invalid program counter')
        break
    visited.add(pc)
    
    # execute command
    command, value = instructions[pc].split(' ')
    if command == 'nop':
        pc += 1
    elif command == 'acc':
        accumulator += int(value)
        pc += 1
    elif command == 'jmp':
        pc += int(value)
    else:
        print('Invalid command')
        break
        
print(accumulator)

