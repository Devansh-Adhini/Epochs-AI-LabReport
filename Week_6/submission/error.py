import numpy as np

def to_bipolar(x):
    return np.where(x == 0, -1, 1)


def to_binary(x):
    return np.where(x == -1, 0, 1)


def train_net(patts):
    n = patts[0].size
    w = np.zeros((n, n))
    for p in patts:
        v = p.reshape(-1, 1)
        w += v @ v.T
    np.fill_diagonal(w, 0)
    return w / len(patts)


def recall(w, x, steps=200):
    s = x.copy()
    n = s.size
    for _ in range(steps):
        for i in range(n):
            s[i] = 1 if np.dot(w[i], s) >= 0 else -1
    return s


def main():
    side = 6
    size = side * side
    num = 10

    stored = [to_bipolar(np.random.randint(0, 2, size)) for _ in range(num)]
    w = train_net(stored)

    for idx, pat in enumerate(stored, 1):
        noisy = pat.copy()
        flips = np.random.choice(size, int(0.2 * size), replace=False)
        noisy[flips] *= -1

        out = recall(w, noisy)

        print(f"\ncase {idx}")
        print("original:")
        print(to_binary(pat.reshape(side, side)))
        print("noisy:")
        print(to_binary(noisy.reshape(side, side)))
        print("recalled:")
        print(to_binary(out.reshape(side, side)))

        if np.array_equal(out, pat):
            print("status: corrected")
        else:
            print("status: failed")

if __name__ == "__main__":
    main()
