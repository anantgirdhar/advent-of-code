"""Day 15: Lens Library"""

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
    return data

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
