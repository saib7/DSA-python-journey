"""
Linked List Examples — Lesson 06
The three essential patterns: fast/slow pointer, reversal, dummy node.

Usage:
    python linked_list_examples.py
"""

import time


# ======================================================================
# NODE CLASS
# ======================================================================

class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ======================================================================
# HELPERS: build and print linked lists from Python lists
# ======================================================================

def build(values):
    """Build a linked list from a Python list. Returns the head."""
    dummy = Node()
    tail = dummy
    for v in values:
        tail.next = Node(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    """Convert a linked list back to a Python list for easy printing."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def build_with_cycle(values, cycle_start_index):
    """Build a list with a cycle back to values[cycle_start_index]."""
    head = build(values)
    if cycle_start_index < 0:
        return head
    # Find the target node and the tail
    target = head
    for _ in range(cycle_start_index):
        target = target.next
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = target
    return head


# ======================================================================
# PATTERN 1: FAST & SLOW POINTER
# ======================================================================

def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def has_cycle(head):
    """Floyd's Tortoise and Hare. O(n) time, O(1) space."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


def has_cycle_naive(head):
    """O(n) time, O(n) space using a set of visited nodes."""
    seen = set()
    while head:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False


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


# ======================================================================
# PATTERN 2: REVERSAL
# ======================================================================

def reverse_iterative(head):
    """O(n) time, O(1) space — preferred."""
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


def reverse_recursive(head):
    """O(n) time, O(n) space (call stack). Hits recursion limit on long lists."""
    if not head or not head.next:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


# ======================================================================
# PATTERN 3: DUMMY NODE
# ======================================================================

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


# ======================================================================
# SYNTHESIS: PALINDROME (fast/slow + reverse + walk)
# ======================================================================

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
    # 3. Compare halves
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True


# ======================================================================
# Timing helper
# ======================================================================

def time_it(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  {label:<45} {elapsed:10.3f} ms")


if __name__ == "__main__":
    print("=" * 75)
    print("LINKED LISTS IN ACTION")
    print("=" * 75)

    # --- Correctness ---
    print("\n✅ Correctness")
    print("-" * 75)

    lst = build([1, 2, 3, 4, 5])
    print(f"  Built: {to_list(lst)}")

    print(f"  find_middle([1,2,3,4,5]).val         → {find_middle(lst).val}")
    print(f"  reverse_iterative → {to_list(reverse_iterative(build([1, 2, 3, 4, 5])))}")
    print(f"  reverse_recursive → {to_list(reverse_recursive(build([1, 2, 3, 4, 5])))}")

    merged = merge_two_lists(build([1, 3, 5]), build([2, 4, 6]))
    print(f"  merge_two_lists([1,3,5], [2,4,6]) → {to_list(merged)}")

    after = remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)
    print(f"  remove_nth_from_end([1..5], n=2)     → {to_list(after)}")

    print(f"  is_palindrome([1,2,2,1])             → {is_palindrome(build([1, 2, 2, 1]))}")
    print(f"  is_palindrome([1,2,3])               → {is_palindrome(build([1, 2, 3]))}")

    # --- Cycle detection ---
    print("\n🔬 Cycle detection: Floyd (O(1) space) vs set-based (O(n) space)")
    print("-" * 75)

    no_cycle = build([1, 2, 3, 4, 5])
    with_cycle = build_with_cycle([1, 2, 3, 4, 5], cycle_start_index=2)

    print(f"  has_cycle (no cycle):   Floyd={has_cycle(no_cycle)}   Naive={has_cycle_naive(no_cycle)}")
    print(f"  has_cycle (with cycle): Floyd={has_cycle(with_cycle)}   Naive={has_cycle_naive(with_cycle)}")

    # --- Speed comparison on large linked list ---
    print("\n🔬 Cycle detection speed on a long list")
    print("-" * 75)
    for size in [10_000, 100_000, 1_000_000]:
        no_cycle = build(list(range(size)))
        print(f"\nList length: {size:,}")
        time_it("Floyd's (O(1) space)", has_cycle, no_cycle)
        time_it("Set-based (O(n) space)", has_cycle_naive, no_cycle)

    print("\n✅ Both are O(n) time, but Floyd's uses constant memory —")
    print("   the key win for interview questions.")
