import numpy as np

N = 10
A, B, C = 500, 500, 1
max_iter = 300

np.random.seed(26)
dist = np.random.randint(1, 100, (N, N))
np.fill_diagonal(dist, 0)

state = np.random.randint(0, 2, (N, N))


def fix_rows(x):
    for i in range(N):
        r = np.sum(x[i])
        if r == 0:
            j = np.random.randint(N)
            x[i, j] = 1
        elif r > 1:
            ones = np.where(x[i] == 1)[0]
            keep = np.random.choice(ones)
            x[i] = np.zeros(N)
            x[i, keep] = 1
    return x


def fix_cols(x):
    for j in range(N):
        c = np.sum(x[:, j])
        if c == 0:
            i = np.random.randint(N)
            x[i, j] = 1
        elif c > 1:
            ones = np.where(x[:, j] == 1)[0]
            keep = np.random.choice(ones)
            x[:, j] = np.zeros(N)
            x[keep, j] = 1
    return x


def is_valid(x):
    return np.all(np.sum(x, axis=1) == 1) and np.all(np.sum(x, axis=0) == 1)


def update(x):
    y = x.copy()
    for i in range(N):
        for j in range(N):
            r = np.sum(x[i]) - x[i, j]
            c = np.sum(x[:, j]) - x[i, j]

            s = -A * r - B * c

            nxt = (j - 1) % N
            prv = (j + 1) % N
            s -= C * (np.dot(dist[i], x[:, nxt]) + np.dot(dist[:, i], x[:, prv]))

            y[i, j] = 1 if s < 0 else 0

    y = fix_rows(y)
    y = fix_cols(y)
    return y


print("distance_matrix:")
print(dist)
print()


for t in range(max_iter):
    new = update(state)
    if is_valid(new):
        state = new
        print("final_state:")
        print(state)
        print("\nstatus: valid")
        break

    if np.array_equal(state, new):
        state = new
        print("final_state:")
        print(state)
        print("\nstatus:", "valid" if is_valid(state) else "invalid")
        break

    state = new
