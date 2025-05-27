# DAX Time Intelligence

```dax
MTD Revenue = CALCULATE([Revenue], DATESMTD('Date'[Date]))
QTD Revenue = CALCULATE([Revenue], DATESQTD('Date'[Date]))
YTD Revenue = CALCULATE([Revenue], DATESYTD('Date'[Date]))
Prev Year   = CALCULATE([Revenue], SAMEPERIODLASTYEAR('Date'[Date]))
```
