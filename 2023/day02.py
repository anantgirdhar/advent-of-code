"""Day 02: Cube Conundrum"""

import sys

def find_possible_games(games, maxR, maxG, maxB):
    """Find which games are possible

    A game is possible if the number of balls of each color does not exceed the
    maximum number of balls available in the bag.
    """
    possible_games = []
    for game_id, subsets in games.items():
        for (R, G, B) in subsets:
            if R > maxR or G > maxG or B > maxB:
                # This is an infeasible game
                break
        else:
            possible_games.append(game_id)
    return possible_games

def parse_data(data):
    """Parse the data to make it usable"""
    # Store each game as a list of [R, G, B] cubes
    games = {}
    for line in data:
        game_id, subsets = line.split(':')
        game_id = int(game_id.split(' ')[-1])
        games[game_id] = []
        for subset in subsets.split(';'):
            subset = subset.split(',')
            R, G, B = 0, 0, 0
            for cubes in subset:
                cubes = cubes.split(' ')
                # cubes[0] should be empty because of the split on space
                if cubes[2] == 'red':
                    R = int(cubes[1])
                elif cubes[2] == 'green':
                    G = int(cubes[1])
                elif cubes[2] == 'blue':
                    B = int(cubes[1])
            games[game_id].append([R, G, B])
    return games

def read_data(filename):
    """Read the data from the file"""
    with open(filename, 'r') as infile:
        data = infile.read()
    data = data.splitlines()
    return data

def main(filename):
    data = read_data(filename)
    games = parse_data(data)
    possible_games = find_possible_games(games, 12, 13, 14)
    # print(possible_games)
    print(f'Sum of possible games: {sum(possible_games)}')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
