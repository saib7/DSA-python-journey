# 📘 06 · Linked Lists

> **Goal:** Master the three essential linked list patterns — fast/slow pointer, reversal, and the dummy node technique.

---

## ⚡ Quick Recap (read this for fast revision)

- A **linked list** = nodes with `val` + `next`, not in contiguous memory
- Trade-off vs array: **O(1) insert/delete** anywhere (with node ref) but **O(n) random access**
- **Three essential patterns:**
  1. **Fast & slow pointer** — cycle detection, find middle, Nth from end
  2. **Reversal** — iterative three-pointer dance (O(1) space, prefer over recursive)
  3. **Dummy node** — eliminates head-change edge cases
- **Floyd's cycle detection:** O(n) time, **O(1) space** (vs O(n) space for the set approach)
- Reversal iterative = O(1) space; recursive = O(n) space (call stack)
- Python has no built-in linked list — `collections.deque` is closest

---

## 1. What & why

Each node holds data and a reference to the next node.

```
[1|•] → [2|•] → [3|•] → None
```

**Types:** singly, doubly, circular.

### Trade-offs vs Python `list`

| Operation                     | `list` (array) | Linked list       |
| ----------------------------- | -------------- | ----------------- |
| Access by index               | **O(1)** ✅    | O(n)              |
| Insert at start               | O(n)           | **O(1)** ✅       |
| Insert at end (with tail ref) | O(1) amort.    | O(1)              |
| Insert in middle (with ref)   | O(n)           | **O(1)** ✅       |
| Search by value               | O(n)           | O(n)              |
| Memory                        | Compact        | Overhead per node |

---

## 2. Building blocks in Python

```python
class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

head = Node(1, Node(2, Node(3)))   # 1 → 2 → 3

# The fundamental traversal
current = head
while current:
    print(current.val)
    current = current.next
```

Every linked list algorithm is a variation of this loop.

---

## 3. Pattern 1: Fast & Slow Pointer

Two pointers, one at 2× speed. Powers a surprising number of problems.

### Find the middle

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**O(n) time, O(1) space.** Single pass — beats the two-pass "count then walk" approach.

### Floyd's cycle detection (Tortoise and Hare)

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Why it works:** once both pointers are in the cycle, fast gains 1 position per step relative to slow. The gap shrinks by 1 each step → they must meet.

**O(n) time, O(1) space.** The set-based approach is O(n) time AND O(n) space.

### Remove Nth from end — gap technique

```python
def remove_nth_from_end(head, n):
    dummy = Node(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next     # skip target
    return dummy.next
```

Notice the **dummy node** — it handles the case where head itself needs to be removed.

---

## 4. Pattern 2: Reversal

### Iterative — three-pointer dance ✅ preferred

```python
def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next   # 1. save next
        current.next = prev        # 2. flip the arrow
        prev = current             # 3. advance prev
        current = next_node        # 4. advance current
    return prev
```

**O(n) time, O(1) space.**

Trace `1 → 2 → 3 → None`:
```
Start:   prev=None, curr=1
Step 1:  next=2, 1.next=None  → prev=1, curr=2
Step 2:  next=3, 2.next=1     → prev=2, curr=3
Step 3:  next=None, 3.next=2  → prev=3, curr=None
Return prev=3. List is 3 → 2 → 1 → None.
```

### Recursive

```python
def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)   # leap of faith
    head.next.next = head                # attach current to reversed tail
    head.next = None                     # break old link
    return new_head
```

**O(n) time, O(n) space** for the call stack. Prefer iterative in production — long lists blow Python's recursion limit.

---

## 5. Pattern 3: The Dummy Node

When an operation might modify the head, add a dummy node so the head is never a special case.

### Merge two sorted lists

```python
def merge_two_lists(l1, l2):
    dummy = Node(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2               # attach remainder
    return dummy.next                  # skip the dummy
```

