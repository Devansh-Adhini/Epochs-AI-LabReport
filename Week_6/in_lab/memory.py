import numpy as np

def to_bipolar(x):
    return np.where(x == 0, -1, 1)


def to_binary(x):
    return np.where(x == -1, 0, 1)


def hopfield_train(patts):
    n = patts[0].size
    w = np.zeros((n, n))
    for p in patts:
        v = p.reshape(-1, 1)
        w += v @ v.T
    np.fill_diagonal(w, 0)
    return w / len(patts)


def hopfield_recall(w, x, steps=100):
    s = x.copy()
    n = s.size
    for _ in range(steps):
        for i in range(n):
            s[i] = 1 if np.dot(w[i], s) >= 0 else -1
    return s


if __name__ == "__main__":
    raw = [np.random.randint(0, 2, (10, 10)) for _ in range(3)]
    patts = [to_bipolar(r.flatten()) for r in raw]

    w = hopfield_train(patts)

    noisy = raw[0].copy()
    noisy[0, 0] = 1 - noisy[0, 0]
    noisy_vec = to_bipolar(noisy.flatten())

    out = hopfield_recall(w, noisy_vec)
    out_bin = to_binary(out.reshape(10, 10))

    print("original:")
    print(raw[0])
    print("\nnoisy:")
    print(noisy)
    print("\nrecalled:")
    print(out_bin)
