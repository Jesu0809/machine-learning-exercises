import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

ANGULAR_DIST_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ml-frontend", "dist", "ml-frontend", "browser"
)

@app.route("/")
@app.route("/<path:filename>")
def home(filename="index.html"):
    return send_from_directory(ANGULAR_DIST_PATH, filename)

@app.route("/template")
def template():
    return render_template("index.html")