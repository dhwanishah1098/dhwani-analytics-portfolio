# ⚙️ Automated KPI Reporting Pipeline (Python + Power BI)

A production-ready automated reporting pipeline that replaces manual Excel-based KPI compilation with a scheduled Python ETL process feeding directly into Power BI — reducing reporting turnaround from 2 days to under 6 hours.

## 📌 Project Overview

Many organisations still rely on analysts manually compiling data from multiple sources into Excel before building reports. This project automates that entire chain:

1. **Extract:** Pull data from multiple CSV/Excel sources (simulating ERP/database exports)
2. **Transform:** Clean, validate, join, and calculate KPIs in Python
3. **Load:** Write clean data to a structured output for Power BI refresh
4. **Schedule:** Run automatically every Monday at 7AM via `schedule` library
5. **Alert:** Email summary when pipeline completes or fails

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python (pandas, schedule, smtplib) | ETL pipeline & automation |
| Power BI (DirectQuery / Import) | Dashboard layer |
| SQL (MySQL) | Intermediate data store |
| Excel | Source data format |

## 📁 Project Structure
```
09_kpi_automation_pipeline/
├── src/
│   ├── extract.py             # Load raw source files
│   ├── transform.py           # Clean, join, calculate KPIs
│   ├── load.py                # Write to output / database
│   ├── alerting.py            # Email notifications
│   └── scheduler.py           # Automated run scheduler
├── config/
│   └── pipeline_config.yaml   # Source paths, KPI definitions
├── data/
│   ├── raw/                   # Input files
│   └── output/                # Clean output for Power BI
├── logs/
│   └── pipeline.log
└── README.md
```

## 🔍 Core Pipeline
```python
import pandas as pd
import glob
import logging
from datetime import datetime

logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO)

def extract():
    files = glob.glob('data/raw/*.xlsx')
    dfs = []
    for f in files:
        df = pd.read_excel(f)
        df['source_file'] = f
        dfs.append(df)
    raw = pd.concat(dfs, ignore_index=True)
    logging.info(f"[EXTRACT] Loaded {len(raw):,} rows from {len(files)} files")
    return raw

def transform(df):
    # Remove duplicates
    df.drop_duplicates(subset=['order_id'], inplace=True)
    # Standardise dates
    df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
    df.dropna(subset=['order_date', 'vendor_id'], inplace=True)
    # Calculate KPIs
    df['days_to_deliver'] = (df['delivery_date'] - df['order_date']).dt.days
    df['on_time'] = df['days_to_deliver'] <= df['sla_days']
    df['defect_flag'] = df['quality_status'] == 'Defect'
    logging.info(f"[TRANSFORM] Clean records: {len(df):,}")
    return df

def load(df):
    output_path = f"data/output/kpi_report_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output_path, index=False)
    logging.info(f"[LOAD] Written to {output_path}")
    return output_path

# Run pipeline
raw = extract()
clean = transform(raw)
output = load(clean)
print(f"Pipeline complete. Output: {output}")
```

## 📊 KPIs Tracked
- On-Time Delivery Rate (%)
- Vendor Defect Rate (%)
- Average Lead Time (days)
- Stockout Frequency
- Weekly Fulfilment Volume

---
*Inspired by real automation work at North Link Melbourne Food Group (Jun–Dec 2025)*
