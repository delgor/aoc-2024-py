from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

reports = []
for line in input_lines:
    reports.append([int(x) for x in line.split()])


def report_safe(report):
    previous_sign = None
    for idx in range(1, len(report)):
        diff = report[idx] - report[idx - 1]

        if abs(diff) > 3:
            return False
        elif abs(diff) < 1:
            return False

        sign = diff/abs(diff)
        if previous_sign == None:
            pass
        elif sign != previous_sign:
            return False

        previous_sign = sign

    return True

def report_safe_with_dampener(report):
    if report_safe(report):
        return True
    else:
        for idx in range(0, len(report)):
            report_without_idx = [*report[0:idx], *report[idx+1:]]
            if report_safe(report_without_idx):
                return True
    return False

# check safety
total_safe = 0
total_safe_with_dampener = 0
for report in reports:
    is_report_safe = report_safe(report)
    print(f"{report} is safe? {is_report_safe}")
    if report_safe(report):
        total_safe += 1

    if report_safe_with_dampener(report):
        total_safe_with_dampener += 1

print(f"Total safe is {total_safe}")
print(f"Total safe with dampener is {total_safe_with_dampener}")
