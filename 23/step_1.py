"""
AdventOfCode2020 day 23 (https://adventofcode.com/2020/day/23)

aha, fun with a ring buffer
(note: very fragile code, almost no checks, globals, etc...)

"""

# ieniemini klasje (ik hou niet van classes schrijven in Python)
class Node():
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

input_str = '643719258'
#input_str = '389125467' # input from example
input_list = [int(i) for i in input_str]

# onze 'pointers' naar de data (nodes)
current_cup = None
picked_up = None

# initialize our 'ring-buffer'
last = None
for i in input_list:
    node = Node(i)
    if last:
        last.next = node
    else:
        current_cup = node
    last = node
last.next = current_cup

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
    if minus_one < 1:
        minus_one = 9
    if not in_picked_up(minus_one):
        return minus_one
    else:
        return get_destination_label(minus_one)

def find_destination_node(value):
    node = current_cup
    while (value != node.value):
        node = node.next
    return node

for _ in range(100):
    print_ring_buffer()
    pick_up_three_after_current()
    print_ring_buffer()
    print_picked_up()
    destination_label = get_destination_label(current_cup.value)
    print(destination_label)
    node = find_destination_node(destination_label)
    insert_picked_up_after_node(node)
    current_cup = current_cup.next
    print_ring_buffer()


# result: 5 --> 4 --> 8 --> 9 --> 6 --> 7 --> 2 --> 3 --> 1 --> 
# i.e. answer : 54896723

