# 📘 05 · Hash Tables & Dictionaries

> **Goal:** Master the most-used pattern in interviews — turning O(n²) brute forces into O(n) with O(1) lookup.

---

## ⚡ Quick Recap (read this for fast revision)

- Hash tables (`dict`, `set`) give **O(1) average** for get/set/in lookup
- Trade **space for time**: O(n) space, O(n) time (vs O(1) space, O(n²) brute)
- Keys must be **hashable** (immutable): `str`, `int`, `tuple`, `frozenset` — not `list` or `dict`
- **Five patterns:** membership check · frequency count · complement lookup · grouping · prefix-sum
- **`x in list`** is O(n); **`x in set`** is O(1) — the single most common Python optimization
- **Subarray Sum = K** uses prefix sum + dict, initialized with `{0: 1}`

---

## 1. What Python gives you

### `dict` and `set` complexity

| Operation      | Average | Worst |
| -------------- | ------- | ----- |
| `d[key]`       | O(1)    | O(n)  |
| `d[key] = v`   | O(1)    | O(n)  |
| `key in d`     | O(1)    | O(n)  |
| `del d[key]`   | O(1)    | O(n)  |
| `set` — same operations, same complexity | | |

Worst case (O(n)) is rare — happens only with pathological hash collisions.

### Hashable requirement

| Hashable ✅       | Not hashable ❌ |
| ----------------- | --------------- |
| `str`, `int`      | `list`          |
| `tuple`           | `dict`, `set`   |
| `frozenset`       | any mutable     |

Convert list → tuple when you need it as a key: `tuple(sorted(s))`.

---

## 2. The five core patterns

### 🔹 Pattern 1: Membership check → `set`

```python
def has_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```
**O(n) time, O(n) space.** Beats nested loop O(n²).

### 🔹 Pattern 2: Frequency counting → `Counter` / `dict`

```python
from collections import Counter, defaultdict

# Pythonic
c = Counter("hello")   # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# Manual with .get()
counts = {}
for x in arr:
    counts[x] = counts.get(x, 0) + 1

# Manual with defaultdict (preferred)
counts = defaultdict(int)
for x in arr:
    counts[x] += 1
```

### 🔹 Pattern 3: Complement lookup → **Two Sum (unsorted)**

For each `x`, ask *"did I already see `target - x`?"*

```python
def two_sum(nums, target):
    seen = {}                          # value → index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []
```
**O(n) time, O(n) space** — vs O(n²) brute force.

### 🔹 Pattern 4: Grouping → `defaultdict(list)`

**Group Anagrams:** anagrams share the same sorted characters.

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))         # tuple = hashable
        groups[key].append(s)
    return list(groups.values())
```

### 🔹 Pattern 5: Prefix Sum + Hash Map → **Subarray Sum Equals K**

Count contiguous subarrays with sum = k. **Most-tested advanced hash pattern.**

**Insight:**
- Let `prefix[i]` = sum of first i elements
- Subarray sum from `i+1` to `j` = `prefix[j] - prefix[i]`
- We want `prefix[j] - prefix[i] = k`, i.e., `prefix[i] = prefix[j] - k`
- For each j, count how many prior prefix sums equal `prefix[j] - k`

```python
def subarray_sum(nums, k):
    count = 0
    running_sum = 0
    prefix_counts = {0: 1}             # empty prefix = sum 0, appears once
    for x in nums:
        running_sum += x
        if (running_sum - k) in prefix_counts:
            count += prefix_counts[running_sum - k]
        prefix_counts[running_sum] = prefix_counts.get(running_sum, 0) + 1
    return count
