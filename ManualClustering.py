import os
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "credit_risk_manual.csv")
df = pd.read_csv(CSV_PATH)

FEATURE_X = "debt_to_income_ratio"
FEATURE_Y = "annual_income_k"
CLUSTER_NAMES = {0: "Low risk", 1: "Moderate risk", 2: "High risk"}
K = 3
N_ITERATIONS = 3

POINTS = df[[FEATURE_X, FEATURE_Y]].to_numpy()

INITIAL_CENTROIDS = np.array([
    [15.0, 150.0],
    [35.0, 90.0],
    [55.0, 35.0],
])


def _distances(points, centroids):
    return np.array([[float(np.linalg.norm(p - c)) for c in centroids] for p in points])


def _assign(distances):
    return np.argmin(distances, axis=1)


def _update_centroids(points, assignment, previous_centroids):
    new_centroids = previous_centroids.copy()
    for k in range(K):
        members = points[assignment == k]
        if len(members) > 0:
            new_centroids[k] = members.mean(axis=0)
    return new_centroids


def _within_cluster_variance(points, assignment, centroids):
    variance = {}
    for k in range(K):
        members = points[assignment == k]
        if len(members) > 0:
            variance[k] = float(np.mean(np.sum((members - centroids[k]) ** 2, axis=1)))
        else:
            variance[k] = 0.0
    return variance


def _run_iterations():
    centroids = INITIAL_CENTROIDS.copy()
    history = []
    for i in range(N_ITERATIONS):
        distances = _distances(POINTS, centroids)
        assignment = _assign(distances)
        new_centroids = _update_centroids(POINTS, assignment, centroids)
        variance = _within_cluster_variance(POINTS, assignment, new_centroids)
        history.append({
            "iteration": i + 1,
            "centroidsBefore": centroids.copy(),
            "distances": distances,
            "assignment": assignment,
            "centroidsAfter": new_centroids.copy(),
            "variance": variance,
        })
        centroids = new_centroids
    return history


HISTORY = _run_iterations()


def getContext():
    return {
        "records": int(len(df)),
        "featureX": FEATURE_X,
        "featureXUnit": "%",
        "featureY": FEATURE_Y,
        "featureYUnit": "thousand USD",
        "k": K,
        "iterations": N_ITERATIONS,
        "clusterNames": CLUSTER_NAMES,
        "source": "Synthetic dataset generated for this activity "
                  "(data/generate_datasets.py) and read from data/credit_risk_manual.csv.",
    }


def getInitialCentroids():
    return [
        {"cluster": k, FEATURE_X: float(c[0]), FEATURE_Y: float(c[1])}
        for k, c in enumerate(INITIAL_CENTROIDS)
    ]


def getIteration(n):
    h = HISTORY[n - 1]
    records = []
    for i in range(len(POINTS)):
        records.append({
            "index": i,
            FEATURE_X: float(POINTS[i][0]),
            FEATURE_Y: float(POINTS[i][1]),
            "distanceToCluster0": float(h["distances"][i][0]),
            "distanceToCluster1": float(h["distances"][i][1]),
            "distanceToCluster2": float(h["distances"][i][2]),
            "assignedCluster": int(h["assignment"][i]),
        })
    return {
        "iteration": n,
        "records": records,
        "centroidsBefore": [
            {"cluster": k, FEATURE_X: float(c[0]), FEATURE_Y: float(c[1])}
            for k, c in enumerate(h["centroidsBefore"])
        ],
        "centroidsAfter": [
            {"cluster": k, "name": CLUSTER_NAMES[k], FEATURE_X: float(c[0]), FEATURE_Y: float(c[1])}
            for k, c in enumerate(h["centroidsAfter"])
        ],
        "variance": {int(k): v for k, v in h["variance"].items()},
        "clusterSizes": {
            int(k): int(np.sum(h["assignment"] == k)) for k in range(K)
        },
    }


def getVarianceComparison():
    return {
        "iterations": [h["iteration"] for h in HISTORY],
        "varianceByCluster": {
            int(k): [h["variance"][k] for h in HISTORY] for k in range(K)
        },
        "totalVariance": [float(sum(h["variance"].values())) for h in HISTORY],
    }


_INK = "#e6ecff"
_CLUSTER_COLORS = ["#5cc9f5", "#ffd166", "#ff8c8c"]
_MARKER = "#ffffff"
_GRID = "#5a6a99"


def _finish(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", transparent=True, dpi=110)
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def generateInitialPlot():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.scatter(POINTS[:, 0], POINTS[:, 1], alpha=0.6, s=26, color="#8b7fd6",
               edgecolors="none", label="Records")
    ax.scatter(INITIAL_CENTROIDS[:, 0], INITIAL_CENTROIDS[:, 1], marker="X", s=220,
               color=_MARKER, edgecolors="#1c2450", linewidths=1.5, zorder=5,
               label="Initial centroids")

    ax.set_title("Initial Data and Centroids", color=_INK, fontweight="bold")
    ax.set_xlabel("Debt-to-income ratio (%)", color=_INK)
    ax.set_ylabel("Annual income (thousand USD)", color=_INK)
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK, fontsize=8)
    fig.tight_layout()
    return _finish(fig)


def generateIterationPlot(n):
    h = HISTORY[n - 1]
    assignment = h["assignment"]
    centroids = h["centroidsAfter"]

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for k in range(K):
        members = POINTS[assignment == k]
        ax.scatter(members[:, 0], members[:, 1], alpha=0.6, s=26,
                   color=_CLUSTER_COLORS[k], edgecolors="none",
                   label=f"{k} = {CLUSTER_NAMES[k]}")

    ax.scatter(centroids[:, 0], centroids[:, 1], marker="X", s=220, color=_MARKER,
               edgecolors="#1c2450", linewidths=1.5, zorder=5, label="Updated centroids")

    ax.set_title(f"Iteration {n}: Assignments and Updated Centroids",
                 color=_INK, fontweight="bold")
    ax.set_xlabel("Debt-to-income ratio (%)", color=_INK)
    ax.set_ylabel("Annual income (thousand USD)", color=_INK)
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK, fontsize=8)
    fig.tight_layout()
    return _finish(fig)


def generateVariancePlot():
    comp = getVarianceComparison()

    fig, ax = plt.subplots(figsize=(7, 4.2))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for k in range(K):
        ax.plot(comp["iterations"], comp["varianceByCluster"][k], marker="o",
               color=_CLUSTER_COLORS[k], linewidth=2, label=f"{k} = {CLUSTER_NAMES[k]}")
    ax.plot(comp["iterations"], comp["totalVariance"], marker="s", linestyle="--",
           color=_INK, linewidth=1.5, label="Total")

    ax.set_title("Within-Cluster Variance Across Iterations", color=_INK, fontweight="bold")
    ax.set_xlabel("Iteration", color=_INK)
    ax.set_ylabel("Within-cluster variance", color=_INK)
    ax.set_xticks(comp["iterations"])
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK, fontsize=8)
    fig.tight_layout()
    return _finish(fig)
