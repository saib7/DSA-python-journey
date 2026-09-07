"""
Stacks & Queues Examples — Lesson 07
Fundamentals, monotonic stack, and monotonic deque patterns.

Usage:
    python stack_queue_examples.py
"""

import time
from collections import deque


# ======================================================================
# STACK BASICS
# ======================================================================

def is_valid(s):
    """Valid Parentheses. O(n) time, O(n) space."""
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack


# ======================================================================
# QUEUE USING TWO STACKS
# ======================================================================

class MyQueue:
    """Amortized O(1) per operation."""
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x):
        self.in_stack.append(x)

    def pop(self):
        self._shift()
        return self.out_stack.pop()

    def peek(self):
        self._shift()
        return self.out_stack[-1]

    def empty(self):
        return not self.in_stack and not self.out_stack

    def _shift(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())


# ======================================================================
# MONOTONIC STACK PATTERNS
# ======================================================================

def next_greater(nums):
    """For each element, next greater to the right (or -1). O(n)."""
    result = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            result[j] = x
        stack.append(i)
    return result


def daily_temperatures(temps):
    """Days until a warmer temperature. O(n)."""
    result = [0] * len(temps)
    stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def next_greater_circular(nums):
    """Circular version — loop through twice. O(n)."""
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return result


# ======================================================================
# BRUTE FORCE COMPARISON
# ======================================================================

def next_greater_brute(nums):
    """O(n²) brute force to compare with monotonic stack."""
    result = [-1] * len(nums)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[i]:
                result[i] = nums[j]
                break
    return result


# ======================================================================
# MONOTONIC DEQUE — SLIDING WINDOW MAXIMUM
# ======================================================================

def max_sliding_window(nums, k):
    """Sliding window max. O(n) with monotonic deque."""
    result = []
    q = deque()
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)
        if q[0] <= i - k:
            q.popleft()
        if i >= k - 1:
            result.append(nums[q[0]])
    return result


def max_sliding_window_brute(nums, k):
    """O(n × k) brute force for comparison."""
    result = []
    for i in range(len(nums) - k + 1):
        result.append(max(nums[i:i + k]))
    return result


# ======================================================================
# BFS TEMPLATE (previewed here, essential in Phase 3)
# ======================================================================

def bfs_grid(grid, start):
    """Return count of cells reachable from start using 4-directional BFS."""
    rows, cols = len(grid), len(grid[0])
    visited = {start}
    q = deque([start])
    count = 0
    while q:
        r, c = q.popleft()
        count += 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == 1:
                visited.add((nr, nc))
                q.append((nr, nc))
    return count


# ======================================================================
# ⚠️ QUEUE-USING-LIST vs QUEUE-USING-DEQUE — Python interview trap
# ======================================================================

def enqueue_dequeue_list(n):
    q = []
    for i in range(n):
        q.append(i)
    while q:
        q.pop(0)          # ❌ O(n) — everything shifts


def enqueue_dequeue_deque(n):
    q = deque()
    for i in range(n):
        q.append(i)
    while q:
        q.popleft()       # ✅ O(1)


# ======================================================================
# Timing helper
# ======================================================================

def time_it(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  {label:<50} {elapsed:10.3f} ms")


if __name__ == "__main__":
    print("=" * 78)
    print("STACKS & QUEUES IN ACTION")
    print("=" * 78)

    # --- Correctness ---
    print("\n✅ Correctness")
    print("-" * 78)
    print(f"  is_valid('({{[]}})')                     → {is_valid('({[]})')}")
    print(f"  is_valid('([)]')                        → {is_valid('([)]')}")

    q = MyQueue()
    for x in [1, 2, 3]:
        q.push(x)
    print(f"  MyQueue push 1,2,3; pop, pop, peek     → {q.pop()}, {q.pop()}, {q.peek()}")

    print(f"  next_greater([2,1,2,4,3])              → {next_greater([2, 1, 2, 4, 3])}")
    print(f"  daily_temperatures([73,74,75,71,69,72,76,73])")
    print(f"    → {daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])}")
    print(f"  next_greater_circular([1,2,1])         → {next_greater_circular([1, 2, 1])}")
    print(f"  max_sliding_window([1,3,-1,-3,5,3,6,7], k=3)")
    print(f"    → {max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)}")

    grid = [
        [1, 1, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 0, 1],
        [1, 0, 1, 1],
    ]
    print(f"  bfs_grid from (0,0) — cells reachable   → {bfs_grid(grid, (0, 0))}")

    # --- Next Greater speed comparison ---
    print("\n🔬 Next Greater Element: O(n²) brute vs O(n) monotonic stack")
    print("-" * 78)
    for size in [1_000, 10_000, 50_000]:
        nums = list(range(size, 0, -1))         # worst case: decreasing
        print(f"\nInput size: {size:,}")
        time_it("O(n²) next_greater_brute", next_greater_brute, nums)
        time_it("O(n)  next_greater (monotonic stack)", next_greater, nums)

    # --- Sliding Window Max ---
    print("\n🔬 Sliding Window Max: O(n × k) brute vs O(n) monotonic deque")
    print("-" * 78)
    for size, k in [(10_000, 100), (100_000, 500), (500_000, 1000)]:
        nums = list(range(size, 0, -1))
        print(f"\nInput size: {size:,}, k: {k}")
        time_it("O(n × k) max_sliding_window_brute", max_sliding_window_brute, nums, k)
        time_it("O(n)     max_sliding_window (deque)", max_sliding_window,     nums, k)

    # --- The Python queue trap ---
    print("\n🔬 Queue: list.pop(0) trap vs deque.popleft()")
    print("-" * 78)
    for size in [10_000, 50_000, 100_000]:
        print(f"\nQueue length: {size:,}")
        time_it("❌ list.pop(0)  (O(n) per pop)", enqueue_dequeue_list, size)
        time_it("✅ deque.popleft() (O(1) per pop)", enqueue_dequeue_deque, size)

    print("\n✅ The deque version is orders of magnitude faster on any real queue.")
