"""
Australian Car Sales Analysis (2019–2024)
Author: Dhwani Shah | Master of Business Analytics, Victoria University

Methods:
  - Exploratory Data Analysis (EDA)
  - Multiple Linear Regression (predicting sale price)
  - Correlation analysis
  - Feature encoding & model evaluation (R², RMSE, MAPE)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import os, warnings
warnings.filterwarnings('ignore')

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data', 'car_sales_raw.csv')
OUT  = os.path.join(BASE, 'visuals')
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(DATA):
    exec(open(os.path.join(BASE,'data','generate_data.py')).read())

df = pd.read_csv(DATA)
NAVY='#1F3864'; TEAL='#2E86AB'; GOLD='#F4A261'; RED='#E63946'
PALETTE=['#1F3864','#2E86AB','#4CAF93','#F4A261','#E63946','#9B59B6','#F39C12','#27AE60']
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})

print(f"\n{'='*60}\n  AUSTRALIAN CAR SALES ANALYSIS (2019–2024)\n{'='*60}")
print(f"  Records: {len(df):,} | Years: {df['year'].min()}–{df['year'].max()}")
print(f"\n  Descriptive Statistics:")
print(df['sale_price'].describe().rename('sale_price_AUD').round(0).to_string())

# ── Chart 1: Sales volume by state ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9,5))
state_s = df.groupby('state').size().sort_values(ascending=False)
bars = ax.bar(state_s.index, state_s.values, color=PALETTE[:len(state_s)], edgecolor='white')
for bar, v in zip(bars, state_s.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10, f'{v:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
pct_nv = state_s[['NSW','VIC']].sum()/state_s.sum()*100
ax.text(0.98,0.95,f'NSW+VIC = {pct_nv:.0f}% of total', transform=ax.transAxes,ha='right',va='top',fontsize=9,
        color=TEAL,bbox=dict(boxstyle='round,pad=0.3',facecolor='#EAF4FB',edgecolor=TEAL,alpha=0.8))
ax.set_title('Vehicle Sales by State (2019–2024)',fontsize=14,fontweight='bold',color=NAVY,pad=15)
ax.set_xlabel('State',fontsize=11); ax.set_ylabel('Units Sold',fontsize=11)
plt.tight_layout(); plt.savefig(f'{OUT}/01_sales_by_state.png',dpi=150,bbox_inches='tight'); plt.close()
print(f"\n  ✓ Chart 1: Sales by state → NSW+VIC = {pct_nv:.0f}%")

# ── Chart 2: EV adoption trend ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9,5))
ev = df.groupby(['year','fuel_type']).size().unstack(fill_value=0)
for col, color in zip(ev.columns, PALETTE):
    ax.plot(ev.index, ev[col], marker='o', linewidth=2.5, color=color, label=col, markersize=6)
ev_g = (ev.get('Electric',pd.Series([0]*len(ev))).iloc[-1] /
        max(ev.get('Electric',pd.Series([1]*len(ev))).iloc[0],1) - 1)*100
ax.set_title('Fuel Type Trend (2019–2024)',fontsize=14,fontweight='bold',color=NAVY,pad=15)
ax.set_xlabel('Year',fontsize=11); ax.set_ylabel('Units Sold',fontsize=11)
ax.legend(fontsize=10); ax.set_xticks(ev.index)
ax.text(0.02,0.97,f'EV growth: +{ev_g:.0f}%', transform=ax.transAxes,va='top',fontsize=9,
        color=RED,fontweight='bold',bbox=dict(boxstyle='round,pad=0.3',facecolor='#FDECEA',edgecolor=RED,alpha=0.8))
plt.tight_layout(); plt.savefig(f'{OUT}/02_fuel_type_trend.png',dpi=150,bbox_inches='tight'); plt.close()
print(f"  ✓ Chart 2: EV adoption trend → +{ev_g:.0f}% growth")

# ── Chart 3: Brand market share pie ──────────────────────────────────────────
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(13,6))
brand_share = df.groupby('brand').size().sort_values(ascending=False)
brand_avg   = df.groupby('brand')['sale_price'].mean().sort_values()
ax1.pie(brand_share, labels=brand_share.index, autopct='%1.1f%%',
        colors=PALETTE, startangle=140, pctdistance=0.82,
        wedgeprops=dict(edgecolor='white',linewidth=1.5))
ax1.set_title('Brand Market Share',fontsize=13,fontweight='bold',color=NAVY)
bars = ax2.barh(brand_avg.index, brand_avg.values/1000, color=PALETTE[:len(brand_avg)], edgecolor='white')
for bar, val in zip(bars, brand_avg.values/1000):
    ax2.text(val+0.3, bar.get_y()+bar.get_height()/2, f'${val:.0f}K', va='center', fontsize=9)
ax2.set_title('Average Sale Price by Brand',fontsize=13,fontweight='bold',color=NAVY)
ax2.set_xlabel('Average Price (AUD $000s)',fontsize=10)
plt.suptitle('Brand Analysis — Australian Car Market',fontsize=14,fontweight='bold',color=NAVY)
plt.tight_layout(); plt.savefig(f'{OUT}/03_brand_analysis.png',dpi=150,bbox_inches='tight'); plt.close()
print(f"  ✓ Chart 3: Brand market share → {brand_share.index[0]} leads")

# ════════════════════════════════════════════════════════
# MULTIPLE LINEAR REGRESSION — Predicting Sale Price
# Features: year, quarter, brand (encoded), body_type (encoded), fuel_type (encoded)
# ════════════════════════════════════════════════════════
print(f"\n  {'─'*60}")
print("  MULTIPLE LINEAR REGRESSION — Sale Price Prediction")
df_reg = df.copy()
for col in ['brand','body_type','fuel_type','state']:
    le = LabelEncoder()
    df_reg[col+'_enc'] = le.fit_transform(df_reg[col])

features = ['year','quarter','brand_enc','body_type_enc','fuel_type_enc','state_enc']
X = df_reg[features]
y = df_reg['sale_price']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

lr = LinearRegression()
lr.fit(X_tr, y_tr)
y_pred = lr.predict(X_te)
r2   = r2_score(y_te, y_pred)
rmse = np.sqrt(mean_squared_error(y_te, y_pred))
mape = np.mean(np.abs((y_te.values - y_pred)/y_te.values))*100

print(f"  Features used : {', '.join(features)}")
print(f"  Train size    : {len(X_tr):,}  |  Test size: {len(X_te):,}")
print(f"  R²            : {r2:.4f}")
print(f"  RMSE          : ${rmse:,.0f}")
print(f"  MAPE          : {mape:.2f}%")
print(f"\n  Feature Coefficients:")
for feat, coef in sorted(zip(features, lr.coef_), key=lambda x: abs(x[1]), reverse=True):
    print(f"    {feat:<18}: {coef:>+10,.2f}")

# Correlation matrix
print(f"\n  Correlation with Sale Price:")
corr = df_reg[features+['sale_price']].corr()['sale_price'].drop('sale_price').sort_values(key=abs, ascending=False)
for feat, val in corr.items():
    print(f"    {feat:<18}: {val:>+.4f}")

# Chart 4: Regression diagnostics
fig, axes = plt.subplots(1,3,figsize=(15,5))
axes[0].scatter(y_te, y_pred, alpha=0.3, s=15, color=TEAL)
mn,mx = y_te.min(),y_te.max()
axes[0].plot([mn,mx],[mn,mx],color=RED,linewidth=1.5,linestyle='--',label='Perfect fit')
axes[0].set_title(f'Actual vs Predicted\nR²={r2:.4f}',fontsize=11,fontweight='bold',color=NAVY)
axes[0].set_xlabel('Actual Price ($)'); axes[0].set_ylabel('Predicted Price ($)')
axes[0].legend(fontsize=9)

resid = y_te.values - y_pred
axes[1].hist(resid, bins=30, color=TEAL, edgecolor='white', alpha=0.85)
axes[1].axvline(0, color=RED, linewidth=1.5, linestyle='--')
axes[1].set_title('Residual Distribution',fontsize=11,fontweight='bold',color=NAVY)
axes[1].set_xlabel('Residual ($)'); axes[1].set_ylabel('Frequency')

coef_df = pd.Series(np.abs(lr.coef_), index=features).sort_values()
axes[2].barh(coef_df.index, coef_df.values, color=PALETTE[:len(coef_df)], edgecolor='white')
axes[2].set_title('Feature Importance\n(|Coefficient|)',fontsize=11,fontweight='bold',color=NAVY)
axes[2].set_xlabel('|Coefficient|')
plt.suptitle('Multiple Linear Regression — Sale Price Prediction Diagnostics',fontsize=13,fontweight='bold',color=NAVY)
plt.tight_layout(); plt.savefig(f'{OUT}/04_regression_diagnostics.png',dpi=150,bbox_inches='tight'); plt.close()
print(f"\n  ✓ Chart 4: Regression diagnostics (actual vs predicted, residuals, coefficients)")

# Chart 5: Seasonal quarterly pattern
fig, ax = plt.subplots(figsize=(9,5))
q_s = df.groupby('quarter').size().reset_index(name='units')
bars = ax.bar(q_s['quarter'], q_s['units'], color=[NAVY,TEAL,GOLD,RED], edgecolor='white', width=0.6)
for bar, v in zip(bars, q_s['units']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5, f'{v:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_xticks([1,2,3,4]); ax.set_xticklabels(['Q1\n(Jan–Mar)','Q2\n(Apr–Jun)','Q3\n(Jul–Sep)','Q4\n(Oct–Dec)'])
ax.set_title('Sales Volume by Quarter — Seasonal Pattern',fontsize=14,fontweight='bold',color=NAVY,pad=15)
ax.set_xlabel('Quarter',fontsize=11); ax.set_ylabel('Units Sold',fontsize=11)
plt.tight_layout(); plt.savefig(f'{OUT}/05_seasonal_pattern.png',dpi=150,bbox_inches='tight'); plt.close()
print("  ✓ Chart 5: Seasonal quarterly pattern")

print(f"\n{'='*60}\n  CONCLUSIONS\n{'='*60}")
print(f"  1. NSW+VIC account for {pct_nv:.0f}% of national sales.")
print(f"  2. EV registrations grew {ev_g:.0f}% from 2019–2024.")
print(f"  3. Multiple Linear Regression achieves R²={r2:.3f},")
print(f"     explaining {r2*100:.0f}% of sale price variance.")
print(f"  4. Brand and fuel type are the strongest price predictors.")
print(f"  5. MAPE of {mape:.1f}% indicates predictions are within")
print(f"     ~${(mape/100*df['sale_price'].mean()):,.0f} of actual price on average.")
print(f"\n  Charts saved to: visuals/\n{'='*60}\n")
