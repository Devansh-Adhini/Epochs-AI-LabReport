import time
import heapq

class PuzzleNode:
    def __init__(self, board, parent=None, move=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


GOAL_BOARD = tuple(tuple(row) for row in [
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2]
])

INITIAL_BOARD = [
    [2, 2, 1, 1, 1, 2, 2], 
    [2, 2, 1, 1, 1, 2, 2], 
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1], 
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]


def heuristic_count(board):
    """Count number of pieces remaining (1s)"""
    return sum(row.count(1) for row in board)


def heuristic_distance(board):
    """Sum of Manhattan distances of pieces to center (3,3)"""
    total = 0
    for i in range(7):
        for j in range(7):
            if board[i][j] == 1:
                total += abs(i - 3) + abs(j - 3)
    return total


def generate_successors(node, heuristic):
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
                        # Only valid if middle is 1 and target is 0
                        if node.board[mi][mj] == 1 and node.board[ni][nj] == 0:
                            new_board = [row[:] for row in node.board]
                            new_board[i][j] = 0
                            new_board[mi][mj] = 0
                            new_board[ni][nj] = 1

                            child = PuzzleNode(
                                new_board,
                                parent=node,
                                move=[(i,j),(ni,nj)],
                                g=node.g + 1,
                                h=heuristic(new_board)
                            )
                            successors.append(child)
    return successors


def a_star_search(start_board, heuristic):
    start_node = PuzzleNode(start_board, g=0, h=heuristic(start_board))
    frontier = []
    heapq.heappush(frontier, start_node)
    visited = set()

    while frontier:
        current = heapq.heappop(frontier)
        board_tuple = tuple(tuple(row) for row in current.board)

        if board_tuple == GOAL_BOARD:
            print("Search completed")
            return current

        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        for child in generate_successors(current, heuristic):
            child_tuple = tuple(tuple(row) for row in child.board)
            if child_tuple not in visited:
                heapq.heappush(frontier, child)

    return None


def extract_moves(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    return path[::-1]


if __name__ == "__main__":
    print("A* search started with heuristic 1")
    start_time = time.time()
    result = a_star_search(INITIAL_BOARD, heuristic_count)
    end_time = time.time()

    if result:
        print("Total cost:", result.f)
        print("Time:", round(end_time - start_time, 2), "seconds")
        print("Moves:")
        for mv in extract_moves(result):
            print(mv)
    else:
        print("No solution found.")

    print("\nA* search started with heuristic 2")
    start_time = time.time()
    result = a_star_search(INITIAL_BOARD, heuristic_distance)
    end_time = time.time()

    if result:
        print("Total cost:", result.f)
        print("Time:", round(end_time - start_time, 2), "seconds")
        print("Moves:")
        for mv in extract_moves(result):
            print(mv)
    else:
        print("No solution found.")
