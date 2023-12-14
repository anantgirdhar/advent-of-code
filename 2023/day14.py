"""Day 14: Parabolic Reflector Dish"""

import sys

def compute_total_load(platform):
    """Return the total load on the platform

    This function accepts the distribution of rocks on the platform and
    computes the total load. This is represented as a list of strings. It
    assumes that the platform is tilted so that the rocks roll as far west as
    they can.
    """
    # The load of a rock is given by its distance from the eastern edge
    # So the max load is the number of columns in the grid
    # It might be easier to go over the characters in reverse order
    total_load = 0
    for line in platform:
        # Create a list of loads for rocks on the line
        line_loads = []
        for i, char in enumerate(reversed(list(line))):
            match char:
                case '#':
                    # We've reached an immovable rock
                    # Add all the loads found so far to the total_load and
                    # start tracking line_loads again
                    total_load += sum(line_loads)
                    line_loads = []
                case 'O':
                    # This is a movable rock
                    # Give it a load in the list
                    # Add a 1 because python indexing starts at 0 not 1
                    line_loads.append(i + 1)
                case '.':
                    # Update the loads of all rocks by adding one to each rock in the
                    # list - this accounts for them being able to roll westward
                    line_loads = [n + 1 for n in line_loads]
        # If there are any loads that made it all the way to the west end, add
        # them to the total_loads
        total_load += sum(line_loads)
    return total_load

def parse_data(data):
    """Parse the data to make it usable"""
    # Since the rocks can roll north and south, instead of storing the rock
    # positions row-wise, it might make more sense to store everything
    # column-wise, ie., transpose the data
    platform = [''] * len(data[0])
    for line in data:
        for i, char in enumerate(list(line)):
            platform[i] += char
    return platform

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    platform = parse_data(data)
    total_load = compute_total_load(platform)
    print(f'Total load: {total_load}')
    return platform

if __name__ == "__main__":
    filename = sys.argv[1]
    platform = main(filename)
