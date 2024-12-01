from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

left_list = []
right_list = []
for line in input_lines:
    left, right = line.split()
    left_list.append(int(left))
    right_list.append(int(right))

left_list = list(sorted(left_list))
right_list = list(sorted(right_list))

total_diff = 0
for left, right in zip(left_list, right_list):
    total_diff += abs(left - right)

print(f"total_diff = {total_diff}")

similarity_score = 0
for left in left_list:
    similarity_score += left * right_list.count(left)

print(f"similarity_score = {similarity_score}")