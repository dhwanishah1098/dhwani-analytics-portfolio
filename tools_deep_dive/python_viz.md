# Python Visualisation

## plotly patterns
```python
import plotly.express as px
fig = px.bar(df, x='month', y='revenue', color='region',
             title='Revenue by Region', template='plotly_white')
fig.update_layout(legend_title='Region')
```

## matplotlib for reports
```python
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
```
