import math
from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

# Fetch rules
order_rules = []
processed_lines = 0
for line in input_lines:
    processed_lines += 1
    if line == "":
        break

    pages = line.split("|")
    pages = [int(x) for x in pages]
    rule = (pages[0], pages[1])
    order_rules.append(rule)

# Fetch update sets:
update_sets = []
for line in input_lines[processed_lines:]:
    processed_lines += 1
    if line == "":
        break

    pages = line.split(",")
    pages = [int(x) for x in pages]
    update_sets.append(pages)

#for rule in order_rules:
#    print(f"Rule: print {rule[0]} before {rule[1]}")

def check_order(update_set):
    """Return true if set matches all rules"""
    # For all pages in set, check:
    # Does it violate any rules regarding pages before it?
    # Does it violate any rules regarding pages after it?
    #print(f"Checking Set {update_set}")
    for idx in range(0, len(update_set)):
        current_page = update_set[idx]
        #print(f"Set {update_set} | Checking idx {idx}: {update_set[idx]}")

        # Check rules for all pages before the current
        for before_idx in range(0, idx):
            before_page = update_set[before_idx]
            #print(f"before_idx: {before_idx} -> {before_page}")
            rule_that_must_not_exist = (current_page, before_page)
            #print(f"Could be broken by rule BEFORE {rule_that_must_not_exist}")
            if rule_that_must_not_exist in order_rules:
                #print(f"broken rule: {rule_that_must_not_exist}")
                return False

        # Check rules for all pages before the current
        for after_idx in range(idx+1, len(update_set)):
            after_page = update_set[after_idx]
            #print(f"after_idx: {after_idx} -> {after_page}")
            rule_that_must_not_exist = (after_page, current_page)
            #print(f"Could be broken by rule AFTER {rule_that_must_not_exist}")
            if rule_that_must_not_exist in order_rules:
                #print(f"broken rule: {rule_that_must_not_exist}")
                return False

    return True

def repair_order(update_set) -> [int]:
    """Return the repaired order"""
    # For all pages in set, check:
    # Does it violate any rules regarding pages before it?
    # Does it violate any rules regarding pages after it?
    #print(f"Checking Set {update_set}")
    for idx in range(0, len(update_set)):
        current_page = update_set[idx]
        #print(f"Set {update_set} | Checking idx {idx}: {update_set[idx]}")

        # Check rules for all pages before the current
        for before_idx in range(0, idx):
            before_page = update_set[before_idx]
            #print(f"before_idx: {before_idx} -> {before_page}")
            rule_that_must_not_exist = (current_page, before_page)
            #print(f"Could be broken by rule BEFORE {rule_that_must_not_exist}")
            if rule_that_must_not_exist in order_rules:
                #print(f"broken rule: {rule_that_must_not_exist}")
                update_set[before_idx], update_set[idx] = update_set[idx], update_set[before_idx]
                return repair_order(update_set)

        # Check rules for all pages before the current
        for after_idx in range(idx+1, len(update_set)):
            after_page = update_set[after_idx]
            #print(f"after_idx: {after_idx} -> {after_page}")
            rule_that_must_not_exist = (after_page, current_page)
            #print(f"Could be broken by rule AFTER {rule_that_must_not_exist}")
            if rule_that_must_not_exist in order_rules:
                #print(f"broken rule: {rule_that_must_not_exist}")
                update_set[after_idx], update_set[idx] = update_set[idx], update_set[after_idx]
                return repair_order(update_set)

    return update_set


part1 = 0
part2 = 0
for update_set in update_sets:
    if check_order(update_set):
        print(f"Set valid: {update_set}")
        middle_idx = int(math.floor(len(update_set)/2))
        middle_page = update_set[middle_idx]
        #print(f"Middle page: {middle_idx} - {middle_page}")
        part1 += middle_page
    else:
        repaired_order = repair_order(update_set)
        print(f"Repaired order: {repaired_order}")
        middle_idx = int(math.floor(len(repaired_order)/2))
        middle_page = repaired_order[middle_idx]
        part2 += middle_page


print(f"part1: {part1}")
print(f"part2: {part2}")

#for rule in order_rules:
#    print(f"Found rule: {rule}")
