import os
from flask import Flask, jsonify, render_template, request, send_from_directory
import LinearRegression

app = Flask(__name__)

ANGULAR_DIST_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ml-frontend", "dist", "ml-frontend", "browser"
)

@app.route("/template")
def template():
    return render_template("index.html")

@app.route("/api/predict-salary", methods=["POST"])
def predict_salary():
    data = request.get_json()
    years = float(data["years"])
    result = LinearRegression.calculateSalary(years)
    return jsonify({"result": round(float(result), 2)})


@app.route("/")
@app.route("/<path:filename>")
def home(filename="index.html"):
    file_path = os.path.join(ANGULAR_DIST_PATH, filename)
    if filename != "index.html" and not os.path.isfile(file_path):
        filename = "index.html"
    return send_from_directory(ANGULAR_DIST_PATH, filename)