"""
AdventOfCode 2020, day 21 (https://adventofcode.com/2020/day/21)

We have foods, ingredients and allergeens

Rules:
- Each allergen is found in exactly one ingredient.
- Each ingredient contains zero or one allergen.
- However, even if an allergen isn't listed, the ingredient that contains 
  that allergen could still be present: 
  * maybe they forgot to label it, or 
  * maybe it was labeled in a language you don't know  <<== hmm,...

"""

# stap 1, de invoer in lezen en wat opslaan
with open('input.txt') as f:
    blob = f.read()[:-1]
lines = blob.split('\n')

# foods are identified by line numbers
food_ingredients = {}
food_allergens = {}
for food_number, line in enumerate(lines):
    ingredient_str, allergens_str = line.split(' (contains ')
    allergens_str = allergens_str.replace(')', '')
    food_ingredients[food_number] = ingredient_str.split(' ')
    food_allergens[food_number]   = allergens_str.split(', ')

# tally it up a bit...
foods       = list(food_ingredients.keys())
ingredients = list(set([item for sublist in food_ingredients.values() for item in sublist]))
allergens   = list(set([item for sublist in food_allergens.values() for item in sublist]))

# we hebben :  38 foods (nummertjes)
#               8 allergenen (leesbare tekst)
#             200 ingredienten (onleesbare tekst)
#
# ik voel een 3D tabel aankomen:
#
#      allergen
#          \
#           \
#            \____________
#             |       food
#             |
#             |
#             |
#        ingredient 
#

# Of toch niet...

# lets use a set 'could' (contain) : tuple(ingriedient,allergen)
could = set()
for food in foods:
    for i in food_ingredients[food]:
        for a in food_allergens[food]:
            could.add((i,a))

# Oke lets write the six functions that connect the '3 dimensions'

def ingredients_that_could_contain(allergen):
    return [i for i in ingredients if (i,allergen) in could]

def ingredients_that_are_in(food):
    return food_ingredients[food]

def allergen_that_could_be_in(ingredient):
    return [a for a in allergens if (ingredient,a) in could]

def allergens_that_are_in(food):
    return food_allergens[food]

def foods_that_contains_a(allergen):
    return[f for f in foods if allergen in food_allergens[f]] 

def food_that_contains_i(ingredient):
    return[f for f in foods if ingredient in food_ingredients[f]] 

# Reread the question for step 1 again:
#
#    The first step is to determine which ingredients can't possibly 
#    contain any of the allergens in any food in your list. 
#

if False:

    # dit werkte niet daarom maar even in een if-false block gezet

    for i in ingredients:
        print('====================')
        print(i, ingredients.index(i))
        print(food_that_contains_i(i))
        print(allergen_that_could_be_in(i))
        print('--------------------')
        for a in allergen_that_could_be_in(i):
            # suppose "a is in i" :
            #    check all foods that contain i
            #        and check if a also is in that food
            # if that is not the case then a cannot be in i and therefore
            # we can make an improvement that statement in our 'could' lookup
            for f in food_that_contains_i(i):
                if a in allergens_that_are_in(f):
                    pass
                else:
                    print(a, "cannot be in ", i , " according to food", f)
                    #could.remove((i,a))
                    # klote, dit werkt niet vanwege de regel:
                    # "that allergen could still be present"
                    break # no need to check other foods  


            
possible_i_for_a = {}
for a in allergens:
    print('====================')
    print(a)
    print(foods_that_contains_a(a))
    possible_i = set(ingredients)
    for f in foods_that_contains_a(a):
        # nu maken we gebruik van de intersectie (update) methode van een set
        possible_i.intersection_update(set(ingredients_that_are_in(f)))
    print(possible_i)
    possible_i_for_a[a] = list(possible_i)

# handmatig gechecked dat we (na wat eliminatie) een 1-op-1 relatie 
# hebben, nu nog even ge-automatiseerd, is altijd wat geklier

for _ in range(10): # 10 will do the trick
    for a, possible_i in possible_i_for_a.items():
        if len(possible_i) == 1:
            match = possible_i[0]
            # we've got a single match, remove it from the others
            for a2, possible_i2 in possible_i_for_a.items():
                if a != a2 and match in possible_i2:
                    possible_i2.remove(match)

# note: possible_i_for_a heeft nu nog maar 1 ingredient voor elke alergeen

print('\n\n')
i_without_a = ingredients.copy()
for a, possible_i in possible_i_for_a.items():
    enigste_i = possible_i[0]    
    print (enigste_i, '   bevat ', a)  
    i_without_a.remove(enigste_i)

answer = 0
for i in i_without_a:
    for f in foods:
        if i in food_ingredients[f]:
            answer += 1
print('\n\n  answer = ', answer)

# waarschijnlijk heb ik step_1 te ingewikkeld gedaan, stap 2 is nu een makkie

canonical_dangerous_ingredient_list = []

print(possible_i_for_a)
keys = list(possible_i_for_a.keys())
keys.sort()
for k in keys:
    canonical_dangerous_ingredient_list.append(possible_i_for_a[k][0])

print('\n\n  answer : ', ','.join(canonical_dangerous_ingredient_list))

