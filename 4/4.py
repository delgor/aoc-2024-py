from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

in_field = input_lines

def find_word_in_direction(word, field, idx_in_word, idx_row, idx_col, dir_row, dir_col):
    idx_row += dir_row
    idx_col += dir_col
    idx_in_word += 1
    try:
        if idx_in_word == len(word):
            return True
        elif idx_row < 0 or idx_row > len(field):
            return False
        elif idx_col < 0 or idx_col > len(field[idx_row]):
            return False
        elif field[idx_row][idx_col] == word[idx_in_word]:
            #print(f"Matched {idx_in_word}: {field[idx_row][idx_col]} == {word[idx_in_word]}")
            return find_word_in_direction(word, field, idx_in_word, idx_row, idx_col, dir_row, dir_col)
        else:
            return False
    except IndexError:
        return False

def find_word(word, field):
    sum = 0
    for idx_row in range(0, len(field)):
        for idx_col in range(0, len(field[idx_row])):
            #print(f"Checking at {idx_row},{idx_col}: {field[idx_row][idx_col]}")
            if field[idx_row][idx_col] == word[0]:
                print(f"Possible start at {idx_row},{idx_col}")
                for row_direction in [-1, 0, 1]:
                    for col_direction in [-1, 0, 1]:
                        if row_direction == 0 and col_direction == 0:
                            pass
                        else:
                            if find_word_in_direction(word, field, 0, idx_row, idx_col, row_direction, col_direction):
                                print(f"Found match at {idx_row},{idx_col} in direction {row_direction},{col_direction}")
                                sum += 1
    return sum

def find_x_mas(field):
    sum = 0
    for idx_row in range(0, len(field)):
        for idx_col in range(0, len(field[idx_row])):
            # print(f"Checking at {idx_row},{idx_col}: {field[idx_row][idx_col]}")
            if field[idx_row][idx_col] == "A":
                #print(f"Possible start at {idx_row},{idx_col}")
                # Check for X Mas only - not for e.g. |\ "crosses"
                found_mas_es = 0
                for row_direction, col_direction in [(-1, -1), (-1, 1), (1, -1), (1,1)]:
                    if find_word_in_direction("MAS", field, -1, idx_row - 2 * row_direction,
                                              idx_col - 2 * col_direction, row_direction, col_direction):
                        found_mas_es += 1

                # Found at least 2 MAS here? Then it's a cross!
                if found_mas_es >= 2:
                    sum += 1
    return sum

count = find_word("XMAS", in_field)
print(f"count: {count}")

count = find_x_mas(in_field)
print(f"part2: {count}")
