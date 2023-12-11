"""Day 07: Camel Cards"""

import functools
import re
import sys

def get_card_value(card, jokers):
    """Return the value of a card

    This function takes in a card and returns its value. It also accepts an
    optional argument to indicate whether or not jokers are used. Jokers have
    the lowest value among any card.
    """
    match card:
        case 'A':
            return 14
        case 'K':
            return 13
        case 'Q':
            return 12
        case 'J' if jokers:
            return 1
        case 'J':
            return 11
        case 'T':
            return 10
        case other:
            return int(card)

def get_hand_type(hand, jokers):
    """Get the type of a hand

    This function returns the type of a hand as a number. There are five types
    of hands:
    - Five of a kind (6)
    - Four of a kind (5)
    - Full house (4)
    - Three of a kind (3)
    - Two pair (2)
    - One pair (1)
    - High card (0)
    """
    # Define the types of hands as compiled regular expressions that can be used
    # later
    # These do require the cards to be listed in value order
    PATTERNS = [
            FIVE_KIND := re.compile(r'(.)\1{4}'),
            FOUR_KIND := re.compile(r'(.)\1{3}'),
            FULL_HOUSE := re.compile(r'(.)\1(.)\2\2|(.)\3\3(.)\4'),
            THREE_KIND := re.compile(r'(.)\1\1'),
            TWO_PAIR := re.compile(r'.?(.)\1.?(.)\2.?'),
            ONE_PAIR := re.compile(r'(.)\1'),
    ]
    PATTERNS_WITH_JOKERS = [
            FIVE_KIND_WITH_JOKERS:= re.compile(r'(.)\1\1\1\1|J(.)\2\2\2|JJ(.)\3\3|JJJ(.)\4|JJJJ'),
            FOUR_KIND_WITH_JOKERS:= re.compile(r'(.)\1{3}|J.*(.)\2{2}|JJ.*(.)\3|JJJ'),
            FULL_HOUSE_WITH_JOKERS:= re.compile(r'(.)\1(.)\2\2|(.)\3\3(.)\4|J(.)\5(.)\6|JJ(.)(.)\7|JJ(.)\8(.)'),
            THREE_KIND_WITH_JOKERS:= re.compile(r'(.)\1\1|J.*(.)\2|JJ'),
            TWO_PAIR_WITH_JOKERS:= re.compile(r'.?(.)\1.?(.)\2.?|J.*(.)\3'),
            ONE_PAIR_WITH_JOKERS:= re.compile(r'(.)\1|J'),
    ]
    # Sort the cards
    cards = ''.join(sorted(hand, key=lambda x: get_card_value(x, jokers)))
    # Now check against the patterns
    for i, pattern in enumerate(PATTERNS_WITH_JOKERS if jokers else PATTERNS):
        if re.search(pattern, cards):
            return len(PATTERNS) - i
    # If nothing matches, we just have a high card
    return 0

def compare_hands(h1, h2, jokers):
    """Compare two hands

    This function takes in two hands (as strings) and compares them. It returns
    -1 if h1 has smaller rank, 0 if they are equal, and 1 if h1 has larger
    rank. Note that a smaller rank means a weaker hand.

    Ties are broken by comparing the first card in the hand and the lower card
    has lower rank.
    """
    # First check what type each hand is
    # To do this, sort the cards in the hand first
    h1_type = get_hand_type(h1, jokers=jokers)
    h2_type = get_hand_type(h2, jokers=jokers)
    if h1_type < h2_type:
        return -1
    elif h1_type > h2_type:
        return 1
    # Otherwise, the types are he same so we need to compare the individual cards
    for card1, card2 in zip(h1, h2):
        card1_value = get_card_value(card1, jokers)
        card2_value = get_card_value(card2, jokers)
        if card1_value < card2_value:
            # If the first card has higher index, it is a worse card and so has a
            # lower rank
            return -1
        elif card1_value > card2_value:
            return 1
    # If all of that compares equal, then they're the same hand
    return 0

def compute_winnings(hands, bids, jokers):
    """Compute the winnings from all hands

    This function takes a list of hands and ranks them. It then computes the
    winnings by multiplying each hand's bid with it's rank.
    """
    # Not sure if there is a better way of doing this but I got a little tired
    # trying to figure out if there was a better way and I couldn't get
    # compare_hands() to work in the key argument to sorted when it was just
    # applied to the list of bids
    def _compare_bids_using_hands(bid1, bid2):
        """Compare two bids using their hands

        This function takes in two bids. Each bid is a tuple that contains the
        bid amount and the hand that it was bid on. It then "sorts" them in
        based on the hands.
        """
        return compare_hands(bid1[1], bid2[1], jokers=jokers)
    sorted_bids, _ = zip(*sorted(
        zip(bids, hands),
        key=functools.cmp_to_key(_compare_bids_using_hands)
        ))
    # Now compute the winnings by multiplying the bids by the rank
    # In this case, since we have a sorted list of bids in increasing order by
    # rank, the rank is just the index of the bid + 1 (because the list starts
    # at index 0)
    return sum((i + 1) * bid for i, bid in enumerate(sorted_bids))

def parse_data(data):
    """Parse the data to make it usable"""
    hands = []
    bids = []
    for line in data:
        hand, bid = line.split(' ')
        hands.append(hand)
        bids.append(int(bid))
    return hands, bids

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    hands, bids = parse_data(data)
    winnings = compute_winnings(hands, bids, jokers=False)
    print(f'The winnings without jokers are: {winnings}')
    winnings = compute_winnings(hands, bids, jokers=True)
    print(f'The winnings with jokers are: {winnings}')
    return hands, bids

if __name__ == "__main__":
    filename = sys.argv[1]
    hands, bids = main(filename)
