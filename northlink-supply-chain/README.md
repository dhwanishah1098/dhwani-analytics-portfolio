# 🏭 Supply Chain Analytics Dashboard — North Link Melbourne Food Group

A real-world business intelligence project delivered during a 6-month Business Analyst internship. Built Power BI dashboards and automated KPI pipelines for a Melbourne-based food distribution company, resulting in measurable operational improvements.

## 📌 Project Overview

North Link Melbourne Food Group required better visibility into their supply chain. Manual Excel-based reporting was slow, inconsistent, and lacked drill-down capability. This project delivered:
- Automated KPI refresh pipeline (from 2-day turnaround → 6 hours)
- Power BI dashboards tracking vendor lead times, defect rates, and fulfilment
- Python-based data cleaning across 15 fragmented Excel datasets
- Stakeholder training and a 12-page dashboard user guide

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Power BI (DAX, drill-through) | Interactive KPI dashboards |
| Python (pandas) | Data cleaning & transformation |
| SQL (MySQL) | Data consolidation & joins |
| MS Excel | Raw source data management |
| Jira / Agile | Project tracking |

## 📁 Project Structure
```
03_northlink_supply_chain/
├── data/
│   └── supply_chain_sample.csv       # Anonymised sample dataset
├── notebooks/
│   └── data_cleaning_pipeline.ipynb  # Python ETL pipeline
├── sql/
│   └── vendor_performance_queries.sql
├── powerbi/
│   └── dashboard_structure.md        # DAX measures & visual layout
├── docs/
│   └── dashboard_user_guide_excerpt.md
└── README.md
```

## 📊 Outcomes Delivered
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Report turnaround | 2 days | 6 hours | **−75%** |
| Data consistency | Baseline | +22% | **+22%** |
| Missing/duplicate records | Baseline | −25% | **−25%** |
| Dashboard adoption | ~30% | 85% | **+183%** |
| On-time fulfilment | Baseline | +12% | **+12%** |
| Cost savings (SKU optimisation) | — | A$45,000/qtr | **New saving** |

## 🔍 Sample DAX Measure (Power BI)
```dax
On_Time_Fulfilment_Rate = 
DIVIDE(
    COUNTROWS(FILTER(Orders, Orders[Delivery_Status] = "On Time")),
    COUNTROWS(Orders),
    0
) * 100
```

## 🔍 Sample Python Cleaning Script
```python
import pandas as pd
import glob

# Load and consolidate 15 Excel files
files = glob.glob('data/raw/*.xlsx')
dfs = [pd.read_excel(f) for f in files]
df = pd.concat(dfs, ignore_index=True)

# Remove duplicates and nulls
df.drop_duplicates(subset=['order_id'], inplace=True)
df.dropna(subset=['vendor_id', 'delivery_date'], inplace=True)

# Standardise date format
df['delivery_date'] = pd.to_datetime(df['delivery_date'], dayfirst=True)

print(f"Clean records: {len(df):,}")
df.to_csv('data/clean/supply_chain_clean.csv', index=False)
```

## 📌 Note
This project uses anonymised and representative sample data. Business-sensitive figures have been generalised.

---
*Internship Project | North Link Melbourne Food Group | Jun–Dec 2025*
