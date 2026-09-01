"""
Sliding Window Examples — Lesson 04
Fixed & variable-size window patterns with live timing comparisons.

Usage:
    python sliding_window_examples.py
"""

import time
from collections import Counter


# ======================================================================
# FIXED-SIZE WINDOW
# ======================================================================

def max_sum_subarray(arr, k):
    """Max sum of a subarray of size k. O(n)."""
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for right in range(k, len(arr)):
        window_sum += arr[right] - arr[right - k]
        max_sum = max(max_sum, window_sum)
    return max_sum


def max_sum_subarray_brute(arr, k):
    """Brute force: sum every window from scratch. O(n × k)."""
    max_sum = float('-inf')
    for i in range(len(arr) - k + 1):
        s = sum(arr[i:i + k])
        if s > max_sum:
            max_sum = s
    return max_sum


# ======================================================================
# VARIABLE-SIZE WINDOW — "longest with X" pattern (shrink on INVALID)
# ======================================================================

def longest_unique_substring(s):
    """Longest substring without repeating characters. O(n)."""
    seen = set()
    left = 0
    longest = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        longest = max(longest, right - left + 1)
    return longest


def longest_at_most_k_distinct(s, k):
    """Longest substring with at most k distinct chars. O(n)."""
    count = {}
    left = 0
    longest = 0
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        longest = max(longest, right - left + 1)
    return longest


# ======================================================================
# VARIABLE-SIZE WINDOW — "shortest with X" pattern (shrink on VALID)
# ======================================================================

def min_subarray_sum(arr, target):
    """Minimum length subarray with sum >= target. O(n)."""
    left = 0
    window_sum = 0
    min_len = float('inf')
    for right in range(len(arr)):
        window_sum += arr[right]
        while window_sum >= target:
            min_len = min(min_len, right - left + 1)
            window_sum -= arr[left]
            left += 1
    return 0 if min_len == float('inf') else min_len


def min_window(s, t):
    """Min window in s containing all chars of t. O(n + m)."""
    if not s or not t:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best_len = float('inf')
    best_start = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best_len == float('inf') else s[best_start:best_start + best_len]


# ======================================================================
# Timing helper
# ======================================================================

def time_it(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  {label:<45} {elapsed:10.3f} ms")


if __name__ == "__main__":
    print("=" * 75)
    print("SLIDING WINDOW PATTERN IN ACTION")
    print("=" * 75)

    # --- Correctness ---
    print("\n✅ Correctness")
    print("-" * 75)
    print(f"  max_sum_subarray([2,1,5,1,3,2], k=3)     → {max_sum_subarray([2,1,5,1,3,2], 3)}")
    print(f"  longest_unique_substring('abcabcbb')     → {longest_unique_substring('abcabcbb')}")
    print(f"  longest_at_most_k_distinct('eceba', 2)   → {longest_at_most_k_distinct('eceba', 2)}")
    print(f"  min_subarray_sum([2,3,1,2,4,3], 7)       → {min_subarray_sum([2,3,1,2,4,3], 7)}")
    print(f"  min_window('ADOBECODEBANC', 'ABC')       → {min_window('ADOBECODEBANC', 'ABC')!r}")

    # --- Fixed window speedup ---
    print("\n🔬 Fixed window: O(n × k) brute force vs O(n) sliding window")
    print("-" * 75)
    for size, k in [(10_000, 100), (100_000, 500), (500_000, 1000)]:
        arr = list(range(size))
        print(f"\nInput size: {size:,}, window k: {k}")
        time_it("O(n × k) max_sum_subarray_brute", max_sum_subarray_brute, arr, k)
        time_it("O(n)     max_sum_subarray",        max_sum_subarray,       arr, k)

    # --- Variable window on large strings ---
    print("\n🔬 Variable window on large strings (O(n) even with nested while)")
    print("-" * 75)
    for size in [10_000, 100_000, 1_000_000]:
        # Repeat "abcdefg" to make a long string with bounded uniqueness
        s = ("abcdefg" * (size // 7 + 1))[:size]
        print(f"\nString length: {size:,}")
        time_it("longest_unique_substring", longest_unique_substring, s)
        time_it("longest_at_most_k_distinct (k=3)", longest_at_most_k_distinct, s, 3)

    print("\n✅ Both scale linearly — the amortization argument in action.")
