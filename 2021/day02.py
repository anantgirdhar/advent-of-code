"""Day 2: Dive!

Compute the horizontal and vertical position of the submarine given a
sequence of commands.
"""

import numpy as np
import sys

def move_old(commands, starting_position=(0, 0)):
    """Find the new position using the old algorithm

    The positon is measured as a horizontal distance and a depth, i.e.,
    the depth increases as you go down.
    """
    x, y = starting_position
    for command in commands:
        direction, amount = command.split(' ')
        amount = int(amount)
        match direction:
            case 'forward':
                x += amount
            case 'down':
                y += amount
            case 'up':
                y -= amount
    return x, y

def move_new(commands, start_position=(0, 0, 0)):
    """Find the new position using the new algorithm

    The position is still measured as a horizontal distance and a depth,
    i.e., the depth increases as you go down. We also have a third
    "coordinate" now called the "aim". Here is what the commands do
    under the new algorithm:

    1. 'down X' increases the aim by X units
    2. 'up X' decreases the aim by X units
    3. 'forward X' does two things:
        - It increases the horizontal position by X
        - It increases the depth by aim * X
    """
    x, y, aim = start_position
    for command in commands:
        direction, amount = command.split(' ')
        amount = int(amount)
        match direction:
            case 'forward':
                x += amount
                y += aim * amount
            case 'down':
                aim += amount
            case 'up':
                aim -= amount
    return x, y

def main(filename):
    with open(filename, 'r') as datafile:
        commands = datafile.read().splitlines()
    # Find the new position under the old agorithm
    x, y = move_old(commands)
    print(f'New position = {x}, {y}')
    print(f'Product of coordinates = {x * y}')
    # Find the new position under the new algorithm
    x, y = move_new(commands)
    print(f'New position = {x}, {y}')
    print(f'Product of coordinates = {x * y}')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
