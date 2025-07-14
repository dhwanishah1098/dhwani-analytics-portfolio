# Case Study: RFM Customer Segmentation

## Business Problem
A retail client had no systematic way to identify high-value customers,
at-risk segments, or optimal timing for reactivation campaigns.

## Approach
1. Extracted 12 months of transaction data (10,000+ records)
2. Computed RFM scores using quantile-based binning (5-band scoring)
3. Classified customers into 6 segments using rule-based logic
4. Added CLV estimation and campaign ROI calculator per segment
5. Built segment migration tracker for period-over-period comparison

## Business Outcomes
- Identified **Champions** segment contributing 38% of total revenue (12% of customers)
- Flagged 847 **At Risk** customers with >$500 lifetime value for reactivation
- Campaign targeting **Loyal Customers** yielded 23% higher conversion vs blanket send

## Tools
Python · pandas · matplotlib · seaborn · openpyxl
