from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from backend.utils.predictor import analyze_tax

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json

        result = analyze_tax(
            annual_income=float(data["annual_income"]),
            investment_80c=float(data["investment_80c"]),
            hra=float(data["hra"]),
            prev_tax=float(data["previous_tax"]),
            employment_type=data["employment_type"],
            extra_80c=float(data["extra_80c"])
        )

        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
