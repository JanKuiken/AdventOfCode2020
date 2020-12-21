# Oops, code is pretty messy because my first attempt had a serious flaw
# (see step_1_doet_het_niet_goed.py) and i applied some silly patches
# to fix it to get right answer.
# (i changed parsing from the right instead of left....)
# I promise to clean up for 'part two'
 
from collections import namedtuple

# test data
lines = [
    '3+4*5',
    '3*4+5',
    '2 * 3 + (4 * 5)',
    '5 + (8 * 3 + 9 + 3 * 4 * 3)',
    '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
    '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
]


with open('input.txt') as f:
    lines = f.readlines()


# Quick inspection of the input file:
# - numbers all have only one digit and are not 0 or 1, so in '23456789'
# - operators '+' and '*' have spaces around them (we could remove them...)
# - parenthes seem to behave as expected
# - lines may start with a '('
# - all lines have at least one operator
# - inside parenthesis is at least one operator

# ( I guess part 2 will be about '+' having a higher precedence than '*'...
#   ... or right to left evaluation...., i hope the latter then i only
#   need to make one change...

# shall we use a (parse) tree? with a named tuple as node, that'll be fun

node = namedtuple('node', ['left', 'right', 'char']) # that should do the trick

digits = "0123456789"

def find_opening_paren(s):
    """
    pretty much weirdified, due to modifing, first failed attempt
    """
    reverserd = list(s)
    reverserd.reverse()
    n_open = 0    
    for i,c in enumerate(reverserd):
        if c == ')':
            n_open += 1
        if c == '(':
            n_open -= 1
        if n_open == -1:
            s1 = reverserd[:i]
            s1.reverse()
            s2 = reverserd[i+1:]
            s2.reverse()
            return (''.join(s1), ''.join(s2))
    msg = 'Error finding opening parenthesis in : ' + s
    raise ValueError(msg)

def parse(s):
    """
    Parses a string and return a node
    """
    print('Parsing : ', s)
    if len(s) == 0:
        msg = 'Not expecting an empty string'
        raise ValueError(msg)
    
    c = s[-1]
    if c == ')':
        content, remainder = find_opening_paren(s[:-1])
        temp = parse(content)
    elif c in digits:
        remainder = s[:-1]
        temp = node(None, None, c)
    else:
        msg =  'Parse Error in : ' + s
        raise ValueError(msg)
               
    if remainder == '':
        # we're done !
        return temp
        
    # Oke now we expect an operator and a (new)remainder
    c = remainder[-1]
    new_remainder = remainder[:-1]
    if c in "+*":
        return node(temp, parse(new_remainder), c)
    else:
        msg = 'Was expecting an operator in :' + remainder
        raise ValueError(msg)

def evaluate(node):
    if node.char in digits:
        return int(node.char)
    elif node.char == '+':
        return evaluate(node.left) + evaluate(node.right)
    elif node.char == '*':
        return evaluate(node.left) * evaluate(node.right)
    else:
        msg = 'Error in evaluate (bummer)'
        raise ValueError(msg)

answer = 0    
for line in lines:
    # clean up a bit
    line = line.replace('\n','')
    line = line.replace(' ','')
    # parse
    top_node = parse(line)    
    # eval
    value = evaluate(top_node)
    print(line, ' = ', value)
    answer += value

print('\n\n answer:', answer)


