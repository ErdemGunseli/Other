def process_hands():
    with open("Problem_Files/54_poker.txt") as f:
        hands_string = f.read()

        # This creates a 2D list with 10 cards in each sublist:
        hands = [cards.split(' ') for cards in hands_string.split('\n')]

        # This further divides each sublist into 2 lists, each list containing one player's cards:
        return [[ten_cards[:5], ten_cards[5:]] for ten_cards in hands]


def royal_flush(hand): pass


def straight_flush(hand): pass


def four_of_a_kind(hand): pass


def full_house(hand): pass


def flush(hand): pass


def straight(hand): pass


def three_of_a_kind(hand): pass


def two_pairs(hand): pass


def one_pair(hand): pass


# Returns True, removes the highest card and returns the remaining:
def high_card(hand): pass


# Returns a list of values for each card (number in front, converting T, J, Q, K, A to increasing numbers)
def get_card_values(hand): pass


def get_rank(hand):
    ranks = [royal_flush, straight_flush, four_of_a_kind, full_house,
             flush, straight, three_of_a_kind, two_pairs, one_pair, high_card]

    rank_count = len(ranks)

    for index, rank in enumerate(ranks):
        rank_valid, remaining_cards = rank(hand)
        remaining_card_values = get_card_values(remaining_cards)
        if rank_valid: return [rank_count - index, remaining_card_values]


set_of_hands = process_hands()

p1_win_count = 0
for hands in set_of_hands:
    h1 = hands[0]
    h2 = hands[1]

    # A 2D list of ranks and remaining card values for each player:
    ranks = [get_rank(hand) for hand in hands]

    if ranks[0][0] > ranks[1][0]:
        p1_win_count += 1

    # If the ranks of the hands are the same, comparing value the highest remaining card in each hand:
    elif ranks[0] == ranks[1]:

        p1_remaining_values = sorted(ranks[0][1])
        p2_remaining_values = sorted(ranks[1][1])


        # Create a loop that repeatedly compares and removes the last value (highest value)
        # from each list until the highest values are not the same:


    print(f"Player 1 has cards {h1} and Player 2 has cards {h2}. \n\n\n")