```
**O(n) time, O(n) space** vs O(n²) naive.

**Why `{0: 1}` initialization?** So subarrays starting from index 0 are counted. If `running_sum == k`, we need `running_sum - k = 0` present in the map.

---

## 3. Recognition signals

| Phrase in problem                             | Pattern                    |
| --------------------------------------------- | -------------------------- |
| "Have I seen X?" / "duplicates"               | `set`                      |
| "Count occurrences" / "frequency"             | `Counter` / `dict`         |
| "Two/three numbers sum to..."                 | Complement lookup          |
| "Anagram" / "same letters"                    | Sorted-tuple key           |
| "Group by ..."                                | `defaultdict(list)`        |
| "Subarray with sum K" / "divisible by K"      | **Prefix sum + dict**      |
| "First non-repeating..."                      | `Counter`                  |
| "Fastest lookup"                              | `set` / `dict`             |

---

## 4. Two-Pointer vs Hash Map — when to choose

| Situation                       | Winner                                  |
| ------------------------------- | --------------------------------------- |
| Array is **sorted**             | Two-pointer (O(1) space)                |
| Array is **unsorted**           | Hash map (O(n) space, O(n) time)        |
| **Can't sort** (immutable, etc.) | Hash map                                |
| **Space is tight**              | Sort + two-pointer (O(n log n), O(1))   |
| Need indices of original array  | Hash map (sorting scrambles indices)    |

---

## 5. 🐍 Python idioms cheat sheet

```python
from collections import Counter, defaultdict

# Counter tricks
c = Counter("hello")
c.most_common(2)              # [('l', 2), ('h', 1)]
c1 + c2                       # add counts across two Counters
c1 - c2                       # subtract counts (drops non-positive)

# defaultdict
groups = defaultdict(list)    # missing key → []
counts = defaultdict(int)     # missing key → 0
adjacency = defaultdict(set)  # for graph building

# Counting without defaultdict
counts[x] = counts.get(x, 0) + 1

# Set operations
a & b   # intersection
a | b   # union
a - b   # difference
a ^ b   # symmetric difference

# Dict comprehension
inverted = {v: k for k, v in original.items()}
```

---

## 6. Gotchas

| Pitfall                                       | Why it bites                                  |
| --------------------------------------------- | --------------------------------------------- |
| Using `list` as dict key                      | `TypeError: unhashable type`                  |
| `d[missing_key]`                              | `KeyError` — use `.get()` or `defaultdict`    |
| Iterating and mutating dict at same time      | `RuntimeError: dictionary changed size`       |
| Assuming worst case is O(1)                   | Adversarial inputs can trigger collisions     |
| Forgetting `{0: 1}` in prefix sum problems    | Misses subarrays starting from index 0        |

---

## 7. Practice problems

```python
# 1. Contains Duplicate (LC 217, Easy)
def contains_duplicate(nums):
    ...

# 2. Two Sum (LC 1, Easy) — unsorted array
def two_sum(nums, target):
    ...

# 3. Valid Anagram (LC 242, Easy)
def is_anagram(s, t):
    ...

# 4. Group Anagrams (LC 49, Medium)
def group_anagrams(strs):
    ...

# 5. Subarray Sum Equals K (LC 560, Medium) — the important one!
def subarray_sum(nums, k):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
# 1. Contains Duplicate
def contains_duplicate(nums):
    return len(set(nums)) != len(nums)
# Also fine: build set as you go and check membership

# 2. Two Sum
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []

# 3. Valid Anagram
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)

# 4. Group Anagrams
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())

# 5. Subarray Sum Equals K
def subarray_sum(nums, k):
    count = 0
    running_sum = 0
    prefix_counts = {0: 1}
    for x in nums:
        running_sum += x
        if (running_sum - k) in prefix_counts:
            count += prefix_counts[running_sum - k]
        prefix_counts[running_sum] = prefix_counts.get(running_sum, 0) + 1
    return count
```

**Complexity:**
- (1) O(n) time, O(n) space
- (2) O(n) time, O(n) space
- (3) O(n) time, O(1) space (26 letters, constant)
- (4) O(n × k log k) time — where k is max word length
- (5) O(n) time, O(n) space

</details>

---

## 8. 🎯 Must-Memorize

- `dict`/`set` are **O(1) average** for lookup — the core optimization
- **`x in list` is O(n); `x in set` is O(1)** — always convert to set for repeated lookups
- Keys must be **hashable** — convert lists to tuples via `tuple(...)`
- **Two Sum (hash) pattern:** iterate once, check for complement, store as you go
- **Group by pattern:** `defaultdict(list)` + a hashable key function
- **Prefix sum + dict** with `{0: 1}` init solves "subarray with sum X" in O(n)
- Hash map beats two-pointer when data is **unsorted** or **indices matter**

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/hash_table_examples.py`](./examples/hash_table_examples.py)
- ⏮️ Previous: [Sliding Window](./02-sliding-window.md)
- ⏭️ Next: Linked Lists *(coming)*
