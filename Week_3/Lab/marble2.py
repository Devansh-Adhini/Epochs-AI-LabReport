import time

class PuzzleNode:
    def __init__(self, board, parent=None, cost=0):
        self.board = board
        self.parent = parent
        self.move = None
        self.g = cost

    def __lt__(self, other):
        return self.g < other.g


GOAL_BOARD = [
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2]
]

INITIAL_BOARD = [
    [2, 2, 1, 1, 1, 2, 2], 
    [2, 2, 1, 1, 1, 2, 2], 
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1], 
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]

nodes_expanded = 0

def generate_successors(node):
    global nodes_expanded
    successors = []

    jump_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    mid_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(7):
        for j in range(7):
            if node.board[i][j] == 1:
                for d in range(4):
                    ni, nj = i + jump_offsets[d][0], j + jump_offsets[d][1]
                    mi, mj = i + mid_offsets[d][0], j + mid_offsets[d][1]

                    if 0 <= ni < 7 and 0 <= nj < 7 and node.board[mi][mj] == 1 and node.board[ni][nj] == 0:
                        new_board = [row[:] for row in node.board]
                        new_board[i][j] = 0
                        new_board[mi][mj] = 0
                        new_board[ni][nj] = 1

                        child = PuzzleNode(new_board, node, cost=node.g + 1)
                        child.move = [(i, j), (ni, nj)]
                        successors.append(child)
                        nodes_expanded += 1
    return successors


def best_first_search():
    frontier = []
    visited = set()

    start_node = PuzzleNode(INITIAL_BOARD)
    frontier.append(start_node)

    while frontier:
        current = frontier.pop()

        print(f"Current state with path cost: {current.g}")
        for row in current.board:
            print(row)
        print()

        if current.board == GOAL_BOARD:
            print("Search completed")
            return current

        visited.add(str(current.board))

        for child in generate_successors(current):
            if str(child.board) not in visited:
                frontier.append(child)

    return None


def extract_moves(goal_node):
    path = []
    while goal_node.parent:
        path.append(goal_node.move)
        goal_node = goal_node.parent
    return path[::-1]


if __name__ == "__main__":
    print("Best First Search started")
    start_time = time.time()
    solution_node = best_first_search()
    end_time = time.time()

    if solution_node:
        print(f"Total nodes expanded: {nodes_expanded}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("Final state:")
        for row in solution_node.board:
            print(row)
        print("\nMoves:")
        moves = extract_moves(solution_node)
        for mv in moves:
            print(mv)
    else:
        print("No solution found.")
