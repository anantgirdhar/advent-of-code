"""Day 14: Parabolic Reflector Dish"""

import functools
import sys
from tqdm import tqdm

@functools.cache
def rotate_right(platform):
    """Return a left rotation of the platform

    This function accepts the platform as a list of strings and returns another
    list of strings that represent the platform rotated by 90 degrees
    clockwise.
    """
    rotated = [''] * len(platform[0])
    for line in reversed(platform):
        for i, char in enumerate(list(line)):
            rotated[i] += char
    return rotated

@functools.cache
def rotate_left(platform):
    """Return a right rotation of the platform

    This function accepts the platform as a list of strings and returns another
    list of strings that represent the platform rotated by 90 degrees
    counter-clockwise.
    """
    rotated = [''] * len(platform[0])
    for line in platform:
        for i, char in enumerate(list(line)):
            rotated[i] += char
    return rotated

@functools.cache
def rotate_180(platform):
    """Return a 180 degree rotation of the platform

    This function accepts the platform as a list of strings and returns another
    list of strings that represent the platform rotated by 180 degrees.
    """
    return [line[::-1] for line in reversed(platform)]

@functools.cache
def process_line(line):
    """Return the new line after shifting westward

    This function accepts a line of the platform and returns a new line
    representing the new locations of the rocks after they have all shifted as
    far west as they can.
    """
    shifted = []
    for chunk in line.split('#'):
        # Each chunk now only contains .'s and O's
        # Just rearrange them to have O's on the left and .'s on the right
        num_Os = 0
        num_dots = 0
        for char in list(chunk):
            match char:
                case 'O':
                    num_Os += 1
                case '.':
                    num_dots += 1
        shifted.append('O' * num_Os + '.' * num_dots)
    return '#'.join(shifted)

@functools.cache
def rotate_and_tilt(platform):
    """Return the rotated left-tilted platform state

    This function accepts a platform, rotates it to the right, tilts it to the
    left and returns the new state.
    """
    return [process_line(line) for line in rotate_right(platform)]

def compute_total_load(platform):
    """Return the total load on the platform

    This function accepts the distribution of rocks on the platform and
    computes the total load. This is represented as a list of strings. It
    assumes that the platform is rotated so that the left side is north. It
    does not tilt the platform.
    """
    # The load of a rock is given by its distance from the eastern edge
    # It might be easier to go over the characters in reverse order
    total_load = 0
    for line in platform:
        for i, char in enumerate(reversed(list(line))):
            if char == 'O':
                total_load += i + 1
    return total_load

def compute_post_shifting_load(platform, num_tilts):
    """Return the total load after shifting

    This function accepts the distribution of rocks on the platform; tilts it
    num_tilts times in the north, then west, then south, and then east; and
    finally computes the total load on the north side.
    """
    # Instead of writing separate functions for tilting the platform in the
    # four directions, we can rotate the platform by 90 degrees clockwise
    # before every tilt and then tilt it in the same direction (towards the
    # left edge)
    # Since we are tilting towards the left edge, we should rotate the data so
    # that the north edge is pointing down. This way when we rotate it before
    # tilting it the first time, we'll tilt towards the north edge
    # This involves flipping everything
    platform = rotate_180(tuple(platform))
    # Now begin rotating and tilting
    for _ in tqdm(range(num_tilts)):
        # Rotate right and tilt the platform to the new left
        platform = rotate_and_tilt(tuple(platform))
    # Here is the direction the left edge corresponds to after all these rotations:
    # - 1: north
    # - 2: west
    # - 3: south
    # - 4: east
    # If we want to find the load on the north edge, that needs to be on the
    # left (because of how the load calculation function is written)
    # So just rotate to the appropriate direction
    match (num_tilts % 4):
        case 1:
            # Already pointing north
            pass
        case 2:
            platform = rotate_left(tuple(platform))
        case 3:
            platform = rotate_180(tuple(platform))
        case 0:
            platform = rotate_right(tuple(platform))
    # Now compute and return the load on the north (left) end
    return compute_total_load(platform)

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    platform = read_data(filename)
    total_load = compute_post_shifting_load(platform, num_tilts=1)
    print(f'Total load after one north tilt: {total_load}')
    total_load = compute_post_shifting_load(platform, num_tilts=4*1000000000)
    print(f'Total load after 1000000000 NWSE cycles: {total_load}')
    return platform

if __name__ == "__main__":
    filename = sys.argv[1]
    platform = main(filename)
