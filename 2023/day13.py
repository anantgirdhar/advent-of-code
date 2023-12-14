"""Day 13: Point of Incidence"""

import sys

import numpy as np

def find_vertical_mirror(pattern):
    """Return the location of a vertical mirror

    This function accepts a pattern of ash and rocks (as a np.chararray) and
    returns the location of a vertical mirror. The location returned is the
    number of columns preceeding the mirror. If no mirror is found, it returns
    None.
    """
    # Find the number of rows and columns in this pattern
    _, C = pattern.shape
    for i in range(C-1):
        if np.all(pattern[:, i] == pattern[:, i + 1]):
            # If two adjacent rows are the same, there is a mirror between
            # them if all rows moving outwards are also the same
            for j in range(i - 1, -1, -1):
                if i + (i - j) + 1 == C:
                    # We've reached the right boundary and confirmed the mirror
                    return i + 1
                if not np.all(pattern[:, j] == pattern[:, i + (i - j) + 1]):
                    # This is not a mirror
                    break
            else:
                return i + 1
    # No mirror found
    return None

def find_horizontal_mirror(pattern):
    """Return the location of a horizontal mirror

    This function accepts a pattern of ash and rocks (as a np.chararray) and
    returns the location of a horizontal mirror. The location returned is the
    number of columns preceeding the mirror. If no mirror is found, it returns
    None.
    """
    # Find the number of rows and columns in this pattern
    R, _ = pattern.shape
    for i in range(R-1):
        if np.all(pattern[i, :] == pattern[i + 1, :]):
            # If two adjacent rows are the same, there is a mirror between
            # them if all rows moving outwards are also the same
            for j in range(i - 1, -1, -1):
                if i + (i - j) + 1 == R:
                    # We've reached the lower boundary and confirmed the mirror
                    return i + 1
                elif not np.all(pattern[j, :] == pattern[i + (i - j) + 1, :]):
                    # This is not a mirror
                    break
            else:
                return i + 1
    # No mirror found
    return None

def summarize(maps):
    """Return a summarized value of all the maps

    This function accepts a list of maps and returns a "summarized" value that
    describes this combination of maps. This function finds the location of the
    mirror in every map and then uses these location values to compute the
    "summary number".
    """
    summary_number = 0
    for pattern in maps:
        if (location := find_horizontal_mirror(pattern)):
            summary_number += 100 * location
        else:
            location = find_vertical_mirror(pattern)
            summary_number += location
    return summary_number

def parse_data(data):
    """Parse the data to make it usable"""
    # Convert the maps to np.chararray's so that it's easier to slice in each
    # direction
    maps = []
    current_map = []
    for line in data:
        if not line:
            # We've finished the map
            maps.append(np.char.asarray(current_map))
            current_map = []
            continue
        # Turn the current line into a list of characters
        current_map.append(list(line))
    # Add the last map to the list of maps
    maps.append(np.char.asarray(current_map))
    return maps

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    maps = parse_data(data)
    summary_number = summarize(maps)
    print(f'Summary number: {summary_number}')
    return maps

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
