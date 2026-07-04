"""Generate synthetic Australian car sales dataset with strong feature-price relationships."""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 5000

states     = ['NSW','VIC','QLD','WA','SA','ACT','TAS']
state_w    = [0.32, 0.28, 0.20, 0.10, 0.06, 0.02, 0.02]
state_premium = {'NSW':1.05,'VIC':1.03,'ACT':1.08,'WA':1.02,'QLD':0.98,'SA':0.96,'TAS':0.93}

brands     = ['Toyota','Mazda','Hyundai','Ford','Kia','Mitsubishi','Tesla','BYD','Isuzu','Nissan']
brand_w    = [0.184,0.115,0.102,0.095,0.090,0.080,0.075,0.060,0.055,0.144]
brand_base = {'Toyota':38000,'Mazda':33000,'Hyundai':30000,'Ford':44000,'Kia':29000,
              'Mitsubishi':36000,'Tesla':78000,'BYD':52000,'Isuzu':58000,'Nissan':32000}

body_types = ['SUV','Sedan','Ute','Hatchback','Van','Wagon']
body_w     = [0.41, 0.22, 0.18, 0.12, 0.04, 0.03]
body_mult  = {'SUV':1.18,'Ute':1.12,'Wagon':1.05,'Van':1.08,'Sedan':1.0,'Hatchback':0.88}

fuel_types = ['Petrol','Diesel','Hybrid','Electric']
fuel_mult  = {'Electric':1.55,'Hybrid':1.22,'Diesel':1.10,'Petrol':1.0}

years   = np.random.choice(range(2019,2025), n, p=[0.12,0.13,0.14,0.17,0.22,0.22])
months  = np.random.choice(range(1,13), n)
states_col  = np.random.choice(states, n, p=state_w)
brands_col  = np.random.choice(brands, n, p=brand_w)
body_col    = np.random.choice(body_types, n, p=body_w)

fuel_col = []
for y, b in zip(years, brands_col):
    if b in ['Tesla','BYD']:
        fuel_col.append('Electric')
    elif y >= 2022:
        fuel_col.append(np.random.choice(fuel_types, p=[0.44,0.22,0.22,0.12]))
    else:
        fuel_col.append(np.random.choice(fuel_types, p=[0.58,0.28,0.12,0.02]))

prices = []
for b, body, fuel, state, yr in zip(brands_col, body_col, fuel_col, states_col, years):
    p = brand_base[b]
    p *= body_mult[body]
    p *= fuel_mult[fuel]
    p *= state_premium[state]
    p *= (1 + (yr - 2019) * 0.025)   # ~2.5% annual price inflation
    p *= np.random.uniform(0.93, 1.07)  # ±7% noise
    prices.append(round(p, -2))

df = pd.DataFrame({
    'year':yr_col, 'month':months, 'quarter':((months-1)//3+1),
    'state':states_col, 'brand':brands_col, 'body_type':body_col,
    'fuel_type':fuel_col, 'sale_price':prices,
})

# fix column name typo
df = df.rename(columns={'year': 'year'})
years_arr = years
df['year'] = years_arr

os.makedirs(os.path.dirname(__file__), exist_ok=True)
df.to_csv(os.path.join(os.path.dirname(__file__), 'car_sales_raw.csv'), index=False)
print(f"Generated {len(df)} records → data/car_sales_raw.csv")
