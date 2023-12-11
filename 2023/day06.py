"""Day 06: Wait For It"""

import math
import sys

def _ways_to_win(race_time, record_distance):
    """Return how many ways there are to win a race

    This function accepts a race time and a record distance and then returns
    how many ways there are to win the race. The race is won if the distance
    travelled in the time is more than the record distance. The speed of the
    boat is increased by 1 unit for each unit of time the button is held down.
    """
    # Let:
    # - rt be the race time
    # - D be the record distance
    # - ht be the time the button is held down (hold time)
    # Then, the time remaining for the boat to travel is (t - ht)
    # Also, the boat's speed (once the button is released) is also ht
    # Further, the distance travelled is (t - ht) * ht
    # We want (t - ht) * ht > D, i.e. we want:
    # ht**2 - t*ht + D < 0
    # And we want to find the number of integer solutions to this problem
    # If we find the roots of this quadratic equation, then we'll know the
    # values of ht at which this is an equality, i.e., the values at which the
    # distance travelled by the boat equal the record distance D.
    # Then we can just find how many integers there are between these two time
    # values. If the roots are integers, then we just need to make sure to only
    # take the integer values that are strictly between these values
    min_ht = 0.5 * (race_time - math.sqrt(race_time ** 2 - 4 * record_distance))
    max_ht = 0.5 * (race_time + math.sqrt(race_time ** 2 - 4 * record_distance))
    # If these are integers, just push the values a little toward each other so
    # that the rest of the algorithm works
    if min_ht - int(min_ht) < 1e-6:
        min_ht += 0.1
    # I believe that the solutions should be symmetrical, i.e, if min_ht is an
    # integer then max_ht will be too. But I'm not 100% positive because I
    # haven't thought about it a lot so I'll just check both to be safe
    if max_ht - int(max_ht) < 1e-6:
        max_ht -= 0.1
    # Now we just need to count how many integers there are between these two
    # values
    return math.floor(max_ht) - math.ceil(min_ht) + 1

def compute_error_margin(race_times, record_distances):
    """Compute the error margin for all races

    This function accepts a list of race times and a list of record distances
    and computes the number of ways there are to win each of these races. See
    _ways_to_win() for more details. Then it find the product of these values
    to compute the margin of error.
    """
    return math.prod([_ways_to_win(t, d)
                      for (t, d) in zip(race_times, record_distances)])

def parse_data(data):
    """Parse the data to make it usable"""
    times = []
    distances = []
    # Extract the times from the first line
    # Ignore the initial string saying 'Time:'
    # Everything else is separated by at least one space
    for time in data[0].split(' ')[1:]:
        if not time:
            # Ignore any blank entries caused due to multiple spaces
            continue
        times.append(int(time))
    # Do the same for distances
    for distance in data[1].split(' ')[1:]:
        if not distance:
            # Ignore any blank entries caused due to multiple spaces
            continue
        distances.append(int(distance))
    return times, distances

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    times, distances = parse_data(data)
    error_margin = compute_error_margin(times, distances)
    print(f'Error margin: {error_margin}')
    return data

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
