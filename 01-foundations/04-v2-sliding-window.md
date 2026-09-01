# 📘 04 · The Sliding Window Pattern

> **Goal:** Master the pattern for contiguous subarray/substring problems — the sibling of two-pointer, and one of the highest-ROI interview patterns.

---

## ⚡ Quick Recap (read this for fast revision)

- A **window** = range `[left, right]` sliding through the array
- Only ONE element enters and ONE leaves per slide → **O(1) update instead of recompute**
- Two flavors:
  - **Fixed-size** (window of size k): `sum += arr[right] - arr[right - k]`
  - **Variable-size** (expand right, shrink left based on condition)
- The template for variable window: **for right → include → while invalid: shrink left → update answer**
- ⚠️ Variable window is **O(n)** despite a nested `while` — amortization: `left` moves at most n times total
- Signals: *"of size k"*, *"longest / shortest contiguous"*, *"at most K distinct"*, *"substring containing"*

---

## 1. The core idea

> When a window slides, only ONE element enters and ONE leaves. Update state in O(1); don't recompute.

This is what turns **O(n × k)** or **O(n²)** into **O(n)**.

---

## 2. Fixed-size window

**Signal:** "subarray/substring **of size k**"

### Template

```python
def fixed_window(arr, k):
    window_state = compute_state(arr[:k])   # first window
    best = window_state
    for right in range(k, len(arr)):
        window_state += f(arr[right]) - f(arr[right - k])  # O(1) update
        best = optimize(best, window_state)
    return best
```

### Example: max sum of subarray of size k

```python
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for right in range(k, len(arr)):
        window_sum += arr[right] - arr[right - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

**Complexity:** O(n) time, O(1) space (vs O(n × k) brute force).

---

## 3. Variable-size window

**Signal:** "**longest / shortest** contiguous subarray/substring such that **[condition]**"

### The template — memorize this shape

```python
def variable_window(arr):
    left = 0
    state = ...            # set, dict, running sum, etc.
    result = 0             # or float('inf') for min problems
    
    for right in range(len(arr)):
        # 1. INCLUDE arr[right] in the window (update state)
        add(state, arr[right])
        
        # 2. SHRINK from the left while window is INVALID
        while not is_valid(state):
            remove(state, arr[left])
            left += 1
        
        # 3. Window is now valid — update answer
        result = max(result, right - left + 1)
    
    return result
```

### Example: longest substring without repeating characters

```python
def longest_unique_substring(s):
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
```

Trace `"abcabcbb"`:
```
right=0 'a': seen={a},       longest=1
right=1 'b': seen={a,b},     longest=2
right=2 'c': seen={a,b,c},   longest=3
right=3 'a': shrink → remove 'a', left=1, seen={b,c,a}, longest=3
right=4 'b': shrink → remove 'b', left=2, seen={c,a,b}, longest=3
...
```

### 🧩 The logic chain — why this actually works

It's easy to see the code moves two pointers. It's less obvious *why* that's guaranteed to give the correct, longest answer. Here's the full reasoning, broken into five small, connected steps — each one only makes sense once you accept the one before it.

| # | Step | In plain words |
|:---:|---|---|
| 1️⃣ | **Invariant** | The window `[left, right]` always holds only **distinct** characters — never a duplicate, at any point in the run. |
| 2️⃣ | **Maintenance** | Growing `right` by one might break that rule. If it does, shrinking `left` — one step at a time — removes the duplicate and restores the rule before moving on. |
| 3️⃣ | **Optimality** | `left` only ever moves the **minimum** amount needed to fix the duplicate — never more. So `[left, right]` is the **biggest possible** valid window that ends exactly at `right`. |
| 4️⃣ | **Correctness** | Since step 3 finds the best window for *every* ending point `right = 0, 1, ..., n-1`, and the true answer must end *somewhere*, the biggest window found across the whole scan **is** the true longest substring. |
| 5️⃣ | **Complexity** | `right` moves forward `n` times total. `left` never moves backward, so it can also move forward at most `n` times total, across the *entire* run — not per step. Total work ≤ `2n` → **O(n)**. |

> [!TIP]
> Read it as a chain: **1** is the rule the algorithm protects → **2** is *how* it protects it → **3** is why protecting it *minimally* matters → **4** is why that gives the *correct* answer → **5** is why doing all of this still only costs *linear* time.

---

### ⚠️ Why is it O(n) despite the nested `while`?

**The amortization argument:**
- `right` moves forward exactly `n` times
- `left` **also** moves forward at most `n` times total (never backwards)
- Total pointer moves ≤ 2n → **O(n)**

Count total pointer moves, not nested loops. Interview gotcha.

---

## 4. Advanced: Min Window Substring

Find the smallest window in `s` containing all chars of `t`. Example: `s="ADOBECODEBANC"`, `t="ABC"` → `"BANC"`.

```python
from collections import Counter

