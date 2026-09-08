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
    dti = np.round(rng.uniform(5.0, 65.0, N_LOAN), 1)
    z = 0.18 * (dti - 38.0)
    defaulted = rng.binomial(1, sigmoid(z))
    df = pd.DataFrame({
        "debt_to_income_ratio": dti,
        "defaulted": defaulted,
    })
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


def make_credit_approval(rng):
    annual_income = np.round(rng.uniform(15000, 180000, N_CREDIT), 0)
    dti = np.round(rng.uniform(5.0, 65.0, N_CREDIT), 1)
    history = np.round(rng.uniform(0.0, 30.0, N_CREDIT), 1)
    open_lines = rng.integers(0, 16, N_CREDIT)

    income_n = (annual_income - 15000) / (180000 - 15000)
    dti_n = (dti - 5.0) / (65.0 - 5.0)
    history_n = history / 30.0
    lines_n = open_lines / 15.0

    score = (2.6 * income_n
             - 3.0 * dti_n
             + 1.8 * history_n
             - 1.6 * lines_n
             - 0.2)
    approved = rng.binomial(1, sigmoid(5.5 * score))

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
    loan.to_csv(os.path.join(OUT_DIR, "loan_default.csv"), index=False)
    credit.to_csv(os.path.join(OUT_DIR, "credit_approval.csv"), index=False)
    print(len(loan), "rows -> loan_default.csv")
    print(len(credit), "rows -> credit_approval.csv")


if __name__ == "__main__":
    main()
