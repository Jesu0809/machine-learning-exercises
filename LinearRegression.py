import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from sklearn.linear_model import LinearRegression

# scikit-learn

data = {
    "Years of Experience": [10, 15, 12, 8, 14, 5, 16, 7, 11, 13, 9, 4, 18, 3, 17, 6, 14, 2, 20, 1],
    "Monthly Salary (COP)": [9200000, 13200000, 10700000, 7900000, 12150000, 5600000, 13600000, 7200000, 10000000, 11700000, 8500000, 4900000, 15200000, 4000000, 14700000, 6200000, 12350000, 3400000, 16500000, 2500000]
}

df = pd.DataFrame(data)

x = df[["Years of Experience"]]
y = df["Monthly Salary (COP)"]

model = LinearRegression()
model.fit(x, y)

def calculateSalary(years):
    result = model.predict([[years]])[0]
    return result