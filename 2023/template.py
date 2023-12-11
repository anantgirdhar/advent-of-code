"""Day <++>"""

import sys

def parse_data(data):
    """Parse the data to make it usable"""
    <++>

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    <++> = parse_data(data)
    return data

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
