
from string import ascii_lowercase

with open('input.txt') as f:
    alles = f.read()

instructions_org   = alles[:-1].split('\n')

def run_program(instructions):

    # init computer
    accumulator    = 0
    visited        = set()
    pc             = 0

    while(True):

        # check program counter
        if pc in visited:
            print('Loop detected')
            return False
        if pc < 0 or pc >= len(instructions):
            print('Invalid program counter')
            return False
        if pc == (len(instructions) - 1):
            print('Program finished correctly!')
            print(accumulator)
            return True
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
            return False
            
# just try to run the program with 1 instruction changed
for i in range(len(instructions_org)):
    print(i)
    instructions = instructions_org.copy()
    if instructions[i][0:3] == 'jmp':
        instructions[i] = instructions[i].replace('jmp', 'nop')
    elif instructions[i][0:3] == 'nop':
        instructions[i] = instructions[i].replace('nop', 'jmp')
    if run_program(instructions):
        break

