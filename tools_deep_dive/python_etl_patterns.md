# Python ETL Patterns

## Standard Pipeline Structure
```python
def run_pipeline(config: dict) -> dict:
    # 1. Extract
    df = load_data(config['source'])

    # 2. Validate
    errors = validate_schema(df)
    if errors: raise ValueError(f'Schema errors: {errors}')

    # 3. Transform
    df = clean_data(df)
    df = apply_business_rules(df)

    # 4. Load
    export_to_warehouse(df, config['target'])

    # 5. Report
    return summarise(df)
```

## Useful pandas Patterns
```python
# Safe groupby with fill
df.groupby('region')['revenue'].sum().reindex(ALL_REGIONS, fill_value=0)

# Conditional column
df['status'] = np.where(df['margin'] >= 0.35, 'On Target', 'Below Target')

# Period-over-period in one pass
df['mom_growth'] = df.groupby('product')['revenue'].pct_change()
```

## Scheduling with schedule library
```python
import schedule, time
schedule.every().monday.at('08:00').do(run_weekly_report)
while True:
    schedule.run_pending()
    time.sleep(60)
```
