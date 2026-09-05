import os
import math
from flask import Flask, jsonify, request, send_from_directory, Response
import LinearRegression

app = Flask(__name__)

ANGULAR_DIST_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ml-frontend", "dist", "ml-frontend", "browser"
)

@app.route("/api/predict-salary", methods=["POST"])
def predict_salary():
    data = request.get_json(silent=True) or {}
    try:
        years = float(data["years"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "A numeric 'years' value is required."}), 400

    result = LinearRegression.calculateSalary(years)
    info = LinearRegression.getModelInfo()
    return jsonify({
        "result": round(float(result), 2),
        "years": years,
        "slope": info["slope"],
        "intercept": info["intercept"],
        "equation": info["equation"],
        "withinRange": info["xMin"] <= years <= info["xMax"],
        "xMin": info["xMin"],
        "xMax": info["xMax"],
    })

@app.route("/api/model-info", methods=["GET"])
def model_info():
    return jsonify(LinearRegression.getModelInfo())

@app.route("/api/regression-plot")
def regression_plot():
    predict_raw = request.args.get("predict")
    predict_x = None
    if predict_raw not in (None, ""):
        try:
            predict_x = float(predict_raw)
        except ValueError:
            predict_x = None
    image_bytes = LinearRegression.generateRegressionPlot(predict_x)
    return Response(image_bytes, mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

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

@app.route("/")
@app.route("/<path:filename>")
def home(filename="index.html"):
    file_path = os.path.join(ANGULAR_DIST_PATH, filename)
    if filename != "index.html" and not os.path.isfile(file_path):
        filename = "index.html"
    return send_from_directory(ANGULAR_DIST_PATH, filename)