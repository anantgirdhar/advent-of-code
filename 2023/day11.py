"""Day 11: Cosmic Expansion"""

import sys

def compute_total_pairwise_distances(galaxy_locations):
    """Return the total intergalactic distances

    This function accepts the locations of the galaxies and computes the
    shortests pairwise distances. It then returns the sum of all the computed
    distances.
    """
    distances = []
    for i, (g1x, g1y) in enumerate(galaxy_locations):
        for (g2x, g2y) in galaxy_locations[i+1:]:
            distances.append(abs(g1x-g2x) + abs(g1y-g2y))
    return sum(distances)

def locate_galaxies(image):
    """Return a list of locations of the galaxies

    This function accepts an image of the universe and returns a list of tuples
    describing the locations of the galaxies.
    """
    locations = []
    for i, row in enumerate(image):
        for j, character in enumerate(row):
            if character == '#':
                locations.append((i, j))
    return locations

def expand_universe(image):
    """Return the expanded universe

    This function accepts the image of the galaxies and returns the expanded
    universe. The rows and columns of the image that don't contain any galaxies
    expand and become double their width.
    """
    # First find the rows and columns that don't have any galaxies
    # Initialize: Assume that no row or column contains a galaxy and update
    # this guess whenever one is found
    rows_without_galaxies = list(range(len(image)))
    columns_without_galaxies = list(range(len(image[0])))
    for i, row in enumerate(image):
        for j, character in enumerate(row):
            if character == '#':
                # We found a galaxy in this row and column
                try:
                    columns_without_galaxies.remove(j)
                except ValueError:
                    # Already removed so don't need to do anything
                    pass
                try:
                    rows_without_galaxies.remove(i)
                except ValueError:
                    # Already removed so don't need to do anything
                    pass
    expanded_image = []
    # First expand the columns
    for row in image:
        row = list(row)
        # Make sure to reverse the list of column indices so that, as the
        # universe expands, we don't need to keep track of new column numbers
        for j in reversed(columns_without_galaxies):
            row.insert(j, '.')
        expanded_image.append(''.join(row))
    # Now expand the rows by adding rows at the appropriate indices
    empty_row = '.' * len(expanded_image[0])
    for i in reversed(rows_without_galaxies):
        expanded_image.insert(i, empty_row)
    return expanded_image

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    image = read_data(filename)
    image = expand_universe(image)
    galaxy_locations = locate_galaxies(image)
    total_distance = compute_total_pairwise_distances(galaxy_locations)
    print(f'Total of all pairwise distances: {total_distance}')
    return image

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
