"""Day 12: Hot Springs"""

import functools
import itertools as it
import re
import sys

@functools.cache
def count_permutations_string_based(sequence, damage_counts):
    """Count the permutations for a sequence

    This function takes in a sequence string and the counts of damaged springs
    in the sequence as a tuple. It then returns the number of arrangements of
    damaged springs that are possible.
    """
    counts = 0
    i = 0
    while i < len(sequence):
        # Get the count of damaged springs in the current group
        group_target = damage_counts[0]
        # Start a count of how many we've seen in the current group
        current_group = 0
        current_group_start = -1
        if sequence[i] == '.':
            # This does not count towards anything
            # Just advance to the next character
            i += 1
            continue
        if sequence[i] == '?':
            # We have some freedom to choose what will happen here
            # If there is nothing in this group so far, then assume this is
            # damaged
            if not current_group:
                # TODO: I believe this condition is always true
                current_group = 1
                current_group_start = i
                # Now we need to be able to expand this group until we hit the
                # target
                while current_group < group_target:
                    i += 1
                    if i == len(sequence):
                        # We've overshot the sequence length and failed
                        # This does not contribute to the count
                        # Reset and move on to the next character, ie., assume
                        # that the group start was an operational spring
                        # instead
                        i = current_group_start + 1
                        # Need to continue in the outer loop
                        # So break outof this inner loop
                        break
                    if sequence[i] == '.':
                        # Then we cannot expand the group
                        # We have failed: this arrangement does not work
                        # Reset and move on to the next character
                        i = current_group_start + 1
                        # Need to continue in the outer loop
                        # So break out of this inner loop
                        break
                    current_group += 1
                else:
                    # Now that we're here, we've been able to expand the group
                    # by the right amount
                    # Now we need to make sure it is separated from all the
                    # other groups
                    i += 1
                    if i < len(sequence) and sequence[i] == '#':
                        # We've failed again: this arrangement does not work
                        # Reset and move on to the next character
                        i = current_group_start + 1
                        continue  # this resets everything else
                    # If we've made it here then things seem to have worked so
                    # far
                    if len(damage_counts) == 1:
                        # This was the last group we needed to satisfy and
                        # we've made it to the end
                        # Now we just need to make sure that there are no more
                        # broken springs in the rest of the string and, if
                        # there aren't, then we can count this as a possible
                        # arrangement
                        if '#' in sequence[i+1:]:
                            # We've failed
                            i = current_group_start + 1
                        else:
                            # Count this as a possible arrangement
                            #TODO: Can this be changed to return 1?
                            counts += 1
                            # Now reset everything and check if the starting
                            # question mark could have been a good spring
                            i = current_group_start + 1
                            continue  # this resets everything else
                    else:
                        # Now we can recursively compute arrangements for the rest
                        # of the sequence
                        counts += count_permutations(
                                sequence[i+1:],
                                damage_counts[1:],
                                )
                        # Once we get to this point, we can go back to the start of
                        # the group and go down the other path - assume that it was
                        # an operational spring and look at what happens then
                        # To do this, we just need to reset a few counters
                        i = current_group_start + 1
                        continue  # this resets everything else
        elif sequence[i] == '#':
            # We don't have the freedom to choose what to do here
            # Start a new group here
            current_group = 1
            current_group_start = i
            # Expand the group until we hit the target
            while current_group < group_target:
                i += 1
                if i == len(sequence):
                    # We've overshot the sequence length and failed
                    return counts
                if sequence[i] == '.':
                    # Then we cannot expand the group
                    # We have failed: this arrangement does not work
                    return counts
                current_group += 1
            # Now that we're here, we've been able to expand the group by
            # the right amount
            # Now we need to make sure it is separated from all the other
            # groups
            i += 1
            if i < len(sequence) and sequence[i] == '#':
                # We've failed again: this arrangement does not work
                return counts
            if len(damage_counts) == 1:
                # This was the last group we needed to satisfy and we've
                # made it to the end
                # Now we just need to make sure that there are no more
                # broken springs in the rest of the string and, if
                # there aren't, then we can count this as a possible
                # arrangement
                if '#' in sequence[i+1:]:
                    # We've failed
                    return counts
                else:
                    # Count this as a possible arrangement
                    #TODO: Can this be changed to return 1?
                    counts += 1
                    return counts
            else:
                # Now we can recursively compute arrangements for the rest
                # of the sequence
                counts += count_permutations(
                        sequence[i+1:],
                        damage_counts[1:],
                        )
                # Once we get to this point, we can't go back to the start of
                # the group and assume that the operational spring we started
                # with is damaged
                # So return the counts here
                return counts
    return counts

def count_permutations_binary_based(sequence, damage_counts):
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

def total_permutations(sequences, damage_counts, folds=1):
    """Return the total permutations for all records

    This function accepts the sequences and corresponding damage counts. It
    then computes the number of possible arrangements for each record and
    returns the total number of arrangements across all the different records.

    This function also accepts an optional folds parameter that signifies how
    many times the records are folded over.
    """
    num_permutations = 0
    for sequence, counts in zip(sequences, damage_counts):
        sequence = '?'.join([sequence] * folds)
        counts = counts * folds
        num_permutations += count_permutations(sequence, counts)
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
    num_permutations = total_permutations(sequences, damage_counts, folds=1)
    print(f'Total number of permutations with 1 fold: {num_permutations}')
    num_permutations = total_permutations(sequences, damage_counts, folds=5)
    print(f'Total number of permutations with 5 folds: {num_permutations}')
    return sequences, damage_counts

if __name__ == "__main__":
    filename = sys.argv[1]
    method = sys.argv[2]
    match method:
        case 'binary':
            count_permutations = count_permutations_binary_based
        case 'string':
            count_permutations = count_permutations_string_based
        case default:
            raise ValueError(f'Unknown method "{method}"')
    sequences, damage_counts = main(filename)
