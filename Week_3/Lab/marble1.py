import time
import heapq

class PuzzleNode:
    def __init__(self, board, parent=None, cost=0):
        self.board = board
        self.parent = parent
        self.move = None
        self.g = cost

    def __lt__(self, other):
        return self.g < other.g


GOAL = [
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2]
]

INITIAL = [
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

                    if 0 <= ni < 7 and 0 <= nj < 7:
                        # The jump is only valid if middle is 1 and target is 0, and not jumping over 2
                        if node.board[mi][mj] == 1 and node.board[ni][nj] == 0:
                            new_board = [row[:] for row in node.board]
                            new_board[i][j] = 0
                            new_board[mi][mj] = 0
                            new_board[ni][nj] = 1

                            child = PuzzleNode(new_board, node, cost=node.g + 1)
                            child.move = [(i, j), (ni, nj)]
                            successors.append(child)
                            nodes_expanded += 1
    return successors


def priority_queue_search():
    frontier = []
    explored_set = set()

    start = PuzzleNode(INITIAL)
    heapq.heappush(frontier, start)

    while frontier:
        current = heapq.heappop(frontier)

        # Check if goal
        if current.board == GOAL:
            print("Search completed")
            return current

        # Convert board to tuple to store in explored_set
        board_tuple = tuple(tuple(row) for row in current.board)
        if board_tuple in explored_set:
            continue
        explored_set.add(board_tuple)

        for child in generate_successors(current):
            child_tuple = tuple(tuple(row) for row in child.board)
            if child_tuple not in explored_set:
                heapq.heappush(frontier, child)

    return None


def extract_moves(goal_node):
    move_list = []
    while goal_node.parent:
        move_list.append(goal_node.move)
        goal_node = goal_node.parent
    return move_list[::-1]


if __name__ == "__main__":
    print("Priority Queue Search started")
    start_time = time.time()
    solution_node = priority_queue_search()
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
