import os
import math
from flask import Flask, jsonify, request, send_from_directory, Response
import LinearRegression
import LogisticRegressionModel
import DecisionTreeModel
import ClusteringModel
<<<<<<< HEAD
=======
import ManualClustering
>>>>>>> 88e3dfa369317a2a4c101b82685973e7d47ca7fc

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

@app.route("/api/logreg/classify", methods=["POST"])
def logreg_classify():
    data = request.get_json(silent=True) or {}
    try:
        ratio = float(data["ratio"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "A numeric 'ratio' value is required."}), 400
    return jsonify(LogisticRegressionModel.classify(ratio))

@app.route("/api/logreg/model-info", methods=["GET"])
def logreg_model_info():
    return jsonify(LogisticRegressionModel.getModelInfo())

@app.route("/api/logreg/metrics", methods=["GET"])
def logreg_metrics():
    return jsonify(LogisticRegressionModel.getMetrics())

@app.route("/api/logreg/scatter-plot")
def logreg_scatter_plot():
    predict_raw = request.args.get("predict")
    predict_x = None
    if predict_raw not in (None, ""):
        try:
            predict_x = float(predict_raw)
        except ValueError:
            predict_x = None
    image_bytes = LogisticRegressionModel.generateScatterPlot(predict_x)
    return Response(image_bytes, mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/logreg/confusion-plot")
def logreg_confusion_plot():
    image_bytes = LogisticRegressionModel.generateConfusionMatrixPlot()
    return Response(image_bytes, mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/logreg/sigmoid-plot")
def logreg_sigmoid_plot():
    image_bytes = LogisticRegressionModel.generateSigmoidPlot()
    return Response(image_bytes, mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/logreg/dataset", methods=["GET"])
def logreg_dataset():
    df = LogisticRegressionModel.df
    total_records = len(df)

    limit = int(request.args.get("limit", 20))
    limit = max(1, limit)

    total_pages = max(1, math.ceil(total_records / limit))

    page = int(request.args.get("page", 1))
    page = max(1, min(page, total_pages))

    start = (page - 1) * limit
    page_df = df.iloc[start:start + limit]

    records = [
        {"ratio": row["debt_to_income_ratio"], "defaulted": int(row["defaulted"])}
        for _, row in page_df.iterrows()
    ]

    return jsonify({
        "records": records,
        "page": page,
        "limit": limit,
        "totalRecords": total_records,
        "totalPages": total_pages
    })

TREE_FIELDS = ("annual_income", "debt_to_income_ratio",
               "credit_history_length", "open_credit_lines")

@app.route("/api/tree/classify", methods=["POST"])
def tree_classify():
    data = request.get_json(silent=True) or {}
    try:
        values = {field: float(data[field]) for field in TREE_FIELDS}
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "All four numeric fields are required."}), 400
    return jsonify(DecisionTreeModel.classify(values))

@app.route("/api/tree/model-info", methods=["GET"])
def tree_model_info():
    return jsonify(DecisionTreeModel.getModelInfo())

@app.route("/api/tree/metrics", methods=["GET"])
def tree_metrics():
    return jsonify(DecisionTreeModel.getMetrics())

@app.route("/api/tree/scatter-plot")
def tree_scatter_plot():
    highlight = None
    if all(request.args.get(f) not in (None, "") for f in TREE_FIELDS):
        try:
            highlight = {f: float(request.args.get(f)) for f in TREE_FIELDS}
        except ValueError:
            highlight = None
    image_bytes = DecisionTreeModel.generateScatterPlot(highlight)
    return Response(image_bytes, mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/tree/confusion-plot")
def tree_confusion_plot():
    return Response(DecisionTreeModel.generateConfusionMatrixPlot(),
                    mimetype="image/png", headers={"Cache-Control": "no-store"})

@app.route("/api/tree/importance-plot")
def tree_importance_plot():
    return Response(DecisionTreeModel.generateFeatureImportancePlot(),
                    mimetype="image/png", headers={"Cache-Control": "no-store"})

@app.route("/api/tree/tree-plot")
def tree_tree_plot():
    return Response(DecisionTreeModel.generateTreePlot(),
                    mimetype="image/png", headers={"Cache-Control": "no-store"})

@app.route("/api/tree/dataset", methods=["GET"])
def tree_dataset():
    df = DecisionTreeModel.df
    total_records = len(df)

    limit = int(request.args.get("limit", 20))
    limit = max(1, limit)

    total_pages = max(1, math.ceil(total_records / limit))

    page = int(request.args.get("page", 1))
    page = max(1, min(page, total_pages))

    start = (page - 1) * limit
    page_df = df.iloc[start:start + limit]

    records = [
        {
            "annual_income": int(row["annual_income"]),
            "debt_to_income_ratio": row["debt_to_income_ratio"],
            "credit_history_length": row["credit_history_length"],
            "open_credit_lines": int(row["open_credit_lines"]),
            "approved": int(row["approved"]),
        }
        for _, row in page_df.iterrows()
    ]

    return jsonify({
        "records": records,
        "page": page,
        "limit": limit,
        "totalRecords": total_records,
        "totalPages": total_pages
    })

CLUSTER_FIELDS = ("annual_income", "debt_to_income_ratio",
                  "credit_history_length", "open_credit_lines")

@app.route("/api/clustering/predict", methods=["POST"])
def clustering_predict():
    data = request.get_json(silent=True) or {}
    try:
        values = {field: float(data[field]) for field in CLUSTER_FIELDS}
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "All four numeric fields are required."}), 400
    return jsonify(ClusteringModel.predict(values))

