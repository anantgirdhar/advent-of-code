"""Day 08: Haunted Wasteland"""

import re
import sys

def navigate(directions, maze):
    """Navigate through the maze

    This function takes in the list of directions and a dict describing the
    maze. The list of directions is a sequence of 0s and 1s representing left
    and right turns. Only these turns in the given order can be used to solve
    the maze. The maze dict itself is a mapping from nodes to tuples of nodes.
    The tuple represents the destination nodes after taking left and right
    turns respectively from the source node.

    This function then returns the number of steps required to reach the
    destination node (ZZZ) starting at the source node (AAA). 
    """
    # Start at node AAA
    current_node = 'AAA'
    num_steps = 0
    # Now we keep going until we get to ZZZ
    # Note the directions list is finite but, if it runs out, we need to jump
    # back to the start of that list
    while True:
        for direction in directions:
            current_node = maze[current_node][direction]
            num_steps += 1
            if current_node == 'ZZZ':
                break
        if current_node == 'ZZZ':
            break
    return num_steps

def parse_data(data):
    """Parse the data to make it usable"""
    directions = None
    mapping = {}
    # Define the structure of the mapping line as a compiled RE
    # This will capture the three values which can be referred to
    map_line_pattern = re.compile(r'(\w{3})\s*=\s*\((\w{3}), (\w{3})\)')
    for line in data:
        if not line:
            # If the line is empty, skip it
            continue
        elif directions is None:
            directions = line
            # Change the directions to be 0 for left and 1 for right
            directions = directions.replace('L', '0')
            directions = directions.replace('R', '1')
            # Now split it so that it forms a list
            directions = [int(d) for d in list(directions)]
        else:
            # This is part of the maze map so save it as a map with the source
            # node as the key and the destinations as a tuple of values with
            # the 0th element being the left destination and the 1th element
            # being the right destination
            match = re.match(map_line_pattern, line)
            mapping[match.group(1)] = (match.group(2), match.group(3))
    return directions, mapping

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    directions, mapping = parse_data(data)
    num_steps = navigate(directions, mapping)
    print(f'Number of steps to reach destination: {num_steps}')
    return directions, mapping

if __name__ == "__main__":
    filename = sys.argv[1]
    directions, mapping = main(filename)
