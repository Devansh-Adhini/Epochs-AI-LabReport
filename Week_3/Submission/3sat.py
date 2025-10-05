import string as st
import random as rnd
from itertools import combinations
import numpy as np

def get_input(prompt):
    return int(input(prompt))

def generate_formulas(num_formulas, vars_per_formula, total_vars):
    letters = list(st.ascii_lowercase[:total_vars])
    letters_upper = [c.upper() for c in letters]
    symbols = letters + letters_upper

    max_attempts, unique_set = 20, set()
    all_combinations = list(combinations(symbols, vars_per_formula))
    attempt = 0

    while len(unique_set) < num_formulas and attempt < max_attempts:
        formula = tuple(sorted(rnd.choice(all_combinations)))
        if formula not in unique_set:
            unique_set.add(formula)
        attempt += 1

    return [list(f) for f in unique_set]


def make_assignment(symbols, total_vars):
    lower_vals = list(np.random.choice([0, 1], total_vars))
    upper_vals = [1 - v for v in lower_vals]
    return dict(zip(symbols, lower_vals + upper_vals))


def evaluate_formula(formula, assignment):
    return sum(any(assignment[var] for var in clause) for clause in formula)


def hill_climb(formula, assignment, prev_score, prev_step, total_step):
    best_assignment = assignment.copy()
    best_score = prev_score
    best_step = prev_step

    for var, val in assignment.items():
        total_step += 1
        candidate = assignment.copy()
        candidate[var] = 1 - val
        score = evaluate_formula(formula, candidate)
        if score > best_score:
            best_score = score
            best_assignment = candidate.copy()
            best_step = total_step

    if best_score == prev_score:
        return assignment, best_score, f"{best_step}/{total_step - len(assignment)}"
    
    return hill_climb(formula, best_assignment, best_score, best_step, total_step)


def beam_search(formula, assignment, beam_width, step_count):
    if evaluate_formula(formula, assignment) == len(formula):
        return assignment, f"{step_count}/{step_count}"

    candidates = []
    for var, val in assignment.items():
        step_count += 1
        new_assign = assignment.copy()
        new_assign[var] = 1 - val
        score = evaluate_formula(formula, new_assign)
        candidates.append((new_assign, score, step_count))

    top_candidates = sorted(candidates, key=lambda x: x[1])[-beam_width:]
    for cand in top_candidates:
        if cand[1] == len(formula):
            return cand[0], f"{cand[2]}/{step_count}"

    return beam_search(formula, top_candidates[-1][0], beam_width, step_count)


def variable_neighborhood(formula, assignment, neighborhood_size, step_count):
    if evaluate_formula(formula, assignment) == len(formula):
        return assignment, f"{step_count}/{step_count}", neighborhood_size

    candidates = []
    for var, val in assignment.items():
        step_count += 1
        new_assign = assignment.copy()
        new_assign[var] = 1 - val
        score = evaluate_formula(formula, new_assign)
        candidates.append((new_assign, score, step_count))

    top_candidates = sorted(candidates, key=lambda x: x[1])[-neighborhood_size:]
    for cand in top_candidates:
        if cand[1] == len(formula):
            return cand[0], f"{cand[2]}/{step_count}", neighborhood_size

    return variable_neighborhood(formula, top_candidates[-1][0], neighborhood_size + 1, step_count)


def run():
    num_formulas = get_input("Number of formulas: ")
    vars_per_formula = get_input("Variables per formula: ")
    total_vars = get_input("Total variables: ")

    formulas = generate_formulas(num_formulas, vars_per_formula, total_vars)
    symbols = list(st.ascii_lowercase[:total_vars]) + [c.upper() for c in st.ascii_lowercase[:total_vars]]

    for idx, formula in enumerate(formulas, start=1):
        print(f"\nFormula {idx}: {formula}")
        assignment = make_assignment(symbols, total_vars)
        initial_score = evaluate_formula(formula, assignment)

        _, hc_score, hc_step = hill_climb(formula, assignment, initial_score, 1, 1)
        bs_assign, bs_step = beam_search(formula, assignment, 3, 1)
        vn_assign, vn_score, vn_step = variable_neighborhood(formula, assignment, 1, 1)

        print(f"HC: Score={hc_score}, Step={hc_step}")
        print(f"BS: Score={evaluate_formula(formula, bs_assign)}, Step={bs_step}")
        print(f"VND: Score={evaluate_formula(formula, vn_assign)}, Step={vn_step}, Neighborhood={vn_score}")


if __name__ == "__main__":
    run()
