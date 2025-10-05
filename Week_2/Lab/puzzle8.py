import random
import time
import tracemalloc
from collections import deque

# ---------------- Goal State ----------------
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# ---------------- Puzzle Node ----------------
class PuzzleNode:
    def __init__(self, config, prev=None):
        self.config = config
        self.prev = prev

# ---------------- Generate Neighboring States ----------------
def generate_neighbors(current_node):
    neighbors = []
    zero_pos = current_node.config.index(0)
    shifts = [1, -1, 3, -3]

    for shift in shifts:
        new_pos = zero_pos + shift
        if 0 <= new_pos < 9:
            new_state = current_node.config[:]
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            neighbors.append(PuzzleNode(new_state, current_node))
    return neighbors

# ---------------- Generate Initial State at Given Depth ----------------
def generate_state_at_depth(depth):
    """Generate a puzzle depth moves away from the goal."""
    state = GOAL_STATE[:]
    for _ in range(depth):
        state = random.choice([s.config for s in generate_neighbors(PuzzleNode(state))])
    return state

# ---------------- BFS Search ----------------
def breadth_first_search(start, goal):
    open_queue = deque([PuzzleNode(start)])
    visited_nodes = set()
    explored_count = 0

    while open_queue:
        current = open_queue.popleft()
        current_tuple = tuple(current.config)
        if current_tuple in visited_nodes:
            continue

        visited_nodes.add(current_tuple)
        explored_count += 1

        if current.config == goal:
            path_trace = []
            while current:
                path_trace.append(current.config)
                current = current.prev
            return list(reversed(path_trace)), explored_count

        for neighbor in generate_neighbors(current):
            open_queue.append(neighbor)

    return None, explored_count

# ---------------- Main ----------------
if __name__ == "__main__":
    depth = int(input("Enter the depth for initial state: "))
    initial_state = generate_state_at_depth(depth)
    print(f"Initial state at depth {depth}:")
    print(initial_state)

    tracemalloc.start()
    start_time = time.time()
    
    solution_path, nodes_explored = breadth_first_search(initial_state, GOAL_STATE)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nRuntime: {end_time - start_time:.4f} seconds")
    print(f"Memory used: {peak / 1024 / 1024:.4f} MB")
    print(f"Total nodes explored: {nodes_explored}")

    if solution_path:
        print("\nSolution path:")
        for step in solution_path:
            print(step)
        print(f"Depth of solution: {len(solution_path)-1} moves")
    else:
        print("No solution found.")
