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

def expand_galaxy_locations(galaxy_locations, num_rows, num_cols):
    """Return expanded galactic locations

    This function accepts the locations of the galaxies and returns their new
    locations after the universe has expanded.
    """
    # First find the rows and columns that don't have galaxies
    # These can be identified as the row and column numbers that do not appear
    # in any of the galaxy locations
    rows_without_galaxies = list(range(num_rows))
    columns_without_galaxies = list(range(num_cols))
    galaxy_rows, galaxy_columns = zip(*galaxy_locations)
    # Remove all the galaxy rows and columns now
    for row in set(galaxy_rows):
        rows_without_galaxies.remove(row)
    for column in set(galaxy_columns):
        columns_without_galaxies.remove(column)
    # Now when we expand these rows and columns, we can compute the new
    # galactic locations
    # In this case, we find how many rows and columns come "before" this galaxy
    # in the universe. Each of those needs to get expanded so the galaxy shifts
    # by one unit in each direction per additional row and column added
    new_locations = []
    for row, column in galaxy_locations:
        # Figure out how many rows and columns appear before it
        add_rows = len([r for r in rows_without_galaxies if r < row])
        add_columns = len([c for c in columns_without_galaxies if c < column])
        new_locations.append((row + add_rows, column + add_columns))
    return new_locations

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

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    image = read_data(filename)
    galaxy_locations = locate_galaxies(image)
    galaxy_locations = expand_galaxy_locations(
            locate_galaxies(image),
            num_rows=len(image),
            num_cols=len(image[0]),
            )
    total_distance = compute_total_pairwise_distances(galaxy_locations)
    print(f'Total of all pairwise distances: {total_distance}')
    return image

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
