import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, classification_report
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib
import os

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tax_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATA_PATH)

# -----------------------------
# FEATURES & TARGETS
# -----------------------------
X = df.drop(columns=["Effective_Tax_Paid", "Overpayment_Risk"])

y_reg = df["Effective_Tax_Paid"]
y_clf = df["Overpayment_Risk"]

# -----------------------------
# TRAIN-TEST SPLIT (CORRECT)
# -----------------------------
X_train, X_test, y_reg_train, y_reg_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

_, _, y_clf_train, y_clf_test = train_test_split(
    X, y_clf, test_size=0.2, random_state=42
)

# -----------------------------
# REGRESSION MODEL
# -----------------------------
reg_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

reg_model.fit(X_train, y_reg_train)

reg_preds = reg_model.predict(X_test)

print("Regression MAE:", mean_absolute_error(y_reg_test, reg_preds))
print("Regression R2:", r2_score(y_reg_test, reg_preds))

# Feature importance
importances = pd.Series(
    reg_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nFeature Importances:\n", importances)

# -----------------------------
# CLASSIFICATION MODEL
# -----------------------------
clf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    class_weight="balanced",
    random_state=42
)

clf_model.fit(X_train, y_clf_train)

clf_preds = clf_model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_clf_test, clf_preds))

# -----------------------------
# SAVE MODELS
# -----------------------------
joblib.dump(reg_model, os.path.join(MODEL_DIR, "tax_regression_model.pkl"))
joblib.dump(clf_model, os.path.join(MODEL_DIR, "tax_overpayment_model.pkl"))

print("\n✅ Models saved successfully")


