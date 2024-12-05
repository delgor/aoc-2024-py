import re
from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

#input_lines = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]

def mul_score(input_lines):
    mul_regex = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
    sum = 0
    for line in input_lines:
        for match in mul_regex.finditer(line):
            sum += int(match[1]) * int(match[2])
    return sum

def mul_score_with_enable(input_lines):
    op_regex = re.compile(r"(mul\(([0-9]+),([0-9]+)\))|do\(\)|don't\(\)")
    sum = 0
    mul_enabled = True
    for line in input_lines:
        for match in op_regex.finditer(line):
            print(match)
            if match[0] == "do()":
                mul_enabled = True
            elif match[0] == "don't()":
                mul_enabled = False
            else:
                if mul_enabled:
                    sum += int(match[2]) * int(match[3])
    return sum


print(f"part1: {mul_score(input_lines)}")
print(f"part2: {mul_score_with_enable(input_lines)}")
