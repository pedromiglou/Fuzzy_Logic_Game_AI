from treys import Card, Deck, Evaluator

# royal flush combinations as treys doesnt discriminate royal flush from straight flush
royal_flush= [[Card.new('Ts'),Card.new('Js'),Card.new('Qs'),Card.new('Ks'),Card.new('As')],
              [Card.new('Td'),Card.new('Jd'),Card.new('Qd'),Card.new('Kd'),Card.new('Ad')],
              [Card.new('Tc'),Card.new('Jc'),Card.new('Qc'),Card.new('Kc'),Card.new('Ac')],
              [Card.new('Th'),Card.new('Jh'),Card.new('Qh'),Card.new('Kh'),Card.new('Ah')]]


# initializes Deck and Evaluator
deck = Deck()
evaluator = Evaluator()

# number of draws
n = 52 # maximum draws
n_board = 3 # initial board draws
n_player = 2 #player draws
n = n - n_board - n_player #maximum draws after drawing board and player hand cards


# 1st turn
board = deck.draw(n_board)
p_hand = deck.draw(n_player)
deck = deck.draw(n) # draws remaining cards so its easier to access them

#prints current cards and cards available in the deck
Card.print_pretty_cards(board+p_hand)
Card.print_pretty_cards(deck)
print()


# computes ocurrences with only 4 cards in the board, 2nd turn
prob_2nd_turn = {}
for i in range(n):
    # draws a card to the board
    board_sim = board + [deck[i]]
    p_score_sim = evaluator.evaluate(board_sim, p_hand)
    p_class_sim = evaluator.class_to_string(evaluator.get_rank_class(p_score_sim))
    
    # verifies if the hand is a royal flush or not
    if sorted(board_sim + p_hand) in sorted(royal_flush):
        try:
            prob_2nd_turn['Royal Flush'] += 1
    
        except:
            prob_2nd_turn['Royal Flush'] = 1
    else:      
        try:
            prob_2nd_turn[p_class_sim] += 1
        
        except:
            prob_2nd_turn[p_class_sim] = 1

# computes ocurrences with 5 cards in the board, last turn
prob_3rd_turn = {}
for i in range(n):
    # draws a card to the board
    board_sim = board + [deck[i]]
    for j in range(n-1):
        # draws a 5th and final card to the board
        board_sim = board + [deck[j]]
        p_score_sim = evaluator.evaluate(board_sim, p_hand) 
        p_class_sim = evaluator.class_to_string(evaluator.get_rank_class(p_score_sim)) 
        
        # verifies if the hand is a royal flush or not
        if sorted(board_sim + p_hand) in sorted(royal_flush):
            try:
                prob_2nd_turn['Royal Flush'] += 1
        
            except:
                prob_2nd_turn['Royal Flush'] = 1
        else:
            try:
                prob_3rd_turn[p_class_sim] += 1
        
            except:
                prob_3rd_turn[p_class_sim] = 1

# calculates probability for the hands
prob_2nd_turn.update((key, value /n) for key, value in prob_2nd_turn.items())
prob_3rd_turn.update((key, value /(n*(n-1))) for key, value in prob_3rd_turn.items())

print(r"Hands that are not displayed have 0% chance of ocurring.")
print()


print("2nd turn (Turn)")
print("Hand\tProbability (%)")
for k,v in prob_2nd_turn.items():
    print(k,v)
print()

print("3rd/Last turn (River)")
print("Hand\tProbability (%)")
for k,v in prob_3rd_turn.items():
    print(k,v)