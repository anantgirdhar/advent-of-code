"""Day 3: Binary Diagnostic

Compute the gamma rate and epsilon rate from the binary diagnostic report and
use that to compute the power consumption of the submarine.
"""

import sys

def most_common_bit(numlist, position):
    """Find the most common bit at a position

    To find the most common bit at a specific position, we can find how
    many 1s there are in that position and compare that with how many
    numbers we have in total. To do that, just 'and' each number with a
    binary number that has a 1 in that position and 0s everywhere else,
    i.e. the appropriate power of 2. If there is a 0 in that position,
    the 'and' returns a 0. If not, we get a number back. Then we can
    just count the number of nonzero terms to get the number of 1s. If
    the number of 1s is more than half of the total number of numbers,
    it is the more common bit.

    In the case of a tie, it returns a 1.

    Inputs
    ------
    numlist: list of ints
        The list of diagnostic numbers converted to decimal
    position: int
        The position for which to find the most common bit
    """
    num_numbers = len(numlist)
    # Create the int that represents the binary number with 1 in the
    # appropriate position
    power_of_two = 2 ** position
    results = [num & power_of_two for num in numlist]
    results = [result for result in results if result > 0]
    num_1s = len(results)
    if num_1s >= num_numbers / 2:
        return 1
    else:
        return 0

def find_gamma_rate(numlist, string_length):
    """Compute the gamma rate

    The gamma rate is the binary string where each bit is the most
    common bit in the corresponding position of all numbers in the
    diagnostic report.
    """
    gamma = ''
    for position in range(string_length):
        gamma += str(most_common_bit(numlist, position))
    # We've considered each bit position in reverse so we need to reverse the
    # string and then convert it back to decimal.
    return int(gamma[::-1], 2)

def find_epsilon_rate(gamma_rate, string_length):
    """Compute the epsilon rate

    The epsilon rate is the binary string where each bit is the least
    common bit in the corresponding position of all numbers in the
    diagnostic report.

    Since we already have the gamma rate, we can just flip each bit to
    get the epsilon rate. To flip each bit, just xor with the binary
    string containing all 1s.
    """
    return gamma_rate ^ int('1' * string_length, 2)

def find_power_consumption(numlist, string_length):
    """Compute the power consumption

    The power consumption is defined as the product of the epsilon rate
    and the gamma rate.
    """
    gamma = find_gamma_rate(numlist, string_length)
    epsilon = find_epsilon_rate(gamma, string_length)
    return gamma * epsilon

def find_oxygen_generator_rating(numlist, string_length):
    """Compute the oxygen generator rating

    The oxygen generator rating is found by discarding numbers in
    numlist until only one remains. First consider the most significant
    bit. Find the most common value for that bit position. Keep all
    numbers beginning with that bit and discard the rest. Then move on
    to the next bit.
    """
    # Create a copy of the numlist
    oxygen_generator_rating = numlist[:]
    # Go over the positions from highest to lowest
    # Remember that the positions start at 0 and go up to string_length - 1
    # Also remember to iterate over them from most significant bit to least
    # significant bit
    for position in range(string_length - 1, -1, -1):
        mcb = most_common_bit(oxygen_generator_rating, position)
        # Now cull the list
        # Check if you have this bit in this position by 'and'ing with the
        # appropriate power of 2 (which will have a 1 only this position).
        # Exclude the number if that does not match the most common bit found
        # here, i.e., only include it if the result of the 'and' operation is
        # the most common bit. Remember that the result of the 'and' operation
        # is going to be the power of 2 and not just a 1 or a 0.
        oxygen_generator_rating = [
                num for num in oxygen_generator_rating
                if num & 2 ** position == mcb * 2 ** position
                ]
        if len(oxygen_generator_rating) == 1:
            return oxygen_generator_rating[0]
    # It should never get here, but return it anyway
    return oxygen_generator_rating

def find_co2_scrubber_rating(numlist, string_length):
    """Compute the CO2 scrubber rating

    The CO2 scrubber rating is found by discarding numbers in numlist
    until only one remains. First consider the most significant bit.
    Find the least common value for that bit position. Keep all numbers
    beginning with that bit and discard the rest. Then move on to the
    next bit.
    """
    # Create a copy of the numlist
    co2_scrubber_rating = numlist[:]
    # Go over the positions from highest to lowest
    # Remember that the positions start at 0 and go up to string_length - 1
    # Also remember to iterate over them from most significant bit to least
    # significant bit
    for position in range(string_length - 1, -1, -1):
        mcb = most_common_bit(co2_scrubber_rating, position)
        # To get the least common value for this position, just flip the mcb
        lcb = 1 - mcb
        # Now cull the list
        # Check if you have this bit in this position. See
        # find_oxygen_generator_rating for how to do this.
        co2_scrubber_rating = [
                num for num in co2_scrubber_rating
                if num & 2 ** position == lcb * 2 ** position
                ]
        if len(co2_scrubber_rating) == 1:
            return co2_scrubber_rating[0]
    # It should never get here, but return it anyway
    return co2_scrubber_rating

def find_life_support_rating(numlist, string_length):
    """Compute the life support rating

    The life support rating is the product of the oxygen generator
    rating and the CO2 scrubber rating.
    """
    return (
            find_oxygen_generator_rating(numlist, string_length)
            * find_co2_scrubber_rating(numlist, string_length)
            )

def load_data(filename):
    with open(filename, 'r') as datafile:
        numlist = datafile.read().splitlines()
    return numlist

def clean_data(numlist):
    # Convert each string to a number (remember they're in base 2)
    numlist = [int(num, 2) for num in numlist]
    return numlist

def main(filename):
    numlist = load_data(filename)
    # Find how long each binary string is
    # This assumes that each string has the same length
    string_length = len(numlist[0])
    numlist = clean_data(numlist)
    # Now find the power consumption
    power = find_power_consumption(numlist, string_length)
    print(f'Power = {power}')
    # Then find the life support rating
    life_support_rating = find_life_support_rating(numlist, string_length)
    print(f'Life support rating = {life_support_rating}')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
