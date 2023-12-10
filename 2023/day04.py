"""Day 04: Scratchcards"""

import sys

def compute_number_of_wins(cards):
    """Compute number of wins for each scratchcard

    This function takes in a list of lines representing the scratchcards and
    computes how many winning numbers appear in each scratchcard. It then
    returns this as a list.
    """
    num_wins = []
    for card in cards:
        # Split on the colon to get just the numbers and then split the card
        # into the two parts on it - the winning numbers and the actual numbers
        card = card.split(':')[1].split('|')
        # Now create a list of the numbers on the scratchcard first
        # These are the numbers after the pipe symbol and are space separated
        nums = card[-1].strip().split(' ')
        # Convert to integers after removing any surrounding whitespace
        nums = [int(n.strip()) for n in nums if n]
        # Initialize the number of wins on this card
        num_wins.append(0)
        # Now check if any of the winning numbers are on this card
        # These are also space separated
        for winning_number in card[0].strip().split(' '):
            if not winning_number:
                # If the string is empty, just skip over it
                continue
            winning_number = int(winning_number.strip())
            if winning_number in nums:
                num_wins[-1] += 1
    return num_wins

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    num_wins = compute_number_of_wins(data)
    print(f'Total points: {sum(2**(n-1) if n > 0 else 0 for n in num_wins)}')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
