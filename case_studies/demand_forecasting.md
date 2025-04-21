# Case Study: Demand Forecasting with ARIMA & Prophet

## Business Problem
A food distribution business was experiencing frequent stockouts and
excess inventory, leading to waste and lost sales.

## Approach
1. Cleaned and consolidated 12 months of historical sales data (15 Excel files → 1 pipeline)
2. Built baseline ARIMA model; tested seasonal ARIMA variants
3. Switched to Prophet for better handling of Australian public holidays and promotion effects
4. Incorporated external variables: holiday calendar, promotional flags, supplier lead times

## Results
- **6.2% MAPE** on 12-week horizon (vs ~14% from manual planning)
- **12% improvement** in on-time fulfilment rate
- Safety stock thresholds adjusted across 12 product categories based on model output

## Tools
Python · pandas · Prophet · statsmodels · matplotlib
