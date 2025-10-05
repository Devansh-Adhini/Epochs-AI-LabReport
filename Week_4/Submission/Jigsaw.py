import random
import math
import numpy as np
import matplotlib.pyplot as plt

def cost_function(puzzle, grid_size=4, piece_size=128, img_size=512):
    cost = 0
    img = np.array(puzzle).reshape(img_size, img_size)
    
    for row in range(grid_size):
        for col in range(grid_size - 1):
            x = (col + 1) * piece_size
            y_start = row * piece_size
            y_end = (row + 1) * piece_size
            cost += np.sum(np.abs(img[y_start:y_end, x-1].astype(int) - 
                                   img[y_start:y_end, x].astype(int)))

    for row in range(grid_size - 1):
        for col in range(grid_size):
            y = (row + 1) * piece_size
            x_start = col * piece_size
            x_end = (col + 1) * piece_size
            cost += np.sum(np.abs(img[y-1, x_start:x_end].astype(int) - 
                                   img[y, x_start:x_end].astype(int)))
    
    return cost

def swap_pieces(puzzle, grid_size=4, piece_size=128, img_size=512):
    img = np.array(puzzle).reshape(img_size, img_size)

    i, j = random.sample(range(grid_size * grid_size), 2)
    r1, c1 = divmod(i, grid_size)
    r2, c2 = divmod(j, grid_size)

    y1_start, y1_end = r1 * piece_size, (r1 + 1) * piece_size
    x1_start, x1_end = c1 * piece_size, (c1 + 1) * piece_size
    y2_start, y2_end = r2 * piece_size, (r2 + 1) * piece_size
    x2_start, x2_end = c2 * piece_size, (c2 + 1) * piece_size

    piece1 = img[y1_start:y1_end, x1_start:x1_end].copy()
    img[y1_start:y1_end, x1_start:x1_end] = img[y2_start:y2_end, x2_start:x2_end]
    img[y2_start:y2_end, x2_start:x2_end] = piece1
    
    return img.flatten().tolist()

def simulated_annealing(puzzle, T_initial=2000, alpha=0.9995, stopping_temp=0.01, max_iterations=1000):
    current_state = puzzle.copy()
    current_cost = cost_function(current_state)
    
    best_state = current_state.copy()
    best_cost = current_cost
    
    T = T_initial
    iteration = 0
    
    while T > stopping_temp and iteration < max_iterations:
        new_state = swap_pieces(current_state)
        new_cost = cost_function(new_state)

        delta = new_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_state = new_state
            current_cost = new_cost

            if current_cost < best_cost:
                best_state = current_state.copy()
                best_cost = current_cost
        
        T *= alpha
        iteration += 1
    
    return best_state, best_cost

puzzle = []
file_path = 'scrambled.mat'

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("512"):
            continue
        puzzle.append(int(line))

if puzzle:
    img = np.array(puzzle, dtype=np.uint8).reshape((512, 512))
    img = img.T
    puzzle = img.flatten().tolist()

best_solution = None
best_cost = float('inf')

num_runs = 5
for run in range(num_runs):
    solved, cost = simulated_annealing(puzzle.copy())
    
    if cost < best_cost:
        best_cost = cost
        best_solution = solved.copy()

with open('answer.mat', 'w') as file:
    for item in best_solution:
        file.write(f"{item}\n")

print(f"\nFinal best cost: {best_cost}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(np.array(puzzle).reshape(512, 512), cmap='gray')
plt.title("Before (Transposed)")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(np.array(best_solution).reshape(512, 512), cmap='gray')
plt.title(f"After (Cost: {best_cost})")
plt.axis('off')

plt.tight_layout()
plt.show()