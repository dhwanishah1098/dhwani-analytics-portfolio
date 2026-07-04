# 🧮 Financial Calculator Suite (Python)

A command-line and web-based financial calculator suite built in Python, designed for common personal finance and business calculations relevant to the Australian context.

## 📌 Project Overview

Beyond a basic calculator — this suite covers:
- Standard arithmetic & scientific calculations
- **Loan repayment calculator** (with amortisation schedule)
- **Superannuation growth projector** (Australian super rules)
- **Tax estimator** (ATO 2024–25 brackets)
- **Currency converter** (live AUD rates via API)
- **GST calculator** (10% GST add/remove)

## 🛠️ Tools & Technologies
- Python 3.11 (core logic)
- `tkinter` (desktop GUI version)
- `requests` (live currency API)
- `pandas` (amortisation tables)

## 📁 Project Structure
```
06_calculator_app/
├── src/
│   ├── calculator.py          # Core arithmetic engine
│   ├── loan_calculator.py     # Loan & amortisation
│   ├── super_calculator.py    # Superannuation projector
│   ├── tax_estimator.py       # ATO tax bracket estimator
│   ├── currency_converter.py  # Live AUD converter
│   └── gst_calculator.py      # GST add/remove
├── gui/
│   └── app.py                 # tkinter GUI
├── tests/
│   └── test_calculators.py    # Unit tests
└── README.md
```

## 🔍 Sample — Australian Tax Estimator
```python
def estimate_tax(income: float) -> dict:
    """Estimate Australian income tax (FY2024-25 brackets)."""
    brackets = [
        (18200,   0,      0.00),
        (45000,   0,      0.19),
        (120000,  5092,   0.325),
        (180000,  29467,  0.37),
        (float('inf'), 51667, 0.45),
    ]
    
    tax = 0
    prev_threshold = 0
    for threshold, base, rate in brackets:
        if income <= threshold:
            tax = base + (income - prev_threshold) * rate
            break
        prev_threshold = threshold
    
    medicare_levy = income * 0.02
    total_tax = tax + medicare_levy
    
    return {
        'gross_income':   round(income, 2),
        'income_tax':     round(tax, 2),
        'medicare_levy':  round(medicare_levy, 2),
        'total_tax':      round(total_tax, 2),
        'net_income':     round(income - total_tax, 2),
        'effective_rate': round((total_tax / income) * 100, 2)
    }

# Example
result = estimate_tax(85000)
print(result)
# {'gross_income': 85000, 'income_tax': 18922.5, 'medicare_levy': 1700.0,
#  'total_tax': 20622.5, 'net_income': 64377.5, 'effective_rate': 24.26}
```

## 📈 How to Run
```bash
python src/tax_estimator.py
python src/loan_calculator.py
python gui/app.py   # Full GUI
```

---
*Part of Dhwani Shah's Data Analytics Portfolio*
