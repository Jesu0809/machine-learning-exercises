import os
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
)

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "loan_default.csv")
df = pd.read_csv(CSV_PATH)

FEATURE = "debt_to_income_ratio"
TARGET = "defaulted"
CLASS_LABELS = {0: "Low Risk (repaid on time)", 1: "High Risk (defaulted)"}

X = df[[FEATURE]]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

X_MIN = float(df[FEATURE].min())
X_MAX = float(df[FEATURE].max())


def classify(ratio_value):
    features = pd.DataFrame({FEATURE: [ratio_value]})
    scaled = scaler.transform(features)
    predicted_class = int(model.predict(scaled)[0])
    probability = float(model.predict_proba(scaled)[0][1])
    return {
        "input": float(ratio_value),
        "predictedClass": predicted_class,
        "label": CLASS_LABELS[predicted_class],
        "probabilityHighRisk": probability,
        "withinRange": X_MIN <= ratio_value <= X_MAX,
    }


def getModelInfo():
    counts = df[TARGET].value_counts().sort_index()
    return {
        "records": int(len(df)),
        "trainRecords": int(len(X_train)),
        "testRecords": int(len(X_test)),
        "featureName": FEATURE,
        "featureUnit": "%",
        "targetName": TARGET,
        "classLabels": CLASS_LABELS,
        "positiveClass": 1,
        "coefficient": float(model.coef_[0][0]),
        "intercept": float(model.intercept_[0]),
        "threshold": 0.5,
        "xMin": X_MIN,
        "xMax": X_MAX,
        "xMean": float(df[FEATURE].mean()),
        "classCounts": {int(k): int(v) for k, v in counts.items()},
        "source": "Synthetic dataset generated for this activity "
                  "(data/generate_datasets.py) and read from data/loan_default.csv.",
    }


def getMetrics():
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return {
        "confusionMatrix": {
            "trueNegatives": int(tn),
            "falsePositives": int(fp),
            "falseNegatives": int(fn),
            "truePositives": int(tp),
        },
        "matrix": cm.tolist(),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1Score": float(f1_score(y_test, y_pred, zero_division=0)),
        "testRecords": int(len(y_test)),
    }


_INK = "#e6ecff"
_ACCENT = "#21d4e8"
_CLASS0 = "#5cc9f5"
_CLASS1 = "#ff8c8c"
_MARKER = "#ffd166"
_GRID = "#5a6a99"


def _finish(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", transparent=True, dpi=110)
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def generateScatterPlot(predict_x=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for cls, color in ((0, _CLASS0), (1, _CLASS1)):
        subset = df[df[TARGET] == cls]
        jitter = np.random.default_rng(cls).uniform(-0.04, 0.04, len(subset))
        ax.scatter(subset[FEATURE], np.full(len(subset), cls) + jitter,
                   alpha=0.5, s=18, color=color, edgecolors="none",
                   label=f"{cls} = {CLASS_LABELS[cls]}")

    grid = pd.DataFrame({FEATURE: np.linspace(X_MIN, X_MAX, 200)})
    proba = model.predict_proba(scaler.transform(grid))[:, 1]
    ax.plot(grid[FEATURE], proba, color=_ACCENT, linewidth=2.5, label="P(High Risk)")
    ax.axhline(0.5, color=_GRID, linestyle="--", linewidth=1, alpha=0.7)

    if predict_x is not None:
        p = model.predict_proba(
            scaler.transform(pd.DataFrame({FEATURE: [predict_x]})))[0][1]
        ax.scatter([predict_x], [p], s=120, color=_MARKER, edgecolors="#1c2450",
                   zorder=5, label=f"Your input ({predict_x:g}%)")

    ax.set_title("Loan Default Risk by Debt-to-Income Ratio",
                 color=_INK, fontweight="bold")
    ax.set_xlabel("Debt-to-income ratio (%)", color=_INK)
    ax.set_ylabel("Class  /  P(High Risk)", color=_INK)
    ax.set_yticks([0, 0.5, 1])
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK, fontsize=8)
    fig.tight_layout()
    return _finish(fig)


def generateConfusionMatrixPlot():
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    fig.patch.set_alpha(0)

    ax.imshow(cm, cmap="Blues")
    ticks = ["0 = Low Risk", "1 = High Risk"]
    ax.set_xticks([0, 1], labels=ticks)
    ax.set_yticks([0, 1], labels=ticks)
    ax.set_xlabel("Predicted", color=_INK, fontweight="bold")
    ax.set_ylabel("Actual", color=_INK, fontweight="bold")
    ax.set_title("Confusion Matrix (20% test set)", color=_INK, fontweight="bold")
    ax.tick_params(colors=_INK)

    cell_names = [["TN", "FP"], ["FN", "TP"]]
    thresh = cm.max() / 2
    for i in range(2):
        for j in range(2):
            color = "#ffffff" if cm[i, j] > thresh else "#1c2450"
            ax.text(j, i, f"{cell_names[i][j]}\n{cm[i, j]}", ha="center", va="center",
                    color=color, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    return _finish(fig)


def generateSigmoidPlot():
    z = np.linspace(-8, 8, 200)
    s = 1.0 / (1.0 + np.exp(-z))

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.plot(z, s, color=_ACCENT, linewidth=2.5)
    ax.axhline(0.5, color=_MARKER, linestyle="--", linewidth=1.2, label="Threshold = 0.5")
    ax.axvline(0, color=_GRID, linewidth=1, alpha=0.6)

    ax.set_title("Sigmoid function:  p = 1 / (1 + e^-z)", color=_INK, fontweight="bold")
    ax.set_xlabel("z  (linear combination of the inputs)", color=_INK)
    ax.set_ylabel("Probability of class 1", color=_INK)
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, color="#ffffff", alpha=0.08)
    ax.legend(facecolor="#1c2450", edgecolor=_GRID, labelcolor=_INK)
    fig.tight_layout()
    return _finish(fig)
