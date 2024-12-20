from copy import deepcopy
from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

in_field = input_lines


# lib
def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])


def sub_vec(vec1, vec2):
    return (vec1[0]-vec2[0], vec1[1]-vec2[1])


# Find all antennas and their positions
antennas = dict()

for idx_row in range(0, len(in_field)):
    for idx_col in range(0, len(in_field[idx_row])):
        frequency = in_field[idx_row][idx_col]
        if frequency == ".":
            continue

        if frequency == "#":
            continue

        if frequency not in antennas:
            antennas[frequency] = list()

        antenna_position = (idx_row, idx_col)
        antennas[frequency].append(antenna_position)

# Calculate antinodes for each frequency
def calculate_antinodes(multi=False):
    antinodes = dict()
    for frequency in antennas.keys():
        print(f"Found antennas at '{frequency}': {antennas[frequency]})")

        antinodes[frequency] = set()
        for antenna_first in antennas[frequency]:
            for antenna_second in antennas[frequency]:
                if antenna_first == antenna_second:
                    continue

                vec_diff = sub_vec(antenna_first, antenna_second)

                def in_bounds(antinode):
                    for idx in [0, 1]:
                        if antinode[idx] < 0 or antinode[idx] >= len(in_field):
                            print(f"   outer {antinode}")
                            return False
                    return True

                def add_antinode(antinode):
                    for idx in [0, 1]:
                        if antinode[idx] < 0 or antinode[idx] >= len(in_field):
                            print(f"   outer {antinode}")
                            return

                        if antinode in antinodes[frequency]:
                            print(f"   dupl  {antinode}")
                            return

                    print(f"   added {antinode}")
                    antinodes[frequency].add(antinode)

                first_antinode = sub_vec(antenna_second, vec_diff)
                second_antinode = add_vec(antenna_first, vec_diff)

                print(f"{antenna_first} - {antenna_second} = {vec_diff} -> {first_antinode}, {second_antinode}")

                add_antinode(first_antinode)
                add_antinode(second_antinode)

                if multi:
                    add_antinode(antenna_first)
                    add_antinode(antenna_second)
                    while in_bounds(first_antinode):
                        first_antinode = sub_vec(first_antinode, vec_diff)
                        add_antinode(first_antinode)
                    while in_bounds(second_antinode):
                        second_antinode = add_vec(second_antinode, vec_diff)
                        add_antinode(second_antinode)
    return antinodes


def count_unique_antinodes(antinodes):
    all_antinodes = set()
    for frequency in antinodes.keys():
        all_antinodes.update(antinodes[frequency])

    return len(all_antinodes)


part1 = count_unique_antinodes(calculate_antinodes(False))
print(f"part1: {part1}")

part2 = count_unique_antinodes(calculate_antinodes(True))
print(f"part2: {part2}")
