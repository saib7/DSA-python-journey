# 📘 03 · Arrays, Strings & the Two-Pointer Pattern

> **Goal:** Master the #1 pattern for turning O(n²) brute-force solutions into O(n) — the two-pointer technique.

---

## ⚡ Quick Recap (read this for fast revision)

- Python `list` = dynamic array. `lst[i]` and `append` are O(1); `insert(0, x)` and `in` are O(n)
- Python `str` is **immutable** — `s += t` in a loop is O(n²); use `"".join(parts)` instead
- **Two-pointer pattern** converts many O(n²) problems into O(n)
- Two flavors:
  - **Opposite ends** (converging): sorted arrays, palindromes, pair sum, container
  - **Fast/slow** (same direction): in-place modification, remove duplicates, filter
- Signal words: *"sorted array"*, *"palindrome"*, *"in place"*, *"pair sum"*, *"remove"*

---

## 1. Python arrays & strings — the essentials

### Lists (dynamic arrays)

| Operation           | Complexity        | Note                                          |
| ------------------- | ----------------- | --------------------------------------------- |
| `lst[i]`            | O(1)              | Direct memory offset                          |
| `lst.append(x)`     | O(1) amortized    | Occasional O(n) resize                        |
| `lst.insert(0, x)`  | **O(n)**          | Everything shifts right                       |
| `lst.pop()`         | O(1)              |                                               |
| `lst.pop(0)`        | **O(n)**          | Use `collections.deque` instead               |
| `x in lst`          | **O(n)**          | Use `set` for O(1) membership                 |
| `lst[i:j]`          | O(j − i)          | Creates a copy                                |
| `lst.reverse()`     | O(n), in place    | vs `lst[::-1]` which is O(n) space too        |

### Strings (immutable)

```python
s = "hello"
s[0] = "H"   # ❌ TypeError
```

Consequence — the classic O(n²) trap:

```python
# ❌ O(n²) — creates a new string every iteration
result = ""
for c in some_list:
    result += c

# ✅ O(n) — collect in a list, join once
parts = []
for c in some_list:
    parts.append(c)
result = "".join(parts)
```

### Interview-critical tricks

```python
# Modify a string "in place"
chars = list(s)
chars[0] = "H"
s = "".join(chars)

# Count characters
from collections import Counter
Counter("hello")   # {'l': 2, 'h': 1, 'e': 1, 'o': 1}

# Fast membership check
if x in set(arr):  # O(1) after O(n) set build
    ...
```

---

## 2. The two-pointer pattern

**Idea:** use two indices moving through the array with a shared purpose. Converts O(n²) → O(n) in many problems.

**Why it works:** each pointer move *excludes* a whole set of pairs from further consideration. The pattern lives or dies by this **exclusion argument**.

---

### 🅰️ Flavor 1: Opposite ends (converging)

Start pointers at both ends. Move toward each other.

```
[  1,  2,  3,  4,  5,  6  ]
   ↑                    ↑
  left               right
   →                    ←
```

**Signals:** sorted array · palindrome · pair sum · container.

#### Palindrome check

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```
**Time** O(n) · **Space** O(1) — vs recursive version which is O(n) space.

#### Two Sum (sorted array)

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1     # need bigger sum
        else:
            right -= 1    # need smaller sum
    return []
```

**Why it works (exclusion argument):**
If `arr[left] + arr[right] < target`, then `arr[left]` paired with anything in `[left+1, right]` (all ≤ `arr[right]`) is also too small. So `arr[left]` cannot be part of any answer. Discard it.

#### Container with Most Water

```python
def max_area(heights):
    left, right = 0, len(heights) - 1
    max_water = 0
    while left < right:
        water = min(heights[left], heights[right]) * (right - left)
        max_water = max(max_water, water)
        # Move the shorter side — keeping it can only reduce area
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_water
```

---

### 🅱️ Flavor 2: Fast / slow (same direction)

Both pointers move forward but with different roles:

