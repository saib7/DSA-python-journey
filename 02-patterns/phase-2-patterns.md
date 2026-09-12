# 🎯 Phase 2 Cheatsheet — 10 Interview Patterns

> **Single-page revision reference for Lessons 3–7.** Read this before any interview.

---

## The 10 patterns at a glance

| # | Pattern                        | Recognition signal                          | Time    | Space   |
| - | ------------------------------ | ------------------------------------------- | ------- | ------- |
| 1 | Two-pointer (opposite ends)    | sorted, palindrome, pair sum                | O(n)    | O(1)    |
| 2 | Two-pointer (fast/slow, array) | in-place, remove, filter                    | O(n)    | O(1)    |
| 3 | Sliding window (fixed size)    | "subarray of size k"                        | O(n)    | O(1)    |
| 4 | Sliding window (variable)      | longest/shortest contiguous with X          | O(n)    | O(k)    |
| 5 | Hash set membership            | "seen X before?", duplicates                | O(n)    | O(n)    |
| 6 | Hash frequency count           | count occurrences, anagram                  | O(n)    | O(n)    |
| 7 | Hash complement lookup         | pair sum, unsorted array                    | O(n)    | O(n)    |
| 8 | Prefix sum + hash              | count subarrays with sum K                  | O(n)    | O(n)    |
| 9 | Fast/slow pointer (LL)         | cycle, middle, Nth from end                 | O(n)    | O(1)    |
| 10 | Monotonic stack                | next/prev greater/smaller                   | O(n)    | O(n)    |

---

## 1. Two-Pointer — opposite ends

**Signal:** sorted · palindrome · pair sum · container.

```python
# Template
left, right = 0, len(arr) - 1
while left < right:
    if condition(arr[left], arr[right]):
        # process pair
        left += 1
        right -= 1
    elif ...:
        left += 1
    else:
        right -= 1
```

**Key insight:** exclusion argument — each move discards a whole set of pairs.

---

## 2. Two-Pointer — fast/slow (arrays)

**Signal:** in-place · remove · filter · "no extra space".

```python
# Template
slow = 0
for fast in range(len(arr)):
    if keep(arr[fast]):
        arr[slow] = arr[fast]
        slow += 1
return slow   # new length
```

**Key insight:** `slow` = next answer position, `fast` = scanner.

---

## 3. Sliding Window — fixed size k

**Signal:** "subarray/substring of size k".

```python
# Template
window_state = compute(arr[:k])
best = window_state
for right in range(k, len(arr)):
    window_state += f(arr[right]) - f(arr[right - k])
    best = optimize(best, window_state)
```

**Key insight:** O(1) update per slide (only 1 element in, 1 out).

---

## 4. Sliding Window — variable size

**Signal:** longest/shortest contiguous with property X · "at most K distinct" · "contains all chars".

```python
# Template — LONGEST (shrink while INVALID)
left = 0
state = ...
result = 0
for right in range(len(arr)):
    add(state, arr[right])
    while not is_valid(state):
        remove(state, arr[left])
        left += 1
    result = max(result, right - left + 1)

# Template — SHORTEST (shrink while VALID)
left = 0
state = ...
result = float('inf')
for right in range(len(arr)):
    add(state, arr[right])
    while is_valid(state):
        result = min(result, right - left + 1)
        remove(state, arr[left])
        left += 1
```

**Complexity insight:** O(n) despite nested `while` — amortization: `left` moves ≤ n times total.

---

## 5. Hash Set — membership

**Signal:** "have I seen X?", duplicates.

```python
seen = set()
for x in nums:
    if x in seen:
        return True
    seen.add(x)
```

---

## 6. Hash — frequency counting

**Signal:** count occurrences, anagram, most-frequent.

```python
from collections import Counter, defaultdict

c = Counter(arr)                       # {value: count}
c.most_common(k)                       # top k values

# Manual
counts = defaultdict(int)
for x in arr:
    counts[x] += 1
```

---

## 7. Hash — complement lookup (Two Sum)

**Signal:** pair sum on **unsorted** array.

```python
seen = {}                              # value → index
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```

**Two-pointer vs hash:** sorted → two-pointer (O(1) space); unsorted → hash (O(n) space).

---

## 8. Prefix Sum + Hash Map

**Signal:** "count subarrays with sum K", "divisible by K".

```python
count = 0
running_sum = 0
prefix_counts = {0: 1}                 # ⚠️ MUST init with {0: 1}
for x in nums:
    running_sum += x
    if (running_sum - k) in prefix_counts:
        count += prefix_counts[running_sum - k]
    prefix_counts[running_sum] = prefix_counts.get(running_sum, 0) + 1
```

**Key insight:** sum from i+1 to j = prefix[j] − prefix[i].

---

## 9. Fast/Slow Pointer — Linked Lists (Floyd's)

**Signal:** cycle detection · find middle · Nth from end.

```python
# Cycle detection — Floyd's
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True
return False

# Find middle
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow                            # middle

# Nth from end — gap technique
dummy = Node(0, head)
fast = slow = dummy
for _ in range(n + 1): fast = fast.next
while fast:
    slow = slow.next
    fast = fast.next
slow.next = slow.next.next
return dummy.next
```

