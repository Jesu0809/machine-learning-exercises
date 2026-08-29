import os
from flask import Flask, jsonify, render_template, request, send_from_directory
import LinearRegression

app = Flask(__name__)

ANGULAR_DIST_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ml-frontend", "dist", "ml-frontend", "browser"
)

@app.route("/api/predict-grade", methods=["POST"])
def predict_grade():
    data = request.get_json()
    hours = float(data["hours"])
    result = LinearRegression.calculateGrade(hours)
    return jsonify({"result": round(float(result), 2)})

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