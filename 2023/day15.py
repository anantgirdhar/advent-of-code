"""Day 15: Lens Library"""

from collections import OrderedDict
import sys

def get_hash(string):
    """Return the HASH of a string

    This function accepts a string and returns its HASH as an integer.
    """
    hash_value = 0
    for char in string:
        hash_value += ord(char)
        hash_value *= 17
        hash_value %= 256
    return hash_value

def get_total_hash(strings):
    """Return the total hash value of all strings

    This function accepts a list of strings and returns the sum of their hash
    values.
    """
    return sum([get_hash(string) for string in strings])

def remove_lens(lenses, label):
    """Remove a lens and return the new state

    This function accepts the state of the lenses, removes the lens with the
    given label, if it is present, and returns the new state of the lens
    sequence
    """
    box = get_hash(label)
    if not box in lenses:
        # The box is not present so we don't have to remove anything
        return lenses
    if label not in lenses[box]:
        # The lens is not in the box so we don't have to remove anything
        return lenses
    # Remove the lens
    del lenses[box][label]
    if len(lenses[box]) == 0:
        # If the box is empty, remove it
        del lenses[box]
    return lenses

def add_lens(lenses, label, power):
    """Add a lens and return the new state

    This function accepts the state of the lenses, adds the lens with the given
    label, and returns the new state of the lens sequence. If a lens with that
    label is already present, this function just updates the power of that
    lens.
    """
    box = get_hash(label)
    if not box in lenses:
        # Add the box to the sequence of lenses
        lenses[box] = OrderedDict()
    # Add or update the power
    lenses[box][label] = power
    return lenses

def hashmap(initialization_sequence):
    """Return final state after installing lenses

    This function accepts the initialization sequence as a list of strings. It
    then runs the HASHMAP algorithm and returns the final state of the boxes as
    a dict of OrderedDict's.
    """
    lenses = {}
    for step in initialization_sequence:
        if '-' in step:
            lenses = remove_lens(lenses, step[:-1])
        elif '=' in step:
            lenses = add_lens(lenses, step[:-2], int(step[-1]))
    return lenses

def compute_focussing_power(lens_sequence):
    """Return the total focussing power

    This function accepts a lens sequence as a dict of OrderedDict's and returns
    the total focusing power of the lens configuration.
    """
    total_power = 0
    for box in lens_sequence.keys():
        for slot, (lens, power) in enumerate(lens_sequence[box].items(), start=1):
            total_power += (box + 1) * slot * power
    return total_power

def parse_data(data):
    """Parse the data to make it usable"""
    return data.split(',')

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()[0]  # There is only one input line
    return data

def main(filename):
    data = read_data(filename)
    data = parse_data(data)
    total_hash = get_total_hash(data)
    print(f'Total hash value: {total_hash}')
    lens_sequence = hashmap(data)
    total_power = compute_focussing_power(lens_sequence)
    print(f'Total power of lens sequence after HASHMAP: {total_power}')
    return data

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
