from copy import deepcopy
from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

in_field = input_lines

# Find starting position
position = None
for row_idx in range(0, len(in_field)):
    for col_idx in range(0, len(in_field[row_idx])):
        if in_field[row_idx][col_idx] == "^":
            position = (row_idx, col_idx)
            break
    if position:
        break

print(f"Start at {position}")

start_position = position
start_direction = (-1, 0)
direction = start_direction

def turn_right_90deg(in_direction):
    return in_direction[1], -in_direction[0]

def position_on_field(position, field):
    if position[0] < 0 or position[0] >= len(field):
        return False
    elif position[1] < 0 or position[1] >= len(field[position[0]]):
        return False
    else:
        return True

def advance(position, direction):
    return (position[0]+direction[0], position[1]+direction[1])

def on_field(position):
    return in_field[position[0]][position[1]]

# part 1
visited_field = set()
distinct_visited_fields = 0

# part 2
detected_runways = set()
possible_obstacles = set()

def position_on_runway(position, runway):
    runway_start, runway_end, runway_direction = runway

    check_axis = None
    same_axis = None
    if runway_start[0] == runway_end[0]:
        check_axis = 1
        same_axis = 0
    elif runway_start[1] == runway_end[1]:
        check_axis = 0
        same_axis = 1
    else:
        raise RuntimeError("unknown check axis for runway")

    min_pos = min(runway_start[check_axis], runway_end[check_axis])
    max_pos = max(runway_start[check_axis], runway_end[check_axis])

    if position[check_axis] >= min_pos and position[check_axis] <= max_pos and position[same_axis] == runway_start[same_axis]:
        return True
    return False


# Walk the field
def walk_field(start_position, start_direction, in_field, max_steps=130*130, additional_obstacle=None):
    # part 1
    visited_field = set()
    distinct_visited_fields = 0

    # part 2
    detected_runways = set()
    possible_obstacles = set()

    # loop_abort
    steps = 0
    turns = set()

    position = start_position
    direction = start_direction

    while position_on_field(position, in_field):
        next_position = advance(position, direction)

        turn = (position, direction)
        if turn in turns:
            return None, visited_field, detected_runways, possible_obstacles
        else:
            turns.add(turn)

        if position not in visited_field:
            visited_field.add(position)
            distinct_visited_fields += 1

        steps += 1
        if steps > max_steps:
            return False, visited_field, detected_runways, possible_obstacles

        for runway in detected_runways:
            if position_on_runway(position, runway) and runway[2] == turn_right_90deg(direction) and on_field(next_position) != "#":
                possible_obstacles.add(next_position)

        try:
            if on_field(next_position) == "#" or next_position == additional_obstacle:
                # Also register this line for possible obstacle detection
                # Do this before turning because we need the (reverse) direction
                reverse_direction = (-direction[0], -direction[1])
                line_start_position = line_end_position = position
                try:
                    while True:
                        line_start_position = advance(line_start_position, reverse_direction)
                        if on_field(line_start_position) == "#":
                            break
                except IndexError:
                    pass
                #line_start_position = advance(line_start_position, direction)
                runway = line_start_position, line_end_position, direction
                #print(f"Detected runway: {runway}")
                detected_runways.add(runway)

                # Next field blocked, turn!
                direction = turn_right_90deg(direction)

            else:
                position = next_position
        except IndexError:
            # Well, we left the field. Just advance position, so that while registers it too.
            position = next_position

    return distinct_visited_fields, visited_field, detected_runways, possible_obstacles

distinct_visited_fields, visited_field, detected_runways, possible_obstacles = walk_field(start_position, start_direction, in_field)

print(f"visited fields: {distinct_visited_fields}")

possible_obstacles = 0
#for idx_row in range(0, len(in_field)):
#    for idx_col in range(0, len(in_field[idx_row])):
#        additional_obstacle = (idx_row, idx_col)
for additional_obstacle in visited_field:
    if additional_obstacle == start_position:
        continue
    steps, _, _, _ = walk_field(start_position, start_direction, in_field, additional_obstacle=additional_obstacle)
    print(f"Trying obstacle on {additional_obstacle}, exit after steps: {steps}")
    if steps == None:
        possible_obstacles += 1
        print(f"Found loop obstacle: {additional_obstacle}")

print(f"possible_obstacles: {possible_obstacles}")
#for obstacle in possible_obstacles:
#    print(f"  possible obstacle: {obstacle}")