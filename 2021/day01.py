"""Day 1: Sonar Sweep

In a list of numbers, find the number of times that the numbers increase
from one number to the next.
"""

import numpy as np
import sys

def count_increases(numlist):
    """Count number of times the measurements increase"""
    differences = numlist[1:] - numlist[:-1]
    return np.sum(differences > 0)

def find_window_sums(numlist):
    """Find the sums in the sliding window

    This function find the sums in a three-measurement sliding window, i.e., it
    considers every set of three consecutive measurements in the list and finds
    their sum.
    """
    window_sums = numlist[:-2] + numlist[1:-1] + numlist[2:]
    return window_sums

def main(filename):
    with open(filename, 'r') as datafile:
        numlist = datafile.read()
    numlist = numlist.splitlines()
    numlist = np.array([int(i) for i in numlist])
    num_increases = count_increases(numlist)
    num_window_sum_increases = count_increases(find_window_sums(numlist))
    return num_increases, num_window_sum_increases

if __name__ == "__main__":
    filename = sys.argv[1]
    num_increases, num_window_sum_increases = main(filename)
    print(f'Number of increases = {num_increases}')
    print(f'Number of window sum increases = {num_window_sum_increases}')
