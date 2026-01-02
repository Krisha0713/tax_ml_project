
##  Author
Krishna Priya R
CSE Student | AI/ML Enthusiast

#  Tax Overpayment Risk Analyzer (ML + Flask)

A Machine Learning powered Flask web application that analyzes income tax data, predicts tax liability, detects overpayment risk, and provides personalized tax-saving insights.

---

##  Features

-  ML-based tax prediction using RandomForest
-  Overpayment risk detection
-  Personalized tax-saving suggestions
-  Interactive charts (Chart.js)
-  Dark / Light mode toggle
-  What-if analysis for extra 80C investments
-  Joblib-based ML model loading

---

##  Project Structure

tax_ml_project/
│
├── backend/
│ ├── app.py
│ ├── model/
│ │ └── tax_model.joblib
│ ├── utils/
│ │ └── predictor.py
│ ├── templates/
│ │ └── index.html
│ └── static/
│ ├── style.css
│ └── dashboard.js
│
├── run.py
└── README.md

---

##  Input Parameters

- Annual Income
- Section 80C Investment
- Extra 80C Investment
- HRA
- Previous Tax Paid
- Employment Type (Salaried / Self-employed)

---

##  Output

- Predicted Tax
- Overpayment Risk (%)
- Estimated Refund Amount
- Tax Uncertainty Range
- Personalized Insights
- Interactive Risk Chart

---

##  Tech Stack

- Python
- Flask
- Scikit-learn
- Joblib
- HTML / CSS / JavaScript
- Chart.js

---

##  How to Run

### 1️⃣ Install dependencies
```bash
pip install flask flask-cors scikit-learn joblib
python run.py