Without the dummy: every iteration needs `if result is None: result = ...`. With the dummy: clean loop. **Appears in ~50% of linked list problems.**

---

## 6. Recognition signals

| Phrase in problem                             | Pattern                       |
| --------------------------------------------- | ----------------------------- |
| "detect a cycle"                              | **Floyd's** (fast/slow)       |
| "middle of the linked list"                   | Fast/slow                     |
| "Nth node from the end"                       | Fast/slow with **gap = N**    |
| "reverse" (all or part of the list)           | Iterative three-pointer       |
| "merge two sorted lists"                      | **Dummy node** + two pointers |
| "remove/insert" (head may change)             | Dummy node                    |
| "check if palindrome" (linked list)           | Find middle + reverse         |
| "reorder" or "rotate"                         | Find middle + reverse/merge   |

---

## 7. Common pitfalls

| Pitfall                                            | Why it bites                                     |
| -------------------------------------------------- | ------------------------------------------------ |
| Forgetting to save `current.next` before flipping  | You lose the rest of the list                    |
| Not handling empty list (`head is None`)           | Attribute error on `head.next`                   |
| Recursion on long lists (>~1000 nodes)             | Hits Python's recursion limit                    |
| Not using dummy when head might change             | Ugly special-case code for head modification     |
| Forgetting to break the old link in reversal       | Creates an unintended cycle                      |
| Using `is` vs `==`                                 | Node comparison should be `is` (same object)     |

---

## 8. Practice problems

```python
# 1. Reverse Linked List (LC 206, Easy)
def reverse_list(head):
    ...

# 2. Merge Two Sorted Lists (LC 21, Easy)
def merge_two_lists(l1, l2):
    ...

# 3. Linked List Cycle (LC 141, Easy)
def has_cycle(head):
    ...

# 4. Middle of the Linked List (LC 876, Easy)
def middle_node(head):
    ...

# 5. Remove Nth Node From End (LC 19, Medium)
def remove_nth_from_end(head, n):
    ...

# 6. Palindrome Linked List (LC 234) — synthesis problem
def is_palindrome(head):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 1. Reverse — iterative
def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


# 2. Merge two sorted — dummy node
def merge_two_lists(l1, l2):
    dummy = Node(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next


# 3. Cycle detection — Floyd's
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


# 4. Middle — fast/slow
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# 5. Remove Nth from end — fast/slow with gap
def remove_nth_from_end(head, n):
    dummy = Node(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next


# 6. Palindrome — synthesis: find middle + reverse second half + compare
def is_palindrome(head):
    # 1. Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # 2. Reverse second half
    prev = None
    while slow:
        next_node = slow.next
        slow.next = prev
        prev = slow
        slow = next_node
    # 3. Compare first half against reversed second half
    left, right = head, prev
    while right:              # right is shorter or equal
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True
```

**Complexity for all:** O(n) time, O(1) space (except recursive reverse which is O(n) space).

**Problem 6 payoff:** you just combined **three patterns** — fast/slow, reversal, and two-pointer comparison — in a single algorithm. That's exactly what medium-hard interviews look like.

</details>

---

## 9. 🎯 Must-Memorize

- **Node class:** `val` and `next` — the whole data structure
- **Fast/slow pointer** — cycle detection, middle-finding, Nth-from-end in O(1) space
- **Floyd's algorithm** = fast/slow for cycle detection (interview classic)
- **Reversal iterative** — the four-step dance: `save next → flip → advance prev → advance current`
- **Dummy node** — use it whenever the head might change
- Iterative reversal is **O(1) space**; recursive is **O(n) space** — mention this out loud in interviews
- Linked lists have **O(1) insert/delete** with a node reference, **O(n) search/access**

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/linked_list_examples.py`](./examples/linked_list_examples.py)
- ⏮️ Previous: [Hash Tables](./03-hash-tables.md)
- ⏭️ Next: Stacks & Queues *(coming — start of Phase 3 prep)*
