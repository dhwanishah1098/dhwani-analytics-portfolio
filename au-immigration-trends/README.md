# 🌏 Australian Immigration Trends Analysis (2015–2024)

An end-to-end data analysis project exploring visa grants, country of origin, migration pathways, and settlement patterns across Australian states using Department of Home Affairs data.

## 📌 Project Overview

Australia's immigration landscape has shifted dramatically post-COVID. This project investigates:
- Net overseas migration (NOM) trends by year and state
- Top source countries for skilled, student, and humanitarian visas
- Visa subclass popularity over time (482, 485, 189, 190, 500, etc.)
- State/territory distribution of new permanent residents
- Economic contribution analysis: migrant workforce participation rates

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python (pandas, geopandas, plotly) | EDA + choropleth mapping |
| Power BI | Interactive migration dashboard |
| SQL | Visa grant aggregation |
| Tableau | State-level settlement heatmaps |

## 📁 Project Structure
```
02_immigration_australia/
├── data/
│   ├── visa_grants_2015_2024.csv      # 8,000+ simulated records
│   ├── country_of_origin.csv
│   └── state_settlement.csv
├── notebooks/
│   └── immigration_analysis.ipynb
├── sql/
│   └── immigration_queries.sql
├── visuals/
│   ├── migration_choropleth.png
│   └── visa_subclass_trends.png
└── README.md
```

## 📊 Key Findings
- **485 Temporary Graduate Visa** grants rose 68% between 2021–2024, driven by international student completions
- **India** overtook China as the #1 source country for skilled migrants in 2022
- **Victoria** absorbs the largest share of 485 holders (31%) followed by NSW (28%)
- **Student visa (500)** cancellation rates fell post-COVID as onshore study normalised
- Skilled Independent (189) visa queue has average wait time of 3.2 years

## 🔍 Sample Analysis (Python)
```python
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/visa_grants_2015_2024.csv')

# Top 10 source countries for skilled visas
skilled = df[df['visa_category'] == 'Skilled']
top_countries = skilled.groupby('country_of_birth')['grants'].sum().nlargest(10).reset_index()

fig = px.bar(top_countries, x='country_of_birth', y='grants',
             title='Top 10 Source Countries – Skilled Visas (2015–2024)',
             color='grants', color_continuous_scale='Blues')
fig.show()
```

## 📈 How to Run
```bash
pip install pandas plotly geopandas jupyter
jupyter notebook notebooks/immigration_analysis.ipynb
```

## 📌 Data Source
Modelled on Department of Home Affairs Migration Programme Reports and ABS migration statistics.

---
*Part of Dhwani Shah's Data Analytics Portfolio*
