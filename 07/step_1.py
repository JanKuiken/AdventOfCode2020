
from string import ascii_lowercase

with open('input.txt') as f:
    alles = f.read()

# beetje op schonen
alles = alles.replace('bags','')
alles = alles.replace('bag','')
alles = alles.replace('.','')
#alles = alles.replace('no other','')

regels = alles.split('\n')
regels = regels[:-1] # dunno why, got empty last string, this removes it

bags = {}  # dictionary, our data structure
           # key   - color name
           # value - dictionary{ color-name : number }

for regel in regels:
    bag, raw_contents = regel.split('contain')
    bag = bag.strip()
    bag_contents = {}
    for raw_item in raw_contents.split(','):
        raw_item = raw_item.strip()
        if raw_item != 'no other':
            number, color = raw_item.split(' ', maxsplit=1)
            bag_contents[color.strip()] = int(number)
    # add it to the data
    bags[bag] = bag_contents


# which contains a 'shiny gold' bag

def contains_shiny_gold(color):
    global bags
    this_bag = bags[color]
    if 'shiny gold' in this_bag.keys():
        return True
    for color in this_bag.keys():
        if contains_shiny_gold(color):
            return True
    return False

teller = 0
for color in bags.keys():
    if contains_shiny_gold(color):
        print(color)
        teller += 1

print(teller)

# number of bags in a 'shiny gold bag'....

def numbers_of_bags_in_a_bag(my_color):
    global bags
    this_bag = bags[my_color]
    total = 0
    for color, number in this_bag.items():
        total += number
        total += number * numbers_of_bags_in_a_bag(color)
    return total

print(numbers_of_bags_in_a_bag('shiny gold'))        

