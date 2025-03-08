# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
# ]
# ///
import numpy as np
import pandas as pd

# Set random seed for reproducibility and define number of samples
np.random.seed(42)
n = 2000

# --- Visitor Demographics & Behavior ---
# Age: Normally distributed with mean 50 and std 10, clipped between 18 and 80
ages = np.random.normal(50, 10, n).clip(18, 80).astype(int)

# Nationality: Categorical distribution
nationalities = np.random.choice(
    ['USA', 'India', 'UK', 'Germany', 'Others'],
    size=n,
    p=[0.25, 0.30, 0.15, 0.10, 0.20]
)

# Gender: Randomly assigned
genders = np.random.choice(['Male', 'Female'], size=n)

# Income: Base income from a lognormal distribution;
# Increase income for USA and India by a factor of 1.5 (supports hypothesis 1)
base_income = np.random.lognormal(mean=10, sigma=0.5, size=n)
income = base_income * np.where(np.isin(nationalities, ['USA', 'India']), 1.5, 1.0)

# --- Travel & Booking Data ---
# Booking Channel: 'Digital' with probability 0.6, 'Traditional' with 0.4.
booking_channel = np.random.choice(['Digital', 'Traditional'], size=n, p=[0.6, 0.4])

# Month: Randomly chosen from 1 to 12
months = np.random.choice(np.arange(1, 13), size=n)

# Occupancy Rate: Uniform across months with a mean of 0.8 (small noise only)
occupancy_rate = np.clip(0.8 + np.random.normal(0, 0.05, n), 0, 1)

# Travel Frequency: Based on booking channel;
# Digital users (true hypothesis 2 & 4) tend to travel more than Traditional users.
travel_frequency = np.where(
    booking_channel == 'Digital',
    np.random.poisson(4, n),
    np.random.poisson(2, n)
)
# Ensure at least one travel instance for each record
travel_frequency = np.where(travel_frequency < 1, 1, travel_frequency)

# --- Economic & Spending Patterns ---
# Base spending is proportional to travel frequency and income (scaled down)
base_spending = travel_frequency * (income / 1000)

# Apply adjustments to spending:
# - Digital bookings get a boost (hypothesis 2)
digital_boost = np.where(booking_channel == 'Digital', 100, 0)
# - USA and India receive a spending boost (hypotheses 1 & 9)
nationality_boost = np.where(np.isin(nationalities, ['USA', 'India']), 150, 0)
# - Peak months (Dec, Jan, Feb) get an event boost (hypothesis 7)
peak_boost = np.where(np.isin(months, [12, 1, 2]), 200, 0)

# Final spending calculation with random noise added
spending = base_spending + digital_boost + nationality_boost + peak_boost + np.random.normal(0, 50, n)
spending = np.clip(spending, 0, None)

# --- Assemble the DataFrame ---
df = pd.DataFrame({
    'Age': ages,
    'Nationality': nationalities,
    'Gender': genders,
    'Income': income,
    'Booking_Channel': booking_channel,
    'Month': months,
    'Occupancy_Rate': occupancy_rate,
    'Travel_Frequency': travel_frequency,
    'Spending': spending
})

# Save to CSV
df.to_csv('tourists.csv', index=False)
