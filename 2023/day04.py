"""Day 04: Scratchcards"""

import re
import sys

def count_number_of_wins(card):
    """Count how many wins are on this card

    This function takes in a card's details and computes how many wins there
    are. The card details are a list-like that contains the card number, the
    winning numbers, and the actual numbers.
    """
    num_winning_nums = 0
    # Get a list of the winning numbers on the card
    # Remember that these are space separated
    for winning_number in card[1].strip().split(' '):
        if not winning_number:
            # if the string is empty, just skip over it
            continue
        # Check if the winning number is in the actual numbers
        # We need to make sure winning_number is found exactly in the actual
        # list of numbers. This means ensuring that the value found in the
        # actual list of numbers is either separated from the other numbers by
        # spaces or is at the start / end of the list of numbers (where it may
        # not have a space next to it).
        if re.search(r'(\D|^)' + winning_number + r'(\D|$)', card[2]):
            num_winning_nums += 1
    return num_winning_nums

def compute_number_of_scratchcards(cards):
    """Compute the number of scratchcards won

    This function takes in a list of lines representing the scratchcards and
    computes how many total scratchcards are won (based on the rules given
    behind each scratchcard). It then returns a list of how many of each
    scratchcard were won.
    """
    # Start with 1 copy of every card (the original)
    num_cards = [1, ] * len(cards)
    # Idea: check how many wins each card produces and increment the count of
    # the appropriate number of following cards
    for i, card in enumerate(cards):
        num_wins = count_number_of_wins(card)
        num_cards_added = num_cards[i]
        for j in range(i + 1, i + 1 + num_wins):
            num_cards[j] += num_cards_added
    return num_cards

def compute_points(cards):
    """Compute points for each scratchcard

    This function takes in a list of lines representing the scratchcards and
    computes how many winning numbers appear in each scratchcard. It then
    computes the corresponding points based on the number of wins and returns
    that as a list.
    """
    num_wins = [count_number_of_wins(card) for card in cards]
    return [2**(n-1) if n > 0 else 0 for n in num_wins]

def parse_data(data):
    """Parse the data to make it usable"""
    cards = []
    while data:
        card = data.pop(0)
        # Split out the card number from the rest of the card
        card_number, card = card.split(':')
        # Clean up the card number
        card_number = int(card_number.split(' ')[-1])
        # Now get the winning_numbers and the actual numbers
        # These two parts are separated by a pipe and the each of the
        # individual numbers are space separated
        winning_numbers, actual_numbers = card.split('|')
        cards.append((card_number, winning_numbers.strip(), actual_numbers.strip()))
    return cards

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    cards = read_data(filename)
    cards = parse_data(cards)
    points = compute_points(cards)
    print(f'Total points: {sum(points)}')
    num_cards = compute_number_of_scratchcards(cards)
    print(f'Total cards: {sum(num_cards)}')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
