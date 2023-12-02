"""Day 01: Trebuchet?!"""

import sys
import numpy as np

def extract_real_calibration_values(strings):
    """Extract "real" calibration values for each string in the list of strings

    The calibration value for each string is still a single two-digit number
    (see extract_calibration_values for an explanation). However, now we must
    also account for digits that are spelled out in words.
    """
    # Create a list of possible "digits"
    DIGITS = [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "zero", "one",
            "two", "three", "four", "five", "six", "seven", "eight", "nine",
            ]
    DIGIT_LENGTHS = np.array([len(s) for s in DIGITS])
    # For each string:
    # Find the index at which each "digit" appears in the string
    # Figure out which digit appears first (lowest index) and last (highest
    # index)
    # Combine them to form the two-digit number
    # Return the resulting list of two digit numbers
    indices = [
            np.array([string.find(digit) for digit in DIGITS])
            for string in strings
            ]
    # This will contain a -1 if a "digit" is not found in the string
    # Ignoring these -1 values, the smallest value denotes the "digit" that
    # appears first in the string
    # Consider the index of this value
    # If the index is less than 10, it will directly give us the corresponding
    # "digit" that appears first in the string (and it is an actual numeric
    # digit)
    # If the index is more than 10, then the "digit" is actually a string and,
    # to get its value, we can compute the index modulo 10
    # Save this as the tens digit
    tens_digits = [
            np.where(i >= 0, i, np.inf).argmin() % 10
            for i in indices
            ]
    # We can do a similar computation to get the ones digits
    # I first tried to just look for the highest value in the indices list but
    # it didn't work. I believe it's because a string has the same "digit"
    # twice and so find is only finding the index of the first occurrence.
    # To fix this, I would assume that we can reverse each string, and do the
    # computations.
    flipped_indices = [
            np.array([string[::-1].find(digit[::-1]) for digit in DIGITS])
            for string in strings
            ]
    ones_digits = [
            np.where(i >= 0, i, np.inf).argmin() % 10
            for i in flipped_indices
            ]
    # We can now construct the two-digit number for each string using the tens
    # and ones digits we've found
    calibration_values = [10 * tens + ones for (tens, ones) in zip(tens_digits, ones_digits)]
    return calibration_values

def extract_calibration_values(strings):
    """Extract calibration values for each string in the list of strings

    The calibration value for each string is a single two-digit number formed
    by combining the first digit and the last digit in the string. The function
    returns the corresponding list of calibration values - one for each string
    in the list of strings provided.
    """
    # For each string:
    # Extract all the digits from the string
    # Extract the first and last digit from the resulting list of numbers
    # Combine them to form a single two-digit number
    # Return the resulting list of two-digit numbers
    calibration_values = [
            [char for char in list(string) if char.isdigit()]
            for string in strings
            ]
    calibration_values = [
            int(''.join([digits[0], digits[-1]]))
            for digits in calibration_values
            ]
    return calibration_values

def main(filename):
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    try:
        calibration_values = extract_calibration_values(data)
    except IndexError:
        calibration_values = []
    real_calibration_values = extract_real_calibration_values(data)
    return calibration_values, real_calibration_values

if __name__ == "__main__":
    filename = sys.argv[1]
    calibration_values, real_calibration_values = main(filename)
    # print(f'Calibration values: {calibration_values}')
    # print(f'"Real" calibration values: {real_calibration_values}')
    print(f'Sum of calibration values: {sum(calibration_values)}')
    print(f'Sum of "real" calibration values: {sum(real_calibration_values)}')
