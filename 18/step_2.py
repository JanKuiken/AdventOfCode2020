from collections import namedtuple

with open('input.txt') as f:
    lines = f.readlines()

node = namedtuple('node', ['left', 'right', 'char']) # that should do the trick

digits = "23456789"

def find_closing_paren(s):
    n_open = 0
    for i,c in enumerate(s):
        if c == '(':
            n_open += 1
        if c == ')':
            n_open -= 1
        if n_open == -1:
            return s[:i], s[i+1:]
    msg = 'Error finding closing parenthesis in : ' + s
    raise ValueError(msg)

def token_split(s):
    """
    split string s into digits, operators or multi character string for
    parts that were between parenthesis
    """
    tokens = []
    while s != '':
        c, s = s[0], s[1:]
        if c == '(':
            content, s = find_closing_paren(s)
            tokens.append(content)
        elif c in "0123456789+*":
            tokens.append(c)
        else:
            msg =  'Error in token_split: ' + s
            raise ValueError(msg)
    return tokens

def token_join(tokens):
    """
    Silly function to rejoin tokens again to a string
    """
    s = ''
    for t in tokens:
        if len(t) == 1 :
            s += t
        else:
            s += '(' + t + ')'
    return s

def parse(s):
    """
    Parses a string and return a node
    """
    print('Parsing : ', s)
    if len(s) == 0:
        msg = 'Not expecting an empty string'
        raise ValueError(msg)

    tokens = token_split(s)

    if '*' in tokens:
        i     = tokens.index('*')
        left  = parse(token_join(tokens[:i]))
        right = parse(token_join(tokens[i+1:]))
        return node(left, right, '*')
        
    if '+' in tokens:
        i     = tokens.index('+')
        left  = parse(token_join(tokens[:i]))
        right = parse(token_join(tokens[i+1:]))
        return node(left, right, '+')
    
    if len(tokens) > 1:
        msg = 'Not expecting multiple tokens without an operator'
        raise ValueError(msg)

    token = tokens[0]
    if token in digits:
        return node(None, None, token)
        
    return parse(token)

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


