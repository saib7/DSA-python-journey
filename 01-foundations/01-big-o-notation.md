# 📘 01 · Big-O Notation & Complexity Analysis

> **Goal:** Learn how to measure algorithm performance — the foundation of every DSA topic that follows.

---

## ⚡ Quick Recap (read this for fast revision)

- Big-O measures **how runtime/memory grows with input size** as `n → ∞`
- We **drop constants** (`5n → n`) and **lower-order terms** (`n² + n → n²`)
- Ranking (fast → slow): **O(1) → O(log n) → O(n) → O(n log n) → O(n²) → O(2ⁿ) → O(n!)**
- Python's `dict`/`set` give **O(1)** lookup — this turns many O(n²) brute-force solutions into O(n)
- Watch out: `list.pop(0)` and `x in list` are **O(n)** in Python

---

## 1. What Big-O actually means

Big-O describes how an algorithm's **runtime** (or **memory**) grows as input size grows. We only care about behavior for **large inputs**, so we:

- **Drop constants:** `5n + 100` → `O(n)`
- **Drop non-dominant terms:** `3n² + 50n + 20` → `O(n²)`

As `n` gets very large, only the dominant term matters.

---

## 2. The complexity hierarchy

| Notation     | Name          | Example                            |
| ------------ | ------------- | ---------------------------------- |
| `O(1)`       | Constant      | `arr[5]`, `dict[key]`              |
| `O(log n)`   | Logarithmic   | Binary search                      |
| `O(n)`       | Linear        | Loop through a list                |
| `O(n log n)` | Linearithmic  | Merge sort, Python's `sort()`      |
| `O(n²)`      | Quadratic     | Nested loops                       |
| `O(2ⁿ)`      | Exponential   | Naive recursive Fibonacci          |
| `O(n!)`      | Factorial     | Generating all permutations        |

**Real numbers, for `n = 1,000`:**

| Complexity   | Operations    |
| ------------ | ------------- |
| `O(log n)`   | ~10           |
| `O(n)`       | 1,000         |
| `O(n log n)` | ~10,000       |
| `O(n²)`      | 1,000,000     |
| `O(2ⁿ)`      | unrunnable    |

---

## 3. Code examples

### O(1) — Constant
```python
def get_first(arr):
    return arr[0]
```
Same time whether `arr` has 10 or 10 million items.

### O(n) — Linear
```python
def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val
```

### O(n²) — Quadratic
```python
def has_duplicate(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
```

### O(log n) — Logarithmic (Binary Search)
```python
def binary_search(arr, target):
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
```
For `n = 1,000,000`, this takes only ~20 iterations.

### O(2ⁿ) — Exponential (naive recursion)
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

---

## 4. The five rules of analysis

1. **Drop constants** → `O(2n)` becomes `O(n)`
2. **Drop non-dominant terms** → `O(n² + n)` becomes `O(n²)`
3. **Different inputs → different variables** → looping over array `a` (size `m`) inside a loop over array `b` (size `n`) is `O(m × n)`, **not** `O(n²)`
4. **Sequential operations add** → `O(n) + O(n)` = `O(n)`
5. **Nested operations multiply** → loop inside loop = `O(n) × O(n)` = `O(n²)`

---

## 5. 🐍 Python-specific cost cheat sheet (interview gold)

### List (`list`)
| Operation              | Complexity        |
| ---------------------- | ----------------- |
| `lst[i]`               | O(1)              |
| `lst.append(x)`        | O(1) amortized    |
| `lst.insert(0, x)`     | **O(n)** ⚠️       |
| `lst.pop()`            | O(1)              |
| `lst.pop(0)`           | **O(n)** ⚠️       |
| `x in lst`             | **O(n)** ⚠️       |
| `len(lst)`             | O(1)              |

> ⚠️ For O(1) ops at *both* ends, use `collections.deque`.

### Dict & Set (`dict`, `set`)
| Operation             | Complexity   |
| --------------------- | ------------ |
| `d[key]`              | O(1) average |
| `d[key] = v`          | O(1) average |
| `key in d`            | O(1) average |
| Same for sets         | O(1) average |

### String (`str`) — strings are **immutable**
| Operation              | Complexity   |
| ---------------------- | ------------ |
| `s + t`                | O(n + m)     |
| `s += t` inside a loop | **O(n²)** ⚠️ |
| `"".join(parts)`       | O(n) ✅      |

---

## 6. Space complexity

Same notation, but measuring **memory** instead of time.

```python
# O(1) space — only one variable
def sum_list(arr):
    total = 0
    for x in arr:
        total += x
    return total

# O(n) space — new list of size n
def doubled(arr):
    return [x * 2 for x in arr]
```

> **Recursion uses call-stack space.** A recursion depth of `n` is `O(n)` space, even if the code looks simple.

---

## 7. Practice exercises

Try these **before** peeking at the answers.

```python
# Exercise 1
def mystery1(arr):
    for x in arr:
        print(x)
    for y in arr:
        print(y)

# Exercise 2
def mystery2(arr):
    for x in arr:
        for y in arr:
            print(x, y)

# Exercise 3
def mystery3(n):
    i = 1
    while i < n:
        print(i)
        i *= 2

# Exercise 4
def mystery4(a, b):
    for x in a:
        for y in b:
            print(x, y)
```

<details>
<summary>📋 Click to reveal answers</summary>

1. **O(n)** — two sequential loops: `n + n = 2n → O(n)`
2. **O(n²)** — nested loops over the same input
3. **O(log n)** — `i` doubles each iteration (1, 2, 4, 8, …)
4. **O(m × n)** — different inputs use different variables (classic interview trap!)

</details>

---

## 8. 🎯 Must-Memorize

- The ranking: **O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)**
- `list.pop(0)` and `x in list` are **O(n)** — use `deque` or `set` instead
- `dict`/`set` lookup is **O(1)** average — your most-used optimization
- String concatenation in a loop is **O(n²)** — always prefer `"".join()`
- Recursion of depth `n` uses **O(n) space** for the call stack

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/big_o_examples.py`](./examples/big_o_examples.py)
- ⏭️ Next: Recursion fundamentals *(coming)*
