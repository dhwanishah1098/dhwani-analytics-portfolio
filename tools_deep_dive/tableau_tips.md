# Tableau — Key Techniques

## LOD Expressions
```
// Fixed LOD — ignore view filters
{ FIXED [Customer ID] : MIN([Order Date]) }

// Include LOD — adds granularity
{ INCLUDE [Product] : AVG([Revenue]) }

// Exclude LOD — removes dimension
{ EXCLUDE [Region] : SUM([Revenue]) }
```

## Useful Calculated Fields
```
// Days since last purchase
DATEDIFF('day', { FIXED [Customer ID] : MAX([Order Date]) }, TODAY())

// % of total
SUM([Revenue]) / TOTAL(SUM([Revenue]))

// Running total
RUNNING_SUM(SUM([Revenue]))
```

## Dashboard Design Principles
- Lead with the KPI, support with the trend, explain with the breakdown
- Consistent colour palette — use colour to encode meaning, not decoration
- Every chart needs a clear title and labelled axes
- Add context: target lines, prior period comparison, annotations
