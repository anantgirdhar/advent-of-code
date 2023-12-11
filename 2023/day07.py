"""Day 07: Camel Cards"""

import functools
import re
import sys

CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1']

# Define the types of hands as compiled regular expressions that can be used
# later
# I believe that some of these require the cards in the hand to be sorted but
# that may not really be true
PATTERNS = [
        FIVE_KIND := re.compile(r'(.)\1{4}'),
        FOUR_KIND := re.compile(r'(.)\1{3}'),
        FULL_HOUSE := re.compile(r'(.)\1(.)\2\2|(.)\3\3(.)\4'),
        THREE_KIND := re.compile(r'(.)\1\1'),
        TWO_PAIR := re.compile(r'.?(.)\1.?(.)\2.?'),
        ONE_PAIR := re.compile(r'(.)\1'),
]

def get_hand_type(hand):
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
    # Sort the cards
    cards = ''.join(sorted(hand))
    # Now check against the patterns
    for i, pattern in enumerate(PATTERNS):
        if re.search(pattern, cards):
            return len(PATTERNS) - i
    # If nothing matches, we just have a high card
    return 0

def compare_hands(h1, h2):
    """Compare two hands

    This function takes in two hands (as strings) and compares them. It returns
    -1 if h1 has smaller rank, 0 if they are equal, and 1 if h1 has larger
    rank. Note that a smaller rank means a weaker hand.

    Ties are broken by comparing the first card in the hand and the lower card
    has lower rank.
    """
    # First check what type each hand is
    # To do this, sort the cards in the hand first
    h1_type = get_hand_type(h1)
    h2_type = get_hand_type(h2)
    if h1_type < h2_type:
        return -1
    elif h1_type > h2_type:
        return 1
    # Otherwise, the types are he same so we need to compare the individual cards
    for card1, card2 in zip(h1, h2):
        if CARDS.index(card1) > CARDS.index(card2):
            # If the first card has higher index, it is a worse card and so has a
            # lower rank
            return -1
        elif CARDS.index(card1) < CARDS.index(card2):
            return 1
    # If all of that compares equal, then they're the same hand
    return 0

def compute_winnings(hands, bids):
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
        return compare_hands(bid1[1], bid2[1])
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
    winnings = compute_winnings(hands, bids)
    print(f'The winnings are: {winnings}')
    return hands, bids

if __name__ == "__main__":
    filename = sys.argv[1]
    hands, bids = main(filename)
