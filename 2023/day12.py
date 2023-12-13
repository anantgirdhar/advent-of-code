"""Day 12: Hot Springs"""

import itertools as it
import re
import sys
import pdb

def count_permutations(sequence, damage_counts):
    """Count the permutations for a sequence

    This function takes in a sequence string and the counts of damaged springs
    in the sequence as a tuple. It then returns the number of arrangements of
    damaged springs that are possible.
    """
    # Create a regular expression that satisifies the damage counts
    pattern_string = []
    for num_damages in damage_counts:
        if num_damages > 1:
            pattern_string.append('#{' + str(num_damages) + '}')
        else:
            pattern_string.append('#')
    # Join each sequence of #'s with at least one .
    pattern_string = r'\.+'.join(pattern_string)
    # Then make sure that this is surrounded by dots or the string boundary
    pattern_string = r'^\.*' + pattern_string + r'\.*$'
    pattern = re.compile(pattern_string)
    # Create a counter to keep track of the counts
    counts = 0
    # Also create a counter to keep track of how many #'s are already in the
    # sequence and, therefore, how many more we'll need
    num_present_damages = 0
    num_needed_damages = 0
    # First convert the sequence to its binary representation
    # Convert all #'s to 1's, all .'s to 0's
    # Represent the ?'s as the "basis" that can be used to generate the set of
    # all achievable values by changing the ?'s to #'s and .'s
    base_sequence_value = ''
    question_values = []
    for i, c in enumerate(sequence):
        # i is the length along the series but we want what binary power this
        # digit corresponds to
        n = len(sequence) - i - 1
        if c == '?':
            question_values.append(2**n)
            base_sequence_value += '0'
        elif c == '#':
            base_sequence_value += '1'
            num_present_damages += 1
        elif c == '.':
            base_sequence_value += '0'
    # Convert it to an actual integer
    base_sequence_value = int(base_sequence_value, 2)
    # Now figure out how many more #'s we need
    num_needed_damages = sum(damage_counts) - num_present_damages
    # Now check if every variation of the ?'s yields a valid sequence
    # for sequence_addition in it.chain.from_iterable(it.combinations(question_values, r) for r in range(len(question_values)+1)):
    for sequence_addition in it.combinations(question_values, num_needed_damages):
        test_sequence = base_sequence_value + sum(sequence_addition)
        # Convert this back to its string representation
        test_sequence_string = ''
        for c in format(test_sequence, '#0' + str(len(sequence)+2) + 'b')[2:]:
            if c == '0':
                test_sequence_string += '.'
            else:
                test_sequence_string += '#'
        # Now check if this satisfies the damage counts
        if re.match(pattern, test_sequence_string):
            counts += 1
    return counts

def total_permutations(sequences, damage_counts):
    """Return the total permutations for all records

    This function accepts the sequences and corresponding damage counts. It
    then computes the number of possible arrangements for each record and
    returns the total number of arrangements across all the different records.
    """
    num_permutations = 0
    for sequence, damage_counts in zip(sequences, damage_counts):
        num_permutations += (count := count_permutations(sequence, damage_counts))
    return num_permutations

def parse_data(data):
    """Parse the data to make it usable"""
    sequences = []
    damage_counts = []
    for line in data:
        record, counts = line.split(' ')
        sequences.append(record)
        damage_counts.append(tuple(int(n) for n in counts.split(',')))
    return sequences, damage_counts

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    sequences, damage_counts = parse_data(data)
    num_permutations = total_permutations(sequences, damage_counts)
    print(f'Total number of permutations: {num_permutations}')
    return sequences, damage_counts

if __name__ == "__main__":
    filename = sys.argv[1]
    sequences, damage_counts = main(filename)
