"""
Big-O Examples — Lesson 01
Run this file to *see* the dramatic differences between complexity classes.

Usage:
    python big_o_examples.py
"""

import time


# ----------------------------------------------------------------------
# O(1) — Constant time
# ----------------------------------------------------------------------
def get_first(arr):
    """O(1): always one operation, regardless of arr size."""
    return arr[0]


# ----------------------------------------------------------------------
# O(n) — Linear time
# ----------------------------------------------------------------------
def find_max(arr):
    """O(n): touch every element once."""
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val


# ----------------------------------------------------------------------
# O(n²) — Quadratic time
# ----------------------------------------------------------------------
def has_duplicate_slow(arr):
    """O(n²): nested loop. Avoid for large inputs."""
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False


# ----------------------------------------------------------------------
# O(n) — Same problem, but faster using a set
# ----------------------------------------------------------------------
def has_duplicate_fast(arr):
    """O(n): one pass with a set. Same problem, way faster."""
    seen = set()
    for x in arr:
        if x in seen:
            return True
        seen.add(x)
    return False


# ----------------------------------------------------------------------
# O(log n) — Binary search
# ----------------------------------------------------------------------
def binary_search(arr, target):
    """O(log n): halve the search space each step."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# ----------------------------------------------------------------------
# O(2ⁿ) — Naive recursive Fibonacci
# ----------------------------------------------------------------------
def fib(n):
    """O(2ⁿ): each call branches into two. Watch this explode."""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


# ----------------------------------------------------------------------
# Helper to time a function
# ----------------------------------------------------------------------
def time_it(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    elapsed = (time.perf_counter() - start) * 1000  # ms
    print(f"  {label:<35} {elapsed:10.3f} ms")


if __name__ == "__main__":
    print("=" * 65)
    print("BIG-O IN ACTION")
    print("=" * 65)

    # --- Compare O(n²) vs O(n) for has_duplicate ---
    print("\n🔬 has_duplicate: O(n²) vs O(n)")
    print("-" * 65)
    for size in [1_000, 5_000, 10_000]:
        arr = list(range(size)) + [0]  # duplicate at the end (worst case)
        print(f"\nInput size: {size:,}")
        time_it("O(n²) has_duplicate_slow", has_duplicate_slow, arr)
        time_it("O(n)  has_duplicate_fast", has_duplicate_fast, arr)

    # --- Binary search speed ---
    print("\n🔬 Searching a sorted list of 10,000,000 numbers for 9,999,999")
    print("-" * 65)
    big = list(range(10_000_000))
    time_it("O(log n) binary_search", binary_search, big, 9_999_999)
    time_it("O(n)     'in' operator", lambda a, t: t in a, big, 9_999_999)

    # --- Exponential blow-up ---
    print("\n🔬 Naive recursive fib(n) — exponential blow-up")
    print("-" * 65)
    for n in [10, 20, 30, 35]:
        time_it(f"fib({n})", fib, n)

    print("\n✅ Notice how O(n²) and O(2ⁿ) explode with input size.")
    print("This is why algorithm choice matters!")
