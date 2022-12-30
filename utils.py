from treys import Card, Deck, Evaluator

def handQuality(cards: list = []):
    # initializes Evaluator
    evaluator = Evaluator()

    # initializes dict to register ocurrences of each hand
    probs = {hand: 0 for hand in ['Royal Flush', 'Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card','counter']}
 
    probs = handQualityHelper(cards, probs, evaluator)
        
    probs.update((key, value/probs["counter"]*100) for key, value in probs.items())
    
    return probs


def handQualityHelper(cards: list, probs: dict, evaluator):
    if len(cards)==7:
        score_sim = evaluator.evaluate(cards[:5], cards[5:])
        class_sim = evaluator.class_to_string(evaluator.get_rank_class(score_sim))
        probs[class_sim] += 1
        probs["counter"] += 1
        return probs
    
    else:
        deck = Deck()
        deck = deck.draw(52)

        for card in cards:
            deck.remove(card)

        for i in range(52-len(cards)):
            probs = handQualityHelper(cards+[deck[i]], probs, evaluator)
        
        return probs


def boardQuality(board: list = []):
    # 5 - Royal Flush, Straight Flush (2)
    # 4 - 4-of-a-kind, Full House, Flush, Straight (4)
    # 3 - 3-of-a-kind, 2 pairs (2)
    # 2 - High pair, or highest card (2)
    # 1 - just noise

    probs = handQuality(board)

    if probs['Royal Flush'] != 0 or probs['Straight Flush'] != 0:
        return 5
    elif probs['Four of a Kind']!=0 or probs['Full House']!=0 or probs['Flush']!=0 or probs['Straight']!=0:
        return 4
    elif probs['Three of a Kind'] != 0 or probs['Two Pair'] != 0:
        return 3

    board = [Card.int_to_pretty_str(x)[1] for x in board]

    for i in range(len(board)):
        if board[i] == "A":
            board[i] = 14
        elif board[i] == "T":
            board[i] = 10
        elif board[i] == "J":
            board[i] = 11
        elif board[i] == "Q":
            board[i] = 12
        elif board[i] == "K":
            board[i] = 13
        else:
            board[i] = int(board[i][0])

    sum_board = 0
    for i in range(len(board)):
        sum_board += board[i]
    
    if sum_board > 7*len(board):
        return 2
    
    else:
        return 1