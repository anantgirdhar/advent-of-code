"""Day 01: Trebuchet?!"""

import sys

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
    calibration_values = extract_calibration_values(data)
    return calibration_values

if __name__ == "__main__":
    filename = sys.argv[1]
    calibration_values = main(filename)
    # print(f'Calibration values: {calibration_values}')
    print(f'Sum of calibration values: {sum(calibration_values)}')
