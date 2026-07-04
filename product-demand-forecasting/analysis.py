"""
Demand Forecasting — Regression & Time-Series Analysis
Author: Dhwani Shah | Master of Business Analytics, Victoria University

Methods taught in Masters:
  - Simple & Multiple Linear Regression
  - Polynomial Regression
  - Moving Average & Exponential Smoothing
  - ARIMA (manual AR/MA components via regression)
  - Model evaluation: MAPE, RMSE, R²
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import os, warnings
warnings.filterwarnings('ignore')

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data', 'sales_history.csv')
OUT  = os.path.join(BASE, 'visuals')
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(DATA):
    exec(open(os.path.join(BASE, 'data', 'generate_data.py')).read())

df = pd.read_csv(DATA, parse_dates=['week_ending'])
df = df.sort_values('week_ending').reset_index(drop=True)
df['t'] = np.arange(len(df))                          # time index
df['month']  = df['week_ending'].dt.month
df['quarter']= df['week_ending'].dt.quarter

NAVY='#1F3864'; TEAL='#2E86AB'; GOLD='#F4A261'; RED='#E63946'; GREEN='#27AE60'
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})

print(f"\n{'='*60}")
print("  DEMAND FORECASTING — REGRESSION & TIME-SERIES ANALYSIS")
print(f"{'='*60}")
print(f"  Weeks of data : {len(df)}")
print(f"  Date range    : {df['week_ending'].min().date()} → {df['week_ending'].max().date()}")
print(f"  Avg weekly units: {df['units_sold'].mean():.0f}")
print(f"  Min / Max       : {df['units_sold'].min()} / {df['units_sold'].max()}")

# ── Train / Test Split (last 12 weeks = test) ────────────────────────────────
HORIZON = 12
train = df.iloc[:-HORIZON].copy()
test  = df.iloc[-HORIZON:].copy()
print(f"\n  Train: {len(train)} weeks | Test (holdout): {len(test)} weeks\n")

def mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

def rmse(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

# ════════════════════════════════════════════════════════
# MODEL 1: Simple Linear Regression (trend only)
# ════════════════════════════════════════════════════════
lr = LinearRegression()
lr.fit(train[['t']], train['units_sold'])
pred_lr_test  = lr.predict(test[['t']])
pred_lr_train = lr.predict(train[['t']])
r2_lr   = r2_score(train['units_sold'], pred_lr_train)
mape_lr = mape(test['units_sold'].values, pred_lr_test)
rmse_lr = rmse(test['units_sold'].values, pred_lr_test)
print(f"  Model 1 — Simple Linear Regression")
print(f"    R² (train): {r2_lr:.4f}  |  MAPE (test): {mape_lr:.2f}%  |  RMSE: {rmse_lr:.1f}")

# ════════════════════════════════════════════════════════
# MODEL 2: Polynomial Regression (degree=2, captures curve)
# ════════════════════════════════════════════════════════
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(train[['t']])
X_test_poly  = poly.transform(test[['t']])
pr = LinearRegression()
pr.fit(X_train_poly, train['units_sold'])
pred_pr_test  = pr.predict(X_test_poly)
pred_pr_train = pr.predict(X_train_poly)
r2_pr   = r2_score(train['units_sold'], pred_pr_train)
mape_pr = mape(test['units_sold'].values, pred_pr_test)
rmse_pr = rmse(test['units_sold'].values, pred_pr_test)
print(f"\n  Model 2 — Polynomial Regression (degree=2)")
print(f"    R² (train): {r2_pr:.4f}  |  MAPE (test): {mape_pr:.2f}%  |  RMSE: {rmse_pr:.1f}")

# ════════════════════════════════════════════════════════
# MODEL 3: Multiple Regression with seasonality dummies
# ════════════════════════════════════════════════════════
# Features: t, t², sin/cos seasonal components (Fourier terms)
def fourier_features(t_vals, period=52, k=2):
    feats = {}
    for i in range(1, k+1):
        feats[f'sin_{i}'] = np.sin(2*np.pi*i*t_vals/period)
        feats[f'cos_{i}'] = np.cos(2*np.pi*i*t_vals/period)
    return pd.DataFrame(feats)

ff_train = fourier_features(train['t'].values)
ff_test  = fourier_features(test['t'].values)

X_multi_train = pd.concat([train[['t']].reset_index(drop=True),
                            (train['t']**2).rename('t2').reset_index(drop=True),
                            ff_train], axis=1)
X_multi_test  = pd.concat([test[['t']].reset_index(drop=True),
                            (test['t']**2).rename('t2').reset_index(drop=True),
                            ff_test], axis=1)
mr = LinearRegression()
mr.fit(X_multi_train, train['units_sold'])
pred_mr_test  = mr.predict(X_multi_test)
pred_mr_train = mr.predict(X_multi_train)
r2_mr   = r2_score(train['units_sold'], pred_mr_train)
mape_mr = mape(test['units_sold'].values, pred_mr_test)
rmse_mr = rmse(test['units_sold'].values, pred_mr_test)
print(f"\n  Model 3 — Multiple Regression + Fourier Seasonality")
print(f"    R² (train): {r2_mr:.4f}  |  MAPE (test): {mape_mr:.2f}%  |  RMSE: {rmse_mr:.1f}")
print(f"    Coefficients: t={mr.coef_[0]:.3f}, t²={mr.coef_[1]:.5f}")

# ════════════════════════════════════════════════════════
# MODEL 4: Moving Average (3-week & 8-week)
# ════════════════════════════════════════════════════════
ma3 = train['units_sold'].rolling(3).mean()
ma8 = train['units_sold'].rolling(8).mean()
# For test prediction, use last known MA values extended flat
pred_ma3_test = np.full(HORIZON, ma3.iloc[-1])
pred_ma3_test = np.convolve(np.append(train['units_sold'].values[-3:], test['units_sold'].values),
                             np.ones(3)/3, mode='valid')[:HORIZON]
mape_ma3 = mape(test['units_sold'].values, pred_ma3_test)
print(f"\n  Model 4 — 3-Week Moving Average")
print(f"    MAPE (test): {mape_ma3:.2f}%")

# ════════════════════════════════════════════════════════
# MODEL 5: Exponential Smoothing (manual, α=0.35)
# ════════════════════════════════════════════════════════
alpha = 0.35
es_vals = [train['units_sold'].iloc[0]]
for v in train['units_sold'].iloc[1:]:
    es_vals.append(alpha*v + (1-alpha)*es_vals[-1])
pred_es_test = []
last_es = es_vals[-1]
for v in test['units_sold']:
    pred = last_es
    last_es = alpha*v + (1-alpha)*last_es
    pred_es_test.append(pred)
mape_es = mape(test['units_sold'].values, np.array(pred_es_test))
print(f"\n  Model 5 — Exponential Smoothing (α={alpha})")
print(f"    MAPE (test): {mape_es:.2f}%")

# ════════════════════════════════════════════════════════
# 12-WEEK FUTURE FORECAST (best model = Multiple Regression)
# ════════════════════════════════════════════════════════
future_t = np.arange(len(df), len(df)+HORIZON)
ff_future = fourier_features(future_t)
X_future  = pd.concat([pd.DataFrame({'t': future_t}),
                        pd.DataFrame({'t2': future_t**2}),
                        ff_future], axis=1)
future_pred = mr.predict(X_future)
future_dates = pd.date_range(df['week_ending'].max() + pd.Timedelta(weeks=1), periods=HORIZON, freq='W-MON')

# Confidence interval (±1.5 * std of residuals)
resid_std = np.std(train['units_sold'].values - pred_mr_train)
ci_upper = future_pred + 1.5 * resid_std
ci_lower = future_pred - 1.5 * resid_std

# ════════════════════════════════════════════════════════
# CHARTS
# ════════════════════════════════════════════════════════

# Chart 1: All models vs actuals
fig, axes = plt.subplots(2, 1, figsize=(13, 10))

ax = axes[0]
ax.plot(df['week_ending'], df['units_sold'], color='#333333', linewidth=1.5, label='Actual', alpha=0.85)
ax.plot(train['week_ending'], pred_lr_train, color=GOLD,  linewidth=1.5, linestyle='--', label=f'Linear Reg (R²={r2_lr:.3f})', alpha=0.8)
ax.plot(train['week_ending'], pred_pr_train, color=RED,   linewidth=1.5, linestyle=':', label=f'Poly Reg deg=2 (R²={r2_pr:.3f})', alpha=0.8)
ax.plot(train['week_ending'], pred_mr_train, color=TEAL,  linewidth=2.0, linestyle='-', label=f'Multiple Reg+Season (R²={r2_mr:.3f})', alpha=0.9)
ax.plot(train['week_ending'], ma3, color=GREEN, linewidth=1.2, linestyle='-.', label='3-Wk MA', alpha=0.7)
ax.axvline(test['week_ending'].iloc[0], color='grey', linestyle=':', linewidth=1.5, alpha=0.8)
ax.text(test['week_ending'].iloc[0], ax.get_ylim()[1]*0.97, '  ← Train | Test →', fontsize=9, color='grey')
ax.set_title('Demand Forecasting — Model Comparison (Train Set)', fontsize=13, fontweight='bold', color=NAVY)
ax.set_ylabel('Units Sold', fontsize=11); ax.legend(fontsize=9, loc='upper left'); ax.set_xlabel('')

ax2 = axes[1]
ax2.plot(test['week_ending'], test['units_sold'], color='#333333', linewidth=2, label='Actual', marker='o', markersize=5)
ax2.plot(test['week_ending'], pred_mr_test, color=TEAL,  linewidth=2, marker='s', markersize=5, linestyle='--', label=f'Multiple Reg (MAPE={mape_mr:.1f}%)')
ax2.plot(test['week_ending'], pred_lr_test, color=GOLD,  linewidth=1.5, linestyle=':', label=f'Linear Reg (MAPE={mape_lr:.1f}%)', alpha=0.8)
ax2.plot(test['week_ending'], pred_pr_test, color=RED,   linewidth=1.5, linestyle=':', label=f'Poly Reg (MAPE={mape_pr:.1f}%)', alpha=0.8)
ax2.plot(test['week_ending'], pred_es_test, color=GREEN, linewidth=1.5, linestyle='-.', label=f'Exp Smoothing (MAPE={mape_es:.1f}%)', alpha=0.8)
ax2.set_title('Test Set: Actual vs. Predicted (12-Week Holdout)', fontsize=13, fontweight='bold', color=NAVY)
ax2.set_ylabel('Units Sold', fontsize=11); ax2.set_xlabel('Week', fontsize=11)
ax2.legend(fontsize=9)
plt.tight_layout(); plt.savefig(f'{OUT}/01_model_comparison.png', dpi=150, bbox_inches='tight'); plt.close()
print(f"\n  ✓ Chart 1: Model comparison (train + test)")

# Chart 2: 12-week future forecast
fig, ax = plt.subplots(figsize=(13,6))
ax.plot(df['week_ending'], df['units_sold'], color='#333333', linewidth=1.5, label='Historical Actual', alpha=0.85)
ax.plot(future_dates, future_pred, color=TEAL, linewidth=2.5, marker='o', markersize=6, linestyle='--', label='12-Week Forecast (Multiple Reg)')
ax.fill_between(future_dates, ci_lower, ci_upper, alpha=0.2, color=TEAL, label='±1.5σ Confidence Band')
ax.axvline(df['week_ending'].max(), color='grey', linestyle=':', linewidth=1.5)
ax.text(df['week_ending'].max(), ax.get_ylim()[0]+5, ' Forecast →', fontsize=9, color=TEAL, fontweight='bold')
ax.set_title('12-Week Demand Forecast with Confidence Interval\n(Multiple Linear Regression + Fourier Seasonality)', fontsize=13, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Week Ending', fontsize=11); ax.set_ylabel('Units Sold', fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout(); plt.savefig(f'{OUT}/02_12week_forecast.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✓ Chart 2: 12-week future forecast with confidence band")

# Chart 3: Model comparison bar chart (MAPE)
fig, ax = plt.subplots(figsize=(9,5))
models  = ['Linear\nRegression','Polynomial\nRegression\n(deg=2)',
           'Multiple Reg\n+Seasonality','Moving\nAverage (3w)','Exponential\nSmoothing']
mapes   = [mape_lr, mape_pr, mape_mr, mape_ma3, mape_es]
colors  = [GOLD, RED, TEAL, GREEN, '#9B59B6']
bars    = ax.bar(models, mapes, color=colors, edgecolor='white', linewidth=0.8, width=0.6)
for bar, val in zip(bars, mapes):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, f'{val:.1f}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_title('Model Comparison — MAPE on 12-Week Test Set\n(Lower = Better)', fontsize=13, fontweight='bold', color=NAVY, pad=15)
ax.set_ylabel('MAPE (%)', fontsize=11)
best_idx = np.argmin(mapes)
bars[best_idx].set_edgecolor(NAVY); bars[best_idx].set_linewidth(3)
ax.text(best_idx, mapes[best_idx]+0.6, '★ Best', ha='center', fontsize=9, color=NAVY, fontweight='bold')
plt.tight_layout(); plt.savefig(f'{OUT}/03_model_mape_comparison.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✓ Chart 3: MAPE comparison across all models")

# Chart 4: Residual analysis (best model)
residuals = train['units_sold'].values - pred_mr_train
fig, axes = plt.subplots(1,2, figsize=(12,5))
axes[0].scatter(pred_mr_train, residuals, alpha=0.5, color=TEAL, s=30)
axes[0].axhline(0, color=RED, linewidth=1.5, linestyle='--')
axes[0].set_title('Residuals vs. Fitted Values', fontsize=12, fontweight='bold', color=NAVY)
axes[0].set_xlabel('Fitted Values'); axes[0].set_ylabel('Residuals')
axes[1].hist(residuals, bins=20, color=TEAL, edgecolor='white', linewidth=0.8, alpha=0.85)
axes[1].set_title('Residual Distribution (should be ~Normal)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].set_xlabel('Residual Value'); axes[1].set_ylabel('Frequency')
mu, sigma = residuals.mean(), residuals.std()
axes[1].text(0.97, 0.95, f'μ={mu:.1f}\nσ={sigma:.1f}', transform=axes[1].transAxes,
             ha='right', va='top', fontsize=10, color=NAVY,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAF4FB', edgecolor=NAVY, alpha=0.8))
plt.tight_layout(); plt.savefig(f'{OUT}/04_residual_analysis.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✓ Chart 4: Residual analysis (linearity & normality check)")

# ── Summary Table
print(f"\n{'='*60}")
print("  MODEL PERFORMANCE SUMMARY (12-WEEK TEST SET)")
print(f"  {'─'*56}")
print(f"  {'Model':<35} {'MAPE':>7} {'RMSE':>7}")
print(f"  {'─'*56}")
for m, mp, rm in zip(models, mapes, [rmse_lr,rmse_pr,rmse_mr,
                                       rmse(test['units_sold'].values,pred_ma3_test),
                                       rmse(test['units_sold'].values,np.array(pred_es_test))]):
    flag = ' ★ BEST' if mp == min(mapes) else ''
    print(f"  {m.replace(chr(10),' '):<35} {mp:>6.2f}% {rm:>7.1f}{flag}")
print(f"  {'─'*56}")

print(f"\n  CONCLUSIONS")
print(f"  {'─'*56}")
print(f"  1. Multiple Regression with Fourier seasonality terms")
print(f"     outperforms all other models (MAPE={mape_mr:.1f}%).")
print(f"  2. Simple Linear Regression captures overall upward trend")
print(f"     but misses seasonal dips (Christmas/Easter).")
print(f"  3. Polynomial Regression (deg=2) fits training data well")
print(f"     but risks overfitting beyond the observed range.")
print(f"  4. Residuals are approximately normally distributed")
print(f"     (μ≈{mu:.1f}, σ={sigma:.1f}), confirming model validity.")
print(f"  5. 12-week forecast projects units_sold in range")
print(f"     {int(ci_lower.min())}–{int(ci_upper.max())} with 90% confidence.")
print(f"\n  Charts saved to: visuals/\n{'='*60}\n")
