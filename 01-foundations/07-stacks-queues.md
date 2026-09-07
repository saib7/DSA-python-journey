# 📘 07 · Stacks & Queues

> **Goal:** Master the LIFO/FIFO fundamentals, and unlock the **monotonic stack** pattern that turns many O(n²) problems into O(n).

---

## ⚡ Quick Recap (read this for fast revision)

- **Stack (LIFO)** — use a Python `list`: `append`, `pop`, `[-1]` all O(1)
- **Queue (FIFO)** — use `collections.deque`: `append`, `popleft` both O(1)
- ⚠️ **NEVER use `list.pop(0)`** for a queue — it's O(n)
- **Valid Parentheses** = stack + `pairs` dict
- **BFS template** = `deque` + `visited` set — memorize this for Phase 3
- **Monotonic stack** = stack maintained in strict order; O(n) amortized
- **Amortization argument** (same as sliding window): each index pushed/popped at most once

---

## 1. Stacks (LIFO)

### Python implementation

```python
stack = []
stack.append(x)   # push, O(1)
x = stack.pop()   # pop from end, O(1)
top = stack[-1]   # peek, O(1)
is_empty = not stack
```

### Classic: Valid Parentheses

```python
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in pairs:                       # closing bracket
            if not stack or stack.pop() != pairs[c]:
                return False
        else:                                # opening bracket
            stack.append(c)
    return not stack
```
**O(n) time, O(n) space.**

### Common stack use cases
- Reversing (push all, pop all)
- Undo/redo
- Iterative DFS
- Expression evaluation (Reverse Polish Notation)

---

## 2. Queues (FIFO)

### Python implementation — `collections.deque`

```python
from collections import deque
q = deque()
q.append(x)      # enqueue at back,   O(1)
x = q.popleft()  # dequeue from front, O(1)
front = q[0]     # peek, O(1)
```

⚠️ **Critical trap:** `list.pop(0)` is **O(n)** — turns O(n) BFS into O(n²). Always use `deque`.

### The BFS template (essential for Phase 3)

```python
from collections import deque

def bfs(start):
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

**Memorize this shape.** You'll use it for trees, graphs, level-order, and shortest-path-in-unweighted-graph.

---

## 3. Monotonic Stack — the "unlock" pattern

A stack whose values are always in strictly **increasing** or **decreasing** order. When a new element would violate the order, pop until it doesn't.

### Classic: Next Greater Element

For each element, find the next greater element to the right (or -1).

`[2, 1, 2, 4, 3]` → `[4, 2, 4, -1, -1]`

```python
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []                                  # holds INDICES; values decreasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            result[j] = x
        stack.append(i)
    return result
```

**Trace `[2, 1, 2, 4, 3]`:**
```
i=0, x=2: push 0.               stack=[0]
i=1, x=1: 2 not < 1. push 1.    stack=[0,1]
i=2, x=2: pop 1, result[1]=2. push 2.  stack=[0,2]
i=3, x=4: pop 2, result[2]=4. pop 0, result[0]=4. push 3.  stack=[3]
i=4, x=3: 4 not < 3. push 4.    stack=[3,4]

Final: [4, 2, 4, -1, -1]
```

### Why is it O(n)?

**Amortization argument** (same as sliding window in Lesson 4):
- Each index is pushed at most once
- Each index is popped at most once
- Total push+pop operations ≤ 2n → **O(n)**

Count total operations, not nested loops.

### The monotonic stack template

```python
def monotonic_stack_template(nums):
    result = [default] * len(nums)
    stack = []                                  # holds indices
    for i, x in enumerate(nums):
        while stack and violates_order(nums[stack[-1]], x):
            j = stack.pop()
            result[j] = compute_answer(x, i, j)
        stack.append(i)
    return result
```

### When to use which invariant

| Problem asks for                | Stack invariant       | Direction    |
| ------------------------------- | --------------------- | ------------ |
| Next **greater** to the right   | Decreasing            | Left → right |
| Next **smaller** to the right   | Increasing            | Left → right |
| Previous **greater** to the left| Decreasing            | Right → left |
| Previous **smaller** to the left| Increasing            | Right → left |

---

## 4. Monotonic Deque — Sliding Window Maximum

For **sliding window max/min**, use a `deque` that's monotonic. Combines Lesson 4 (sliding window) + today's pattern.

```python
from collections import deque

