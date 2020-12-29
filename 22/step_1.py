"""
AdventOfCode2020 day 22 (https://adventofcode.com/2020/day/22)

The problems descriptions screams at me that i should use the
deque class from the collections library.

"""

from collections import deque

# read input (again...)
with open('input.txt') as f:
    blob = f.read()[:-1]

# split in players, skip header (Player x:'), change to integer and make deques
player_1, player_2 = blob.split('\n\n')
player_1 = deque([int(line) for line in player_1.split('\n')[1:]])
player_2 = deque([int(line) for line in player_2.split('\n')[1:]])

# play game
while len(player_1) and len(player_2):       # both players have card(s)

    player_1_card = player_1.popleft()
    player_2_card = player_2.popleft()

    if player_1_card > player_2_card:        # player 1 wins

        player_1.append(player_1_card)
        player_1.append(player_2_card)

    else:                                    # player 2 wins

        player_2.append(player_2_card)
        player_2.append(player_1_card)

# we dont care who has won, we stack the decks together and calculate the score
deck = list(player_1) + list(player_2)
deck.reverse() # inplace
score = 0
for i, card in enumerate(deck):
    score += (i+1) * card

print('\n\n  answer : ', score)

