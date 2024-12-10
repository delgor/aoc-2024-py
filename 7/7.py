from copy import deepcopy
from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

equations = list()

for line in input_lines:
    target, numbers = line.split(":")
    target = int(target)
    numbers = [int(number) for number in numbers.strip().split(" ")]
    equation = (target, numbers)
    equations.append(equation)
    #print(f"Equation to solve: {target} == {numbers} with operands unknown")

def equation_solvable(target, numbers) -> bool:
    if len(numbers) == 1:
        return target == numbers[0]
    elif len(numbers) == 0:
        raise RuntimeError("How did we arrive here?")
    else:
        if numbers[0] > target:
            return False
        remaining_numbers = numbers[2:]

        # Does add solve it?
        combined_value = numbers[0] + numbers[1]
        add_possible = equation_solvable(target, [combined_value, *remaining_numbers])

        # Does mul solve it?
        combined_value = numbers[0] * numbers[1]
        mul_possible = equation_solvable(target, [combined_value, *remaining_numbers])

        return add_possible or mul_possible

part1 = 0
for target, numbers in equations:
    if equation_solvable(target, numbers):
        print(f"{target} == magic({numbers}) is solvable!")
        part1 += target

print(f"part1: {part1}")
