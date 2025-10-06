''' 
format for state: [1, 1, 1, 0, -1, -1, -1]
1 -> east bounded rabbit
-1 -> west bounded rabbit
0 -> empty space
format for move: [ state , step_they_were_appended_into_the_frontier, parent_state ]
'''
from collections import deque

def get_successors(state, parent_state, step):
    successors = []
    n = len(state)
    for i, val in enumerate(state):

        if val == 1:  # east rabbit moves right
            # hop
            if i + 1 < n and state[i + 1] == 0:
                s = list(state)
                s[i], s[i + 1] = 0, 1
                successors.append([s, step, parent_state])
            # jump
            if i + 2 < n and state[i + 1] == -1 and state[i + 2] == 0:
                s = list(state)
                s[i], s[i + 2] = 0, 1
                successors.append([s, step, parent_state])

        elif val == -1:  # west rabbit moves left
            # hop
            if i - 1 >= 0 and state[i - 1] == 0:
                s = list(state)
                s[i], s[i - 1] = 0, -1
                successors.append([s, step, parent_state])
            # jump
            if i - 2 >= 0 and state[i - 1] == 1 and state[i - 2] == 0:
                s = list(state)
                s[i], s[i - 2] = 0, -1
                successors.append([s, step, parent_state])

    return successors

def bfs(start_state, goal_state):
    start_state = list(start_state)
    goal_state = tuple(goal_state)
    
    step_counter = 0
    q = deque([[start_state, step_counter, None]])
    visited = {tuple(start_state): [step_counter, None]}

    while q:
        current, step_added, parent_state = q.popleft()
        current_tuple = tuple(current)

        frontier = [[state, step, parent] for state, step, parent in q]
        visited_list = [[list(k), v[0], v[1]] for k,v in visited.items()]

        # Get successors and append into the queue if not visited
        successors = get_successors(current, current, step_counter)
        for succ_state, succ_step, succ_parent in successors:
            t_succ = tuple(succ_state)
            if t_succ not in visited:
                visited[t_succ] = [succ_step, succ_parent]
                q.append([succ_state, succ_step, succ_parent])

        print(f"\nStep {step_counter}:")
        print(f"State under consideration: {[current, step_added, parent_state]}")
        print(f"Frontier: {frontier}")
        print(f"Visited: {visited_list}")
        step_counter += 1

        # Base case: check if the goal is reached
        if current_tuple == goal_state:
            # Backtrack from goal to start to get the solution path
            path = []
            cur_state = current
            while cur_state is not None:
                path.append(cur_state)
                parent = visited[tuple(cur_state)][1]
                cur_state = parent
            path.reverse()
            return path

        # Get successors and append into the queue if not visited
        successors = get_successors(current, current, step_counter)
        for succ_state, succ_step, succ_parent in successors:
            t_succ = tuple(succ_state)
            if t_succ not in visited:
                visited[t_succ] = [succ_step, succ_parent]
                q.append([succ_state, succ_step, succ_parent])

    return None

start_state = [1, 1, 1, 0, -1, -1, -1]
goal_state  = [-1, -1, -1, 0, 1, 1, 1]

solution_path = bfs(start_state, goal_state)

if solution_path:
    print("\n=== Backtracked solution path ===")
    for idx, s in enumerate(solution_path):
        print(f"{idx}: {s}")
    print(f"\nTotal moves: {len(solution_path)-1}")
else:
    print("No solution found")
