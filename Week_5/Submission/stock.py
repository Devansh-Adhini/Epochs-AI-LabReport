import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
from sklearn.mixture import GaussianMixture


def download_stock_data(ticker, start_date="2014-01-01", end_date="2025-12-21", auto_adjust=False):
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=auto_adjust)
    if "Adj Close" in df.columns:
        price_col = "Adj Close"
    elif "Close" in df.columns:
        price_col = "Close"
    else:
        raise RuntimeError("No Close/Adj Close column found")
    data = pd.DataFrame()
    data["price"] = df[price_col]
    data["returns"] = data["price"].pct_change()
    data = data.dropna()
    return data


def fit_gmm(returns, n_states=3, covariance_type="full", random_state=42):
    X = returns.reshape(-1, 1) if returns.ndim == 1 else returns
    gmm = GaussianMixture(n_components=n_states, covariance_type=covariance_type, random_state=random_state, n_init=10)
    gmm.fit(X)
    posteriors = gmm.predict_proba(X)
    states = gmm.predict(X)
    return gmm, states, posteriors


def compute_transition_matrix(states, n_states):
    T = np.zeros((n_states, n_states), dtype=float)
    for a, b in zip(states[:-1], states[1:]):
        T[a, b] += 1
    row_sums = T.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        T = np.divide(T, row_sums, where=(row_sums != 0))
    for i in range(n_states):
        if np.allclose(row_sums[i, 0], 0):
            T[i, i] = 1.0
    return T


def state_durations(states):
    durations = []
    if len(states) == 0:
        return durations
    cur = states[0]
    length = 1
    for s in states[1:]:
        if s == cur:
            length += 1
        else:
            durations.append((int(cur), int(length)))
            cur = s
            length = 1
    durations.append((int(cur), int(length)))
    return durations


def plot_regimes(data, states, figsize=(14, 6)):
    unique_states = np.unique(states)
    colors = ["red", "blue", "green"]
    plt.figure(figsize=figsize)
    for i, st in enumerate(unique_states):
        mask = states == st
        plt.plot(data.index[mask], data["price"][mask], ".", label=f"state_{st}", color=colors[i])
    plt.plot(data.index, data["price"], color="black", linewidth=0.6, alpha=0.3)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()


def summarize_states(data, states, posteriors):
    df = pd.DataFrame({
        "date": data.index,
        "price": data["price"].values,
        "returns": data["returns"].values,
        "state": states
    })
    summary = []
    n_states = posteriors.shape[1]
    for s in range(n_states):
        mask = df["state"] == s
        if mask.sum() == 0:
            summary.append({
                "state": int(s),
                "count": 0,
                "mean_return": np.nan,
                "std_return": np.nan,
                "mean_price": np.nan
            })
            continue
        summary.append({
            "state": int(s),
            "count": int(mask.sum()),
            "mean_return": float(df.loc[mask, "returns"].mean()),
            "std_return": float(df.loc[mask, "returns"].std()),
            "mean_price": float(df.loc[mask, "price"].mean())
        })
    return pd.DataFrame(summary).sort_values("state").reset_index(drop=True)


def predict_next_state_by_transition(last_state, transition_matrix):
    probs = transition_matrix[last_state]
    return np.argmax(probs), probs


def sample_future_prices_from_gmm(gmm, last_price, steps=10, n_paths=1000, seed=26):
    rng = np.random.RandomState(seed)
    means = gmm.means_.flatten()
    covs = gmm.covariances_.reshape(gmm.n_components, -1) if gmm.covariance_type == "full" else gmm.covariances_
    comp_weights = gmm.weights_
    results = np.zeros((n_paths, steps))
    for p in range(n_paths):
        price = last_price
        for t in range(steps):
            k = rng.choice(gmm.n_components, p=comp_weights)
            if gmm.covariance_type == "full":
                var = covs[k].reshape(1, 1)[0, 0]
            else:
                var = covs[k][0, 0]
            ret = rng.normal(means[k, 0], np.sqrt(abs(var)))
            price = price * (1 + ret)
            results[p, t] = price
    return results


def main():
    ticker = "AAPL"
    start_date = "2014-01-01"
    end_date = "2025-12-21"
    n_states = 3
    data = download_stock_data(ticker, start_date, end_date)
    returns = data["returns"].values
    gmm, states, posteriors = fit_gmm(returns, n_states)
    T = compute_transition_matrix(states, n_states)
    durations = state_durations(states)
    summary = summarize_states(data, states, posteriors)
    plot_regimes(data, states)
    print("transition_matrix:")
    print(pd.DataFrame(T))
    print("\nstate_summary:")
    print(summary)
    print("\nrecent_state_durations (last 10):")
    print(durations[-10:])
    last_state = int(states[-1])
    next_state, next_probs = predict_next_state_by_transition(last_state, T)
    print(f"\nlast_state: {last_state}, predicted_next_state_by_transition: {next_state}, probs: {next_probs}")
    sims = sample_future_prices_from_gmm(gmm, last_price=float(data["price"].iloc[-1]), steps=20, n_paths=200)
    median_path = np.median(sims, axis=0)
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(median_path) + 1), median_path)
    plt.title("Median simulated future price path (GMM sampling)")
    plt.xlabel("Days ahead")
    plt.ylabel("Simulated price")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