@app.route("/api/clustering/model-info", methods=["GET"])
def clustering_model_info():
    return jsonify(ClusteringModel.getModelInfo())

@app.route("/api/clustering/metrics", methods=["GET"])
def clustering_metrics():
    return jsonify(ClusteringModel.getMetrics())

@app.route("/api/clustering/scatter-plot")
def clustering_scatter_plot():
    highlight = None
    if all(request.args.get(f) not in (None, "") for f in CLUSTER_FIELDS):
        try:
            highlight = {f: float(request.args.get(f)) for f in CLUSTER_FIELDS}
        except ValueError:
            highlight = None
    image_bytes = ClusteringModel.generateScatterPlot(highlight)
    return Response(image_bytes, mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/clustering/elbow-plot")
def clustering_elbow_plot():
    return Response(ClusteringModel.generateElbowPlot(),
                    mimetype="image/png", headers={"Cache-Control": "no-store"})

@app.route("/api/clustering/dataset", methods=["GET"])
def clustering_dataset():
    df = ClusteringModel.df
    total_records = len(df)

    limit = int(request.args.get("limit", 20))
    limit = max(1, limit)

    total_pages = max(1, math.ceil(total_records / limit))

    page = int(request.args.get("page", 1))
    page = max(1, min(page, total_pages))

    start = (page - 1) * limit
    page_df = df.iloc[start:start + limit]

    records = [
        {
            "annual_income": int(row["annual_income"]),
            "debt_to_income_ratio": row["debt_to_income_ratio"],
            "credit_history_length": row["credit_history_length"],
            "open_credit_lines": int(row["open_credit_lines"]),
            "approved": int(row["approved"]),
            "cluster": int(row["cluster"]),
        }
        for _, row in page_df.iterrows()
    ]

    return jsonify({
        "records": records,
        "page": page,
        "limit": limit,
        "totalRecords": total_records,
        "totalPages": total_pages
    })

<<<<<<< HEAD
=======
@app.route("/api/manual-clustering/context", methods=["GET"])
def manual_clustering_context():
    return jsonify(ManualClustering.getContext())

@app.route("/api/manual-clustering/initial-centroids", methods=["GET"])
def manual_clustering_initial_centroids():
    return jsonify(ManualClustering.getInitialCentroids())

@app.route("/api/manual-clustering/iteration/<int:n>", methods=["GET"])
def manual_clustering_iteration(n):
    if n < 1 or n > ManualClustering.N_ITERATIONS:
        return jsonify({"error": f"n must be between 1 and {ManualClustering.N_ITERATIONS}."}), 400
    return jsonify(ManualClustering.getIteration(n))

@app.route("/api/manual-clustering/variance", methods=["GET"])
def manual_clustering_variance():
    return jsonify(ManualClustering.getVarianceComparison())

@app.route("/api/manual-clustering/initial-plot")
def manual_clustering_initial_plot():
    return Response(ManualClustering.generateInitialPlot(), mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/manual-clustering/iteration-plot/<int:n>")
def manual_clustering_iteration_plot(n):
    if n < 1 or n > ManualClustering.N_ITERATIONS:
        return jsonify({"error": f"n must be between 1 and {ManualClustering.N_ITERATIONS}."}), 400
    return Response(ManualClustering.generateIterationPlot(n), mimetype="image/png",
                    headers={"Cache-Control": "no-store"})

@app.route("/api/manual-clustering/variance-plot")
def manual_clustering_variance_plot():
    return Response(ManualClustering.generateVariancePlot(), mimetype="image/png",
                    headers={"Cache-Control": "no-store"})
>>>>>>> 88e3dfa369317a2a4c101b82685973e7d47ca7fc

@app.route("/")
@app.route("/<path:filename>")
def home(filename="index.html"):
    file_path = os.path.join(ANGULAR_DIST_PATH, filename)
    if filename != "index.html" and not os.path.isfile(file_path):
        filename = "index.html"
    return send_from_directory(ANGULAR_DIST_PATH, filename)