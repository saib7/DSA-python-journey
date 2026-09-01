"""
Recursion Examples — Lesson 02
Run this file to see recursion patterns and the memoization speedup live.

Usage:
    python recursion_examples.py
"""

import sys
import time
from functools import lru_cache


# ----------------------------------------------------------------------
# Linear recursion
# ----------------------------------------------------------------------
def factorial(n):
    """O(n) time, O(n) space (call stack)."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def list_sum(arr, i=0):
    """O(n) time, O(n) space. Note: uses index to avoid O(n²) from slicing."""
    if i == len(arr):
        return 0
    return arr[i] + list_sum(arr, i + 1)


# ----------------------------------------------------------------------
# Binary recursion — naive vs memoized Fibonacci
# ----------------------------------------------------------------------
def fib_naive(n):
    """O(2ⁿ) time. Painfully slow past n=35."""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_memo(n):
    """O(n) time. Same code shape, vastly faster."""
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# ----------------------------------------------------------------------
# Power — naive O(n) vs fast O(log n) "exponentiation by squaring"
# ----------------------------------------------------------------------
def power_naive(x, n):
    """O(n)."""
    if n == 0:
        return 1
    return x * power_naive(x, n - 1)


def power_fast(x, n):
    """O(log n) — divide-and-conquer."""
    if n == 0:
        return 1
    half = power_fast(x, n // 2)
    return half * half if n % 2 == 0 else half * half * x


# ----------------------------------------------------------------------
# Classic exercises
# ----------------------------------------------------------------------
def reverse_str(s):
    if len(s) <= 1:
        return s
    return reverse_str(s[1:]) + s[0]


def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])


def count_occurrences(arr, target, i=0):
    if i == len(arr):
        return 0
    rest = count_occurrences(arr, target, i + 1)
    return rest + (1 if arr[i] == target else 0)


# ----------------------------------------------------------------------
# Tower of Hanoi — the canonical recursion problem
# ----------------------------------------------------------------------
def hanoi(n, source='A', target='C', helper='B'):
    """Total moves = 2ⁿ - 1."""
    if n == 1:
        print(f"  Move disk 1 from {source} → {target}")
        return
    hanoi(n - 1, source, helper, target)
    print(f"  Move disk {n} from {source} → {target}")
    hanoi(n - 1, helper, target, source)


# ----------------------------------------------------------------------
# Helper
# ----------------------------------------------------------------------
def time_it(label, fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  {label:<35} {elapsed:10.3f} ms")
    return result


if __name__ == "__main__":
    print("=" * 65)
    print("RECURSION IN ACTION")
    print("=" * 65)

    # --- The big lesson: memoization speedup ---
    print("\n🔬 Fibonacci: naive O(2ⁿ) vs memoized O(n)")
    print("-" * 65)
    for n in [20, 30, 35]:
        time_it(f"fib_naive({n})", fib_naive, n)
    print()
    for n in [30, 100, 500]:
        time_it(f"fib_memo({n})", fib_memo, n)
    print("\n  Memoized version handles n=500 instantly. Magic? No — caching.")

    # --- Power: linear vs log ---
    print("\n🔬 power(2, n): O(n) vs O(log n)")
    print("-" * 65)
    for n in [100, 500, 900]:
        time_it(f"power_naive(2, {n})", power_naive, 2, n)
        time_it(f"power_fast(2, {n})",  power_fast,  2, n)

    # --- Other classics ---
    print("\n🔬 Classic recursion examples")
    print("-" * 65)
    print(f"  factorial(10)               = {factorial(10)}")
    print(f"  list_sum([1,2,3,4,5])       = {list_sum([1, 2, 3, 4, 5])}")
    print(f"  reverse_str('hello')        = {reverse_str('hello')!r}")
    print(f"  is_palindrome('racecar')    = {is_palindrome('racecar')}")
    print(f"  count_occurrences([1,2,1,3,1], 1) = {count_occurrences([1,2,1,3,1], 1)}")

    # --- Tower of Hanoi ---
    print("\n🔬 Tower of Hanoi (n=3) — 7 moves expected (2³ − 1)")
    print("-" * 65)
    hanoi(3)

    # --- Recursion limit reminder ---
    print(f"\n⚠️  Python's recursion limit on this system: {sys.getrecursionlimit()}")
    print("    For deep linear recursion, use a loop instead.")
