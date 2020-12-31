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

# test data from example
# player_1 = deque([9, 2, 6, 3, 1])
# player_2 = deque([5, 8, 4, 7, 10])


def play_game(player_1, player_2):

    print('>>>> Start <<<<')
    print(player_1)
    print(player_2)
    
    previous_rounds = set()

    while len(player_1) and len(player_2):       # both players have card(s)
    
        # check special rule:
        if str((player_1, player_2)) in previous_rounds:
            print('>>>> Special repeat rule')
            # move player_2 cards to player_1, to indicate win for player_1
            player_1.extend(player_2)
            player_2.clear()
            print('>>>> Einde <<<<')
            return player_1, player_2
        
        # store this situation, transform to str, set wants hashable items
        previous_rounds.add(str((player_1, player_2)))
 
        player_1_card = player_1.popleft()
        player_2_card = player_2.popleft()
        
        if (    len(player_1) >= player_1_card
            and len(player_2) >= player_2_card ) :
            
            # we start a sub game
            p1 = deque(list(player_1)[:player_1_card])
            p2 = deque(list(player_2)[:player_2_card])
            p1, p2 = play_game(p1, p2)
            
            if len(p1) > len(p2):                    # player 1 wins
                player_1.append(player_1_card)
                player_1.append(player_2_card)
            else:                                    # player 2 wins
                player_2.append(player_2_card)
                player_2.append(player_1_card)
        else:
            
            # normal playing
            if player_1_card > player_2_card:        # player 1 wins
                player_1.append(player_1_card)
                player_1.append(player_2_card)
            else:                                    # player 2 wins
                player_2.append(player_2_card)
                player_2.append(player_1_card)

    print('>>>> Einde <<<<')
    return player_1, player_2


# oke let's play
player_1, player_2 = play_game(player_1, player_2)

# we dont care who has won, we stack the decks together and calculate the score
deck = list(player_1) + list(player_2)
deck.reverse() # inplace
score = 0
for i, card in enumerate(deck):
    score += (i+1) * card

print('\n\n  answer : ', score)

