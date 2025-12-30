import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "tax_regression_model.pkl")

reg_model = joblib.load(MODEL_PATH)  # ✔ loads pickle safely

def analyze_tax(
    annual_income,
    investment_80c,
    hra,
    prev_tax,
    employment_type,
    extra_80c
):
    employment_encoded = 1 if employment_type.lower() == "salaried" else 0

    features = np.array([[
        annual_income,
        investment_80c,
        hra,
        prev_tax,
        employment_encoded,
        extra_80c,
        0,
        0
    ]])

    predicted_tax = float(reg_model.predict(features)[0])

    lower_tax = predicted_tax * 0.9
    upper_tax = predicted_tax * 1.1

    if prev_tax > predicted_tax:
        risk = min((prev_tax - predicted_tax) / predicted_tax, 1)
        loss = prev_tax - predicted_tax
        status = "You may have overpaid tax and could receive a refund."
    else:
        risk = 0
        loss = 0
        status = "Your tax payment seems reasonable."

    MAX_80C = 150000
    used = investment_80c + extra_80c
    remaining = max(0, MAX_80C - used)

    saving = remaining * 0.3
    new_tax = max(predicted_tax - saving, 0)

    suggestions = []
    if remaining > 0:
        suggestions.append(f"You can invest ₹{remaining} more under Section 80C.")
    if hra == 0 and employment_type.lower() == "salaried":
        suggestions.append("You may be eligible for HRA exemption.")
    if prev_tax > predicted_tax:
        suggestions.append("You should consider filing for a refund.")

    return {
        "predicted_tax": round(predicted_tax, 2),
        "tax_range": {
            "min": round(lower_tax, 2),
            "max": round(upper_tax, 2)
        },
        "overpayment_risk": round(risk * 100, 2),
        "estimated_loss": round(loss, 2),
        "status_message": status,
        "what_if": {
            "extra_80c": remaining,
            "new_tax": round(new_tax, 2),
            "tax_saving": round(saving, 2)
        },
        "suggestions": suggestions
    }
