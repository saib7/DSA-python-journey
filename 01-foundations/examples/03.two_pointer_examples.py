"""
Two-Pointer Examples — Lesson 03
Runnable demonstrations of the two-pointer pattern in both flavors.

Usage:
    python two_pointer_examples.py
"""

import time


# ======================================================================
# FLAVOR 1: OPPOSITE ENDS (converging)
# ======================================================================

def is_palindrome(s):
    """O(n) time, O(1) space — better than the recursive version."""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def two_sum_sorted(arr, target):
    """Given SORTED arr, return indices of pair summing to target."""
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1
    return []


def max_area(heights):
    """Container with Most Water — classic LeetCode."""
    left, right = 0, len(heights) - 1
    max_water = 0
    while left < right:
        water = min(heights[left], heights[right]) * (right - left)
        max_water = max(max_water, water)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_water


def sorted_squares(arr):
    """Return squares of a sorted array, sorted, in O(n)."""
    n = len(arr)
    result = [0] * n
    left, right = 0, n - 1
    for i in range(n - 1, -1, -1):
        if abs(arr[left]) > abs(arr[right]):
            result[i] = arr[left] ** 2
            left += 1
        else:
            result[i] = arr[right] ** 2
            right -= 1
    return result


# ======================================================================
# FLAVOR 2: FAST / SLOW (same direction)
# ======================================================================

def remove_duplicates(arr):
    """Remove duplicates from sorted array in place. Return new length."""
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1


def move_zeros(arr):
    """Move all zeros to the end, preserving order of non-zeros."""
    slow = 0
    for fast in range(len(arr)):
        if arr[fast] != 0:
            arr[slow], arr[fast] = arr[fast], arr[slow]
            slow += 1


# ======================================================================
# COMBO: LOOP + TWO-POINTER (3Sum)
# ======================================================================

def three_sum(nums):
    """Return all UNIQUE triplets that sum to 0. O(n²) time."""
    nums = sorted(nums)
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result


# ======================================================================
# BRUTE-FORCE COMPARISONS (to show the speedup)
# ======================================================================

def two_sum_brute(arr, target):
    """O(n²) — the version two-pointer beats."""
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return [i, j]
    return []


def sorted_squares_brute(arr):
    """O(n log n) — square then sort. Two-pointer version is O(n)."""
    return sorted(x * x for x in arr)


# ======================================================================
# Timing helper
# ======================================================================

def time_it(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  {label:<40} {elapsed:10.3f} ms")


if __name__ == "__main__":
    print("=" * 70)
    print("TWO-POINTER PATTERN IN ACTION")
    print("=" * 70)

    # --- Correctness demos ---
    print("\n✅ Correctness")
    print("-" * 70)
    print(f"  is_palindrome('racecar')        → {is_palindrome('racecar')}")
    print(f"  is_palindrome('hello')          → {is_palindrome('hello')}")
    print(f"  two_sum_sorted([1,2,4,7], 9)    → {two_sum_sorted([1,2,4,7], 9)}")
    print(f"  max_area([1,8,6,2,5,4,8,3,7])   → {max_area([1,8,6,2,5,4,8,3,7])}")
    print(f"  sorted_squares([-4,-1,0,3,10])  → {sorted_squares([-4,-1,0,3,10])}")

    arr = [1, 1, 2, 2, 3]
    n = remove_duplicates(arr)
    print(f"  remove_duplicates([1,1,2,2,3])  → length={n}, prefix={arr[:n]}")

    arr = [0, 1, 0, 3, 12]
    move_zeros(arr)
    print(f"  move_zeros([0,1,0,3,12])        → {arr}")

    print(f"  three_sum([-1,0,1,2,-1,-4])     → {three_sum([-1,0,1,2,-1,-4])}")

    # --- Speed comparison ---
    print("\n🔬 Two-pointer O(n) vs brute-force O(n²)")
    print("-" * 70)
    for size in [1_000, 10_000, 50_000]:
        arr = list(range(size))
        target = 2 * size - 3  # exists at the end
        print(f"\nInput size: {size:,}")
        time_it("O(n²) two_sum_brute", two_sum_brute, arr, target)
        time_it("O(n)  two_sum_sorted", two_sum_sorted, arr, target)

    print("\n🔬 Sorted squares: O(n log n) sort vs O(n) two-pointer")
    print("-" * 70)
    for size in [10_000, 100_000, 1_000_000]:
        arr = list(range(-size // 2, size // 2))
        print(f"\nInput size: {size:,}")
        time_it("O(n log n) sorted_squares_brute", sorted_squares_brute, arr)
        time_it("O(n)       sorted_squares",        sorted_squares,       arr)

    print("\n✅ Two-pointer wins by orders of magnitude on large inputs.")
