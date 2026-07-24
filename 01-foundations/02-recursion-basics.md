# 📘 02 · Recursion Fundamentals

> **Goal:** Build the *mental model* of recursion. This is the foundation for trees, graphs, divide-and-conquer, backtracking, and dynamic programming.

---

## ⚡ Quick Recap (read this for fast revision)

- **Recursive leap of faith:** define the base case, then *trust* the recursive call to handle smaller inputs
- Every recursive function needs **(1) a base case** and **(2) progress toward it**
- Recursion of depth `n` uses **O(n) space** on the call stack
- Python's default recursion limit is **~1000**
- Naive binary recursion (like `fib`) is **O(2ⁿ)** — fix with **memoization**
- Python does **NOT** optimize tail calls — write a loop for deep linear recursion
- Never use mutable default arguments (`cache={}`) — use `cache=None` or `@lru_cache`

---

## 1. The mental model

> Define what your function returns for the smallest case, *assume it works* for smaller inputs, and use that to solve the current one.

This is called the **recursive leap of faith**. Don't trace every call mentally — reason about the **contract**.

### Example: sum of a list

```python
def list_sum(arr):
    if not arr:                          # Base case
        return 0
    return arr[0] + list_sum(arr[1:])    # Trust the recursion
```

> ⚠️ This version is actually **O(n²) space** because `arr[1:]` copies the list every call. Use an index instead:

```python
def list_sum(arr, i=0):
    if i == len(arr):
        return 0
    return arr[i] + list_sum(arr, i + 1)
```

Now: **O(n) time, O(n) space** (call stack only).

---

## 2. The three rules of recursion

1. **Base case** — without it: `RecursionError`
2. **Recursive case must move toward the base case** — otherwise infinite recursion
3. **Trust the recursive call** — reason about its contract, don't trace it

---

## 3. The call stack

```
list_sum([1,2,3])
  → list_sum([2,3])     ← 2 frames
    → list_sum([3])     ← 3 frames
      → list_sum([])    ← 4 frames; returns 0
    ← returns 3
  ← returns 5
← returns 6
```

A recursion depth of `n` uses **O(n) space**, even if no extra variables are used.

### Python recursion limit

```python
import sys
sys.getrecursionlimit()       # ~1000 on most systems
sys.setrecursionlimit(10000)  # use sparingly!
```

---

## 4. Recursion patterns

### Linear recursion — one recursive call

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
**Time** O(n) · **Space** O(n)

### Binary recursion — two recursive calls

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```
**Time** O(2ⁿ) · **Space** O(n)

Why O(2ⁿ)? Each call branches into 2, with depth n → roughly 2ⁿ total calls.

### Memoization — caching repeated subproblems

```python
def fib(n, cache=None):
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fib(n - 1, cache) + fib(n - 2, cache)
    return cache[n]
```
**Time** O(n) · **Space** O(n)

### Pythonic memoization with `lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

This is your **entry point to dynamic programming**.

---

## 5. ⚠️ Python does NOT optimize tail recursion

```python
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)   # tail call
```

Languages like Scheme and Scala turn this into a loop under the hood. **Python does not.** Deep linear recursion in Python should be written as a loop.

---

## 6. When to use recursion

| Use it when                                              | Skip it when                                          |
| -------------------------------------------------------- | ----------------------------------------------------- |
| Problem has natural recursive structure (trees, graphs)  | A simple loop is clearer                              |
| Recursive solution is dramatically clearer (DFS)         | You'd hit Python's recursion depth limit              |
| Backtracking (try → recurse → undo)                      | The recursion is "tail-shaped" — just use a loop      |
| Divide-and-conquer (merge sort, quicksort)               | Performance-critical and stack overhead matters       |

---

## 7. 🐍 Python recursion gotchas

| Pitfall                                       | Why it bites                                                                |
| --------------------------------------------- | --------------------------------------------------------------------------- |
| Missing base case                             | `RecursionError: maximum recursion depth exceeded`                          |
| `def f(n, cache={})`                          | Default dict is shared **across all calls** — state leaks                   |
| Slicing in recursion (`arr[1:]`)              | Each slice is O(n) → total becomes O(n²)                                    |
| Expecting tail-call optimization              | Python doesn't do TCO — stack still grows                                   |
| Recursing on large inputs                     | Default limit is ~1000 — convert to iterative for n > 500 to be safe        |

---

## 8. Practice exercises

Try these *before* peeking at solutions.

```python
# 1. Compute x^n for non-negative integer n
def power(x, n):
    ...

# 2. Reverse a string recursively (no .reverse())
def reverse_str(s):
    ...

# 3. Check if a string is a palindrome (recursively)
def is_palindrome(s):
    ...

# 4. Count occurrences of target in a list (recursively)
def count_occurrences(arr, target):
    ...

# 5. Tower of Hanoi: print moves to transfer n disks
#    from peg 'A' to peg 'C' using peg 'B' as helper
def hanoi(n, source='A', target='C', helper='B'):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
# 1. Power — O(n) basic, can be improved to O(log n) (see below)
def power(x, n):
    if n == 0:
        return 1
    return x * power(x, n - 1)

# Optimized: O(log n) via "exponentiation by squaring"
def power_fast(x, n):
    if n == 0:
        return 1
    half = power_fast(x, n // 2)
    return half * half if n % 2 == 0 else half * half * x

# 2. Reverse string
def reverse_str(s):
    if len(s) <= 1:
        return s
    return reverse_str(s[1:]) + s[0]

# 3. Palindrome
def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

# 4. Count occurrences
def count_occurrences(arr, target, i=0):
    if i == len(arr):
        return 0
    rest = count_occurrences(arr, target, i + 1)
    return rest + (1 if arr[i] == target else 0)

# 5. Tower of Hanoi — the canonical recursion problem
def hanoi(n, source='A', target='C', helper='B'):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n - 1, source, helper, target)        # Move n-1 disks aside
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, helper, target, source)        # Bring them on top of disk n
```

**Hanoi insight:** Total moves for n disks = 2ⁿ − 1. The recursion tree has 2ⁿ leaves. The structure of the problem *is* binary recursion.

</details>

---

## 9. 🎯 Must-Memorize

- Every recursive function = **base case + recursive case + progress toward base**
- Recursion depth `n` → **O(n) call stack space**
- Python recursion limit ≈ **1000**
- Naive binary recursion is **O(2ⁿ)** — always consider memoization
- Use `@lru_cache` or pass an explicit `cache=None` — **never `cache={}`**
- Python doesn't optimize **tail calls** — convert tail recursion to loops
- The leap of faith: **define the contract, trust the call**

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/recursion_examples.py`](./examples/recursion_examples.py)
- ⏮️ Previous: [Big-O Notation](./01-big-o-notation.md)
- ⏭️ Next: Arrays & Strings *(coming)*
