import numpy as np
import matplotlib.pyplot as plt

def to_bipolar(x):
    return np.where(x == 0, -1, 1)


def to_binary(x):
    return np.where(x == -1, 0, 1)


def hopfield_train(patterns):
    n = patterns[0].size
    w = np.zeros((n, n))
    for p in patterns:
        p = p.reshape(-1, 1)
        w += p @ p.T
    np.fill_diagonal(w, 0)
    return w / len(patterns)


def hopfield_recall(w, x, steps=100):
    s = x.copy()
    n = s.size
    for _ in range(steps):
        for i in range(n):
            s[i] = 1 if np.dot(w[i], s) >= 0 else -1
    return s


def run_capacity_test():
    neurons = 100
    max_p = 30
    size = (10, 10)
    rates = []

    for p_count in range(1, max_p + 1):
        pats = [to_bipolar(np.random.randint(0, 2, size).flatten()) for _ in range(p_count)]
        w = hopfield_train(pats)

        ok = 0
        for p in pats:
            noisy = p.copy()
            k = int(0.1 * neurons)
            idx = np.random.choice(neurons, k, replace=False)
            noisy[idx] *= -1
            out = hopfield_recall(w, noisy)
            if np.array_equal(out, p):
                ok += 1

        rates.append(ok / p_count)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_p + 1), rates, marker="o")
    plt.axvline(x=int(0.15 * neurons), color="red", linestyle="--", label="capacity")
    plt.title("hopfield network capacity")
    plt.xlabel("stored patterns")
    plt.ylabel("success rate")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    run_capacity_test()
