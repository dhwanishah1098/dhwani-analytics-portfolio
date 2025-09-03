# SQL — Key Patterns for Analytics

## Window Functions
```sql
-- Running total
SUM(revenue) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS running_total

-- Rank within group
RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS regional_rank

-- Previous period comparison
LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue
```

## CTEs for Readability
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(revenue) AS revenue
    FROM fact_sales GROUP BY 1
),
with_growth AS (
    SELECT *, revenue / LAG(revenue) OVER (ORDER BY month) - 1 AS mom_growth
    FROM monthly
)
SELECT * FROM with_growth;
```

## Useful Date Patterns
```sql
-- Current quarter start
DATE_TRUNC('quarter', CURRENT_DATE)

-- Same day last year
CURRENT_DATE - INTERVAL '1 year'

-- Business days between dates
-- Use a calendar table for accuracy
```
