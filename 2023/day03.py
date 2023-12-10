"""Day 03: Gear Ratios"""

import re
import sys

def compute_gear_ratio(idx, line, prev_line, next_line):
    """Find the product of numbers touching a gear

    A gear is a star (*) that has exactly two numbers touching it. This
    function checks to see if the star (defined by the index idx) has exactly
    two numbers touching it and, if so, will return the product of those two
    numbers. If not, it will return None.
    """
    # This assumes that the line always has at least one character before and
    # after idx.
    numbers = []
    # First check the current line to see if any numbers are touching it on the
    # left side
    if line[idx-1].isdigit():
        # When we split on any non-digits, we can be sure that we are getting
        # the entire number touching the star
        num = re.split(r'\D', line[:idx])[-1]
        # print(f'    > Found digit on left: {num}')
        numbers.append(int(num))
    # Now do the same for the right side
    if line[idx+1].isdigit():
        num = re.split(r'\D', line[idx+1:])[0]
        # print(f'    > Found digit on right: {num}')
        numbers.append(int(num))
    # For the prev_line, if there is a digit directly above the star, then
    # there is only one number touching it from the top. Otherwise, there
    # might be two numbers that we can find
    if prev_line:
        if prev_line[idx].isdigit():
            # Go back until you find a non-digit character or the start of the
            # line
            i = idx
            while prev_line[i-1].isdigit():
                i -= 1
            # Now we can just split on non-digits and grab the entire number
            num = re.split(r'\D', prev_line[i:])[0]
            # print(f'    > Found digit directly above: {num}')
            numbers.append(int(num))
        else:
            # If the digit directly above is not a digit, then we can just
            # split prev_line into the left part and the right part. Each part
            # can then be further split on non-digit characters. If the left
            # half has a number touching the star, it will be the last entry in
            # the split list. Similarly, if the right half has a number
            # touching the star, it will be the first entry in the list.
            num = re.split(r'\D', prev_line[:idx])[-1]
            if num:
                # print(f'    > Found digit NW: {num}')
                numbers.append(int(num))
            num = re.split(r'\D', prev_line[idx+1:])[0]
            if num:
                # print(f'    > Found digit NE: {num}')
                numbers.append(int(num))
    # Run a similar process for the next_line
    if next_line:
        if next_line[idx].isdigit():
            i = idx
            while next_line[i-1].isdigit():
                i -= 1
            num = re.split(r'\D', next_line[i:])[0]
            # print(f'    > Found digit directly below: {num}')
            numbers.append(int(num))
        else:
            num = re.split(r'\D', next_line[:idx])[-1]
            if num:
                # print(f'    > Found digit SW: {num}')
                numbers.append(int(num))
            num = re.split(r'\D', next_line[idx+1:])[0]
            if num:
                # print(f'    > Found digit SE: {num}')
                numbers.append(int(num))
    # print(f'    > {numbers}')
    if len(numbers) == 2:
        return numbers[0] * numbers[1]
    else:
        return None

def find_gear_ratios(lines):
    """Find the gear ratios for every gear

    The input is a list of lines that contain digits and symbols. This function
    finds all the gears (*'s) that are adjacent (orthogonally or diagonally) to
    exactly two numbers and returns a list of the products of each pair of
    numbers.
    """
    gear_ratios = []
    for i, line in enumerate(lines):
        # print(f'> {line}')
        # Loop over the characters
        for j, c in enumerate(line):
            if c != '*':
                # If we're not at a star (gear) we can move on
                continue
            else:
                # Once we're at a star, we can check to see if it is a gear
                # and, if so, what it's gear ratio is
                g = compute_gear_ratio(
                        j,
                        line,
                        lines[i-1] if i > 0 else None,
                        lines[i+1] if i < len(lines)-1 else None,
                        )
                if g is not None:
                    gear_ratios.append(g)
    return gear_ratios

def touches_symbol(start_idx, end_idx, line, prev_line, next_line):
    """Check if a substring touches a symbol

    Given a substring on line defined by start_idx to end_idx, check if it
    borders a symbol in line, prev_line, or next_line and return True if it
    does.
    """
    # This assumes that the line always has at least one character before
    # start_idx and at least one character after end_idx
    # Now, extract the characters of line, prev_line, and next_line that are
    # touching (orthogonally and diagonally) the required substring given by
    # start_idx and end_idx. This means that we need to go one character before
    # start_idx and one character after end_idx. Also, python slicing syntax
    # requires the end index to be the first character not wanted in the slice
    # (which is why we need to do end_idx+2).
    all_chars = set(line[start_idx-1:end_idx+2])
    if prev_line:
        all_chars |= set(prev_line[start_idx-1:end_idx+2])
    if next_line:
        all_chars |= set(next_line[start_idx-1:end_idx+2])
    # If any of these characters is a symbol then we're done!
    # Checking if there are any characters that are not periods or digits is
    # sufficient (as the only other option is for it to be a symbol)
    for c in all_chars:
        if not c.isdigit() and c != '.':
            return True
    # If this fails then there is no symbol touching this substring
    return False

def extract_part_numbers(lines):
    """Extract part numbers from the engine schematic

    The input is a list of lines that contain digits and symbols. This function
    extracts all digits that are adjacent (orthogonally or diagonally) to a
    symbol and returns the list of numbers.
    """
    part_numbers = []
    for i, line in enumerate(lines):
        # Create a variable to build up potential part numbers as we iterate
        # over the characters
        found_num = ''
        # On each line, iterate over the characters
        for j, c in enumerate(line):
            if not c.isdigit():
                if not found_num:
                    # If we haven't found any digits yet and this isn't a digit
                    # either, then just move on to the next character
                    continue
                else:
                    # If we have found some digits and this is not a digit,
                    # then we've completed a potential part number
                    # Now we need to check if this has a symbol next to it
                    # First, find the start and end indices
                    end_idx = j - 1
                    start_idx = j - len(found_num)
                    if touches_symbol(
                            start_idx,
                            end_idx,
                            line,
                            lines[i-1] if i > 0 else None,
                            lines[i+1] if i < len(lines)-1 else None,
                            ):
                        part_numbers.append(int(found_num))
                    # Now that we've dealt with this part number, reset it
                    found_num = ''
            else:
                # If this is a digit, then we just concatenate it with our
                # potential part number
                found_num += c
    return part_numbers

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    # There are weird edge cases when a number is at the start or end of a line
    # Instead of trying to correct that, I decided to prepend and append a
    # period to every line
    data = ['.' + line + '.' for line in data]
    return data

def main(filename):
    data = read_data(filename)
    part_numbers = extract_part_numbers(data)
    print(f'Sum of all part numbers: {sum(part_numbers)}')
    gear_ratios = find_gear_ratios(data)
    print(f'Sum of all gear ratios: {sum(gear_ratios)}')
    return data

if __name__ == "__main__":
    filename = sys.argv[1]
    data = main(filename)
