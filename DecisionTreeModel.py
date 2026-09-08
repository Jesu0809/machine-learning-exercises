import os
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
)

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
CLASS_LABELS = {0: "Denied", 1: "Approved"}
MAX_DEPTH = 4

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

RANGES = {f: (float(df[f].min()), float(df[f].max())) for f in FEATURES}


def classify(values):
    row = pd.DataFrame([[values[f] for f in FEATURES]], columns=FEATURES)
    predicted_class = int(model.predict(row)[0])
    probability = float(model.predict_proba(row)[0][1])
    return {
        "input": {f: float(values[f]) for f in FEATURES},
        "predictedClass": predicted_class,
        "label": CLASS_LABELS[predicted_class],
        "probabilityApproved": probability,
    }


def getModelInfo():
    counts = df[TARGET].value_counts().sort_index()
    return {
        "records": int(len(df)),
        "trainRecords": int(len(X_train)),
        "testRecords": int(len(X_test)),
        "features": FEATURES,
        "featureUnits": FEATURE_UNITS,
        "targetName": TARGET,
        "classLabels": CLASS_LABELS,
        "positiveClass": 1,
        "maxDepth": MAX_DEPTH,
        "treeDepth": int(model.get_depth()),
        "leaves": int(model.get_n_leaves()),
        "featureImportances": {f: float(imp)
                               for f, imp in zip(FEATURES, model.feature_importances_)},
        "ranges": {f: {"min": lo, "max": hi} for f, (lo, hi) in RANGES.items()},
        "classCounts": {int(k): int(v) for k, v in counts.items()},
        "source": "Synthetic dataset generated for this activity "
                  "(data/generate_datasets.py) and read from data/credit_approval.csv.",
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
        "trainAccuracy": float(model.score(X_train, y_train)),
        "testRecords": int(len(y_test)),
    }


_INK = "#e6ecff"
_CLASS0 = "#ff8c8c"
_CLASS1 = "#5cc9f5"
_MARKER = "#ffd166"
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

    for cls, color in ((0, _CLASS0), (1, _CLASS1)):
        subset = df[df[TARGET] == cls]
        ax.scatter(subset[fx], subset[fy], alpha=0.5, s=18, color=color,
                   edgecolors="none", label=f"{cls} = {CLASS_LABELS[cls]}")

    if highlight is not None:
        ax.scatter([highlight[fx]], [highlight[fy]], s=150, color=_MARKER,
                   edgecolors="#1c2450", zorder=5, label="Your input")

    ax.set_title("Credit Card Approval by Debt-to-Income Ratio and Income",
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


def generateConfusionMatrixPlot():
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    fig.patch.set_alpha(0)

    ax.imshow(cm, cmap="Blues")
    ticks = ["0 = Denied", "1 = Approved"]
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


def generateFeatureImportancePlot():
    order = np.argsort(model.feature_importances_)
    labels = [FEATURES[i] for i in order]
    values = model.feature_importances_[order]

    fig, ax = plt.subplots(figsize=(7.5, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.barh(labels, values, color=_CLASS1)
    ax.set_title("Feature importances", color=_INK, fontweight="bold")
    ax.set_xlabel("Importance", color=_INK)
    ax.tick_params(colors=_INK)
    for spine in ax.spines.values():
        spine.set_color(_GRID)
    ax.grid(True, axis="x", color="#ffffff", alpha=0.08)
    fig.tight_layout()
    return _finish(fig)


def generateTreePlot():
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_alpha(0)
    plot_tree(model, feature_names=FEATURES, class_names=["Denied", "Approved"],
              filled=True, rounded=True, impurity=False, fontsize=8, ax=ax)
    fig.tight_layout()
    return _finish(fig)
