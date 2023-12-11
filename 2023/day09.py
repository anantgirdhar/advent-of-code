"""Day 09: Mirage Maintenance"""

import sys

import numpy as np

def find_next_element(sequence):
    """Find the next element of the sequence

    This function accepts a list of numbers and finds the next number in the
    sequence. The sequences are, in some sense, a generalization of an
    arithmetic sequence. For the sequence, generate the sequence of differences
    and continue this process recursively until the differences are all 0s.
    Then use the generated sequences to recursively build back up to the
    original sequence to find the next term. This function returns the next
    element of the sequence as an integer.
    """
    # When we recursively find the differences, at some point, we'll get to a
    # sequence where all the elements contain the same value. We can stop at
    # this point. Then to find the next element, we need to recursively add
    # each calculated difference on the way back up the chain. This is
    # equivalent to computing the sum of the last elements of each sequence of
    # differences
    # Initialize the difference and the next element
    diff = sequence
    next_element = 0
    # Also if each value of the sequence is the same, we're done
    while not np.all(diff == diff[0]):
        # The sequence is still changing
        # Add the ending value to the next_element calculation
        # This just keeps the backward step going as we're going down the chain
        # instead of having to do it as a separate step on the way back up and
        # keep all the differences in memory
        next_element += diff[-1]
        # Now, find the next difference
        diff = np.diff(diff)
    # Now all the values in diff are the same
    # Add the last value to give the value of the next_element
    return next_element + diff[-1]

def sum_extrapolated_values(sequences):
    """Compute the sum of the extrapolated values

    This function takes in a list of sequences and finds the next values that
    should appear in these sequences. It then returns the sum of all the
    extrapolated values.
    """
    return sum([find_next_element(seq) for seq in sequences])

def parse_data(data):
    """Parse the data to make it usable"""
    sequences = []
    for line in data:
        sequences.append([int(n) for n in line.split(' ')])
    return sequences

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    sequences = parse_data(data)
    target_value = sum_extrapolated_values(sequences)
    print(f'Sum of all extrapolated values: {target_value}')
    return sequences

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