- **`slow`** = "where the next answer goes"
- **`fast`** = "the scanner looking for the next valid item"

**Signals:** in-place modification · remove · filter · "no extra space".

#### Remove duplicates from sorted array (in place)

```python
def remove_duplicates(arr):
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1   # length of unique prefix
```

Trace `[1, 1, 2, 2, 3]`:
```
slow=0, fast=1: 1 == 1, skip
slow=0, fast=2: 2 != 1, slow=1, arr[1]=2 → [1,2,2,2,3]
slow=1, fast=3: 2 == 2, skip
slow=1, fast=4: 3 != 2, slow=2, arr[2]=3 → [1,2,3,2,3]
Return 3. Unique prefix: [1, 2, 3]
```

#### Move zeros to end (preserve order)

```python
def move_zeros(arr):
    slow = 0
    for fast in range(len(arr)):
        if arr[fast] != 0:
            arr[slow], arr[fast] = arr[fast], arr[slow]
            slow += 1
```

`[0, 1, 0, 3, 12]` → `[1, 3, 12, 0, 0]`. **O(n) time, O(1) space.**

---

## 3. How to recognize two-pointer in an interview

| Phrase in problem                        | Pattern signal              |
| ---------------------------------------- | --------------------------- |
| "sorted array"                           | Opposite-ends two-pointer   |
| "palindrome"                             | Opposite-ends two-pointer   |
| "pair / triplet that sums to X"          | Opposite-ends two-pointer   |
| "in place" / "without extra space"       | Fast/slow two-pointer       |
| "remove duplicates" / "filter"           | Fast/slow two-pointer       |
| "move X to the end"                      | Fast/slow two-pointer       |
| "subarray with property"                 | Sliding window              |

---

## 4. Practice problems

```python
# 1. Reverse an array in place (opposite ends)
def reverse_array(arr):
    ...

# 2. Squares of a sorted array — return sorted squares in O(n).
#    Example: [-4, -1, 0, 3, 10] → [0, 1, 9, 16, 100]
def sorted_squares(arr):
    ...

# 3. Valid Palindrome II — can you make it a palindrome
#    by removing AT MOST one character?
def valid_palindrome_ii(s):
    ...

# 4. 3Sum — return all UNIQUE triplets that sum to 0.
#    Hint: sort first, then loop + two-pointer
def three_sum(nums):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
# 1. Reverse in place
def reverse_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# 2. Sorted squares — O(n). Key insight: the biggest square is
#    always at one of the two ends. Fill the result from the back.
def sorted_squares(arr):
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

# 3. Valid Palindrome II — when mismatch, try skipping either side
def valid_palindrome_ii(s):
    def is_pal_range(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_pal_range(left + 1, right) or is_pal_range(left, right - 1)
        left += 1
        right -= 1
    return True

# 4. 3Sum — sort + fix one + two-pointer on the rest
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue   # skip duplicates for i
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates for left and right
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
```

**Complexity:**
- (1) O(n) time, O(1) space
- (2) O(n) time, O(n) space (for the result)
- (3) O(n) time, O(1) space
- (4) **O(n²)** time — the outer loop wraps a two-pointer scan. This is the pattern for kSum problems.

</details>

---

## 5. 🎯 Must-Memorize

- **Two-pointer converts O(n²) → O(n)** in many array/string problems
- **Opposite ends** works because each move excludes a whole set of pairs (exclusion argument)
- **Fast/slow** works because `slow` marks "answer position" and `fast` scans
- Python `list.pop(0)` is **O(n)** — always use `deque` for queue-like access
- Python strings are **immutable**; build with a list and `"".join()`, never `+=` in a loop
- 3Sum pattern = **loop + two-pointer** = O(n²) — the go-to for kSum problems

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/two_pointer_examples.py`](./examples/two_pointer_examples.py)
- ⏮️ Previous: [Recursion Fundamentals](../01-foundations/02-recursion-basics.md)
- ⏭️ Next: Sliding Window Pattern *(coming)*
