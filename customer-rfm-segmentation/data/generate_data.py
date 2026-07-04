"""Generate synthetic retail transactions dataset for RFM analysis."""
import pandas as pd
import numpy as np
import os

np.random.seed(21)
n_customers = 1000
n_transactions = 10000

customer_ids = [f'C{str(i).zfill(4)}' for i in range(1, n_customers+1)]
# Assign customer types (champion, loyal, at-risk, new, lost)
types = np.random.choice(['champion','loyal','potential','atrisk','lost'],
                          n_customers, p=[0.15,0.20,0.25,0.20,0.20])

records = []
base_date = pd.Timestamp('2024-12-31')
for cid, ctype in zip(customer_ids, types):
    if ctype == 'champion':
        n_orders = np.random.randint(12, 30)
        last_days_ago = np.random.randint(1, 30)
        avg_spend = np.random.uniform(180, 400)
    elif ctype == 'loyal':
        n_orders = np.random.randint(6, 15)
        last_days_ago = np.random.randint(15, 90)
        avg_spend = np.random.uniform(100, 220)
    elif ctype == 'potential':
        n_orders = np.random.randint(3, 8)
        last_days_ago = np.random.randint(30, 120)
        avg_spend = np.random.uniform(60, 130)
    elif ctype == 'atrisk':
        n_orders = np.random.randint(4, 10)
        last_days_ago = np.random.randint(120, 300)
        avg_spend = np.random.uniform(80, 180)
    else:  # lost
        n_orders = np.random.randint(1, 4)
        last_days_ago = np.random.randint(250, 730)
        avg_spend = np.random.uniform(30, 90)

    for i in range(n_orders):
        days_offset = last_days_ago + i * np.random.randint(7, 40)
        order_date = base_date - pd.Timedelta(days=int(days_offset))
        amount = round(max(10, np.random.normal(avg_spend, avg_spend*0.3)), 2)
        records.append({'customer_id': cid, 'customer_type': ctype,
                        'invoice_id': f'INV{len(records):05d}',
                        'invoice_date': order_date.date(),
                        'total_amount': amount,
                        'product_category': np.random.choice(['Electronics','Apparel','Home','Beauty','Sports'],
                                                              p=[0.25,0.20,0.25,0.15,0.15])})

df = pd.DataFrame(records)
os.makedirs(os.path.dirname(__file__), exist_ok=True)
df.to_csv(os.path.join(os.path.dirname(__file__), 'transactions_sample.csv'), index=False)
print(f"Generated {len(df)} transactions for {n_customers} customers → data/transactions_sample.csv")
