"""
Australian Immigration Trends Analysis (2015–2024)
Author: Dhwani Shah | Master of Business Analytics, Victoria University
Data: Synthetic dataset modelled on Dept of Home Affairs migration reports
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data', 'visa_grants_2015_2024.csv')
OUT  = os.path.join(BASE, 'visuals')
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(DATA):
    exec(open(os.path.join(BASE, 'data', 'generate_data.py')).read())

df = pd.read_csv(DATA)
NAVY='#1F3864'; TEAL='#2E86AB'; GOLD='#F4A261'; RED='#E63946'
PALETTE=['#1F3864','#2E86AB','#4CAF93','#F4A261','#E63946','#9B59B6','#F39C12','#27AE60','#E67E22','#16A085']
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})

print(f"\n{'='*55}\n  AUSTRALIAN IMMIGRATION ANALYSIS (2015–2024)\n{'='*55}")
print(f"  Total visa grants: {len(df):,}")

# Chart 1: Grants by year and category
fig, ax = plt.subplots(figsize=(10,5))
pivot = df.groupby(['year','visa_category']).size().unstack(fill_value=0)
pivot.plot(kind='bar', stacked=True, ax=ax, color=PALETTE[:len(pivot.columns)], edgecolor='white', linewidth=0.5)
ax.set_title('Australian Visa Grants by Category (2015–2024)', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Year',fontsize=11); ax.set_ylabel('Visa Grants',fontsize=11)
ax.legend(title='Category', fontsize=9, bbox_to_anchor=(1.01,1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout(); plt.savefig(f'{OUT}/01_grants_by_year_category.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✓ Chart 1: Grants by year and category")

# Chart 2: Top source countries for skilled visas
fig, ax = plt.subplots(figsize=(10,5))
skilled = df[df['visa_category']=='Skilled']
top10 = skilled.groupby('country_of_birth').size().nlargest(10).reset_index(name='grants')
bars = ax.barh(top10['country_of_birth'], top10['grants'], color=PALETTE[:10], edgecolor='white')
for bar, val in zip(bars, top10['grants']):
    ax.text(val+3, bar.get_y()+bar.get_height()/2, f'{val:,}', va='center', fontsize=9)
ax.set_title('Top 10 Source Countries — Skilled Visas (2015–2024)', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Visa Grants', fontsize=11)
top_country = top10.iloc[0]['country_of_birth']
plt.tight_layout(); plt.savefig(f'{OUT}/02_top_source_countries.png', dpi=150, bbox_inches='tight'); plt.close()
print(f"  ✓ Chart 2: Top source countries → {top_country} leads skilled visa grants")

# Chart 3: 485 visa trend
fig, ax = plt.subplots(figsize=(9,5))
v485 = df[df['visa_subclass'].str.startswith('485')].groupby('year').size().reset_index(name='grants')
ax.fill_between(v485['year'], v485['grants'], alpha=0.3, color=TEAL)
ax.plot(v485['year'], v485['grants'], marker='o', linewidth=2.5, color=TEAL, markersize=7)
ax.set_title('485 Temporary Graduate Visa — Grant Trend (2015–2024)', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Year',fontsize=11); ax.set_ylabel('Visa Grants',fontsize=11)
if len(v485) >= 2:
    growth = (v485.iloc[-1]['grants']/v485.iloc[0]['grants']-1)*100
    ax.text(0.02,0.95,f'Growth 2015→2024: +{growth:.0f}%\n(International student completions)',
            transform=ax.transAxes, va='top', fontsize=9, color=TEAL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAF4FB', edgecolor=TEAL, alpha=0.8))
plt.tight_layout(); plt.savefig(f'{OUT}/03_485_visa_trend.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✓ Chart 3: 485 visa growth trend")

# Chart 4: Settlement state distribution
fig, ax = plt.subplots(figsize=(8,5))
state_data = df.groupby('settlement_state').size().sort_values(ascending=False)
pcts = state_data / state_data.sum() * 100
bars = ax.bar(state_data.index, state_data.values, color=PALETTE[:len(state_data)], edgecolor='white')
for bar, pct in zip(bars, pcts):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5, f'{pct:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Migrant Settlement Distribution by State', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('State',fontsize=11); ax.set_ylabel('Visa Grants',fontsize=11)
plt.tight_layout(); plt.savefig(f'{OUT}/04_settlement_by_state.png', dpi=150, bbox_inches='tight'); plt.close()
print(f"  ✓ Chart 4: Settlement by state → VIC {pcts.get('VIC',0):.0f}%, NSW {pcts.get('NSW',0):.0f}%")

# Chart 5: Processing time by visa category
fig, ax = plt.subplots(figsize=(9,5))
proc = df.groupby('visa_category')['processing_days'].median().sort_values()
bars = ax.barh(proc.index, proc.values, color=PALETTE[:len(proc)], edgecolor='white')
for bar, val in zip(bars, proc.values):
    ax.text(val+3, bar.get_y()+bar.get_height()/2, f'{val:.0f} days', va='center', fontsize=9)
ax.set_title('Median Processing Time by Visa Category', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Median Processing Days',fontsize=11)
plt.tight_layout(); plt.savefig(f'{OUT}/05_processing_time.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✓ Chart 5: Processing time by visa category")

print(f"\n{'='*55}\n  CONCLUSIONS\n{'='*55}")
print(f"  1. {top_country} is the #1 source country for skilled visas.")
print(f"  2. 485 graduate visa grants grew significantly 2021–2024,")
print(f"     reflecting post-COVID onshore study normalisation.")
print(f"  3. VIC and NSW absorb ~{(pcts.get('VIC',0)+pcts.get('NSW',0)):.0f}% of all migrants.")
print(f"  4. Temporary visas (482/485) are the largest grant category.")
print(f"  5. Student (500) visa is the single largest subclass.")
print(f"\n  Charts saved to: visuals/\n{'='*55}\n")
