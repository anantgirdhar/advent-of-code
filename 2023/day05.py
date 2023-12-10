"""Day 05: If You Give A Seed A Fertilizer"""

import sys

def convert(number, mapping):
    """Convert a number using a mapping

    This function takes in a source number and converts it to a destination
    number using the provided mapping. The mapping is a list of tuples of the
    form (source range start, source range end, destination range start).
    """
    for source_start, source_end, dest_start in mapping:
        if source_start <= number <= source_end:
            return dest_start + (number - source_start)
    # If all the mappings failed, then map back to the original number
    return number

def seed2location(seed_number, mappings):
    """Convert a seed number to a location number

    This function takes in a seed number and converts it to the corresponding
    location number by going through all the mappings provided in the mappings
    dict. Each individual mapping in the mappings dict must be a list of tuples
    of the form (source range start, source range end, destination range
    start).
    """
    num = seed_number
    num = convert(num, mappings['seed-to-soil map'])
    num = convert(num, mappings['soil-to-fertilizer map'])
    num = convert(num, mappings['fertilizer-to-water map'])
    num = convert(num, mappings['water-to-light map'])
    num = convert(num, mappings['light-to-temperature map'])
    num = convert(num, mappings['temperature-to-humidity map'])
    num = convert(num, mappings['humidity-to-location map'])
    return num

def find_lowest_location_number(seeds, mappings):
    """Find the lowest location number for the seeds

    This function takes a list of seed numbers and a dict of mappings. It uses
    the mappings to figure out what the lowest location number is. For a
    description of the mappings dict, see the seed2location function.
    """
    locations = [seed2location(seed, mappings) for seed in seeds]
    return min(locations)

def parse_data(data):
    """Parse the data to make it usable"""
    # Create some variables to store the information extracted
    maps = {}
    title = ''  # The title of the current map
    # Now extract everything
    for line in data:
        if line.startswith('seeds:'):
            # Extract all the seed numbers
            line = line.split(':')[-1]
            seeds = [int(n.strip()) for n in line.strip().split(' ')]
            continue
        if not line:
            if not title:
                # This line is empty and we're not in the middle of a map
                continue
            else:
                # This line is empty but we have a title
                # This is the end of a map
                # Reset the title
                title = ''
        else:
            if not title:
                # This is the start of a new map
                # This line has the title of the map
                title = line.split(':')[0]
                maps[title] = []
            else:
                # This has information about the mapping
                dest, source, length = line.split(' ')
                dest = int(dest)
                source = int(source)
                length = int(length)
                maps[title].append((source, source + length - 1, dest))
    return seeds, maps


def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    seeds, maps = parse_data(data)
    min_location = find_lowest_location_number(seeds, maps)
    print(f'Lowest location number: {min_location}')
    return seeds, maps

if __name__ == "__main__":
    filename = sys.argv[1]
    seeds, maps = main(filename)
