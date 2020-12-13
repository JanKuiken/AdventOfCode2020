
with open('input.txt') as f:
    blob = f.read()
lines = blob[:-1].split('\n')

# obeservations from input file:
# - angles for R and L are 90,180,270
# - steps for N,E,S,W are < 10
# - steps for F are <= 100
# - 783 commands
# - all commands seem valid

# (lets do some funky code layout, totally ignoring PEP8)

# make a map for direction changes
# nested dict, keys: current_dir, ['R'|'L'], [90|180|270]
dir_change = {
   'N': { 'R' : { 90: 'E', 180: 'S', 270: 'W'},
          'L' : { 90: 'W', 180: 'S', 270: 'E'}, },
   'E': { 'R' : { 90: 'S', 180: 'W', 270: 'N'},
          'L' : { 90: 'N', 180: 'W', 270: 'S'}, },
   'S': { 'R' : { 90: 'W', 180: 'N', 270: 'E'},
          'L' : { 90: 'E', 180: 'N', 270: 'W'}, },
   'W': { 'R' : { 90: 'N', 180: 'E', 270: 'S'},
          'L' : { 90: 'S', 180: 'E', 270: 'N'}, }, }

x = 0    # positive ~ east
y = 0    # positive ~ north
d = 'E' 

for line in lines:

    command = line[0]
    value   = int(line[1:])
    
    if   command == 'N' : y += value
    elif command == 'E' : x += value
    elif command == 'S' : y -= value
    elif command == 'W' : x -= value
    elif command == 'R' : d = dir_change[d][command][value]
    elif command == 'L' : d = dir_change[d][command][value]
    elif command == 'F' :
        if   d == 'N'   : y += value
        elif d == 'E'   : x += value
        elif d == 'S'   : y -= value
        elif d == 'W'   : x -= value
        else            : print('Invalid direction !!'); break
    else                : print('Invalid command !!'); break
    
manhattan_distance = abs(x) + abs(y)
print(manhattan_distance)

