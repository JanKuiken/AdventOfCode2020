"""
 a tile is defined by four 10 binary digits numbers (decimal 0-1023), for
 example the first tile in the inputfile:

  Tile 2131:

            ---> 
         1110010001
        
      1  ###..#...#  1
      1  ##..#.##.#  1        top    : 0b1110010001   ~ 913  (decimal)
      0  ..###...#.  0        right  : 0b1101110011   ~ 883
   ^  0  ......#..#  1 |      bottom : 0b1101001101   ~ 845
   |  1  ##.#.....#  1 |      left   : 0b1000010011   ~ 531
   |  0  ..#..#...#  1 |
   |  0  ......#...  0 v       
      0  ......#...  0
      0  .........#  1
      1  #.##..#.##  1
        
         1011001011    
            <---

 - a rotation of a tile is cycling values of (top, right, bottom, left)
 - a horizontal flip is swapping left and right and binary reverse all
 - a vertical flip is swapping top and bottom and binary reverse all
 
 we have 144 tiles, i.e. a 12x12 matrix
            
"""
from collections import namedtuple, Counter
from functools import reduce
from operator import mul

tile = namedtuple('tile', ['top', 'right', 'bottom', 'left'])

# read data and trans form it
with open('input.txt') as f:
    blob = f.read()[:-1]
    
tiles_txt = blob.split('\n\n')

tiles = {}
for tile_txt in tiles_txt:

    # split tiles, extract tile number and tile content
    header, body = tile_txt.split(':\n')
    tile_number = int(header.replace('Tile ',''))

    # clean up body, join lines, change to 0's and 1's
    body = body.replace('\n','')
    body = body.replace('#','1')
    body = body.replace('.','0')
    
    # find top, right, bottom, left with some fancy indexing
    top    = int( body[0:10]     ,2)
    right  = int( body[9:100:10] ,2)
    bottom = int( body[99:89:-1] ,2)
    left   = int( body[90::-10]  ,2)
    
    # for manual check, print it
    print(tile_number, top, right, bottom, left)
    
    # add it to our data store
    tiles[tile_number] = tile(top, right, bottom, left)


# oke, lets write that 'binary reverse' function 

def binary_reverse(i, n=10):
    """
    reverse the bits of a 10(default) bit number
    """
    s = bin(i)                      # change it to a binary string
    s = s[2:]                       # remove leading '0b'
    s = '0' * n + s                 # add enough leading zeros in front
    s = s[-n:]                      # take last (right) 10 most characters
    l = list(s)                     # make a list of the characters
    l.reverse()                     # reverse it (inplace)
    s = ''.join(l)                  # make it a string again
    return int(s, 2)                # return it as an int with base 2

# first damage assesment: 'what amount sides can connect to other sides?'

sides = []
for t in tiles.values():
    sides.append(t.top)
    sides.append(t.right)
    sides.append(t.bottom)
    sides.append(t.left)
    sides.append(binary_reverse(t.top))
    sides.append(binary_reverse(t.right))
    sides.append(binary_reverse(t.bottom))
    sides.append(binary_reverse(t.left))

count = Counter(sides)
print(count.values())
print(set(count.values()))

# result {1,2}, so we are lucky:
#  - each side fits to only one other side of another piece
#  - we have sides, that dont fit to other pieces, i.e. side or corner pieces

# lets run the count results again through a count:
count_2 = Counter(count.values())
print(count_2)
print(set(count_2.values()))

# ok, this looks solid we have:
print(12 * 4 * 2)       # external sides  (sides * 2 for reversed numbers) 
print(12 * 11 * 2 * 2)  # internal sides  (horizontal + vertical * 2 )

sides_with_no_neightbours = [key for key,values in count.items() if values == 1]

# find tiles with 4 (2* 2 for reversed numbers) sides without neighbours
# that must be corners
corners = []
for tile_number, sides in tiles.items():
    n = 0
    if sides.top                    in sides_with_no_neightbours  : n += 1
    if sides.right                  in sides_with_no_neightbours  : n += 1
    if sides.bottom                 in sides_with_no_neightbours  : n += 1
    if sides.left                   in sides_with_no_neightbours  : n += 1
    if binary_reverse(sides.top)    in sides_with_no_neightbours  : n += 1
    if binary_reverse(sides.right)  in sides_with_no_neightbours  : n += 1
    if binary_reverse(sides.bottom) in sides_with_no_neightbours  : n += 1
    if binary_reverse(sides.left)   in sides_with_no_neightbours  : n += 1
    if n == 4:
        print(tile_number)
        corners.append(tile_number)

print('\n\n answer:', reduce(mul, corners))

