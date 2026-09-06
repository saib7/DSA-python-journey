"""
Hash Table Examples — Lesson 05
The five core hash table patterns with brute-force comparisons.

Usage:
    python hash_table_examples.py
"""

import time
from collections import Counter, defaultdict


# ======================================================================
# PATTERN 1: MEMBERSHIP CHECK
# ======================================================================

def has_duplicate(nums):
    """O(n) with a set."""
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def has_duplicate_brute(nums):
    """O(n²) — the version hash tables beat."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


# ======================================================================
# PATTERN 2: FREQUENCY COUNTING
# ======================================================================

def char_counts(s):
    """Return a dict of char → count."""
    counts = defaultdict(int)
    for c in s:
        counts[c] += 1
    return dict(counts)


def most_frequent_char(s):
    return Counter(s).most_common(1)[0]


# ======================================================================
# PATTERN 3: COMPLEMENT LOOKUP — TWO SUM (UNSORTED)
# ======================================================================

def two_sum(nums, target):
    """O(n) with a dict."""
    seen = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []


def two_sum_brute(nums, target):
    """O(n²)."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ======================================================================
# PATTERN 4: GROUPING
# ======================================================================

def group_anagrams(strs):
    """Group words that are anagrams of each other."""
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())


def is_anagram(s, t):
    """Check if two strings are anagrams."""
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)


# ======================================================================
# PATTERN 5: PREFIX SUM + HASH MAP
# ======================================================================

def subarray_sum(nums, k):
    """Count contiguous subarrays whose sum equals k. O(n)."""
    count = 0
    running_sum = 0
    prefix_counts = {0: 1}
    for x in nums:
        running_sum += x
        if (running_sum - k) in prefix_counts:
            count += prefix_counts[running_sum - k]
        prefix_counts[running_sum] = prefix_counts.get(running_sum, 0) + 1
    return count


def subarray_sum_brute(nums, k):
    """O(n²) brute force."""
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count


# ======================================================================
# BONUS: `x in list` vs `x in set` — the classic Python speedup
# ======================================================================

def count_matches_list(needles, haystack_list):
    """Membership check against a LIST — O(m × n)."""
    count = 0
    for x in needles:
        if x in haystack_list:
            count += 1
    return count


def count_matches_set(needles, haystack_set):
    """Membership check against a SET — O(m)."""
    count = 0
    for x in needles:
        if x in haystack_set:
            count += 1
    return count


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
    print("HASH TABLES IN ACTION")
    print("=" * 75)

    # --- Correctness ---
    print("\n✅ Correctness")
    print("-" * 75)
    print(f"  has_duplicate([1,2,3,4,1])           → {has_duplicate([1,2,3,4,1])}")
    print(f"  char_counts('hello')                 → {char_counts('hello')}")
    print(f"  most_frequent_char('mississippi')    → {most_frequent_char('mississippi')}")
    print(f"  two_sum([3,2,4], 6)                  → {two_sum([3,2,4], 6)}")
    print(f"  is_anagram('anagram', 'nagaram')     → {is_anagram('anagram', 'nagaram')}")
    print(f"  group_anagrams(['eat','tea','tan','ate','nat','bat'])")
    print(f"    → {group_anagrams(['eat','tea','tan','ate','nat','bat'])}")
    print(f"  subarray_sum([1,1,1], 2)             → {subarray_sum([1,1,1], 2)}")
    print(f"  subarray_sum([1,2,3,-2,5], 3)        → {subarray_sum([1,2,3,-2,5], 3)}")

    # --- Two Sum speedup ---
    print("\n🔬 Two Sum: O(n²) brute vs O(n) hash map")
    print("-" * 75)
    for size in [1_000, 10_000, 50_000]:
        nums = list(range(size))
        target = 2 * size - 3
        print(f"\nInput size: {size:,}")
        time_it("O(n²) two_sum_brute", two_sum_brute, nums, target)
        time_it("O(n)  two_sum (hash)", two_sum, nums, target)

    # --- Subarray Sum Equals K speedup ---
    print("\n🔬 Subarray Sum = K: O(n²) brute vs O(n) prefix-sum hash")
    print("-" * 75)
    for size in [1_000, 5_000, 10_000]:
        nums = [1] * size
        k = size // 2
        print(f"\nInput size: {size:,}")
        time_it("O(n²) subarray_sum_brute", subarray_sum_brute, nums, k)
        time_it("O(n)  subarray_sum (hash)", subarray_sum, nums, k)

    # --- x in list vs x in set ---
    print("\n🔬 Membership: `x in list` (O(n)) vs `x in set` (O(1))")
    print("-" * 75)
    for size in [10_000, 100_000, 1_000_000]:
        haystack_list = list(range(size))
        haystack_set = set(haystack_list)
        needles = list(range(0, size, size // 100))  # 100 needles
        print(f"\nHaystack size: {size:,} (100 needles)")
        time_it("`x in list` (O(m × n))", count_matches_list, needles, haystack_list)
        time_it("`x in set`  (O(m))",     count_matches_set,  needles, haystack_set)

    print("\n✅ The last one is often 1000x+ faster on real inputs.")
