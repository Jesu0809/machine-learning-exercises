import os
import math
from flask import Flask, jsonify, render_template, request, send_from_directory, Response
import LinearRegression

app = Flask(__name__)

ANGULAR_DIST_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ml-frontend", "dist", "ml-frontend", "browser"
)

@app.route("/api/predict-salary", methods=["POST"])
def predict_salary():
    data = request.get_json()
    years = float(data["years"])
    result = LinearRegression.calculateSalary(years)
    return jsonify({"result": round(float(result), 2)})

@app.route("/api/regression-plot")
def regression_plot():
    image_bytes = LinearRegression.generateRegressionPlot()
    return Response(image_bytes, mimetype="image/png")

@app.route("/api/salary-data", methods=["GET"])
def salary_data():
    df = LinearRegression.df
    total_records = len(df)

    limit = int(request.args.get("limit", 20))
    limit = max(1, limit)

    total_pages = max(1, math.ceil(total_records / limit))

    page = int(request.args.get("page", 1))
    page = max(1, min(page, total_pages))

    start = (page - 1) * limit
    end = start + limit
    page_df = df.iloc[start:end]

    records = [
        {"years": row["Years of Experience"], "salary": row["Monthly Salary (COP)"]}
        for _, row in page_df.iterrows()
    ]

    return jsonify({
        "records": records,
        "page": page,
        "limit": limit,
        "totalRecords": total_records,
        "totalPages": total_pages
    })

@app.route("/template")
def template():
    return render_template("index.html")

@app.route("/")
@app.route("/<path:filename>")
def home(filename="index.html"):
    file_path = os.path.join(ANGULAR_DIST_PATH, filename)
    if filename != "index.html" and not os.path.isfile(file_path):
        filename = "index.html"
    return send_from_directory(ANGULAR_DIST_PATH, filename)