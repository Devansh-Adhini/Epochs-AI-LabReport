from collections import deque

def get_successors(state, parent_state, step):
    successors = []
    n = len(state)
    for i, val in enumerate(state):

        if val == 1:  # east rabbit moves right
            if i + 1 < n and state[i + 1] == 0:
                s = list(state)
                s[i], s[i + 1] = 0, 1
                successors.append([s, step, parent_state])
            if i + 2 < n and state[i + 1] == -1 and state[i + 2] == 0:
                s = list(state)
                s[i], s[i + 2] = 0, 1
                successors.append([s, step, parent_state])

        elif val == -1:  # west rabbit moves left
            if i - 1 >= 0 and state[i - 1] == 0:
                s = list(state)
                s[i], s[i - 1] = 0, -1
                successors.append([s, step, parent_state])
            if i - 2 >= 0 and state[i - 1] == 1 and state[i - 2] == 0:
                s = list(state)
                s[i], s[i - 2] = 0, -1
                successors.append([s, step, parent_state])

    return successors

def dfs_trace(start_state, goal_state):
    start_state = list(start_state)
    goal_state = tuple(goal_state)
    
    step_counter = 0
    stack = [[start_state, step_counter, None]]
    visited = []

    while stack:
        current, step_added, parent_state = stack.pop()

        visited.append([current, step_added, parent_state])

        frontier = [[state, step, parent] for state, step, parent in stack]

        print(f"\nStep {step_counter}:")
        print(f"State under consideration: {[current, step_added, parent_state[0] if parent_state else None]}")
        print(f"Frontier: {[[f[0], f[1], f[2][0] if f[2] else None] for f in frontier]}")
        print(f"Visited: {[[v[0], v[1], v[2][0] if v[2] else None] for v in visited]}")

        if tuple(current) == goal_state:
            path = []
            cur_entry = [current, step_added, parent_state]
            while cur_entry is not None:
                path.append(cur_entry[0])
                cur_entry = cur_entry[2]
            path.reverse()
            return path

        # Push successors onto stack (DFS order)
        successors = get_successors(current, [current, step_added, parent_state], step_counter + 1)
        for succ in successors:
            stack.append(succ)

        step_counter += 1

    return None

# Example usage
start_state = [1, 1, 1, 0, -1, -1, -1]
goal_state  = [-1, -1, -1, 0, 1, 1, 1]

solution_path = dfs_trace(start_state, goal_state)

if solution_path:
    print("\n=== Backtracked solution path ===")
    for idx, s in enumerate(solution_path):
        print(f"{idx}: {s}")
    print(f"\nTotal moves: {len(solution_path)-1}")
else:
    print("No solution found")
