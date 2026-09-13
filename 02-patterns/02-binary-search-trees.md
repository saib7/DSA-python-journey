# 📘 09 · Binary Search Trees

> **Goal:** Learn the BST invariant, its three core operations, and the inorder theorem — plus the classic min/max bounds trick for validation.

---

## ⚡ Quick Recap (read this for fast revision)

- **BST invariant:** for every node, all left subtree values < node.val < all right subtree values (**recursively**, not just immediate children!)
- **When balanced:** search/insert/delete are **O(log n)**. When skewed → O(n)
- **Inorder theorem:** inorder traversal of a BST gives values in **sorted order** ✨
- **Insert/delete idiom:** return the subtree, parent reattaches (`root.left = insert(root.left, val)`)
- **Validate BST:** pass **min/max bounds** down — don't just check immediate children
- **LCA of BST is O(log n)** (descend until values diverge) — vs O(n) for general tree
- Python has no built-in BST — use `bisect` for sorted-list ops, or `sortedcontainers.SortedList` for O(log n)

---

## 1. The BST invariant

For every node:
- All values in the **left subtree** are **strictly less** than `node.val`
- All values in the **right subtree** are **strictly greater** than `node.val`
- **Both subtrees are themselves BSTs**

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

**Why the invariant matters:** at every node, we eliminate half the tree → O(log n) when balanced.

### BST vs the alternatives

| Structure           | Search       | Insert       | Sorted iteration       |
| ------------------- | ------------ | ------------ | ---------------------- |
| Sorted `list`       | O(log n) (bisect) | O(n) (shift) | O(n)              |
| `dict` / `set`      | O(1) avg     | O(1) avg     | ❌ No order            |
| **BST (balanced)**  | **O(log n)** | **O(log n)** | **O(n) — sorted**      |
| BST (skewed)        | O(n)         | O(n)         | O(n)                   |

---

## 2. The three core operations

### 🔹 Search

```python
def search(root, target):
    if not root:
        return None
    if root.val == target:
        return root
    if target < root.val:
        return search(root.left, target)
    return search(root.right, target)
```

**Iterative version** (production-preferred — no call stack):
```python
def search_iter(root, target):
    while root:
        if root.val == target:
            return root
        root = root.left if target < root.val else root.right
    return None
```

### 🔹 Insert — return-and-reattach idiom

```python
def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root                              # duplicates ignored
```

### 🔹 Delete — three cases

1. **Leaf** → just remove
2. **One child** → replace with child
3. **Two children** → replace value with **inorder successor** (smallest in right subtree), then delete successor

```python
def delete(root, val):
    if not root:
        return None
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:                                    # found node
        if not root.left:  return root.right
        if not root.right: return root.left
        # Two children → find inorder successor
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = delete(root.right, successor.val)
    return root
```

---

## 3. The inorder theorem ✨

> **Inorder traversal of a BST → sorted output.**

This is the single most useful theorem about BSTs.

For the tree above, inorder = `[1, 3, 4, 6, 7, 8, 10, 13, 14]` — sorted.

**What this unlocks:**
- **K-th smallest** → inorder with a counter
- **Validate BST** → check inorder is strictly increasing
- **Sorted iterator** → generator using iterative inorder

---

## 4. Validate BST — the classic pitfall

### ❌ Wrong: only checking immediate children

```python
def is_valid_bst_WRONG(root):
    if not root: return True
    if root.left and root.left.val >= root.val: return False
    if root.right and root.right.val <= root.val: return False
    return is_valid_bst_WRONG(root.left) and is_valid_bst_WRONG(root.right)
```

**Counter-example:**
```
        10
       /  \
      5    15
          /  \
         6    20     ← 6 is in 10's RIGHT subtree, so must be > 10. Not caught!
```

### ✅ Right: pass min/max bounds down

```python
def is_valid_bst(root):
    def validate(node, min_val, max_val):
        if not node:
            return True
        if node.val <= min_val or node.val >= max_val:
            return False
        return (validate(node.left, min_val, node.val)
                and validate(node.right, node.val, max_val))
    return validate(root, float('-inf'), float('inf'))
```

- Every **left** recursion tightens `max_val`
- Every **right** recursion tightens `min_val`

The invariant made explicit.

---

## 5. Two more classic BST problems

### K-th smallest — inorder with early stop

```python
def kth_smallest(root, k):
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val
        current = current.right
```

Iterative because we can **stop early** — don't need to walk the whole tree.

### LCA in a BST — the invariant payoff

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left                 # both smaller → go left
        elif p.val > root.val and q.val > root.val:
            root = root.right                # both larger → go right
        else:
            return root                      # they diverge here → LCA
