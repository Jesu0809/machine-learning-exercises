"""
Reproducible generator for the Activity 2 classification datasets.

Run from the project root:

    python data/generate_datasets.py

It writes two CSV files next to this script:

  * loan_default.csv     -> Logistic Regression  (1 independent variable)
  * credit_approval.csv  -> Decision Tree         (4 independent variables)

Both datasets are synthetic. Each target is drawn from a probability that
depends on the features through a sigmoid, so the relationship is real
(not hand-labeled) but no row is hard-coded. The fixed random seed makes
the output identical on every run.
"""

import os
import numpy as np
import pandas as pd

SEED = 42
N_LOAN = 600
N_CREDIT = 600
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def make_loan_default(rng):
    """Loan Default Risk Prediction.

    X: debt-to-income ratio (%)  -> monthly debt payments / monthly income * 100
    y: defaulted (0 = repaid on time, 1 = defaulted)

    Higher debt-to-income ratio -> higher probability of default.
    """
    dti = np.round(rng.uniform(5.0, 65.0, N_LOAN), 1)

    # 50/50 point around a 38% ratio; slope controls how separable the classes are.
    z = 0.18 * (dti - 38.0)
    prob_default = sigmoid(z)
    defaulted = rng.binomial(1, prob_default)

    df = pd.DataFrame({
        "debt_to_income_ratio": dti,
        "defaulted": defaulted,
    })
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


def make_credit_approval(rng):
    """Credit Card Application Approval.

    X: annual_income (USD), debt_to_income_ratio (%),
       credit_history_length (years), open_credit_lines (count)
    y: approved (0 = denied, 1 = approved)

    Approved when income and credit history are high and the
    debt-to-income ratio and number of open lines are low.
    """
    annual_income = np.round(rng.uniform(15000, 180000, N_CREDIT), 0)
    dti = np.round(rng.uniform(5.0, 65.0, N_CREDIT), 1)
    history = np.round(rng.uniform(0.0, 30.0, N_CREDIT), 1)
    open_lines = rng.integers(0, 16, N_CREDIT)

    # Normalise each feature to roughly [0, 1] before combining.
    income_n = (annual_income - 15000) / (180000 - 15000)
    dti_n = (dti - 5.0) / (65.0 - 5.0)
    history_n = history / 30.0
    lines_n = open_lines / 15.0

    score = (2.6 * income_n
             - 3.0 * dti_n
             + 1.8 * history_n
             - 1.6 * lines_n
             - 0.2)
    prob_approved = sigmoid(5.5 * score)
    approved = rng.binomial(1, prob_approved)

    df = pd.DataFrame({
        "annual_income": annual_income.astype(int),
        "debt_to_income_ratio": dti,
        "credit_history_length": history,
        "open_credit_lines": open_lines.astype(int),
        "approved": approved,
    })
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


def main():
    rng = np.random.default_rng(SEED)

    loan = make_loan_default(rng)
    credit = make_credit_approval(rng)

    loan_path = os.path.join(OUT_DIR, "loan_default.csv")
    credit_path = os.path.join(OUT_DIR, "credit_approval.csv")
    loan.to_csv(loan_path, index=False)
    credit.to_csv(credit_path, index=False)

    print(f"loan_default.csv    -> {len(loan)} rows, "
          f"default rate {loan['defaulted'].mean():.1%}")
    print(f"credit_approval.csv -> {len(credit)} rows, "
          f"approval rate {credit['approved'].mean():.1%}")


if __name__ == "__main__":
    main()
