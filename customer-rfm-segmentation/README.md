# 🎯 Customer Segmentation using RFM Analysis

An end-to-end customer analytics project applying RFM (Recency, Frequency, Monetary) segmentation to a retail transaction dataset. Identifies high-value, at-risk, and churned customer segments to support targeted marketing strategies.

## 📌 Project Overview

RFM analysis scores customers on three dimensions:
- **Recency (R):** How recently did they purchase?
- **Frequency (F):** How often do they purchase?
- **Monetary (M):** How much do they spend?

This project delivers:
- Full RFM scoring pipeline in Python
- Customer segment classification (Champions, Loyal, At-Risk, Lost, etc.)
- Power BI dashboard for segment visualisation
- Actionable marketing recommendations per segment

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python (pandas, datetime) | RFM scoring pipeline |
| scikit-learn (K-Means) | Cluster validation |
| Power BI | Segment dashboard |
| SQL | Transaction aggregation |

## 📁 Project Structure
```
08_customer_segmentation_rfm/
├── data/
│   └── transactions_sample.csv    # 10,000 sample transactions
├── notebooks/
│   └── rfm_analysis.ipynb
├── sql/
│   └── rfm_queries.sql
├── visuals/
│   ├── rfm_segments_chart.png
│   └── segment_revenue_breakdown.png
└── README.md
```

## 🔍 Core RFM Pipeline
```python
import pandas as pd
from datetime import datetime

df = pd.read_csv('data/transactions_sample.csv', parse_dates=['invoice_date'])
snapshot_date = df['invoice_date'].max() + pd.Timedelta(days=1)

# Build RFM table
rfm = df.groupby('customer_id').agg(
    recency   = ('invoice_date', lambda x: (snapshot_date - x.max()).days),
    frequency = ('invoice_id',   'nunique'),
    monetary  = ('total_amount', 'sum')
).reset_index()

# Score 1–5 (5 = best)
rfm['R'] = pd.qcut(rfm['recency'],   5, labels=[5,4,3,2,1])
rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M'] = pd.qcut(rfm['monetary'],  5, labels=[1,2,3,4,5])
rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

# Segment map
def segment(row):
    r, f, m = int(row['R']), int(row['F']), int(row['M'])
    if r >= 4 and f >= 4: return 'Champion'
    elif r >= 3 and f >= 3: return 'Loyal Customer'
    elif r >= 4 and f <= 2: return 'New Customer'
    elif r <= 2 and f >= 3: return 'At Risk'
    elif r <= 2 and f <= 2: return 'Lost'
    else: return 'Potential Loyalist'

rfm['Segment'] = rfm.apply(segment, axis=1)
print(rfm['Segment'].value_counts())
```

## 📊 Segment Results (Sample Dataset)
| Segment | Customers | Avg Revenue | Action |
|---------|-----------|-------------|--------|
| Champions | 18% | $2,340 | Reward & retain |
| Loyal Customers | 22% | $1,180 | Upsell & cross-sell |
| At Risk | 19% | $890 | Win-back campaigns |
| New Customers | 15% | $420 | Onboarding nurture |
| Lost | 26% | $110 | Re-engagement or deprioritise |

---
*Academic Project | Master of Business Analytics, Victoria University | Part of Dhwani Shah's Portfolio*