```

**O(log n) time, O(1) space.** General-tree LCA is O(n) — this is the BST payoff.

### Convert sorted array to balanced BST

```python
def sorted_array_to_bst(nums):
    if not nums:
        return None
    mid = len(nums) // 2
    return TreeNode(
        nums[mid],
        sorted_array_to_bst(nums[:mid]),
        sorted_array_to_bst(nums[mid + 1:])
    )
```

Middle → root, recurse on halves. Guaranteed balanced.

---

## 6. ⚠️ The dark side: balance

Insert values in sorted order and you get a linked list:
```
Insert 1, 2, 3, 4, 5 →
1
 \
  2
   \
    ...
```

Now every operation is **O(n)** — the invariant still holds, but you've lost the reason to use a BST.

**Solutions (not usually asked to implement in interviews):**
- **Self-balancing BSTs:** AVL, Red-Black — rotate to keep height O(log n)
- **Skip lists**
- Python-adjacent: `bisect` module (sorted list ops), `sortedcontainers.SortedList` (all O(log n))

---

## 7. Recognition signals

| Phrase in problem                             | Approach                              |
| --------------------------------------------- | ------------------------------------- |
| "search / find in BST"                        | Iterative descent                     |
| "k-th smallest/largest in BST"                | Inorder with counter                  |
| "validate BST"                                | **Min/max bounds recursion**          |
| "sorted output from tree"                     | Inorder traversal                     |
| "LCA in BST"                                  | Descend until values diverge          |
| "convert sorted array/list to BST"            | Middle → root, recurse halves         |
| "insert / delete in BST"                      | Return-and-reattach recursion         |
| "sorted list, need fast search"               | `bisect` module                       |

---

## 8. Common pitfalls

| Pitfall                                            | Why it bites                                     |
| -------------------------------------------------- | ------------------------------------------------ |
| Validating BST by only checking immediate children | Fails on nested violations                       |
| Forgetting to reassign in insert/delete            | Tree structure not updated                       |
| Assuming BST is always balanced                    | Skewed → O(n) worst case                         |
| Handling duplicates inconsistently                 | Some problems require duplicates left/right      |
| Not handling `None` in delete's two-child case     | Infinite recursion on successor search           |

---

## 9. Practice problems

```python
# 1. Search in a BST (LC 700, Easy)
def search_bst(root, val):
    ...

# 2. Insert into a BST (LC 701, Medium)
def insert_into_bst(root, val):
    ...

# 3. Validate BST (LC 98, Medium) — the classic!
def is_valid_bst(root):
    ...

# 4. Kth Smallest Element in a BST (LC 230, Medium)
def kth_smallest(root, k):
    ...

# 5. Lowest Common Ancestor of BST (LC 235, Easy — thanks to invariant)
def lca_bst(root, p, q):
    ...

# 6. Convert Sorted Array to BST (LC 108, Easy)
def sorted_array_to_bst(nums):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 1. Search — iterative
def search_bst(root, val):
    while root:
        if root.val == val: return root
        root = root.left if val < root.val else root.right
    return None


# 2. Insert
def insert_into_bst(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root


# 3. Validate BST — bounds recursion
def is_valid_bst(root):
    def validate(node, min_val, max_val):
        if not node: return True
        if node.val <= min_val or node.val >= max_val: return False
        return (validate(node.left, min_val, node.val)
                and validate(node.right, node.val, max_val))
    return validate(root, float('-inf'), float('inf'))


# 4. Kth Smallest — iterative inorder, stop at k
def kth_smallest(root, k):
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val
        current = current.right


# 5. LCA — walk down using invariant
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root


# 6. Sorted array → balanced BST
def sorted_array_to_bst(nums):
    if not nums:
        return None
    mid = len(nums) // 2
    return TreeNode(
        nums[mid],
        sorted_array_to_bst(nums[:mid]),
        sorted_array_to_bst(nums[mid + 1:])
    )
```

**Complexity for all:** O(log n) or O(n) depending on balance and problem.
- (1), (2), (5): O(h) time — where h is height (log n if balanced)
- (3), (4), (6): O(n) time (must visit or process most nodes)

</details>

---

## 10. 🎯 Must-Memorize

- BST invariant: **all left values < node.val < all right values, recursively**
- Balanced BST ops are **O(log n)**; skewed BST ops are **O(n)**
- **Inorder on BST = sorted output** (the theorem!)
- Insert/delete idiom: **return the subtree, parent reattaches**
- Validate BST needs **min/max bounds** — checking immediate children isn't enough
- Delete has **3 cases** — two children requires **inorder successor**
- BST LCA descends until values **diverge** — O(log n) vs O(n) for general trees
- Python has no built-in BST — for sorted-list needs use `bisect` or `sortedcontainers.SortedList`

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/bst_examples.py`](./examples/bst_examples.py)
- ⏮️ Previous: [Binary Trees & Traversals](./01-binary-trees.md)
- ⏭️ Next: Heaps & Priority Queues *(coming)*
