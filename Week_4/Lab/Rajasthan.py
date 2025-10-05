import math
import random
import time

def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2+(city1[1]-city2[1])**2)

def td(tour):
    return sum(distance(tour[i], tour[(i+1) % len(tour)]) for i in range(len(tour)))

def simulated_annealing(cities, temperature=10000, cooling_rate=0.995, st=1e-8, maxiter=1000000):
    ct = cities[:]
    bt = ct[:]
    n = len(cities)
    iteration = 1
    while temperature > st and iteration < maxiter:
        [i, j] = sorted(random.sample(range(n), 2))
        new_tour = ct[:]
        new_tour[i:j+1] = reversed(new_tour[i:j+1])
        current_distance = td(ct)
        new_distance = td(new_tour)
        if new_distance < current_distance:
            ct = new_tour
            if new_distance < td(bt):
                bt = new_tour
        elif random.random() < math.exp((current_distance - new_distance) / temperature):
            ct = new_tour  
        temperature *= cooling_rate
        iteration += 1
    return bt, td(bt)

cities = [
    ("Jaipur", (0.72, 0.77)),
    ("Udaipur", (0.48, 0.69)),
    ("Jodhpur", (0.65, 0.66)),
    ("Ajmer", (0.67, 0.74)),
    ("Bikaner", (0.80, 0.68)),
    ("Pushkar", (0.68, 0.73)),
    ("Chittorgarh", (0.49, 0.74)),
    ("Jaisalmer", (0.66, 0.59)),
    ("Mount Abu", (0.48, 0.70)),
    ("Sikar", (0.74, 0.76)),
    ("Neemrana", (0.75, 0.78)),
    ("Kota", (0.52, 0.77)),
    ("Tonk", (0.69, 0.77)),
    ("Barmer", (0.57, 0.63)),
    ("Bundi", (0.55, 0.76)),
    ("Bikaner2", (0.70, 0.75)),
    ("Sawai Madhopur", (0.69, 0.78)),
    ("Fatehpur Sikri", (0.77, 0.80)),
    ("Bhilwara", (0.66, 0.74)),
    ("Mandawa", (0.73, 0.75)),
    ("Jhalawar", (0.45, 0.78))
]

city_names = [c[0] for c in cities]
city_coords = [c[1] for c in cities]

start = time.time()
best_tour, best_distance = simulated_annealing(city_coords)
end = time.time()

print(f"Number of cities: {len(city_coords)}")
print(f"Best distance found: {best_distance:.4f}")
print(f"Time taken: {end - start:.2f} seconds")

best_order = [city_names[city_coords.index(city)] for city in best_tour]
print("Best route sequence:")
print(" → ".join(best_order))
