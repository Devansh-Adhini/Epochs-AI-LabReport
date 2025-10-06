import random
import math
import matplotlib.pyplot as plt
import os

def read_tsp_file(filename):
    cities, start = [], False
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                start = True
                continue
            if line == "EOF" or not start:
                continue
            parts = line.split()
            if len(parts) == 3:
                cities.append((float(parts[1]), float(parts[2])))
    return cities

def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
def tour_cost(t, c): return sum(dist(c[t[i]], c[t[(i+1)%len(t)]]) for i in range(len(t)))

def nearest_neighbor(c):
    n, unv, t = len(c), set(range(len(c))), [0]
    unv.remove(0)
    while unv:
        nxt = min(unv, key=lambda x: dist(c[t[-1]], c[x]))
        t.append(nxt)
        unv.remove(nxt)
    return t

def delta_2opt(t, c, i, j):
    n = len(t)
    a,b,d,e = t[i], t[(i+1)%n], t[j], t[(j+1)%n]
    return (dist(c[a],c[d]) + dist(c[b],c[e])) - (dist(c[a],c[b]) + dist(c[d],c[e]))

def two_opt_swap(t, i, j): return t[:i+1] + t[i+1:j+1][::-1] + t[j+1:]

def local_2opt(t, c):
    improved = True
    while improved:
        improved = False
        for i in range(len(t)-1):
            for j in range(i+2, len(t)):
                d = delta_2opt(t, c, i, j)
                if d < -0.01:
                    t = two_opt_swap(t, i, j)
                    improved = True
                    break
            if improved: break
    return t

def sim_anneal(c, T0, alpha, Tmin, max_iter=150000):
    n = len(c)
    curr = local_2opt(nearest_neighbor(c), c)
    best = curr[:]
    cost = best_cost = tour_cost(curr, c)
    T = T0
    for _ in range(max_iter):
        if T < Tmin: break
        i, j = sorted(random.sample(range(n), 2))
        if j - i < 2: continue
        d = delta_2opt(curr, c, i, j)
        if d < 0 or random.random() < math.exp(-d/T):
            curr = two_opt_swap(curr, i, j)
            cost += d
            if cost < best_cost:
                best, best_cost = curr[:], cost
        T *= alpha
    best = local_2opt(best, c)
    return best, tour_cost(best, c)

def multi_run(cities, runs=5):
    n = len(cities)
    T0, alpha, Tmin = 150*math.sqrt(n), 0.99975, 0.001
    best_tour, best_cost = None, float('inf')
    for _ in range(runs):
        t, d = sim_anneal(cities, T0, alpha, Tmin)
        if d < best_cost:
            best_tour, best_cost = t, d
    return best_tour, best_cost

def plot_tour(t, c, title):
    x = [c[i][0] for i in t] + [c[t[0]][0]]
    y = [c[i][1] for i in t] + [c[t[0]][1]]
    plt.plot(x, y, 'o-', lw=0.8, ms=3)
    plt.title(title)
    plt.grid(True)

problems = {'xqf131.tsp':564, 'xqg237.tsp':1019, 'pma343.tsp':1368, 'pka379.tsp':1332, 'bcl380.tsp':1326}
folder = 'TSP_data'
results = []

for f, opt in problems.items():
    path = os.path.join(folder, f)
    if not os.path.exists(path): continue
    cities = read_tsp_file(path)
    if not cities: continue
    tour, cost = multi_run(cities, 3 if len(cities)>300 else 5)
    diff = ((cost - opt)/opt)*100
    results.append((f.split('.')[0].upper(), len(cities), opt, cost, diff))
    plot_tour(tour, cities, f)

print("\n--- RESULTS ---")
print(f"{'Problem':<10} | {'Cities':<6} | {'Optimal':<9} | {'Found':<9} | {'%Diff':<8}")
for n, c, o, f, d in results:
    print(f"{n:<10} | {c:<6} | {o:<9.2f} | {f:<9.2f} | {d:.2f}%")
plt.show()