def min_window(s, t):
    if not s or not t:
        return ""
    
    need = Counter(t)          # what we still need
    missing = len(t)           # total chars still missing
    left = 0
    best_len = float('inf')
    best_start = 0
    
    for right, ch in enumerate(s):
        if need[ch] > 0:       # needed char
            missing -= 1
        need[ch] -= 1          # can go negative (excess char)
        
        while missing == 0:    # window is valid → try shrinking
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            need[s[left]] += 1
            if need[s[left]] > 0:   # left char was actually needed
                missing += 1
            left += 1
    
    return "" if best_len == float('inf') else s[best_start:best_start + best_len]
```

**Key trick:** `need` dict goes **negative** for excess chars. Only when it becomes positive does the window truly break. This lets us track validity in O(1) per step.

---

## 5. How to recognize sliding window

| Phrase in problem                             | Pattern           |
| --------------------------------------------- | ----------------- |
| "subarray of **size k**"                      | Fixed window      |
| "**longest** subarray/substring with X"       | Variable window   |
| "**shortest / smallest** window that has Y"   | Variable window   |
| "at most K distinct characters"               | Variable window   |
| "contains all characters of ..."              | Variable window   |
| **"contiguous"** appears anywhere             | 🚨 Sliding window |

### Sliding window vs two-pointer

| Two-pointer                        | Sliding window                          |
| ---------------------------------- | --------------------------------------- |
| About **pairs**                    | About **contiguous ranges**             |
| Pointers move toward each other or same direction with different roles | Both pointers move same direction; window expands/shrinks |
| E.g. "pair sum", "palindrome"      | E.g. "longest substring with X"         |

---

## 6. Practice problems

```python
# 1. Max sum of subarray of size k (fixed window warmup)
def max_sum_size_k(arr, k):
    ...

# 2. Longest substring without repeating characters
def longest_unique_substring(s):
    ...

# 3. Longest substring with AT MOST k distinct characters
#    "eceba", k=2 → "ece" length 3
def longest_at_most_k_distinct(s, k):
    ...

# 4. Minimum size subarray sum ≥ target
#    arr=[2,3,1,2,4,3], target=7 → [4,3] length 2
def min_subarray_sum(arr, target):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
# 1. Fixed window
def max_sum_size_k(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for right in range(k, len(arr)):
        window_sum += arr[right] - arr[right - k]
        max_sum = max(max_sum, window_sum)
    return max_sum


# 2. Variable window with a set
def longest_unique_substring(s):
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


# 3. Variable window with a dict tracking counts
def longest_at_most_k_distinct(s, k):
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


# 4. Variable window — SHRINK ON VALID (opposite of longest problems)
def min_subarray_sum(arr, target):
    left = 0
    window_sum = 0
    min_len = float('inf')
    for right in range(len(arr)):
        window_sum += arr[right]
        while window_sum >= target:      # valid → try to shrink!
            min_len = min(min_len, right - left + 1)
            window_sum -= arr[left]
            left += 1
    return 0 if min_len == float('inf') else min_len
```

**Complexity for all four:** O(n) time, O(1)/O(k) space.

**Key contrast:**
- Problems 2 & 3 are "**longest** with X" → shrink while **INVALID**, update answer after the while
- Problem 4 is "**shortest** with X" → shrink while **VALID**, update answer inside the while

</details>

---

## 7. 🎯 Must-Memorize

- **Fixed window:** O(1) update via `state += f(arr[right]) - f(arr[right - k])`
- **Variable window template:** `for right → include → while invalid: shrink → update`
- **Longest problem** → shrink while INVALID, update AFTER the while
- **Shortest problem** → shrink while VALID, update INSIDE the while
- Time complexity: **O(n)** even with nested `while` — amortization: each pointer moves ≤ n times
- Two-pointer = pairs. Sliding window = **contiguous ranges**
- Common state trackers: `set` (uniqueness), `dict/Counter` (counts), running sum

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/sliding_window_examples.py`](./examples/sliding_window_examples.py)
- ⏮️ Previous: [Arrays, Strings & Two-Pointer](./01-arrays-strings-two-pointer.md)
- ⏭️ Next: Linked Lists *(coming)*
