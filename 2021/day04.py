"""Day 4; Giant Squid

Figure out which bingo board wins and then compute the score if you choose that
board to defeat the giant squid!
"""

import numpy as np
import sys

def masks(shape, include_diagonals=False):
    """A generator to get all valid bingo masks."""
    rows, cols = shape
    mask = np.zeros(shape)
    # First check all the rows
    for i in range(rows):
        mask = np.zeros(shape)
        mask[i, :] = 1
        yield mask
    # Then check all columns
    for j in range(cols):
        mask = np.zeros(shape)
        mask[:, j] = 1
        yield mask
    if include_diagonals:
        # Check the diagonals if it is square
        mask = np.zeros(shape)
        np.fill_diagonal(mask, 1)
        yield mask
        mask = np.zeros(shape)
        np.fill_diagonal(np.fliplr(mask), 1)
        yield mask

def check_wins(marked_spots, mask):
    """Get the winning boards according to mask

    Each bingo board can win by either having a complete row or column. The
    winning conditions are represented by masks. This function checks if the
    board has won according to a specific mask.
    """
    # To check if any of the boards matches the mask, we need to check that all
    # the True spots on the mask are True on the board. To do this, we can just
    # logically 'and' them together. If the result is the mask, then that means
    # the conditions is true.
    result = np.logical_and(marked_spots, mask) == mask
    board_matches = np.all(result, axis=(1, 2))
    board_indices = np.argwhere(board_matches == True)
    if board_indices.size == 0:
        return []
    else:
        return board_indices.reshape(1).tolist()

def play_bingo(boards, numlist):
    """Check which bingo boards win with the numbers

    Given a list of numbers and some bingo boards, check which of them
    are complete.
    """
    # "MarK" all the spots that match any of the numbers in numlist. This will
    # create a copy of the boards with True wherever the the required numbers
    # are and False everywhere else.
    marked_spots = np.zeros(boards.shape, dtype=bool)
    for i, num in enumerate(numlist):
        marked_spots = marked_spots | (boards == num)
        # Now check if any of the boards have won by comparing against various masks
        for mask in masks(boards.shape[1:]):  # Get the shape of just one board
            winning_boards = check_wins(marked_spots, mask)
            if len(winning_boards) > 0:
                # There is a winning board!
                # Return the winning board indices with the marked number list
                return (winning_boards, numlist[:i+1])
    return []

def calculate_winning_board_score(board, marked_numbers):
    """Calculate the score of a winning board

    Given a board and the winning_mask, the score of the winning board
    is defined to be the product of the sum of all unmarked numbers on
    that board times the final number that was caused the board to win.
    """
    # Create a mask for where the numbers match the board
    mask = np.zeros(board.shape, dtype=bool)
    for num in marked_numbers:
        mask = mask | (board == num)
    # Flip the mask to get the unmarked spots
    mask = np.logical_not(mask)
    # Multiplying this by 1 should coerce it to integer
    mask = mask * 1
    # Now there are 0s in all the marked spots and 1s in the unmarked spots.
    # Multiply the mask into the board to 0 out the marked numbers and then
    # find their sum.
    board_sum = np.sum(board * mask)
    # The score is this times the last number
    return board_sum * marked_numbers[-1]

def load_data(filename):
    with open(filename, 'r') as datafile:
        data = datafile.read().splitlines()
    return data

def clean_data(data):
    # The first line of data is just a list of numbers
    numbers = data.pop(0)
    numbers = numbers.split(',')
    numbers = [int(num) for num in numbers]
    # Then there is a blank line separating every bingo board
    current_board = None
    board_list = []
    while len(data) > 0:
        line = data.pop(0)
        if line == '':
            # Blank line means we've found a complete board
            if current_board:
                board_list.append(current_board)
            current_board = []
            continue
        # Otherwise, clean and add this line to the current board
        line = [int(num) for num in line.split(' ') if num]
        current_board.append(line)
    # Make sure there aren't any unprocessed boards
    if current_board:
        board_list.append(current_board)
        current_board = []
    # Once we've got all the boards, convert the board list to a numpy array
    # for hopefully easier use later
    boards = np.array(board_list)
    return numbers, boards

def main(filename):
    data = load_data(filename)
    numlist, boards = clean_data(data)
    winning_board_indices, marked_numbers = play_bingo(boards, numlist)
    winning_score = calculate_winning_board_score(boards[winning_board_indices[0]], marked_numbers)
    print(f'Winning board score = {winning_score}')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
