# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "numpy",
#     "pandas",
# ]
# ///
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Reproducibility
random.seed(42)
np.random.seed(42)

N_ROWS = 2000

# Helper to create random dates (last 12 months)
start_date = datetime(2024, 8, 1)


def random_date():
    return start_date + timedelta(days=random.randint(0, 364))


business_units = ["BU_Fabrication", "BU_Logistics", "BU_R&D", "BU_Sales", "BU_IT"]
regions = ["North America", "EMEA", "APAC", "LATAM"]
contract_types = ["Fixed Price", "Time & Materials"]
payment_terms_choices = [15, 30, 45, 60, 90]

# Vendors & performance scores
vendors = [f"Vendor_{i:02}" for i in range(1, 51)]
vendor_scores = np.clip(np.random.normal(loc=75, scale=15, size=len(vendors)), 30, 100)
vendor_score_dict = dict(zip(vendors, vendor_scores))

# Generate data
rows = []
for i in range(N_ROWS):
    invoice_id = f"INV{i + 1:05}"
    date = random_date()
    bu = random.choice(business_units)
    region = random.choices(regions, weights=[0.3, 0.25, 0.25, 0.2])[0]
    vendor = random.choice(vendors)
    perf_score = vendor_score_dict[vendor]

    contract_type = random.choices(contract_types, weights=[0.6, 0.4])[0]
    payment_terms = random.choices(payment_terms_choices, weights=[0.2, 0.4, 0.2, 0.15, 0.05])[0]

    quantity = np.random.poisson(lam=50) + 1  # skewed right
    base_cost = np.random.uniform(10, 100)

    # Negative correlation: cost decreases with log(quantity)
    unit_cost = base_cost * (1 - 0.20 * np.log10(quantity)) + np.random.normal(0, 2)
    unit_cost = max(unit_cost, 1)  # ensure positive

    budget_amount = unit_cost * quantity * np.random.normal(1.02, 0.02)  # small padding

    # variance_percent base
    variance_pct = np.random.normal(0, 0.02)
    # Hypotheses drivers
    if payment_terms > 45:
        variance_pct += 0.05
    if region == "APAC":
        variance_pct += 0.04
    if contract_type == "Time & Materials":
        variance_pct += 0.03
    if perf_score < 70:
        variance_pct += 0.06

    actual_amount = budget_amount * (1 + variance_pct)
    variance_amount = actual_amount - budget_amount

    # Days late logic
    late_prob = 0.1
    if perf_score < 70:
        late_prob = 0.4
    days_late = np.random.poisson(5) if random.random() < late_prob else 0

    invoice_status = "Paid" if days_late == 0 else "Pending"

    rows.append(
        {
            "InvoiceID": invoice_id,
            "InvoiceDate": date,
            "BusinessUnit": bu,
            "Region": region,
            "Vendor": vendor,
            "VendorPerformanceScore": round(perf_score, 1),
            "ContractType": contract_type,
            "PaymentTermsDays": payment_terms,
            "Quantity": quantity,
            "UnitCost": round(unit_cost, 2),
            "BudgetAmount": round(budget_amount, 2),
            "ActualInvoiceAmount": round(actual_amount, 2),
            "VarianceAmount": round(variance_amount, 2),
            "DaysLate": days_late,
            "InvoiceStatus": invoice_status,
        }
    )

df = pd.DataFrame(rows)

# Save CSV
file_path = "fpa.csv"
df.to_csv(file_path, index=False)
