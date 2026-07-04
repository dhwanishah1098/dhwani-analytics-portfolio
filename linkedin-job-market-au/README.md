# 💼 LinkedIn Job Market Analysis — Data & Analytics Roles in Australia (2024–2025)

A data-driven analysis of the Australian analytics job market using scraped LinkedIn job postings to identify in-demand skills, salary benchmarks, top hiring companies, and role trends for Data/Business Analyst positions.

## 📌 Project Overview

What skills do Australian employers actually want in 2025? This project analyses 2,000+ LinkedIn job postings across Data Analyst, Business Analyst, BI Analyst, and Reporting Analyst roles to answer:
- Which tools appear most in job descriptions (Power BI vs Tableau vs Looker)?
- What experience level is most in demand?
- Which industries hire the most analysts?
- How do salaries differ by city and role type?
- What keywords maximise resume ATS pass-through?

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python (pandas, re, wordcloud) | Text mining & keyword extraction |
| Power BI | Dashboard of hiring trends |
| SQL | Job data aggregation |
| matplotlib / seaborn | Visualisations |

## 📁 Project Structure
```
04_linkedin_job_market/
├── data/
│   └── linkedin_jobs_sample.csv       # 500 sample job records
├── notebooks/
│   └── job_market_analysis.ipynb      # Full analysis notebook
├── sql/
│   └── job_trends_queries.sql
├── visuals/
│   ├── skill_frequency_chart.png
│   └── salary_by_city.png
└── README.md
```

## 📊 Key Findings
- **Power BI** appears in 67% of analyst job ads — far ahead of Tableau (41%) and Looker (18%)
- **SQL** is the #1 required hard skill across all analyst role types (82% of postings)
- **Melbourne and Sydney** account for 71% of all analyst job postings nationally
- **$80,000–$95,000** is the modal salary band for junior-to-mid analyst roles
- **Agile/Scrum** mentioned in 44% of BA roles — a growing expectation at entry level
- **Stakeholder management** is the most common soft-skill keyword (58% of BAs)

## 🔍 Sample Python Analysis
```python
import pandas as pd
from collections import Counter
import re

df = pd.read_csv('data/linkedin_jobs_sample.csv')

# Extract skill keywords from job descriptions
skills = ['power bi', 'tableau', 'sql', 'python', 'excel', 'agile',
          'r programming', 'looker', 'azure', 'aws', 'jira']

skill_counts = {}
for skill in skills:
    count = df['description'].str.lower().str.contains(skill).sum()
    skill_counts[skill] = count

skill_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Count'])
skill_df = skill_df.sort_values('Count', ascending=False)
print(skill_df)
```

## 📌 Relevance
This analysis directly informed my own job search strategy — identifying which skills to highlight and which role titles to target in the Australian market.

---
*Part of Dhwani Shah's Data Analytics Portfolio*
