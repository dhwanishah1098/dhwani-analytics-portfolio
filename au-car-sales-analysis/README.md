# 🚗 Australian Car Sales Analysis (2019–2024)

A comprehensive exploratory data analysis and interactive dashboard examining vehicle sales trends across Australian states, brands, fuel types, and price segments.

## 📌 Project Overview

This project analyses publicly available Australian car sales data to uncover:
- Which states drive the highest vehicle volumes
- How EV adoption has grown vs. petrol/diesel from 2019–2024
- Top 10 brands by market share and revenue
- Seasonal sales patterns and economic correlations
- Price segment distribution across demographics

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python (pandas, matplotlib, seaborn) | Data cleaning & EDA |
| Power BI | Interactive dashboard |
| SQL (MySQL) | Data aggregation queries |
| Excel | Raw data pre-processing |

## 📁 Project Structure
```
01_car_sales_australia/
├── data/
│   ├── car_sales_raw.csv          # Simulated dataset (5,000 records)
│   └── state_population.csv       # ABS population data for normalisation
├── notebooks/
│   └── car_sales_analysis.ipynb   # Full EDA notebook
├── sql/
│   └── car_sales_queries.sql      # Aggregation & analysis queries
├── visuals/
│   └── dashboard_screenshot.png   # Power BI dashboard preview
└── README.md
```

## 📊 Key Findings
- **NSW and VIC** account for 54% of total national sales
- **EV registrations** grew 312% between 2021–2024, led by Tesla Model 3 and BYD Atto 3
- **Toyota** remains the #1 brand nationally (18.4% market share) followed by Mazda and Hyundai
- **Q4** consistently peaks (+22% vs. Q1) driven by EOFY fleet replacements and dealer discounts
- **SUV segment** overtook sedans in 2022 and now represents 41% of all new registrations

## 🔍 Sample SQL Query
```sql
SELECT 
    brand,
    state,
    fuel_type,
    COUNT(*) AS total_sales,
    ROUND(AVG(sale_price), 2) AS avg_price,
    SUM(sale_price) AS total_revenue
FROM car_sales
WHERE year BETWEEN 2022 AND 2024
GROUP BY brand, state, fuel_type
ORDER BY total_revenue DESC
LIMIT 20;
```

## 📈 How to Run
```bash
pip install pandas matplotlib seaborn jupyter
jupyter notebook notebooks/car_sales_analysis.ipynb
```

## 📌 Data Source
Simulated dataset modelled on FCAI (Federal Chamber of Automotive Industries) public reports and VFACTS monthly data.

---
*Part of Dhwani Shah's Data Analytics Portfolio | [LinkedIn](https://linkedin.com/in/dhwanishah)*
