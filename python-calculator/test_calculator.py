"""Unit tests for the Scientific Calculator."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from calculator import Calculator

calc = Calculator()
passed = failed = 0

def test(name, got, expected, tol=1e-9):
    global passed, failed
    ok = abs(got - expected) < tol
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: got {got:.6g}, expected {expected:.6g}")
    if ok: passed += 1
    else:   failed += 1

print("\n" + "="*50)
print("  CALCULATOR UNIT TESTS")
print("="*50)
test("add(3, 4)",            calc.add(3, 4),       7)
test("subtract(10, 3)",      calc.subtract(10, 3), 7)
test("multiply(6, 7)",       calc.multiply(6, 7),  42)
test("divide(15, 4)",        calc.divide(15, 4),   3.75)
test("power(2, 8)",          calc.power(2, 8),     256)
test("sqrt(225)",            calc.sqrt(225),       15)
test("log(1000, 10)",        calc.log(1000, 10),   3)
test("factorial(5)",         calc.factorial(5),    120)
test("percent(200, 10)",     calc.percent(200, 10), 20)
calc.memory_store(99)
test("memory_recall",        calc.memory_recall(), 99)

# Error handling
try:
    calc.divide(1, 0)
    print("  [FAIL] divide by zero should raise")
    failed += 1
except ValueError:
    print("  [PASS] divide by zero raises ValueError")
    passed += 1

try:
    calc.sqrt(-4)
    print("  [FAIL] sqrt(-4) should raise")
    failed += 1
except ValueError:
    print("  [PASS] sqrt(-4) raises ValueError")
    passed += 1

print(f"\n  Results: {passed} passed, {failed} failed")
print("="*50 + "\n")
