# Power BI — Key Concepts & Patterns

## DAX Patterns Used
```dax
-- YoY Revenue Growth
YoY Growth % =
DIVIDE(
    [Total Revenue] - CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date])),
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))
)

-- Running Total
Running Revenue =
CALCULATE([Total Revenue], FILTER(ALL('Date'), 'Date'[Date] <= MAX('Date'[Date])))

-- Customer Segment Share
Segment Share = DIVIDE([Segment Revenue], CALCULATE([Total Revenue], ALL(Customers[Segment])))
```

## Data Modelling Best Practices
- Star schema: fact tables connected to dimension tables via single-direction relationships
- Row-Level Security (RLS) for region-based access control
- Separate date dimension table for time intelligence functions

## Performance Tips
- Use integer keys instead of string keys in relationships
- Avoid bidirectional filters unless necessary
- Prefer measures over calculated columns for aggregations
