import numpy as np

def is_valid(x):
    return np.all(np.sum(x, axis=0) == 1) and np.all(np.sum(x, axis=1) == 1)


def fix_rows(x):
    n = x.shape[0]
    for i in range(n):
        s = np.sum(x[i])
        if s == 0:
            j = np.random.randint(n)
            x[i, j] = 1
        elif s > 1:
            ones = np.where(x[i] == 1)[0]
            keep = np.random.choice(ones)
            x[i] = np.zeros(n)
            x[i, keep] = 1
    return x


def fix_cols(x):
    n = x.shape[0]
    for j in range(n):
        s = np.sum(x[:, j])
        if s == 0:
            i = np.random.randint(n)
            x[i, j] = 1
        elif s > 1:
            ones = np.where(x[:, j] == 1)[0]
            keep = np.random.choice(ones)
            x[:, j] = np.zeros(n)
            x[keep, j] = 1
    return x


def eight_rook(n=8, steps=300):
    state = np.zeros((n, n), dtype=int)
    pos = np.random.choice(n*n, n, replace=False)
    state.flat[pos] = 1

    print("initial:")
    print(state)

    for t in range(steps):
        new = state.copy()

        for i in range(n):
            for j in range(n):
                r = np.sum(state[i]) - state[i, j]
                c = np.sum(state[:, j]) - state[i, j]
                s = -(r + c)
                new[i, j] = 1 if s > 0 else 0

        new = fix_rows(new)
        new = fix_cols(new)

        if is_valid(new):
            print("final:")
            print(new)
            print("status: valid")
            return new

        if np.array_equal(new, state):
            break

        state = new

    print("final:")
    print(state)
    print("status:", "valid" if is_valid(state) else "invalid")
    return state


if __name__ == "__main__":
    np.random.seed(26)
    eight_rook()