def max_sliding_window(nums, k):
    result = []
    q = deque()                                 # stores INDICES; values decreasing
    for i, x in enumerate(nums):
        # Remove indices whose values are ≤ x (they can never be the max)
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)
        # Remove leftmost index if it fell out of the window
        if q[0] <= i - k:
            q.popleft()
        # Record max once we have a full window
        if i >= k - 1:
            result.append(nums[q[0]])           # front is always the max
    return result
```

**O(n) time, O(k) space.** The naive is O(n × k). This problem shows up in every serious interview cycle.

---

## 5. Recognition signals

| Phrase in problem                                    | Pattern                     |
| ---------------------------------------------------- | --------------------------- |
| "matching brackets / parentheses"                    | Stack                       |
| "undo" / "reverse"                                   | Stack                       |
| "iterative DFS"                                      | Stack                       |
| "next / previous **greater / smaller** element"      | **Monotonic stack**         |
| "temperature" / "stock price" / "wait N days"        | Monotonic stack             |
| "largest rectangle" / "histogram"                    | Monotonic stack             |
| "BFS" / "level order" / "shortest unweighted path"   | Queue (`deque`)             |
| "sliding window max/min"                             | Monotonic **deque**         |

---

## 6. Common pitfalls

| Pitfall                                            | Why it bites                                   |
| -------------------------------------------------- | ---------------------------------------------- |
| Using `list.pop(0)` as a queue                     | O(n) per pop → O(n²) BFS                       |
| Storing values (not indices) in monotonic stack    | Loses positional info; often you need indices  |
| Wrong monotonic direction                          | Get "previous" instead of "next" (or reverse)  |
| Not clearing stale indices from monotonic deque    | Window boundary bugs in sliding window max     |
| Forgetting to check `if not stack` before `pop`    | `IndexError: pop from empty list`              |

---

## 7. Practice problems

```python
# 1. Valid Parentheses (LC 20, Easy)
def is_valid(s):
    ...

# 2. Implement Queue using Stacks (LC 232, Easy)
class MyQueue:
    def __init__(self): ...
    def push(self, x): ...
    def pop(self): ...
    def peek(self): ...
    def empty(self): ...

# 3. Daily Temperatures (LC 739, Medium) — monotonic stack
def daily_temperatures(temps):
    ...

# 4. Next Greater Element II (LC 503, Medium) — CIRCULAR array
def next_greater_elements(nums):
    ...

# 5. Sliding Window Maximum (LC 239, Hard) — monotonic deque
def max_sliding_window(nums, k):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
from collections import deque

# 1. Valid Parentheses
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack


# 2. Queue using Stacks — amortized O(1) per op
class MyQueue:
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


# 3. Daily Temperatures — store indices; result is DAYS UNTIL warmer
def daily_temperatures(temps):
    result = [0] * len(temps)
    stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


# 4. Next Greater Element II — CIRCULAR: loop through nums twice
def next_greater_elements(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return result


# 5. Sliding Window Maximum — monotonic deque
def max_sliding_window(nums, k):
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
```

**Complexity:**
- (1) O(n) time, O(n) space
- (2) Amortized O(1) per op; each element moves in and out at most once
- (3), (4), (5) O(n) time, O(n) space — amortization argument

</details>

---

## 8. 🎯 Must-Memorize

- **Stack = Python `list`** with `append`/`pop`; **Queue = `collections.deque`** with `append`/`popleft`
- **`list.pop(0)` is O(n)** — never use a list as a queue
- **BFS template** — deque + visited set (Phase 3 workhorse!)
- **Monotonic stack** stores **indices**, not values (usually)
- **Amortization argument:** total pushes + pops ≤ 2n → **O(n)** even with nested `while`
- **Direction rules for monotonic stack:**
  - Next **greater** to right → **decreasing** stack, iterate left→right
  - Next **smaller** to right → **increasing** stack, iterate left→right
- Sliding window max/min = **monotonic deque** (combines sliding window + monotonic pattern)

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/stack_queue_examples.py`](./examples/stack_queue_examples.py)
- ⏮️ Previous: [Linked Lists](./04-linked-lists.md)
- ⏭️ Next: Phase 3 — Binary Trees *(coming!)*
