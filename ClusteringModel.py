import os
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "credit_approval.csv")
df = pd.read_csv(CSV_PATH)

FEATURES = ["annual_income", "debt_to_income_ratio",
            "credit_history_length", "open_credit_lines"]
FEATURE_UNITS = {
    "annual_income": "USD",
    "debt_to_income_ratio": "%",
    "credit_history_length": "years",
    "open_credit_lines": "count",
}
TARGET = "approved"
K = 3
CLUSTER_NAMES = {
    0: "Low risk / established credit",
    1: "Moderate risk / building credit",
    2: "High risk / overextended",
}

X = df[FEATURES]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = KMeans(n_clusters=K, random_state=42, n_init=10)
raw_labels = model.fit_predict(X_scaled)

centroids_original = scaler.inverse_transform(model.cluster_centers_)


_FEATURE_RANGES = {f: (float(df[f].min()), float(df[f].max())) for f in FEATURES}


def _normalize(feature, value):
    lo, hi = _FEATURE_RANGES[feature]
    return (value - lo) / (hi - lo)


def _risk_score(centroid):
    income, dti, history, lines = centroid
    return (2.0 * _normalize("debt_to_income_ratio", dti)
            - 1.5 * _normalize("annual_income", income)
            - 1.0 * _normalize("credit_history_length", history)
            + 0.8 * _normalize("open_credit_lines", lines))


# KMeans assigns cluster ids in arbitrary order, so the ids are re-ranked
# by a simple risk score to keep 0 = lowest risk regardless of fit order.
risk_order = np.argsort([_risk_score(c) for c in centroids_original])
rank_of_raw_label = {int(raw): rank for rank, raw in enumerate(risk_order)}

df = df.copy()
df["cluster"] = [rank_of_raw_label[int(label)] for label in raw_labels]
centroids_ranked = centroids_original[risk_order]

SILHOUETTE = float(silhouette_score(X_scaled, raw_labels))


def predict(values):
    row = pd.DataFrame([[values[f] for f in FEATURES]], columns=FEATURES)
    scaled = scaler.transform(row)
    raw_label = int(model.predict(scaled)[0])
    cluster = rank_of_raw_label[raw_label]
    distance = float(np.linalg.norm(scaled[0] - model.cluster_centers_[raw_label]))
    return {
        "input": {f: float(values[f]) for f in FEATURES},
        "cluster": cluster,
        "clusterName": CLUSTER_NAMES[cluster],
        "distanceToCentroid": distance,
    }


def getModelInfo():
    sizes = df["cluster"].value_counts().sort_index()
    return {
        "records": int(len(df)),
        "features": FEATURES,
        "featureUnits": FEATURE_UNITS,
        "k": K,
        "clusterNames": {int(k): v for k, v in CLUSTER_NAMES.items()},
        "clusterSizes": {int(k): int(v) for k, v in sizes.items()},
        "centroids": {
            int(cluster): {f: float(val) for f, val in zip(FEATURES, centroid)}
            for cluster, centroid in enumerate(centroids_ranked)
        },
        "silhouetteScore": SILHOUETTE,
        "inertia": float(model.inertia_),
        "source": "Same synthetic dataset used by the Decision Tree activity "
                  "(data/generate_datasets.py), read from data/credit_approval.csv, "
                  "clustered without using the 'approved' column.",
    }


def getMetrics():
    sizes = df["cluster"].value_counts().sort_index()
    total = int(len(df))
    approval_rate = df.groupby("cluster")[TARGET].mean().sort_index()
    return {
        "inertia": float(model.inertia_),
        "silhouetteScore": SILHOUETTE,
        "clusterSizes": {int(k): int(v) for k, v in sizes.items()},
        "clusterPercentages": {int(k): float(v) / total for k, v in sizes.items()},
        "approvalRateByCluster": {int(k): float(v) for k, v in approval_rate.items()},
        "clusterNames": {int(k): v for k, v in CLUSTER_NAMES.items()},
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


def generateScatterPlot(highlight=None):
    fx, fy = "debt_to_income_ratio", "annual_income"
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for cluster in range(K):
        subset = df[df["cluster"] == cluster]
        ax.scatter(subset[fx], subset[fy], alpha=0.5, s=18,
                   color=_CLUSTER_COLORS[cluster], edgecolors="none",
                   label=f"{cluster} = {CLUSTER_NAMES[cluster]}")

    fx_i, fy_i = FEATURES.index(fx), FEATURES.index(fy)
    ax.scatter(centroids_ranked[:, fx_i], centroids_ranked[:, fy_i],
               marker="X", s=180, color=_MARKER, edgecolors="#1c2450",
               linewidths=1.5, zorder=5, label="Centroids")

    if highlight is not None:
        ax.scatter([highlight[fx]], [highlight[fy]], s=150, color="#21d4e8",
                   edgecolors="#1c2450", zorder=6, label="Your input")

    ax.set_title("Credit Applicants Segmented by K-Means (k=3)",
                 color=_INK, fontweight="bold")
    ax.set_xlabel("Debt-to-income ratio (%)", color=_INK)
    ax.set_ylabel("Annual income (USD)", color=_INK)
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK, fontsize=8)
    fig.tight_layout()
    return _finish(fig)


def generateElbowPlot():
    ks = range(1, 9)
    inertias = []
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.plot(list(ks), inertias, color="#5cc9f5", marker="o", linewidth=2)
    ax.axvline(K, color="#ffd166", linestyle="--", linewidth=1.2, label=f"Chosen k = {K}")

    ax.set_title("Elbow Method: Inertia vs. Number of Clusters",
                 color=_INK, fontweight="bold")
    ax.set_xlabel("Number of clusters (k)", color=_INK)
    ax.set_ylabel("Inertia (within-cluster sum of squares)", color=_INK)
    ax.set_xticks(list(ks))
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK)
    fig.tight_layout()
    return _finish(fig)
