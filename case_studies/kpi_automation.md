# Case Study: KPI Automation Pipeline

## Business Problem
Procurement and operations teams spent 2 days per week manually compiling
KPI reports from 15 separate Excel files across different systems.

## Solution
Built a scheduled Python ETL pipeline that:
1. Reads and validates source data from multiple systems
2. Applies transformations and business rules
3. Loads into a single consolidated reporting layer
4. Triggers Power BI scheduled refresh automatically
5. Emails a formatted HTML summary to stakeholders

## Impact
- Reporting turnaround cut from **2 days → 6 hours** (75% reduction)
- Data consistency improved by **22%**
- Duplicate/missing records reduced by **25%**
- Ad-hoc report requests reduced by **30%** after user training

## Tools
Python · pandas · Power BI · schedule · Jinja2 · SMTP
