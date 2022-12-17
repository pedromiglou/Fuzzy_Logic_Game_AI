from treys import Card, Deck, Evaluator

# initializes Deck and Evaluator
deck = Deck()
evaluator = Evaluator()

# number of draws
n = 52 # maximum draws
n_board = 3 # initial board draws
n_player = 2 #player draws

deck = deck.draw(n) # draws all cards

board = [
        Card.new('Ad'),
        Card.new('7d'),
        Card.new('2s'),
        ]


p_hand = [
        Card.new('Ah'),
        Card.new('6c'),
        ]

for card in p_hand:
    print(card)
    deck.remove(card)
    
for card in board:
    deck.remove(card)

n = n - n_board - n_player #maximum draws after drawing board and player hand cards


# 1st turn
# board = deck.draw(n_board)
# p_hand = deck.draw(n_player)
# deck = deck.draw(n) # draws remaining cards so its easier to access them

#prints current cards and cards available in the deck
print("Player's hand: ")
Card.print_pretty_cards(p_hand)
print("Community cards: ")
Card.print_pretty_cards(board)
print()


# computes ocurrences with only 4 cards in the board, 2nd turn
prob_turn = {}
for i in range(n):
    # draws a card to the board
    board_sim = board + [deck[i]]
    p_score_sim = evaluator.evaluate(board_sim, p_hand)
    p_class_sim = evaluator.class_to_string(evaluator.get_rank_class(p_score_sim))
       
    try:
        prob_turn[p_class_sim] += 1
    
    except:
        prob_turn[p_class_sim] = 1

# computes ocurrences with 4 and then 5 cards in the board, last turn
prob_turn_and_river = {}
for i in range(n):
    # draws a card to the board
    board_sim = board + [deck[i]]
    for j in range(n-1):
        # draws a 5th and final card to the board
        board_sim = board + [deck[j]]
        p_score_sim = evaluator.evaluate(board_sim, p_hand) 
        p_class_sim = evaluator.class_to_string(evaluator.get_rank_class(p_score_sim)) 

        try:
            prob_turn_and_river[p_class_sim] += 1
    
        except:
            prob_turn_and_river[p_class_sim] = 1

board = board + [deck.pop()] # turns the 4th card
prob_river = {}
# computes ocurrences with 5 cards in the board, last turn
for i in range(n-1):
    board_sim = board + [deck[i]]
    p_score_sim = evaluator.evaluate(board_sim, p_hand) 
    p_class_sim = evaluator.class_to_string(evaluator.get_rank_class(p_score_sim)) 
    try:
        prob_river[p_class_sim] += 1

    except:
        prob_river[p_class_sim] = 1


# calculates probability for the hands
prob_turn.update((key, value /n) for key, value in prob_turn.items())
prob_turn_and_river.update((key, value /(n*(n-1))) for key, value in prob_turn_and_river.items())
prob_river.update((key, value /(n-1)) for key, value in prob_river.items())

print(r"Hands that are not displayed have 0% chance of ocurring.")
print()


print("2nd turn (Turn)")
print("Hand\tProbability (%)")
for k,v in prob_turn.items():
    print(k,v)
print()

print("2nd and 3rd turn (Turn and River)")
print("Hand\tProbability (%)")

for k,v in prob_turn_and_river.items():
    print(k,v)
print()

print("3rd turn (River) after drawing the 4th card")
print("Hand\tProbability (%)")

for k,v in prob_river.items():
    print(k,v)