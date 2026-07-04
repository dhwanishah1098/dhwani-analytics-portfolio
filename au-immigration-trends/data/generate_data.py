"""Generate synthetic Australian immigration visa grants dataset."""
import pandas as pd
import numpy as np
import os

np.random.seed(7)
n = 8000

countries = ['India','China','Philippines','Nepal','Pakistan','United Kingdom',
             'Sri Lanka','Vietnam','South Korea','New Zealand','Bangladesh','Malaysia',
             'United States','Indonesia','Germany']
country_w = [0.22,0.16,0.10,0.09,0.07,0.06,0.05,0.04,0.03,0.03,0.03,0.03,0.02,0.02,0.05]

visa_subclasses = {
    'Skilled':     ['189 – Skilled Independent','190 – Skilled Nominated','491 – Skilled Regional'],
    'Temporary':   ['482 – Temp Skill Shortage','485 – Temp Graduate','400 – Temp Work'],
    'Student':     ['500 – Student'],
    'Humanitarian':['200 – Refugee','202 – Global Special'],
    'Family':      ['820 – Partner (Temp)','801 – Partner (Perm)','143 – Contributory Parent'],
}
all_visas = [v for vl in visa_subclasses.values() for v in vl]
visa_w    = [0.09,0.07,0.05, 0.14,0.18,0.04, 0.18, 0.05,0.03, 0.07,0.05,0.06]

states = ['VIC','NSW','QLD','WA','SA','ACT','TAS']
state_w = [0.31,0.28,0.18,0.11,0.07,0.03,0.02]

years  = np.random.choice(range(2015,2025), n, p=[0.09,0.10,0.11,0.12,0.08,0.06,0.11,0.13,0.12,0.08])
countries_col = np.random.choice(countries, n, p=country_w)
visas_col     = np.random.choice(all_visas,  n, p=visa_w)
states_col    = np.random.choice(states,     n, p=state_w)

# Grant outcome: mostly approved, some refused
outcomes = np.random.choice(['Granted','Refused','Withdrawn'], n, p=[0.82,0.13,0.05])
processing_days = np.random.randint(30, 730, n)

df = pd.DataFrame({
    'year': years, 'country_of_birth': countries_col,
    'visa_subclass': visas_col,
    'visa_category': [next(k for k,v in visa_subclasses.items() if vs in v) for vs in visas_col],
    'settlement_state': states_col,
    'outcome': outcomes,
    'processing_days': processing_days
})
df = df[df['outcome'] == 'Granted'].reset_index(drop=True)

os.makedirs(os.path.dirname(__file__), exist_ok=True)
df.to_csv(os.path.join(os.path.dirname(__file__), 'visa_grants_2015_2024.csv'), index=False)
print(f"Generated {len(df)} visa grant records → data/visa_grants_2015_2024.csv")
