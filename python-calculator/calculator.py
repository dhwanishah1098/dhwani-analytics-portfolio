"""
Scientific Calculator — Python CLI
Author: Dhwani Shah | Master of Business Analytics, Victoria University

Features: basic arithmetic, power, square root, logarithm, factorial, memory store/recall
"""
import math

class Calculator:
    def __init__(self):
        self.history = []
        self.memory = 0

    def add(self, a, b):
        result = a + b
        self._record(f"{a} + {b}", result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._record(f"{a} - {b}", result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._record(f"{a} × {b}", result)
        return result

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is undefined.")
        result = a / b
        self._record(f"{a} ÷ {b}", result)
        return result

    def power(self, base, exp):
        result = base ** exp
        self._record(f"{base}^{exp}", result)
        return result

    def sqrt(self, a):
        if a < 0:
            raise ValueError("Square root of negative number is undefined in real numbers.")
        result = math.sqrt(a)
        self._record(f"√{a}", result)
        return result

    def log(self, a, base=10):
        if a <= 0:
            raise ValueError("Logarithm requires a positive argument.")
        result = math.log(a, base)
        self._record(f"log_{base}({a})", result)
        return result

    def factorial(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Factorial requires a non-negative integer.")
        result = math.factorial(n)
        self._record(f"{n}!", result)
        return result

    def percent(self, a, pct):
        result = a * pct / 100
        self._record(f"{pct}% of {a}", result)
        return result

    def memory_store(self, val):
        self.memory = val
        print(f"  Memory stored: {val}")

    def memory_recall(self):
        return self.memory

    def _record(self, expr, result):
        self.history.append(f"  {expr} = {result}")

    def show_history(self):
        if not self.history:
            print("  No calculations yet.")
        else:
            print("\n  Calculation History:")
            for h in self.history[-10:]:
                print(h)


def run_demo():
    calc = Calculator()
    print("\n" + "="*50)
    print("  SCIENTIFIC CALCULATOR — DEMO")
    print("="*50)

    ops = [
        ("Addition",         calc.add(145.75, 234.25)),
        ("Subtraction",      calc.subtract(500, 185.50)),
        ("Multiplication",   calc.multiply(42, 7.5)),
        ("Division",         calc.divide(1250, 4)),
        ("Power",            calc.power(2, 10)),
        ("Square Root",      calc.sqrt(144)),
        ("Log base 10",      calc.log(1000)),
        ("Natural Log",      calc.log(math.e, math.e)),
        ("Factorial",        calc.factorial(8)),
        ("Percent",          calc.percent(850, 15)),
    ]

    for label, result in ops:
        print(f"  {label:<20}: {result}")

    calc.memory_store(calc.add(100, 200))
    print(f"  Memory Recall       : {calc.memory_recall()}")
    calc.show_history()
    print("="*50 + "\n")


if __name__ == "__main__":
    run_demo()
