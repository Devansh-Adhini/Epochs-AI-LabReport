from collections import deque

def is_valid(state):
    m, c, _ = state
    if m < 0 or c < 0 or m > 3 or c > 3: return False
    if m > 0 and m < c: return False
    if 3 - m > 0 and 3 - m < 3 - c: return False
    return True

def get_successors(state):
    s = []
    m, c, b = state
    moves = [(2,0),(0,2),(1,1),(1,0),(0,1)]
    if b == 1:
        for x,y in moves:
            ns = (m - x, c - y, 0)
            if is_valid(ns): s.append(ns)
    else:
        for x,y in moves:
            ns = (m + x, c + y, 1)
            if is_valid(ns): s.append(ns)
    return s

def bfs(start, goal):
    q = deque([(start, [])])
    v = set()
    while q:
        s, p = q.popleft()
        if s in v: continue
        v.add(s)
        p = p + [s]
        if s == goal: return p
        for nxt in get_successors(s):
            q.append((nxt, p))
    return None

start, goal = (3,3,1), (0,0,0)
sol = bfs(start, goal)

if sol:
    print("Solution path:")
    for i, step in enumerate(sol):
        print(f"Step {i}: {step}")
    print(f"\nFinal Path: {sol}")
else:
    print("No solution found.")
