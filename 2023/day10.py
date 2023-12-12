"""Day 10: Pipe Maze"""

import sys

PIPES = {
        '|': ('N', 'S'),
        '-': ('W', 'E'),
        'L': ('N', 'E'),
        'J': ('N', 'W'),
        '7': ('W', 'S'),
        'F': ('S', 'E'),
        '.': ('.', '.'),
        }

def advance(maze, point, direction):
    """Get the next point and direction in the maze

    This function takes a point as a tuple of values, a cardinal direction, and
    the maze. It then returns the coordinates of the adjacent point in that
    # direction, and the direction of the next pipe in the maze.
    """
    match direction:
        case 'N':
            next_point = (point[0]-1, point[1])
        case 'S':
            next_point = (point[0]+1, point[1])
        case 'W':
            next_point = (point[0], point[1]-1)
        case 'E':
            next_point = (point[0], point[1]+1)
        case default:
            raise ValueError(f'Invalid direction "{direction}"')
    # Find the next pipe so we can use it to find the next direction
    next_pipe = maze[next_point[0]][next_point[1]]
    # Now, from the pipe's perspective, we came from the pipe opening that is
    # opposite to 'direction' to get into this pipe. Since the pipe is
    # described by its two openings, if we can remove this direction, the other
    # direction will be where we want to go next
    entrance_direction = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E',
            }[direction]
    # Now, the other direction is the exit and what we want
    for pipe_direction in PIPES[next_pipe]:
        if pipe_direction != entrance_direction:
            break
    next_direction = pipe_direction
    return next_point, next_direction

def find_furthest_point(maze, starting_location, connected_pipes):
    """Find the furthest point along the maze

    This function accepts the maze as a list of strings, the starting location,
    and the two pipes connecting to the starting location. It then traverses
    the maze to find the locations of the points that are the furthest away
    from it and returns the coordinates of the point along with the number of
    steps it would take to get there. This function assumes that there is a
    unique middle point along the loop.
    """
    # Travel the loop from both sides until you hit the same point
    # Then that is the middle point and is the furthest away
    # We know we're going to move at least one space so advance the initial
    # points
    point1, direction1 = advance(maze, starting_location, connected_pipes[0])
    point2, direction2 = advance(maze, starting_location, connected_pipes[1])
    num_steps = 1
    # Now loop until the points are the same again (that's also why I advanced
    # it - so that the points would not be the same at the beginning and we'd
    # enter the loop)
    while point1 != point2:
        point1, direction1 = advance(maze, point1, direction1)
        point2, direction2 = advance(maze, point2, direction2)
        num_steps += 1
    return point1, num_steps

def parse_data(data):
    """Parse the data to make it usable"""
    # I could store the maze as a list of lists with each entry pointing to the
    # index of the cell we go to next, but I feel like that might use up a lot
    # more memory, so I'll leave it as a string and then just navigate through
    # the string
    # I will use this function to find the starting position and the directions
    # of the two pipes connected to the starting position though
    for i, line in enumerate(data):
        if (j := line.find('S')) != -1:
            # The starting position is (i, j)
            start = (i, j)
            break
    # Now let's find the two directions the two connected pipes are in
    connected_pipes = []
    # Just check the 4 locations touching this cell
    # First check the top
    if i > 0:
        pipe = data[i-1][j]
        # Check if this pipe has an opening on the south side
        if 'S' in PIPES[pipe]:
            # If it does, then it is one of the two pipes that connects to the
            # starting location
            connected_pipes.append('N')
    # Next check the south side
    if i < len(data) - 1:
        pipe = data[i+1][j]
        if 'N' in PIPES[pipe]:
            connected_pipes.append('S')
    # Next check the west side
    if j > 0:
        pipe = data[i][j-1]
        if 'E' in PIPES[pipe]:
            connected_pipes.append('W')
    # Finally check the east side
    if j < len(data[i]) - 1:
        pipe = data[i][j+1]
        if 'W' in PIPES[pipe]:
            connected_pipes.append('E')
    return start, connected_pipes

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    starting_location, connected_pipes = parse_data(data)
    furthest_point, num_steps = find_furthest_point(data, starting_location, connected_pipes)
    print(f'Number of steps to furthest point: {num_steps}')
    return data, starting_location, connected_pipes

if __name__ == "__main__":
    filename = sys.argv[1]
    data, start_location, connected_pipes = main(filename)
