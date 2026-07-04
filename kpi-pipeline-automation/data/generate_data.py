"""Generate synthetic supply chain / KPI source data files."""
import pandas as pd
import numpy as np
import os

np.random.seed(55)
BASE = os.path.dirname(__file__)
os.makedirs(os.path.join(BASE, 'raw'), exist_ok=True)
os.makedirs(os.path.join(BASE, 'output'), exist_ok=True)

vendors = [f'V{str(i).zfill(3)}' for i in range(1,21)]
products = [f'SKU-{str(i).zfill(4)}' for i in range(1,51)]

for week in range(1,16):
    n = np.random.randint(120,180)
    order_dates = pd.date_range('2025-01-01', periods=week*7, freq='D')
    df = pd.DataFrame({
        'order_id':       [f'ORD-W{week:02d}-{i:04d}' for i in range(n)],
        'vendor_id':      np.random.choice(vendors, n),
        'product_id':     np.random.choice(products, n),
        'order_date':     np.random.choice(order_dates, n),
        'sla_days':       np.random.choice([3,5,7,10], n, p=[0.2,0.4,0.3,0.1]),
        'actual_days':    np.random.randint(2, 14, n),
        'quantity':       np.random.randint(10,500, n),
        'unit_cost':      np.round(np.random.uniform(5, 200, n), 2),
        'quality_status': np.random.choice(['Pass','Defect','Pending'], n, p=[0.88,0.08,0.04]),
    })
    df['delivery_date'] = pd.to_datetime(df['order_date']) + pd.to_timedelta(df['actual_days'], unit='D')
    df['order_date']    = pd.to_datetime(df['order_date']).dt.strftime('%d/%m/%Y')
    df['delivery_date'] = df['delivery_date'].dt.strftime('%d/%m/%Y')
    df['total_cost']    = (df['quantity'] * df['unit_cost']).round(2)
    path = os.path.join(BASE, 'raw', f'week_{week:02d}_orders.csv')
    df.to_csv(path, index=False)

print(f"Generated 15 weekly CSV files in data/raw/")
