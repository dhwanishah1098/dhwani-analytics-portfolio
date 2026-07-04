"""Generate synthetic weekly sales time-series for demand forecasting."""
import pandas as pd
import numpy as np
import os

np.random.seed(33)
dates = pd.date_range('2022-01-03', '2024-12-30', freq='W-MON')
n = len(dates)

# Base trend + seasonality + noise
trend     = np.linspace(300, 480, n)
annual    = 60 * np.sin(2*np.pi*np.arange(n)/52 - np.pi/2)   # summer peak AU
noise     = np.random.normal(0, 25, n)
units     = np.round(trend + annual + noise).astype(int)
units     = np.maximum(units, 50)

# Easter & Christmas dips
for i, d in enumerate(dates):
    if d.month == 12 and d.day >= 20: units[i] = int(units[i] * 0.72)
    if d.month ==  4 and d.day <= 10: units[i] = int(units[i] * 0.85)

df = pd.DataFrame({'week_ending': dates, 'units_sold': units})
os.makedirs(os.path.dirname(__file__), exist_ok=True)
df.to_csv(os.path.join(os.path.dirname(__file__), 'sales_history.csv'), index=False)
print(f"Generated {len(df)} weekly records → data/sales_history.csv")
