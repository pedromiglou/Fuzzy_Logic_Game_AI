from treys import Card, Deck, Evaluator
from itertools import combinations
def calcProb(hand: list = [], board: list = []):

    # convert treys class names to fuzzy inputs
    hand_dict = {'Royal Flush': 'probRF', 'Straight Flush': 'probSF', 
                 'Four of a Kind': 'probFK', 'Full House': 'probFH',
                 'Flush': 'probF', 'Straight': 'probS',
                 'Three of a Kind': 'probTK', 'Two Pair': 'probTP',
                 'Pair': 'probOP', 'High Card': 'probHC'
                 }

    # initializes Deck and Evaluator
    deck = Deck()
    evaluator = Evaluator()

    n = 52 #maximum number of draws
    deck = deck.draw(n) # draws all cards

    # if player and board hands are empty, create new
    if hand == [] and board == []:
        hand.append(deck.pop())
        hand.append(deck.pop())
        
        board.append(deck.pop())
        board.append(deck.pop())
        board.append(deck.pop())

    else:
        #hand = [Card.new(card) for card in hand]
        #board = [Card.new(card) for card in board]
            
        for card in hand:
            deck.remove(card)
            
        for card in board:
            deck.remove(card)

    # number of draws
    n_board = len(board) # initial board draws
    n_player = len(hand) #player draws

    n = n - n_board - n_player #maximum draws after drawing board and player hand cards

    # computes ocurrences with only 4 or 5 cards in the board, 2nd turn
    prob = {hand: 0 for hand in hand_dict.values()}
 
    if n_board == 5:
        score_sim = evaluator.evaluate(board, hand)
        class_sim = evaluator.class_to_string(evaluator.get_rank_class(score_sim))
        
        prob[hand_dict[class_sim]] += 1
    
    elif n_board==4:
        for i in range(n):
            # draws a card to the board
            board_sim = board + [deck[i]]
            score_sim = evaluator.evaluate(board_sim, hand)
            class_sim = evaluator.class_to_string(evaluator.get_rank_class(score_sim))
            
            prob[hand_dict[class_sim]] += 1
    
    else:
        for i in range(n):
            for j in range(n):
                if i==j:
                    continue
                # draws a card to the board
                board_sim = board + [deck[i]] + [deck[j]]
                score_sim = evaluator.evaluate(board_sim, hand)
                class_sim = evaluator.class_to_string(evaluator.get_rank_class(score_sim))
                
                prob[hand_dict[class_sim]] += 1
        
    prob.update((key, value /(n)*100) for key, value in prob.items())
    
    return prob
