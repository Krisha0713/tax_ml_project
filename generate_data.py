import numpy as np
import pandas as pd

np.random.seed(42)
n = 4000

# Age
age = np.random.randint(22, 60, n)

# Income distribution (India-like)
income = np.concatenate([
    np.random.normal(400000, 150000, int(n*0.4)),
    np.random.normal(800000, 250000, int(n*0.4)),
    np.random.normal(1500000, 400000, int(n*0.2))
])
income = np.clip(income, 250000, 3000000)

# Employment type
employment = np.random.choice([0, 1], n, p=[0.7, 0.3])  # 0 salaried, 1 self-employed

# 80C behavior (most don't max it)
inv_80c = []
for inc in income:
    if inc < 500000:
        inv_80c.append(np.random.uniform(0, 50000))
    elif inc < 1000000:
        inv_80c.append(np.random.uniform(30000, 120000))
    else:
        inv_80c.append(np.random.uniform(80000, 150000))
inv_80c = np.array(inv_80c)

# 80D insurance
ins_80d = np.random.uniform(0, 50000, n)

# HRA only for salaried
hra = np.where(
    employment == 0,
    np.random.uniform(0.1, 0.3, n) * income,
    0
)
hra = np.clip(hra, 0, 200000)

# Other deductions
other_ded = np.random.uniform(0, 70000, n)

# Approx effective tax (behavioral, not slab-accurate)
taxable_income = income - (inv_80c + ins_80d + hra + other_ded)
taxable_income = np.clip(taxable_income, 0, None)

effective_tax = (
    0.05 * np.minimum(taxable_income, 500000) +
    0.2 * np.clip(taxable_income - 500000, 0, 500000) +
    0.3 * np.clip(taxable_income - 1000000, 0, None)
)

# Real-world noise (human inefficiency)
effective_tax *= np.random.uniform(0.9, 1.15, n)

# Previous year tax
prev_tax = effective_tax * np.random.uniform(0.85, 1.2, n)

# Overpayment risk
overpay = (prev_tax > effective_tax * 1.1).astype(int)

df = pd.DataFrame({
    "Age": age,
    "Annual_Income": income,
    "Employment_Type": employment,
    "Investment_80C": inv_80c,
    "Insurance_80D": ins_80d,
    "HRA_Claimed": hra,
    "Other_Deductions": other_ded,
    "Previous_Year_Tax": prev_tax,
    "Effective_Tax_Paid": effective_tax,
    "Overpayment_Risk": overpay
})

df.to_csv("tax_data.csv", index=False)
print("Dataset generated:", df.shape)