**Bonus — Reversal (iterative):**
```python
prev = None
current = head
while current:
    next_node = current.next
    current.next = prev
    prev = current
    current = next_node
return prev
```

**Dummy node:** use whenever head might change (merge, remove-Nth, etc.).

---

## 10. Monotonic Stack

**Signal:** next/previous greater/smaller · temperatures · histogram.

```python
result = [default] * len(nums)
stack = []                             # holds INDICES
for i, x in enumerate(nums):
    while stack and violates_order(nums[stack[-1]], x):
        j = stack.pop()
        result[j] = compute_answer(x, i, j)
    stack.append(i)
```

**Direction rules:**

| Want                            | Stack invariant | Direction    |
| ------------------------------- | --------------- | ------------ |
| Next **greater** to right       | Decreasing      | Left → right |
| Next **smaller** to right       | Increasing      | Left → right |
| Previous **greater** to left    | Decreasing      | Right → left |
| Previous **smaller** to left    | Increasing      | Right → left |

**Complexity insight:** O(n) — amortization: each index pushed/popped at most once.

---

## Bonus: BFS template (essential in Phase 3)

```python
from collections import deque

visited = {start}
q = deque([start])
while q:
    node = q.popleft()
    # process node
    for neighbor in get_neighbors(node):
        if neighbor not in visited:
            visited.add(neighbor)
            q.append(neighbor)
```

**⚠️ NEVER use `list.pop(0)` for a queue** — it's O(n). Always `deque.popleft()`.

---

## 🐍 Python cost cheatsheet (interview gold)

### List
| Operation           | Complexity     |
| ------------------- | -------------- |
| `lst[i]`            | O(1)           |
| `lst.append(x)`     | O(1) amortized |
| `lst.insert(0, x)`  | **O(n)** ⚠️    |
| `lst.pop()`         | O(1)           |
| `lst.pop(0)`        | **O(n)** ⚠️    |
| `x in lst`          | **O(n)** ⚠️    |
| `lst[i:j]`          | O(j − i)       |

### Dict / Set / Deque
| Operation           | Complexity     |
| ------------------- | -------------- |
| `d[key]`, `key in d`| O(1) avg       |
| `set` — add/in/remove| O(1) avg      |
| `deque.append/popleft/pop/appendleft` | O(1) |

### String (immutable!)
| Operation           | Complexity     |
| ------------------- | -------------- |
| `s + t`             | O(n + m)       |
| `s += t` in a loop  | **O(n²)** ⚠️   |
| `"".join(parts)`    | O(n) ✅        |

---

## 🚨 Master recognition table

| Phrase in problem                             | Pattern              |
| --------------------------------------------- | -------------------- |
| "sorted array" + pair                         | Two-pointer (opposite) |
| "palindrome"                                  | Two-pointer (opposite) |
| "in place" / "no extra space" (array)         | Two-pointer (fast/slow) |
| "remove" / "filter" (in place)                | Two-pointer (fast/slow) |
| "subarray of size k"                          | Sliding window (fixed) |
| "longest / shortest contiguous"               | Sliding window (variable) |
| "at most K distinct"                          | Sliding window (variable) |
| "contains all chars of ..."                   | Sliding window (min window) |
| "duplicate" / "seen before"                   | Set                  |
| "count occurrences" / "frequency"             | Counter / dict       |
| "anagram" / "group by letters"                | Sorted-tuple key + defaultdict(list) |
| "two/three numbers sum to X" (unsorted)       | Hash complement      |
| "subarray sum = K"                            | Prefix sum + hash    |
| "cycle" / "middle of linked list"             | Floyd's fast/slow    |
| "Nth from end"                                | Fast/slow with gap N |
| "reverse linked list"                         | Iterative 3-pointer  |
| "merge two sorted lists"                      | Dummy node           |
| "matching brackets"                           | Stack                |
| "next / previous greater / smaller"           | Monotonic stack      |
| "BFS" / "level order" / "shortest unweighted" | Queue (`deque`)      |
| "sliding window max/min"                      | Monotonic deque      |

---

## 🎯 Interview-day final checklist

- [ ] Can identify pattern from problem statement in <30 seconds
- [ ] Can write the variable-window template from memory
- [ ] Can write the BFS template from memory
- [ ] Can write iterative linked-list reversal from memory
- [ ] Know why prefix-sum init is `{0: 1}` (not `{}`)
- [ ] Know why monotonic stack is O(n) (amortization argument)
- [ ] Know Python cost pitfalls: `list.pop(0)`, `x in list`, `s += t` in loop
- [ ] Can articulate: two-pointer vs hash (sorted vs unsorted; O(1) vs O(n) space)

---

> **Lessons this cheatsheet covers:** [03 Arrays & Two-Pointer](../02-linear-structures/01-arrays-strings-two-pointer.md) · [04 Sliding Window](../02-linear-structures/02-sliding-window.md) · [05 Hash Tables](../02-linear-structures/03-hash-tables.md) · [06 Linked Lists](../02-linear-structures/04-linked-lists.md) · [07 Stacks & Queues](../02-linear-structures/05-stacks-queues.md)
