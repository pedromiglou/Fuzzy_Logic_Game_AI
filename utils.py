from treys import Card, Deck, Evaluator


def hand_quality(cards: list = []):
    # initializes Evaluator
    evaluator = Evaluator()

    # initializes dict to register ocurrences of each hand
    probs = {
        hand: 0
        for hand in [
            "Royal Flush",
            "Straight Flush",
            "Four of a Kind",
            "Full House",
            "Flush",
            "Straight",
            "Three of a Kind",
            "Two Pair",
            "Pair",
            "High Card",
            "counter",
        ]
    }

    probs = hand_quality_helper(cards, probs, evaluator)

    probs.update((key, value / probs["counter"] * 100) for key, value in probs.items())

    return probs


def hand_quality_helper(cards: list, probs: dict, evaluator):
    if len(cards) == 7:
        score_sim = evaluator.evaluate(cards[:5], cards[5:])
        class_sim = evaluator.class_to_string(evaluator.get_rank_class(score_sim))
        
        add = False
        for hand_type in ['Royal Flush', 'Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card']:
            if hand_type==class_sim:
                add = True
            
            if add:
                probs[class_sim] += 1
        
        probs["counter"] += 1
        return probs
    else:
        deck = Deck()
        deck = deck.draw(52)

        for card in cards:
            deck.remove(card)

        for i in range(52 - len(cards)):
            probs = hand_quality_helper(cards + [deck[i]], probs, evaluator)

    return probs


def board_quality(board: list = []):
    # 5 - Royal Flush, Straight Flush (2)
    # 4 - 4-of-a-kind, Full House, Flush, Straight (4)
    # 3 - 3-of-a-kind, 2 pairs (2)
    # 2 - High pair, or highest card (2)
    # 1 - just noise

    probs = hand_quality(board)

    if probs["Royal Flush"] != 0 or probs["Straight Flush"] != 0:
        return 5
    elif (
        probs["Four of a Kind"] != 0
        or probs["Full House"] != 0
        or probs["Flush"] != 0
        or probs["Straight"] != 0
    ):
        return 4
    elif probs["Three of a Kind"] != 0 or probs["Two Pair"] != 0:
        return 3

    board = [Card.int_to_pretty_str(x)[1] for x in board]

    for i, board_i in enumerate(board):
        if board_i == "A":
            board[i] = 14
        elif board_i == "T":
            board[i] = 10
        elif board_i == "J":
            board[i] = 11
        elif board_i == "Q":
            board[i] = 12
        elif board_i == "K":
            board[i] = 13
        else:
            board[i] = int(board[i][0])

    sum_board = sum(board)
    return 2 if sum_board > 7 * len(board) else 1
