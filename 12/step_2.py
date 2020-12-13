
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

# part two, add waypoint (relative to the ship), remove direction
x = 0    # positive ~ east
y = 0    # positive ~ north
wx = 10
wy = 1

def rotate_waypoint(command, value, old_wx, old_wy):
    if   value == 180:
        # rotate waypoint 180 degrees
        new_wx = -old_wx
        new_wy = -old_wy
    elif (    (command == 'R' and value == 90 )
           or (command == 'L' and value == 270) ) :
        # rotate waypoint 90 degrees clock wise
        new_wx =  old_wy
        new_wy = -old_wx
    elif (    (command == 'R' and value == 270)
           or (command == 'L' and value == 90 ) ) :
        # rotate waypoint 90 degrees counter clock wise
        new_wx = -old_wy
        new_wy =  old_wx
    else:
        print('Unknown oops in function "rotate_waypoint"')

    return new_wx, new_wy



for line in lines:

    command = line[0]
    value   = int(line[1:])
    
    if   command == 'N' : wy += value
    elif command == 'E' : wx += value
    elif command == 'S' : wy -= value
    elif command == 'W' : wx -= value
    elif command == 'R' : wx, wy = rotate_waypoint(command, value, wx, wy)
    elif command == 'L' : wx, wy = rotate_waypoint(command, value, wx, wy)
    elif command == 'F' : x += value * wx; y += value * wy
    else                : print('Invalid command !!'); break
    
manhattan_distance = abs(x) + abs(y)
print(manhattan_distance)

