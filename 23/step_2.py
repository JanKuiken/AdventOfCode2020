"""
AdventOfCode2020 day 23 (https://adventofcode.com/2020/day/23)

aha, fun with a ring buffer
(note: very fragile code, almost no checks, globals, etc...)

Part two:
met grote aantallen.....:

  "10_000_000 x iets doen" is veel maar nog wel te doen....
  "10_000_000 x 1_000_000 x iets doen" is te veel...

De "x 1_000_000" zit um in de functie 'find_destination_node' waar ook een
loop in zit. Wellicht kunnen we loop eruit halen door een dictionary aan
te maken voor het opzoeken van de destination node (key=label, value=node).
(het verhaal gaat dat dictionaries lightning fast zijn...)

print statements nog even weghalen en zo...
"""

# ieniemini klasje (ik hou niet van classes schrijven in Python)
class Node():
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

input_str = '643719258'
# input_str = '389125467' # input from example
input_list = [int(i) for i in input_str]

# add labels for Part Two
for l in range(10, 1_000_001):   # let op +1, we zijn begonnen bij 1
    input_list.append(l)
print('list created')

# onze 'pointers' naar de data (nodes)
current_cup = None
picked_up = None

label_node_map = {}
min_value = min(input_list) # some globals for 'get_destination_label'
max_value = max(input_list)

# initialize our 'ring-buffer'
last = None
for i in input_list:
    node = Node(i)
    label_node_map[i] = node
    if last:
        last.next = node
    else:
        current_cup = node
    last = node
last.next = current_cup
print('ring buffer created')


def print_ring_buffer():
    stop_node = None
    node = current_cup
    while True:
        print(node.value, end=' --> ')
        if not stop_node:
            stop_node = node
        node = node.next
        if node == stop_node:
            break
    print()

def print_picked_up():
    print(picked_up.value, picked_up.next.value, picked_up.next.next.value)

def in_picked_up(value):
    return (    value == picked_up.value
             or value == picked_up.next.value
             or value == picked_up.next.next.value )
             
def pick_up_three_after_current():
    global picked_up
    picked_up                = current_cup.next
    current_cup.next         = current_cup.next.next.next.next 
    picked_up.next.next.next = None

def insert_picked_up_after_node(node):
    global picked_up
    picked_up.next.next.next = node.next
    node.next                = picked_up
    picked_up                = None

def get_destination_label(value):
    """Even moeilijk doen, er weer wat recursie in gooien"""
    minus_one = value - 1
    if minus_one < min_value:
        minus_one = max_value
    if not in_picked_up(minus_one):
        return minus_one
    else:
        return get_destination_label(minus_one)

def find_destination_node(value):
    node = current_cup
    while (value != node.value):
        node = node.next
    return node

def find_destination_node_2(value):
    return label_node_map[value]

N = 10_000_000
for m in range(N):
    if m%10000 == 0:
        print(m)
    pick_up_three_after_current()
    destination_label = get_destination_label(current_cup.value)
    node = find_destination_node_2(destination_label)
    insert_picked_up_after_node(node)
    current_cup = current_cup.next

# print_ring_buffer()

node_one = find_destination_node_2(1)
print(node_one.value)
print(node_one.next.value)
print(node_one.next.next.value)
print('\n\n answer : ', node_one.next.value * node_one.next.next.value)

