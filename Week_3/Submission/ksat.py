import string
import random
from itertools import combinations

def ask_integer(msg):
    return int(input(msg))

def create_random_clauses(num_clauses, vars_per_clause, total_vars):
    lower_vars = list(string.ascii_lowercase[:total_vars])
    upper_vars = [v.upper() for v in lower_vars]
    all_vars = lower_vars + upper_vars

    max_attempts = 18
    unique_clauses = set()
    possible_combinations = list(combinations(all_vars, vars_per_clause))

    attempt = 0
    while len(unique_clauses) < num_clauses and attempt < max_attempts:
        clause = tuple(sorted(random.choice(possible_combinations)))
        if clause not in unique_clauses:
            unique_clauses.add(clause)
        attempt += 1

    return [list(c) for c in unique_clauses]


def run():
    print("=== Random Clause Generator ===")
    num_clauses = ask_integer("Number of clauses: ")
    vars_per_clause = ask_integer("Variables per clause: ")
    total_vars = ask_integer("Total variables: ")

    clauses = create_random_clauses(num_clauses, vars_per_clause, total_vars)
    for idx, clause in enumerate(clauses, start=1):
        print(f"Clause {idx}: {clause}")


if __name__ == "__main__":
    run()
